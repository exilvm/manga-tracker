const LRU = require('lru-cache');
const crypto = require('crypto');
const { authLogger } = require('../utils/logging');

const { bruteforce } = require('../utils/ratelimits');
const { db } = require('.');
const { sessionLogger } = require('../utils/logging');


const userCache = new LRU(({
  max: 50,
  maxAge: 86400000, // 1 day in ms
  noDisposeOnSet: true,
  updateAgeOnGet: true,
}));

const userPromises = new Map();

const dev = process.env.NODE_ENV !== 'production';

async function generateAuthToken(uid, userUUID) {
  return new Promise((resolve, reject) => {
    crypto.randomBytes(32+9, (err, buf) => {
      if (err) {
        return reject(err);
      }

      const token = buf.toString('base64', 0, 33);
      const lookup = buf.toString('base64', 33);

      const sql = `INSERT INTO auth_tokens (user_id, hashed_token, expires_at, lookup) VALUES ($1, encode(digest($2, 'sha256'), 'hex'), $3, $4)`;
      const age = 2592e+6; // 30 days
      resolve(db.query(sql, [uid, token, new Date(Date.now() + age), lookup])
        .then(() => `${lookup};${token};${Buffer.from(userUUID).toString('base64')}`));
    });
  });
}
module.exports.generateAuthToken = generateAuthToken;

function regenerateAuthToken(uid, lookup, userUUID, cb) {
  crypto.randomBytes(32, (err, buf) => {
    if (err) {
      return cb(err, false);
    }

    const token = buf.toString('base64');

    const sql = `UPDATE auth_tokens SET hashed_token=encode(digest($3, 'sha256'), 'hex') WHERE user_id=$1 AND lookup=$2 RETURNING expires_at`;
    db.one(sql, [uid, lookup, token])
      .then(row => {
        cb(null, `${lookup};${token};${Buffer.from(userUUID).toString('base64')}`, row.expiresAt);
      })
      .catch(sqlErr => cb(sqlErr, false));
  });
}

module.exports.authenticate = (req, email, password, cb) => {
  if (password.length > 72) return cb(null, false);

  const sql = `SELECT user_id, username, user_uuid, theme, admin FROM users WHERE email=$1 AND pwhash=crypt($2, pwhash)`;
  db.oneOrNone(sql, [email, password])
    .then(row => {
      if (!row) {
        return cb(null, false);
      }

      function setUser(currentRow, token) {
        // Try to regen session
        req.session.regenerate((err) => {
          if (err) {
            console.error(err);
            req.session.userId = undefined;
            return cb(err, false);
          }
          req.session.userId = currentRow.userId;
          userCache.set(currentRow.userId, {
            userId: currentRow.userId,
            username: currentRow.username,
            uuid: currentRow.userUuid,
            theme: currentRow.theme,
            admin: currentRow.admin,
          });
          return cb(null, token);
        });
      }

      if (req.body.rememberme !== true) {
        return setUser(row, true);
      }

      generateAuthToken(row.userId, row.userUuid)
        .then(token => setUser(row, token))
        .catch(err => {
          console.error(err);
          cb(err, false);
        });
    })
    .catch(err => {
      console.error(err);
      cb(err, false);
    });
};

function getUser(uid, cb) {
  if (!uid) return cb(null, null);

  const user = userCache.get(uid);
  if (user) return cb(user, null);

  const sql = `SELECT username, user_uuid, theme, admin FROM users WHERE user_id=$1`;
  db.oneOrNone(sql, [uid])
    .then(row => {
      if (!row) return cb(null, null);

      const val = {
        username: row.username,
        uuid: row.userUuid,
        userId: uid,
        theme: row.theme,
        admin: row.admin,
      };
      userCache.set(uid, val);
      cb(val, null);
    })
    .catch(err => {
      console.error(err);
      cb(null, err);
    });
}
module.exports.getUser = getUser;

module.exports.requiresUser = (req, res, next) => {
  getUser(req.session.userId, (user, err) => {
    req.user = user;
    next(err);
  });
};

function clearUserAuthTokens(uid) {
  const sql = `DELETE FROM auth_tokens WHERE user_id=$1`;
  return db.query(sql, [uid]);
}
module.exports.clearUserAuthTokens = clearUserAuthTokens;

function getUserByToken(lookup, token, uuid) {
  const sql = `
    SELECT u.user_id, u.username, u.user_uuid, u.theme, u.admin
    FROM auth_tokens INNER JOIN users u on u.user_id=auth_tokens.user_id 
    WHERE expires_at > NOW() AND user_uuid=$1 AND lookup=$2 AND hashed_token=encode(digest($3, 'sha256'), 'hex')
  `;

  return db.oneOrNone(sql, [uuid, lookup, token]);
}

