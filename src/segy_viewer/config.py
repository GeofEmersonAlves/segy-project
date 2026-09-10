# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : config.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
        Concentra configurações da aplicação, principalmente aquelas que não pertencem ao domínio.

            -tamanho inicial da janela
            -reader padrão
            -quantidade inicial de traces para visualização
            -diretório de logs
            -limites de cache

Histórico:
       13/08/2026 - Início da implementação da Classe
===============================================================================
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    app_version: str = "0.5.0-alpha"
    app_name: str = f"Segy Viewer (Version {app_version})"
    app_author: str = "Emerson Alves da Silva"
    app_theme = ""
    segy_extensions: tuple[str, ...] = (".sgy", ".segy") #Extensões SEG-Y reconhecidas

    default_trace_block_size: int = 500  # Tamanho inicial da janela, ainda precisa ajustar,
    BUTTON_STYLE = """
                        QPushButton {
                            border: 1px solid #cfcfcf;
                            border-radius: 4px;
                            background-color: #f5f5f5;
                            padding: 1px;
                        }
                    
                        QPushButton:hover {
                            background-color: #e3e3e3;
                            border: 1px solid #a9a9a9;
                        }
                    
                        QPushButton:pressed {
                            background-color: #d0d0d0;
                        }
                    """

    STATUS_BAR_BUTTON_STYLE = """
                                QPushButton {
                                    border: 1px solid transparent;
                                    border-radius: 3px;
                                    padding: 2px 6px;
                                    background-color: transparent;
                                }
                            
                                QPushButton:hover {
                                    background-color: #e5e5e5;
                                    border: 1px solid #c5c5c5;
                                }
                            
                                QPushButton:pressed {
                                    background-color: #d0d0d0;
                                }
                            
                                QPushButton:checked {
                                    background-color: #d6e9ff;
                                    border: 1px solid #7aaee6;
                                }
                            
                                QPushButton:hover {
                                    background-color: #e3e3e3;
                                    border-radius: 3px;
                                    border: 1px solid #a9a9a9;
                                }
                            """

    TREE_BROWSER_STYLE = """
                            QTreeView::item:selected {
                                background-color: #0078D7;
                                color: white;
                            }
                        
                            QTreeView::item:selected:!active {
                                background-color: #0078D7;
                                color: white;
                            }
                        """
    COMBO_BOX_STYLE = """
                        QComboBox {
                            background-color: white;
                            border: 1px solid #909090;
                            padding: 3px 6px;
                            min-width: 150px;
                        }
                    
                        QComboBox:hover {
                            border: 1px solid #507f9d;
                        }
                    
                        QComboBox::drop-down {
                            width: 24px;
                            border-left: 1px solid #b0b0b0;
                        }
                    """
    TOOL_BAR_STYLE = """
                        QToolBar {
                            background-color: #eaf5fc;
                            border: none;
                            spacing: 4px;
                            padding: 2px;
                        }
                    
                        QToolBar QToolButton {
                            border: 1px solid transparent;
                            border-radius: 3px;
                            padding: 3px;
                        }
                    
                        QToolBar QToolButton:hover {
                            background-color: #c5dceb;
                            border: 1px solid #8aa9bd;
                        }
                    
                        QToolBar QToolButton:pressed {
                            background-color: #aecbdd;
                        }
                    
                        QToolBar QToolButton:disabled {
                            background-color: transparent;
                        }
                    
                        QToolBar::separator {
                            width: 1px;
                            margin: 4px 6px;
                            background-color: #8a8a8a;
                        }
                    """
    SEISMIC_DATA_WINDOW_TOOL_BAR_STYLE = """
                                        QToolBar {
                                            spacing: 1px;
                                            padding: 1px;
                                        }
                            
                                        QToolButton {
                                            padding: 1px;
                                            margin: 0px;
                                        }
                                        """
    SEISMIC_SCROLLBAR_STYLE = """
                                     QScrollBar:horizontal {
                                        background: #eeeeee;
                                        height: 30px;
                                        margin: 0px 30px 0px 30px;
                                        border: 1px solid #b8b8b8;
                                    }
                                
                                    QScrollBar::handle:horizontal {
                                        background: #a8a8a8;
                                        min-width: 60px;
                                        border: 1px solid #777777;
                                        border-radius: 3px;
                                    }
                                
                                    QScrollBar::handle:horizontal:hover {
                                        background: #909090;
                                    }
                                
                                    QScrollBar::handle:horizontal:pressed {
                                        background: #787878;
                                    }
                                
                                    QScrollBar::add-line:horizontal {
                                        background: #dddddd;
                                        width: 29px;
                                        subcontrol-position: right;
                                        subcontrol-origin: margin;
                                        border: 1px solid #aaaaaa;
                                    }
                                
                                    QScrollBar::sub-line:horizontal {
                                        background: #dddddd;
                                        width: 29px;
                                        subcontrol-position: left;
                                        subcontrol-origin: margin;
                                        border: 1px solid #aaaaaa;
                                    }
                                
                                    QScrollBar::add-page:horizontal {
                                        background: #eeeeee;
                                    }
                                
                                    QScrollBar::sub-page:horizontal {
                                        background: #eeeeee;
                                    }
                                """

    # -quantidade inicial de traces para visualização
    # -diretório de logs
    # -limites de cache