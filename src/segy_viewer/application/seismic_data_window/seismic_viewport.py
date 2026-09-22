# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : seismic_viewport.py
Autor      : Emerson Alves da Silva
Versão     : 1.0
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Classe que é objeto central para representar o viewport, classe que será
    compartilhada pelos 3 widgets da Seismic Data Window, assim os 3 widgets apresentarão
    informações dos mesmos.

Histórico:

       04/09/2026 - Início da implementação
       16/09/2026 - Inclusão da propriedade trace_under_mouse_position, que guarda
                  o número do traco para qual o ponteiro do mouse esta apontado
                  assim, todos os widgets terão esta referencia. A propriedade
                  selected_trace ser alterada quando o usuário clicar no traco.
===============================================================================
"""

from dataclasses import dataclass

@dataclass
class SeismicViewport:
    """
        first_trace_position: Representa o primeiro traço exibido,
                            não representa o indice físico do traço dentro do arquivo.
    """
    first_trace_position: int = 0
    trace_count: int = 300

    selected_trace: int | None = None
    trace_under_mouse_position: int | None = None


    time_min_ms: float = 0.0
    time_max_ms: float | None = None

    @property
    def selected_trace_number(self) -> int | None:
        if self.selected_trace is None:
            return None

        return self.selected_trace + 1
