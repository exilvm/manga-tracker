import React, { useEffect } from 'react';
import { IconButton, Input } from '@material-ui/core';
import {
  Cancel as CancelIcon,
  Edit as EditIcon,
  Save as SaveIcon,
  Delete as DeleteIcon,
} from '@material-ui/icons';
import { actions, defaultColumn } from 'react-table';

import { noop } from '../../utils/utilities';

actions.startEditingRow = 'startEditingRow';
actions.stopEditingRow = 'stopEditingRow';

/**
 * Default implementation of the row save action.
 * Will update current row values to the edited ones.
 * @param row The row generated by react table
 * @param state Current state of react table
 */
export function defaultOnSaveRow(row, state) {
  Object.keys(state).forEach(key => {
    row.values[key] = state[key];
  });
}

function prepareRow(row, { instance: {
  onSaveRow = defaultOnSaveRow,
  onCancelRow = noop,
  onEditRow = noop,
  onDeleteRow = noop,
  startEditingRow,
  stopEditingRow,
}}) {
  row.startEditingRow = () => startEditingRow(row.id);
  row.stopEditingRow = () => stopEditingRow(row.id);
  row.onSaveRow = onSaveRow;
  row.onCancelRow = onCancelRow;
  row.onEditRow = onEditRow;
  row.onDeleteRow = onDeleteRow;
}

function isRowBeingEdited(row, rowEditStates) {
  return Boolean(rowEditStates[row.id]);
}

/**
 * Simple function that sets the row edit state after a cell has been edited
 * @param newValue The new value for that cell
 * @param rowState current rowEditStates
 * @param cell current cell that was edited
 */
export function processCellEdit(newValue, rowState, cell) {
  rowState[cell.row.id][cell.column.id] = newValue;
}

function reducer(state, action) {
  if (action.type === actions.init) {
    return {
      rowEditStates: {},
      ...state,
    };
  }

  // Start editing row
  if (action.type === actions.startEditingRow) {
    const { id } = action;

    if (state.rowEditStates[id]) {
      return state;
    }

    const newRowEditStates = { ...state.rowEditStates };
    newRowEditStates[id] = {};

    return {
      ...state,
      rowEditStates: newRowEditStates,
    };
  }

  // Stop editing row
  if (action.type === actions.stopEditingRow) {
    const { id } = action;

    if (!state.rowEditStates[id]) {
      return state;
    }

    const newRowEditStates = { ...state.rowEditStates };
    newRowEditStates[id] = false;

    return {
      ...state,
      rowEditStates: newRowEditStates,
    };
  }
}

function useInstance(instance) {
  const {
    rows,
    flatHeaders,
    state: { rowEditStates },
    dispatch,
    disableEditing,
    disableDeleting,
    allColumns,
  } = instance;

  // Show or hide edit column
  useEffect(() => {
    allColumns
      .filter(c => c.id === '__edit')
      .forEach(c => c.toggleHidden(disableEditing));
  }, [allColumns, disableEditing]);
  // Show or hide row delete column
  useEffect(() => {
    allColumns
      .filter(c => c.id === '__delete')
      .forEach(c => c.toggleHidden(disableDeleting));
  }, [allColumns, disableDeleting]);

  // Add properties to rows
  const editingFlatRows = React.useMemo(() => {
    const editingFlatRowsInner = [];

    rows.forEach(row => {
      row.beingEdited = !disableEditing && isRowBeingEdited(row, rowEditStates);

      if (row.beingEdited) {
        editingFlatRowsInner.push(row);
      }
    });

    return editingFlatRowsInner;
  }, [rows, disableEditing, rowEditStates]);

  // Add properties to columns
  const editableColumns = React.useMemo(() => {
    const editableColumnsInner = [];

    flatHeaders.forEach(col => {
      col.canEdit = col.canEdit === undefined ? true : col.canEdit;
      if (col.canEdit) {
        editableColumnsInner.push(col);
      }
    });

    return editableColumnsInner;
  }, [flatHeaders]);

  // Start row edit dispatch
  const startEditingRow = React.useCallback(
    (id) => dispatch({ type: actions.startEditingRow, id }),
    [dispatch]
  );

  // Stop row edit dispatch
  const stopEditingRow = React.useCallback(
    (id) => dispatch({ type: actions.stopEditingRow, id }),
    [dispatch]
  );

  Object.assign(instance, {
    editingFlatRows,
    startEditingRow,
    stopEditingRow,
    editableColumns,
  });
}