function parseAuthCookie(authCookie) {
  /*
  Try to find the remember me token.
  If found associate current session with user and regenerate session id (this is important)
  If something fails or user isn't found we remove possible user id from session and continue
   */
  const [lookup, token, uuidBase64] = authCookie.split(';', 3);
  if (!uuidBase64) {
    return [null, null, null];
  }

  const uuid = Buffer.from(uuidBase64, 'base64').toString('ascii');
  if (uuid.length < 32) {
    return [null, null, null];
  }
  return [lookup, token, uuid];
}

// eslint-disable-next-line arrow-body-style
module.exports.checkAuth = (app) => {
  return function checkAuth(req, res, next) {
    const authCookie = req.cookies.auth;
    // We don't need to check authentication for resources generated by next.js
    if (req.session.userId || !authCookie) {
      return next();
    }

    if (userPromises.has(authCookie)) {
      authLogger.debug('Race condition prevention');
      userPromises.get(authCookie)
        .then(userId => {
          if (userId) {
            req.session.userId = userId;
          }
        })
        .finally(next);
      return;
    }

    const p = new Promise((resolve, reject) => {
      bruteforce.prevent(req, res, () => {
        authLogger.debug('Checking auth from db for %s %s', req.originalUrl, req.cookies.auth);
        const [lookup, token, uuid] = parseAuthCookie(req.cookies.auth);
        if (!token) {
          res.clearCookie('auth');
          req.session.userId = undefined;
          resolve();
          next();
          return;
        }

        getUserByToken(lookup, token, uuid)
          .then(row => {
            if (!row) {
              sessionLogger.info('Session not found. Clearing cookie');
              res.clearCookie('auth');
              req.session.userId = undefined;
              resolve();

              const checkLookup = `SELECT u.user_id FROM auth_tokens 
                                   INNER JOIN users u ON auth_tokens.user_id = u.user_id 
                                   WHERE user_uuid=$1 AND lookup=$2`;

              db.oneOrNone(checkLookup, [uuid, lookup])
                .then(innerRow => {
                  if (!innerRow) return next();
                  // TODO Display warning
                  clearUserAuthTokens(innerRow.userId)
                    .finally(() => {
                      app.sessionStore.clearUserSessions(innerRow.userId, () => {
                        sessionLogger.info('Invalid auth token found for user. Sessions cleared');
                        next();
                      });
                    });
                })
                .catch(next);
              return;
            }

            userCache.set(row.userId, {
              userId: row.userId,
              username: row.username,
              uuid: row.userUuid,
              theme: row.theme,
              admin: row.admin,
            });
            // Try to regen session
            req.session.regenerate((err) => {
              if (err) {
                req.session.userId = undefined;
                reject(err);
                return next(err);
              }
              regenerateAuthToken(row.userId, lookup, uuid, (regenErr, newToken, expiresAt) => {
                if (regenErr || !newToken) {
                  console.error('Failed to regenerate/change token', regenErr);
                  reject(regenErr);
                  return next(regenErr);
                }
                authLogger.debug('regen %s', newToken);

                req.session.userId = row.userId;
                res.cookie('auth', newToken, {
                  httpOnly: true,
                  secure: !dev,
                  sameSite: 'lax',
                  expires: expiresAt,
                });
                resolve(row.userId);
                return next();
              });
            });
          })
          .catch(err => {
            resolve();
            req.session.userId = undefined;
            res.clearCookie('auth');
            if (err.code === '22P02') {
              res.status(400).end();
              return;
            }
            authLogger.error(err);
            next(err);
          });
      });
    });
    userPromises.set(authCookie, p);
    p.finally(() => {
      authLogger.debug('Deleting promise');
      userPromises.delete(authCookie);
    });
  };
};

function clearUserAuthToken(uid, auth, cb) {
  const [lookup, token] = auth.split(';', 3);

  const sql = `DELETE FROM auth_tokens WHERE user_id=$1 AND lookup=$2 AND hashed_token=encode(digest($3, 'sha256'), 'hex')`;
  db.query(sql, [uid, lookup, token])
    .then(() => cb(null))
    .catch(err => cb(err));
}
module.exports.clearUserAuthToken = clearUserAuthToken;

module.exports.modifyCacheUser = (uid, modifications) => {
  const user = userCache.get(uid);
  if (!user) return;
  userCache.set(uid, { ...user, ...modifications });
};

module.exports.clearUserCache = () => {
  userCache.reset();
};
