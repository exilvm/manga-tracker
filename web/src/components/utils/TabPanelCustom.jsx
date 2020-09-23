import React, { useEffect, useMemo, useState } from 'react';

export const TabPanelCustom = (props) => {
  const {
    children,
    value,
    index,
    noRerenderOnChange = false,
    ...other
  } = props;

  const [rendered, setRendered] = useState(value === index);

  useEffect(() => setRendered(rendered || value === index),
    [index, rendered, value]);

  const style = useMemo(() => {
    if (value === index || !noRerenderOnChange) return { display: undefined };
    return { display: 'none' };
  }, [value, index, noRerenderOnChange]);

  return (
    <div
      role='tabpanel'
      hidden={!noRerenderOnChange && value !== index}
      style={style}
      {...other}
    >
      {((rendered && noRerenderOnChange) || value === index) && children}
    </div>
  );
};
