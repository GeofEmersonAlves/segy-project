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
    app_version: str = "0.1.0"     #Versão
    app_author: str = "Emerson Alves da Silva"
    app_theme = ""

    segy_extensions: tuple[str, ...] = (".sgy", ".segy") #Extensões SEG-Y reconhecidas
    default_trace_block_size: int = 500  # Tamanho inicial da janela, ainda precisa ajustar,
    button_style = """
                        QPushButton {
                            border: 1px solid #cfcfcf;
                            border-radius: 4px;
                            background-color: #f5f5f5;
                            padding: 3px;
                        }
                    
                        QPushButton:hover {
                            background-color: #e3e3e3;
                            border: 1px solid #a9a9a9;
                        }
                    
                        QPushButton:pressed {
                            background-color: #d0d0d0;
                        }
                    """

    # -quantidade inicial de traces para visualização
    # -diretório de logs
    # -limites de cache