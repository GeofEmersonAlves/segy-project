# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_data_window_use_cases.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
     Interface da camada application utilizada pela SeismicDataWindow.
     A presentation conhece apenas esta classe e os DTOs retornados por ela.
     Toda a lógica de acesso aos dados fica delegada à sessão.

Histórico:
       14/09/2026 - Criação da classe
===============================================================================
"""
from pathlib import Path
from segy_viewer.application.seismic_data_window import SeismicViewport
from segy_viewer.application.seismic_data_window.dto import SeismicWindowInfoDTO, SeismicDataBlockDTO
from segy_viewer.application.seismic_data_window.services import SeismicDataSession

class SeismicDataWindowUseCases:
    def __init__(self, session: SeismicDataSession) -> None:
        self._session = session
        self._is_open = False

    @property
    def is_open(self) -> bool:
        return self._is_open


    def open(self, path: Path) -> SeismicWindowInfoDTO:
        """
        Abre uma sessão de dados para a Seismic Data Window.
        """
        if self._is_open:
            raise RuntimeError("Seismic data session is already open.") #Talvez trocar por uma mensagem

        info = self._session.open(path)
        self._is_open = True

        return info


    def load_data(self, viewport: SeismicViewport,
                        header_keys: tuple[str, ...],
                        graph_header_keys: tuple[str, ...]) -> SeismicDataBlockDTO:
        """
        Carrega os dados necessários para atender ao viewport atual.
        A SeismicDataWindow informa:
            - viewport atual;
            - headers mostrados no TraceHeaderView;
            - headers mostrados no TraceAttributeGraphView.
        A sessão decide:
            - quais posições precisam ser carregadas;
            - tamanho do buffer;
            - quais índices físicos correspondem às posições;
            - como ler os dados do arquivo;
            - se dados já disponíveis em cache podem ser reutilizados.
        """

        if not self._is_open:
            raise RuntimeError("Seismic data session is not open.")

        return self._session.load_data(viewport=viewport,
                                       header_keys=header_keys,
                                       graph_header_keys=graph_header_keys)


    def close(self) -> None:
        if not self._is_open:
            return

        try:
            self._session.close()

        finally:
            self._is_open = False


