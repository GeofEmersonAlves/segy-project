# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : segyFile_inspector.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Classe que cria o Widget SegyFileInpecto, Abas que mostram o resumo e os Header do arquiv

    SegyFileBrowser
    ├── Recebe um nome de um arquivo SEGY
    ├── Solicita as informações do arquivo para um "use case"
    ├── Permite salvar as informações em arquivos
    ├── Quando nao tem arquivo limpa o conteudo das abas e exibe só a sumary
    └── Permite limpar o nome do arquivo, e todas as informações são limpas

Histórico:
       16/08/2026 - Implementação da Classe
       19/08/2026 - Continuação da implementação do widget
       21/08/2026 - Início da criação das tabelas das abas Bin Header e Trace Header
       27/08/2026 - Finalização das funcionalidades da aba Text Header
===============================================================================
"""
from idlelib.rpc import response_queue
from pathlib import Path
from PySide6.QtCore import Signal, Qt, QSize, Slot
from PySide6.QtGui import QFontDatabase, QTextOption, QIcon
from PySide6.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QPlainTextEdit,
                               QStatusBar, QTableView, QHeaderView, QPushButton, QFileDialog, QMessageBox)
from segy_viewer.application.use_cases import SegyFileInspectorUseCases
from segy_viewer.application.dto import SegyFileInspectionDTO, CheckResponseDto
from segy_viewer.application.types import InspectorSectionType
from segy_viewer.presentation.desktop.model import BinaryTraceHeaderTableModel

_BASE_DIR = Path(__file__).resolve().parents[5]
_WHITESPACE_ICO = _BASE_DIR / "resources" / "icons" / "withespace.png"
_EXPORT_ICO = _BASE_DIR / "resources" / "icons" / "export.png"
_IMPORT_TEXT_HEADER_ICO = _BASE_DIR / "resources" / "icons" / "import.png"
_RESET_TEXT_HEADER_ICO = _BASE_DIR / "resources" / "icons" / "reset.png"
_UPDATE_TEXT_HEADER_ICO = _BASE_DIR / "resources" / "icons" / "update.png"


class SegyFileInspector(QWidget):
    segy_inspector_empty = Signal()  # Signal emitido o inspector está vázio
    segy_inspector_has_data = Signal()

    def __init__(self,
                 inspector_use_cases: SegyFileInspectorUseCases,
                 status_bar_button_style:str,
                 parent=None):

        super().__init__(parent)
        self.use_cases = inspector_use_cases
        self._segy_path: Path |None = None
        self._inspetion_dto : SegyFileInspectionDTO |None = None
        self._status_bar_button_style = status_bar_button_style

        self._tabs = QTabWidget() #Cria o wigdget tabs
        self._tab_sumary: QWidget= self._tab_factory(InspectorSectionType.SUMMARY)
        self._tab_text_header: QWidget= self._tab_factory(InspectorSectionType.TEXT_HEADER)
        self._tab_bin_header: QWidget = self._tab_factory(InspectorSectionType.BIN_HEADER)
        self._tab_trace_header: QWidget = self._tab_factory(InspectorSectionType.TRACE_HEADER)

        self._tabs.addTab(self._tab_sumary, InspectorSectionType.SUMMARY)
        self._tabs.addTab(self._tab_text_header, InspectorSectionType.TEXT_HEADER)
        self._tabs.addTab(self._tab_bin_header, InspectorSectionType.BIN_HEADER)
        self._tabs.addTab(self._tab_trace_header, InspectorSectionType.TRACE_HEADER)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._tabs)

#=======================================================================
    @property
    def segy_path(self) -> Path | None:
        return self._segy_path

    @segy_path.setter
    def segy_path(self, segy_path: Path | None) -> None:
        self._segy_path = segy_path
        if self._segy_path is None:
            self.clear_tabs_content()

        else:
            self._fill_tabs_with_dto()

# =======================================================================

    def clear_tabs_content(self):
       _empyt_sumaty = "There are no files selected at the moment.\n"
       _empyt_sumaty += "Select a SEG-Y file to inspect"
       self._summary_text.setPlainText(_empyt_sumaty)
       self._text_header.setPlainText("")
       self._bin_headers_table_model.set_data(data={})
       self._trace_header_table_model.set_data(data={})

       #Esconde as abas deixando somente summary visivel
       # Esconde os botoes de reset e update
       self._hide_show_text_header_buttons(is_visible=False)
       self._tabs.setTabVisible(1, False)
       self._tabs.setTabVisible(2, False)
       self._tabs.setTabVisible(3, False)

       self.segy_inspector_empty.emit()

# =======================================================================
    def _fill_tabs_with_dto(self):
        inspetion_dto: SegyFileInspectionDTO = self.use_cases.inspect_segy_file.execute(self._segy_path)
        self._inspetion_dto = inspetion_dto

        self._summary_text.setPlainText(inspetion_dto.summary)
        self._text_header.setPlainText(inspetion_dto.text_header)

        self._bin_headers_table_model.set_data(data=inspetion_dto.binary_header)
        self._trace_header_table_model.set_data(data=inspetion_dto.trace_header)

        # Mostra todas as abas
        self._tabs.setTabVisible(1, True)
        self._tabs.setTabVisible(2, True)
        self._tabs.setTabVisible(3, True)
        #Esconde os botoes de reset e update
        self._hide_show_text_header_buttons(is_visible=False)

        self.segy_inspector_has_data.emit()

    def _tab_factory(self, section_name: InspectorSectionType) -> QWidget:
        def _create_text_view() -> QPlainTextEdit:
            _text_view = QPlainTextEdit()
            _text_view.setReadOnly(True)
            _font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
            _text_view.setFont(_font)
            _text_view.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
                | Qt.TextInteractionFlag.TextSelectableByKeyboard
            )

            return _text_view

        def _create_table_view(section_name: InspectorSectionType)->QTableView:
            _table_view = QTableView()

            if section_name == InspectorSectionType.BIN_HEADER:
                _table_view.setModel(self._bin_headers_table_model)

            elif section_name == InspectorSectionType.TRACE_HEADER:
                _table_view.setModel(self._trace_header_table_model)

            _header = _table_view.horizontalHeader()
            _header.setSectionResizeMode(0,QHeaderView.ResizeMode.ResizeToContents)
            _header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
            _header.setSectionResizeMode(2,QHeaderView.ResizeMode.ResizeToContents)

            _header.setSectionResizeMode(3,QHeaderView.ResizeMode.ResizeToContents)

            return _table_view

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        section_widget = QWidget()

        if section_name == InspectorSectionType.SUMMARY:
            self._summary_text = _create_text_view()
            layout.addWidget(self._summary_text)

        elif section_name == InspectorSectionType.TEXT_HEADER:
            def _create_status_bar_button(icon_path:Path, txt_tooltip:str) -> QPushButton:
                button = QPushButton()
                button.setIcon(QIcon(str(icon_path)))
                button.setIconSize(QSize(15, 17))
                button.setToolTip(txt_tooltip)
                button.setStyleSheet(self._status_bar_button_style)

                return button

            self._text_header =_create_text_view()
            self._text_header_status_bar = QStatusBar()

            #Cria os botões da status bar do Text Header
            self._export_text_header_button = _create_status_bar_button(icon_path=_EXPORT_ICO,
                                                                        txt_tooltip = "Export Text Header to text file" )
            self._export_text_header_button.clicked.connect(self._export_text_header)

            self._import_text_header_button = _create_status_bar_button(icon_path=_IMPORT_TEXT_HEADER_ICO,
                                                                        txt_tooltip = "Import text file to this Segy Text Header" )
            self._import_text_header_button.clicked.connect(self._import_text_header)

            self._show_whitespace_button = _create_status_bar_button(icon_path = _WHITESPACE_ICO,
                                                                     txt_tooltip = "Show whitespaces")
            self._show_whitespace_button.setCheckable(True)
            self._show_whitespace_button.toggled.connect(lambda checked:
                                                         self._set_show_invisible_characters(
                                                                                self._text_header,
                                                                                checked
                                                                                ))

            #Cria os botões Reset e Update do Text Header
            self._reset_text_header_button = _create_status_bar_button(icon_path=_RESET_TEXT_HEADER_ICO,
                                                                       txt_tooltip = "Reset Text Header to original text" )
            self._reset_text_header_button.setText("Reset")
            self._reset_text_header_button.clicked.connect(self._reset_text_header)
            self._update_text_header_button = _create_status_bar_button(icon_path=_UPDATE_TEXT_HEADER_ICO,
                                                                        txt_tooltip = "Update Text Header to SEGY file" )
            self._update_text_header_button.setText("Update")
            self._update_text_header_button.clicked.connect(self._update_text_header)
            self._hide_show_text_header_buttons(is_visible=False)

            # Adiciona os botões Reset e Update na status bar do Text Header
            self._text_header_status_bar.addPermanentWidget(self._reset_text_header_button)
            self._text_header_status_bar.addPermanentWidget(self._update_text_header_button)
            #Adiciona os botões na status bar do Text Header
            self._text_header_status_bar.addPermanentWidget(self._export_text_header_button)
            self._text_header_status_bar.addPermanentWidget(self._import_text_header_button)
            self._text_header_status_bar.addPermanentWidget(self._show_whitespace_button)

            self._text_header.cursorPositionChanged.connect(self._update_text_header_status_bar)  #Para atualizar a barra de status do Text Header

            layout.addWidget(self._text_header)
            layout.addWidget(self._text_header_status_bar)

        elif section_name == InspectorSectionType.BIN_HEADER:
            self._bin_headers_table_model = BinaryTraceHeaderTableModel(field_key="bin_header_field")
            self._binary_header_table_view = _create_table_view(section_name)
            layout.addWidget(self._binary_header_table_view)

        elif section_name == InspectorSectionType.TRACE_HEADER:
            self._trace_header_table_model = BinaryTraceHeaderTableModel(field_key="trace_header_field")
            self._trace_header_table_view = _create_table_view(section_name)
            layout.addWidget(self._trace_header_table_view)

        section_widget.setLayout(layout)
        return section_widget

    @Slot()
    def _update_text_header_status_bar(self):
        cursor =  self._text_header.textCursor()
        lin = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        self._text_header_status_bar.showMessage(f"Lin: {lin} | Col: {col}")

    @Slot()
    def _set_show_invisible_characters(self, text_view: QPlainTextEdit, enabled: bool) -> None:
        option = text_view.document().defaultTextOption()

        flags = option.flags()

        if enabled:
            flags |= QTextOption.Flag.ShowTabsAndSpaces
            flags |= QTextOption.Flag.ShowLineAndParagraphSeparators
        else:
            flags &= ~QTextOption.Flag.ShowTabsAndSpaces
            flags &= ~QTextOption.Flag.ShowLineAndParagraphSeparators

        option.setFlags(flags)
        text_view.document().setDefaultTextOption(option)

    @Slot()
    def _export_text_header(self):
        _file_name = self.segy_path.stem + "_TEXT_HEADER"
        txt_file_path = str(self.segy_path.parent / _file_name)
        txt_file_path, selected_filter = QFileDialog.getSaveFileName(self,
                                                                    "Export Text Header to text file",
                                                                    txt_file_path,
                                                                    self.use_cases.export_segy_dto.TXT_FILTER
                                                                     )
        if len(txt_file_path) > 0:
            _file_saved = self.use_cases.export_segy_dto.execute(segy_inspetion_dto = self._inspetion_dto,
                                                                 section_name = InspectorSectionType.TEXT_HEADER,
                                                                 file_path = Path(txt_file_path),
                                                                 file_filter = selected_filter
                                                                 )
            if _file_saved:
                QMessageBox.information(self, "Text Header Saved","File saved successfully.")

            else:
                QMessageBox.critical(self, "Text Header NOT Saved","Problems saving the file!")

    @Slot()
    def _import_text_header(self):
        file_path = self.segy_path.parent
        filter = self.use_cases.export_segy_dto.TXT_FILTER + ";;"
        filter += self.use_cases.export_segy_dto.ALL_FILES_FILTER
        file_name, selected_filter = QFileDialog.getOpenFileName(self,
                                                                 caption="Import text file to this Segy Text Header",
                                                                 dir=str(file_path),
                                                                 filter=filter
                                                                 )
        if len(file_name) > 0:
            text_header = self.use_cases.text_header_from_txt_file.read_text_header_from_file(Path(file_name))
            response_dto: CheckResponseDto = self.use_cases.text_header_from_txt_file.validate_text(text_header)
            if response_dto.checked_pass:
               self._text_header.setPlainText(text_header)
               self._hide_show_text_header_buttons(is_visible=True)

            else:
                QMessageBox.critical(self,"Error",response_dto.message )


    @Slot()
    def _reset_text_header(self):
        _resp =  QMessageBox.question(self,"Confirmation", "Do you want to restore the original Text Header?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                     )
        if _resp == QMessageBox.StandardButton.Yes:
            self._text_header.setPlainText(self._inspetion_dto.text_header)
            self._hide_show_text_header_buttons(is_visible=False)

    @Slot()
    def _update_text_header(self):
        _resp = QMessageBox.question(self, "Confirmation", "Do you want to save Text Header in Segy file?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                     )

        if _resp == QMessageBox.StandardButton.Yes:
            use_case = self.use_cases.text_header_from_txt_file
            text_header = self._text_header.toPlainText()
            response_dto: CheckResponseDto = use_case.write_text_header_into_segy(self.segy_path, text_header)
            if response_dto.checked_pass:
                self._hide_show_text_header_buttons(is_visible=False)
                QMessageBox.information(self, "Text Header Saved","Text Header saved successfully.")
                self._fill_tabs_with_dto()

            else:
                QMessageBox.critical(self, "Error",response_dto.message )


    def _hide_show_text_header_buttons(self,is_visible: bool) -> None:
        self._reset_text_header_button.setDisabled(not is_visible)
        self._update_text_header_button.setDisabled(not is_visible)
        self._reset_text_header_button.setVisible(is_visible)
        self._update_text_header_button.setVisible(is_visible)



