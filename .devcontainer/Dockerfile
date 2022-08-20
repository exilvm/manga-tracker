ARG VARIANT=16-bullseye
FROM mcr.microsoft.com/vscode/devcontainers/typescript-node:${VARIANT}

# Download the script
RUN wget https://github.com/microsoft/vscode-dev-containers/raw/main/script-library/python-debian.sh -P /tmp/library-scripts/

# Setup default python tools in a venv via pipx to avoid conflicts
ENV PIPX_HOME=/usr/local/py-utils \
    PIPX_BIN_DIR=/usr/local/py-utils/bin
ENV PATH=${PATH}:${PIPX_BIN_DIR}
RUN bash /tmp/library-scripts/python-debian.sh \ 
    && apt-get clean -y && rm -rf /var/lib/apt/lists/* tmp/library-scripts