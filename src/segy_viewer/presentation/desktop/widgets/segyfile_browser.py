# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : segyfile_browser.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Classe que cria o Widget SegyFileBrowser, um visualizador da arvore de pastas
    e arquivos que mostra somente os arquivos *.sgy e *.segy .

    SegyFileBrowser
    ├── navega pelas pastas
    ├── exibe somente *.sgy e *.segy
    ├── reconhece arquivos SEG-Y
    ├── usa ícone próprio para SEG-Y
    ├── persiste a última pasta visitada
    └── emite seleção de um SEG-Y

Histórico:
       14/08/2026 - Implementação da Classe
===============================================================================
"""
from PySide6.QtWidgets import (QWidget, QTreeView, QFileSystemModel,
                               QVBoxLayout, QFileIconProvider, QHBoxLayout,
                               QHeaderView, QAbstractItemView, QPushButton,
                               QFileDialog, QLabel, QComboBox, QSizePolicy)
from PySide6.QtCore import (QFileInfo, QDir, Slot,  QSettings, Signal,
                            QItemSelection, QStandardPaths, QSize, Qt)
from PySide6.QtGui import QIcon
from pathlib import Path

_BASE_DIR = Path(__file__).resolve().parents[5]
_ICONS_DIR = _BASE_DIR / "resources" / "icons"
_SEGY_ICON = _ICONS_DIR / "segyFile.ico"
_ICON_UP_BUTTON = _ICONS_DIR / "folder_up.ico"
_ICON_OPEN_FOLDER = _ICONS_DIR / "open_folder.ico"
_ICON_SORT_BUTTON1 = _ICONS_DIR / "sort_AZ.ico"
_ICON_SORT_BUTTON2 = _ICONS_DIR / "sort_019.ico"
_ICON_REFRESH_BUTTON = _ICONS_DIR / "reload_folder.ico"

#==================================================
class _SegyFileIconProvider(QFileIconProvider):
    def __init__(self, segy_icon: Path, segy_extensions: tuple[str, ...]):
        super().__init__()
        self._segy_icon = QIcon(str(segy_icon))
        self._segy_extensions = segy_extensions

    def icon(self, info: QFileInfo) -> QIcon:
        if isinstance(info, QFileInfo):
            if info.isFile():
                suffix = f".{info.suffix()}".lower()
                if suffix in self._segy_extensions:
                    return self._segy_icon

        return super().icon(info)


#==================================================
class SegyFileBrowser(QWidget):


    file_selected = Signal(Path)

    def __init__(self, segy_extensions: tuple[str, ...], button_style: str, parent=None):
        super().__init__(parent)

        self._settings = QSettings("SegyViewer", "SegyViewer")
        self._button_style = button_style
        self._segy_extensions = segy_extensions
        self.model = QFileSystemModel(self)

        # So mostra o conteudo da pasta atual, sem expandir
        initial_path = self._inital_path()
        root_index = self.model.index(str(initial_path))  #Este é usado no self.tree
        self.model.setRootPath(str(initial_path))

        name_filters = [f'*{ext}' for ext in self._segy_extensions]
        self.model.setNameFilters(name_filters)
        self.model.setNameFilterDisables(False)

        self._icon_sgyfile = _SegyFileIconProvider(segy_icon = _SEGY_ICON,
                                                   segy_extensions=self._segy_extensions)

        self.model.setIconProvider(self._icon_sgyfile)

        self.tree = QTreeView(self)
        self.tree.setModel(self.model)

        #So mostra o conteudo da pasta atual, sem expandir
        self.tree.setRootIndex(root_index)
        self.tree.setRootIsDecorated(False)
        self.tree.setItemsExpandable(False)

        self.tree.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tree.setSelectionBehavior( QAbstractItemView.SelectionBehavior.SelectRows)

        self.tree.selectionModel().selectionChanged.connect(self._on_selection_changed)
        self.tree.doubleClicked.connect(self._on_double_clicked)

        self.tree.hideColumn(2)
        self.tree.hideColumn(3)
        self.tree.setColumnWidth(0, 200)
        self.tree.setColumnWidth(1, 75)
        self.tree.sortByColumn(0, Qt.SortOrder.AscendingOrder)

        header = self.tree.header()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)

        #Botões para navegação do SegyFileBrowser
        buttons_layout = QHBoxLayout()

        self.up_button = self._make_button("", _ICON_UP_BUTTON, "Go to previous directory")
        self.up_button.clicked.connect(self._button_level_up_clicked)

        self.open_folder_button = self._make_button("", _ICON_OPEN_FOLDER, "Open other directory")
        self.open_folder_button.clicked.connect(self._button_open_folder_clicked)

        self.sort_button1 = self._make_button("", _ICON_SORT_BUTTON1, "Change file name sort order")
        self.sort_button1.clicked.connect(self._button_sort_name_clicked)

        self.sort_button2 = self._make_button("", _ICON_SORT_BUTTON2, "Change file size sort order")
        self.sort_button2.clicked.connect(self._button_sort_size_clicked)


        self.refresh_button = self._make_button("", _ICON_REFRESH_BUTTON, "Refresh list")
        self.refresh_button.clicked.connect(self._refresh_current_directory)

        buttons_layout.addWidget(self.up_button)
        buttons_layout.addWidget(self.open_folder_button)
        buttons_layout.addWidget(self.sort_button1)
        buttons_layout.addWidget(self.sort_button2)
        buttons_layout.addWidget(self.refresh_button)
        buttons_layout.addStretch()

        self.path_label = QLabel()
        self.path_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.path_label.setText(str(initial_path))

        layout = QVBoxLayout(self)
        layout.addLayout(buttons_layout)
        layout.addWidget(self.path_label)
        layout.addWidget(self.tree)


#========================================================================================================
    @Slot()
    def _button_level_up_clicked(self):
        current_index = self.tree.rootIndex()
        current_path = Path(self.model.filePath(current_index))
        parent_path = current_path.parent
        self._set_current_diretory(parent_path)

        if parent_path == current_path:
            return

        parent_index = self.model.index(str(parent_path))
        self.tree.setRootIndex(parent_index)

    @Slot()
    def _button_open_folder_clicked(self):
        dialog = QFileDialog(self, "Selecionar pasta")
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        dialog.setOption(QFileDialog.Option.ShowDirsOnly, False)
        dialog.setOption(QFileDialog.Option.DontUseNativeDialog,True)
        current_index = self.tree.rootIndex()
        current_path = Path(self.model.filePath(current_index))
        dialog.setDirectory(str(current_path))

        # Mostrar apenas arquivos SEG-Y
        filter_str = f'Arquivos SEG-Y {self._segy_extensions}'.replace('.','*.').replace("'","").replace(",","")
        dialog.setNameFilter(filter_str)
        # Ícone personalizado
        dialog.setIconProvider(self._icon_sgyfile)

        if dialog.exec():
            path = dialog.selectedFiles()[0]
            index = self.model.index(path)
            self.tree.setRootIndex(index)
            self._set_current_diretory(Path(path))

    @Slot()
    def _button_sort_name_clicked(self):
        current_order = self.tree.header().sortIndicatorOrder()

        if current_order == Qt.SortOrder.AscendingOrder:
            new_order = Qt.SortOrder.DescendingOrder
        else:
            new_order = Qt.SortOrder.AscendingOrder

        self.tree.sortByColumn(0, new_order)

    @Slot()
    def _button_sort_size_clicked(self):
        current_order = self.tree.header().sortIndicatorOrder()

        if current_order == Qt.SortOrder.AscendingOrder:
            new_order = Qt.SortOrder.DescendingOrder
        else:
            new_order = Qt.SortOrder.AscendingOrder

        self.tree.sortByColumn(1, new_order)

    @Slot()
    def _refresh_current_directory(self) -> None:
        current_index = self.tree.rootIndex()
        current_path = self.model.filePath(current_index)

        self.model.setRootPath("")
        new_index = self.model.setRootPath(current_path)

        self.tree.setRootIndex(new_index)

    @Slot()
    def _on_selection_changed(self, selected: QItemSelection, _deselected: QItemSelection) -> None:
        indexes = selected.indexes()
        if not indexes:
            return

        index = indexes[0].siblingAtColumn(0)
        path = Path(self.model.filePath(index))
        if path.is_file():
            self.file_selected.emit(path)

    @Slot()
    def _on_double_clicked(self, index) -> None:
        index = index.siblingAtColumn(0)

        path = Path(self.model.filePath(index))

        if path.is_dir():
            self.tree.setRootIndex(index)
            self._set_current_diretory(path)

# ========================================================================================================
    def _inital_path(self)->Path:
        saved_path = self._settings.value("file_browser/last_directory")
        if saved_path:
            path = Path(saved_path)

            if path.exists() and path.is_dir():
                return path

        documents = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)

        if documents and Path(documents).is_dir():
            return Path(documents)

        return Path(QDir.rootPath())

    def _make_button(self, text_button: str, path_icon: Path, tooltip_text: str ) -> QPushButton:
        btn = QPushButton(text_button)
        btn.setIcon(QIcon(str(path_icon)))
        btn.setIconSize(QSize(25, 25))
        btn.setToolTip(tooltip_text)
        btn.setStyleSheet(self._button_style)

        return btn

    def _set_current_diretory(self, path:Path) -> None:
        self._settings.setValue("file_browser/last_directory", str(path))
        self.path_label.setText(str(path))