function DefaultEditCell({ value, cell, state }) {
  return (
    <Input
      defaultValue={value}
      onChange={(event => processCellEdit(event.target.value, state.rowEditStates, cell))}
    />
  );
}

function visibleColumns(columns, { instance }) {
  const {
    classes,
    disableDeleting,
    disabledEditing,
    initialState,
    confirm,
  } = instance;

  const arr = [];
  if (disabledEditing) arr.push('__edit');
  if (disableDeleting) arr.push('__delete');

  instance.initialState.hiddenColumns = [
    ...initialState.hiddenColumns || [],
    ...arr,
  ];

  const onStartEdit = (row) => {
    row.startEditingRow();
    row.onEditRow(row);
  };

  const onSaveEdit = (row, state, inst) => {
    row.stopEditingRow();
    row.onSaveRow(row, state.rowEditStates[row.id], inst);
  };

  const onCancelEdit = (row, state, inst) => {
    row.stopEditingRow();
    row.onCancelRow(row, state.rowEditStates[row.id], inst);
  };

  const onDelete = (row) => {
    confirm({
      description: `Do you want to delete row ${JSON.stringify(row.values)}`,
      confirmationText: 'Delete',
      confirmationButtonProps: { 'aria-label': 'Confirm delete row' },
    })
      .then(() => {
        row.stopEditingRow();
        row.onDeleteRow(row);
      })
      .catch(() => {});
  };

  return [
    {
      id: '__edit',
      padding: 'checkbox',
      Header: () => null,
      Cell: (inst) => {
        const { row, state } = inst;
        return (
          <div className={classes.editCell}>
            {!row.beingEdited ? (
              <IconButton onClick={() => onStartEdit(row)} name='edit'>
                <EditIcon />
              </IconButton>
            ) : (
              <>
                <IconButton name='save' onClick={() => onSaveEdit(row, state, inst)}>
                  <SaveIcon />
                </IconButton>
                <IconButton name='cancel' onClick={() => onCancelEdit(row, state, inst)}>
                  <CancelIcon />
                </IconButton>
              </>
            )}
          </div>
        );
      },
    },
    ...columns.map(col => ({
      OriginalCell: col.Cell || defaultColumn.Cell,
      EditCell: col.EditCell || DefaultEditCell,
      ...col,
      Cell: ({ row, cell }) => (
        // TODO rename canEdit to editable
        (cell.column.canEdit && row.beingEdited) ?
          cell.render('EditCell') :
          cell.render('OriginalCell')
      ),
    })),
    {
      id: '__delete',
      padding: 'checkbox',
      Header: () => null,
      // eslint-disable-next-line react/display-name
      Cell: (inst) => {
        const { row } = inst;
        return (
          <IconButton name='delete' onClick={() => onDelete(row)} aria-label='Delete row'>
            <DeleteIcon />
          </IconButton>
        );
      },
    },
  ];
}

/**
 * Sets the hidden columns based on initial options
 */
function useOptions(options) {
  const {
    disableDeleting,
    disableEditing,
    initialState,
  } = options;

  const arr = [];
  if (disableEditing) arr.push('__edit');
  if (disableDeleting) arr.push('__delete');

  return {
    initialState: {
      ...initialState,
      hiddenColumns: [
        ...initialState.hiddenColumns || [],
        ...arr,
      ],
    },
  };
}

/**
 * Parameters accepted by this plugin
 * - onSaveRow: Function called when row is saved. Defaults to `defaultOnSaveRow`
 * - onCancelRow: Function called when row edit was cancelled
 * - onEditRow: Function called when row editing begins
 * - classes.editCell: Class name for edit cell content
 * - disableEditing: boolean that determines whether editing is enabled or not
 */
export const useEditable = hooks => {
  hooks.visibleColumns.push(visibleColumns);
  hooks.useOptions.push(useOptions);
  hooks.stateReducers.push(reducer);
  hooks.useInstance.push(useInstance);
  hooks.prepareRow.push(prepareRow);
};
