# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : binary_trace_headers_table_model.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Classe para o modelo das tabelas do Binary e Trace Header para o QtableView

       21/08/2026 - Implementação da Classe
===============================================================================
"""

from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt

class BinaryTraceHeaderTableModel(QAbstractTableModel):
    COLUMNS = (
        "Bytes",
        "Description",
        "Value",
        "Data Type",
    )

    def __init__(self, field_key: str, data: dict | None = None, parent=None):
        super().__init__(parent)

        self._field_key = field_key
        self._data = data or {}
        self._items = list(self._data.values())

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self._items)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.COLUMNS)

    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        item = self._items[index.row()]

        value = item["value"]
        field = item[self._field_key]

        if role == Qt.ItemDataRole.DisplayRole:
            match index.column():

                case 0:
                    return f'{field["byte_start"]} - {field["byte_end"]}'

                case 1:
                    return field["description"]

                case 2:
                    return "" if value is None else str(value)

                case 3:
                    return field["data_type"]

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if index.column() == 2:
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            elif index.column() in (0,3):
                return Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter

        return None

    def headerData(self, section: int, orientation: Qt.Orientation,role = Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation == Qt.Orientation.Horizontal:
            return self.COLUMNS[section]

        return section + 1

    def set_data(self, data: dict) -> None:
        self.beginResetModel()

        self._data = data
        self._items = list(data.values())

        self.endResetModel()