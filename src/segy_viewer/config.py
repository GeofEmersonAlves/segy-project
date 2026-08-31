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
    app_name: str = "SEG-Y Viewer" #Nome da aplicação
    app_version: str = "1.0.0"     #Versão
    app_author: str = "Emerson Alves da Silva"
    app_theme = ""

    segy_extensions: tuple[str, ...] = (".sgy", ".segy") #Extensões SEG-Y reconhecidas

    default_trace_block_size: int = 500  # Tamanho inicial da janela, ainda precisa ajustar,
    button_style = """
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

    status_bar_button_style = """
                                QToolButton {
                                    border: 1px solid transparent;
                                    border-radius: 3px;
                                    padding: 2px 6px;
                                    background-color: transparent;
                                }
                            
                                QToolButton:hover {
                                    background-color: #e5e5e5;
                                    border: 1px solid #c5c5c5;
                                }
                            
                                QToolButton:pressed {
                                    background-color: #d0d0d0;
                                }
                            
                                QToolButton:checked {
                                    background-color: #d6e9ff;
                                    border: 1px solid #7aaee6;
                                }
                            
                                QPushButton:hover {
                                    background-color: #e3e3e3;
                                    border-radius: 3px;
                                    border: 1px solid #a9a9a9;
                                }"
                            """

    tree_browser_style = """
                            QTreeView::item:selected {
                                background-color: #0078D7;
                                color: white;
                            }
                        
                            QTreeView::item:selected:!active {
                                background-color: #0078D7;
                                color: white;
                            }
                        """

    # -quantidade inicial de traces para visualização
    # -diretório de logs
    # -limites de cache