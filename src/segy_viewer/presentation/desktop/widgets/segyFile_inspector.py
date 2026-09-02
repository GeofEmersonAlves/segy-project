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
       28/08/2026 - Melhoras e novas funcionalidades e padronização das abas de Texto
       01/09/2026 - Inclusão de um signal quando muda de tab na tela
===============================================================================
"""
from pathlib import Path
from PySide6.QtCore import Signal, Qt, QSize, Slot
from PySide6.QtGui import QFontDatabase, QTextOption, QIcon, QPalette
from PySide6.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QPlainTextEdit,
                               QStatusBar, QTableView, QHeaderView, QPushButton, QFileDialog, QMessageBox, QLabel)
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
_DAY_THEME_ICO =   _BASE_DIR / "resources" / "icons" / "day.png"
_NIGHT_THEME_ICO = _BASE_DIR / "resources" / "icons" / "night.png"

class SegyFileInspector(QWidget):
    segy_inspector_empty = Signal()  # Signal emitido o inspector está vázio
    segy_inspector_has_data = Signal()
    segy_inspector_tab_changed = Signal(str)

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
        self._tabs.tabBarClicked.connect(self._emit_tab_changed_signal)

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

    @property
    def section_type(self) -> InspectorSectionType:
        return InspectorSectionType
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

    def export_summary(self):
        self._export_dto_content(InspectorSectionType.SUMMARY)

    def export_text_header(self) :
        self._export_dto_content(InspectorSectionType.TEXT_HEADER)

    def export_binary_header(self) :
        self._export_dto_content(InspectorSectionType.BIN_HEADER)

    def export_trace_header(self) :
        self._export_dto_content(InspectorSectionType.TRACE_HEADER)

    def import_text_header(self):
        self._import_text_header()

    def show_summary(self) :
        self._tabs.setCurrentIndex(0)

    def show_text_header(self) :
        self._tabs.setCurrentIndex(1)

    def show_binary_header(self) :
        self._tabs.setCurrentIndex(2)

    def show_trace_header(self) :
        self._tabs.setCurrentIndex(3)
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
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        section_widget = QWidget()

        if section_name == InspectorSectionType.SUMMARY:
            self._summary_text = self._create_text_view()
            self._summary_cursor_position_label = QLabel()
            self._summary_theme_button = self._create_status_bar_button(icon_path=_DAY_THEME_ICO,
                                                                        txt_tooltip="Change Theme Light/Dark")
            self._summary_text_status_bar = self._create_text_status_bar(self._summary_text,
                                                                         self._summary_cursor_position_label,
                                                                         self._summary_theme_button)
            layout.addWidget(self._summary_text)
            layout.addWidget(self._summary_text_status_bar)


        elif section_name == InspectorSectionType.TEXT_HEADER:
            self._text_header =self._create_text_view()
            self._text_header_cursor_position_label = QLabel()
            self._text_header_theme_button = self._create_status_bar_button(icon_path=_DAY_THEME_ICO,
                                                                            txt_tooltip="Change Theme Light/Dark")
            self._text_header_status_bar = self._create_text_status_bar(self._text_header,
                                                                        self._text_header_cursor_position_label,
                                                                        self._text_header_theme_button)
            #Cria os botões da status bar do Text Header
            self._export_text_header_button = self._create_status_bar_button(icon_path=_EXPORT_ICO,
                                                                             txt_tooltip="Export Text Header to text file")
            self._export_text_header_button.clicked.connect(lambda : self._export_dto_content(InspectorSectionType.TEXT_HEADER))
            self._import_text_header_button = self._create_status_bar_button(icon_path=_IMPORT_TEXT_HEADER_ICO,
                                                                             txt_tooltip = "Import text file to this Segy Text Header" )
            self._import_text_header_button.clicked.connect(self._import_text_header)

            #Cria os botões Reset e Update do Text Header
            self._reset_text_header_button = self._create_status_bar_button(icon_path=_RESET_TEXT_HEADER_ICO,
                                                                       txt_tooltip = "Reset Text Header to original text" )
            self._reset_text_header_button.setText("Reset")
            self._reset_text_header_button.clicked.connect(self._reset_text_header)
            self._update_text_header_button = self._create_status_bar_button(icon_path=_UPDATE_TEXT_HEADER_ICO,
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

            layout.addWidget(self._text_header)
            layout.addWidget(self._text_header_status_bar)

        elif section_name == InspectorSectionType.BIN_HEADER:
            self._bin_headers_table_model = BinaryTraceHeaderTableModel(field_key="bin_header_field")
            self._binary_header_table_view = self._create_table_view(section_name)
            layout.addWidget(self._binary_header_table_view)

        elif section_name == InspectorSectionType.TRACE_HEADER:
            self._trace_header_table_model = BinaryTraceHeaderTableModel(field_key="trace_header_field")
            self._trace_header_table_view = self._create_table_view(section_name)
            layout.addWidget(self._trace_header_table_view)

        section_widget.setLayout(layout)
        return section_widget

    def _create_text_view(self) -> QPlainTextEdit:
        _text_view = QPlainTextEdit()
        _text_view.setReadOnly(True)
        _font = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        _font.setPointSize(12)
        _text_view.setFont(_font)
        _text_view.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
            | Qt.TextInteractionFlag.TextSelectableByKeyboard
        )

        return _text_view

    def _create_text_status_bar(self, text_view: QPlainTextEdit, status_label: QLabel, theme_button : QPushButton) -> QStatusBar:
        def _add_padding_left_button(button: QPushButton):
            button.setStyleSheet(
                self._status_bar_button_style +
                """
                QPushButton {
                    padding: 2px 1px;
                }
                """
            )
        _show_whitespace_button = self._create_status_bar_button(icon_path=_WHITESPACE_ICO,txt_tooltip="Show whitespaces")
        _show_whitespace_button.setCheckable(True)
        _add_padding_left_button(_show_whitespace_button)

        _left_button_size = QSize(15, 15)
        _show_whitespace_button.setIconSize(_left_button_size)
        _show_whitespace_button.toggled.connect(lambda checked:
                                                     self._set_show_invisible_characters(
                                                         text_view,
                                                         checked
                                                     ))

        status_bar = QStatusBar()
        text_view.cursorPositionChanged.connect(lambda :
                                                self._update_text_header_status_bar(text_view, status_label)
                                                )  # Para atualizar a barra de status do Text Header

        theme_button.setCheckable(True)
        _add_padding_left_button(theme_button)
        theme_button.setIconSize(_left_button_size)
        theme_button.toggled.connect(lambda checked:
                                     self._change_text_edit_theme(text_view=text_view,
                                                                  theme_button=theme_button,
                                                                  enabled=checked)
                                     )
        status_bar.addWidget(_show_whitespace_button)
        status_bar.addWidget(status_label)
        status_bar.addWidget(theme_button)

        return status_bar

    def _create_status_bar_button(self, icon_path: Path, txt_tooltip: str) -> QPushButton:
        button = QPushButton()
        button.setIcon(QIcon(str(icon_path)))
        button.setIconSize(QSize(20, 20))
        button.setToolTip(txt_tooltip)
        button.setStyleSheet(self._status_bar_button_style)

        return button

    def _create_table_view(self, section_name: InspectorSectionType)->QTableView:
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

    @Slot(int)
    def _emit_tab_changed_signal(self,index:int)->None:
        tab_text = self._tabs.tabText(index)
        self.segy_inspector_tab_changed.emit(tab_text)

    @Slot()
    def _change_text_edit_theme(self, text_view: QPlainTextEdit, theme_button : QPushButton, enabled: bool):
        palette = text_view.palette()
        text_color = palette.color(QPalette.ColorRole.Text)
        background_color = palette.color(QPalette.ColorRole.Base)
        palette.setColor(QPalette.ColorRole.Text, background_color)
        palette.setColor(QPalette.ColorRole.Base, text_color)
        text_view.setPalette(palette)

        if enabled:
            theme_button.setIcon(QIcon(str(_NIGHT_THEME_ICO)))
        else:
            theme_button.setIcon(QIcon(str(_DAY_THEME_ICO)))



    @Slot()
    def _update_text_header_status_bar(self, text_view: QPlainTextEdit, text_label: QLabel) -> None:
        cursor =  text_view.textCursor()
        lin = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        text_label.setText(f"Lin: {lin} | Col: {col}")

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
    def _export_dto_content(self, section_name:InspectorSectionType):
        _file_name = self.segy_path.stem
        _file_name += "_" + section_name.value.replace(" ", "_")

        if section_name in (InspectorSectionType.SUMMARY, InspectorSectionType.TEXT_HEADER):
            _file_filter=self.use_cases.export_segy_dto.TXT_FILTER

        elif section_name in (InspectorSectionType.BIN_HEADER, InspectorSectionType.TRACE_HEADER):
            _file_filter = self.use_cases.export_segy_dto.DICT_FILE_FILTERS

        _file_path = str(self.segy_path.parent / _file_name)
        _file_path, selected_filter = QFileDialog.getSaveFileName(self,
                                                                    caption=f"Export {section_name.value} to file",
                                                                    dir=_file_path,
                                                                    filter=_file_filter
                                                                     )
        if len(_file_path) > 0:
            _file_saved = self.use_cases.export_segy_dto.execute(segy_inspetion_dto = self._inspetion_dto,
                                                                 section_name = section_name,
                                                                 file_path = Path(_file_path),
                                                                 file_filter = selected_filter
                                                                 )
            if _file_saved:
                QMessageBox.information(self, f"{section_name.value} Saved","File saved successfully.")

            else:
                QMessageBox.critical(self, f"{section_name.value} NOT Saved","Problems saving the file!")


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



