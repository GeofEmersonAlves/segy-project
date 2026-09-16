# -*- coding: utf-8 -*-
"""
===============================================================================
Projeto    : segy-project
Arquivo    : h_synchronized_seismic_data_widget.py
Autor      : Emerson Alves da Silva
Python     : Python 3.12.13 | packaged by Anaconda, Inc.

Descrição:
       Classe base para os widgets que compõem a área principal de visualização
    da Seismic Data Window, essa classe garante o sincronismo horizontal no widget.

       Esta classe concentra apenas propriedades e operações comuns necessárias
    para manter o sincronismo horizontal entre:

        - TraceHeaderView
        - SeismicDataView
        - TraceAttributeGraphView
        - Qualquer outro novo widget que queira colocar na Seismic Data Window e
        precise que ele tenha sincronismo horizontal.

       Cada widget utiliza o mesmo SeismicViewport e, consequentemente, trabalha com a
    mesma faixa de traços visíveis. A classe não possui responsabilidades específicas de desenho .

       Todo widget que queira exibir dados sincronizados horizontalmente com outros widgest na
    Seismic Data Window deve ser filho de HSynchronizedSeismicDataWidget para garantir o sincronismo
    horizontal dos dados exibidos

Histórico:
       11/09/2026 - Criacão do Widget
===============================================================================
"""

from PySide6.QtWidgets import QWidget
from segy_viewer.application.seismic_data_window import SeismicViewport

class HSynchronizedSeismicDataWidget(QWidget):
    """
    Classe base dos widgets que compõem a visualização sísmica com sincronizacao horizontal.

    O SynchronizedSeismicDataWidget fornece:

        - acesso ao SeismicViewport compartilhado;
        - primeiro traço visível;
        - quantidade de traços visíveis;
        - traço selecionado;
        - limites horizontais da área de plotagem;
        - espaçamento horizontal entre traços;
        - conversão do índice global do traço para coordenada X;
        - conversão da coordenada X para índice do traço;
        - atualização da visualização.

    O eixo vertical não é tratado nesta classe, pois cada widget possui
    um sistema vertical diferente.
    """

    def __init__(self, viewport: SeismicViewport, parent=None):
        super().__init__(parent)

        self._viewport = viewport

        # Margens horizontais comuns à área de visualização.
        # É importante que os widgets sincronizados utilizem os mesmos valores para
        # garantir que permaneçam horizontalmente alinhados.
        self._left_margin: float = 55.0
        self._right_margin: float = 5.0

    # ======================================================================
    # Viewport
    # ======================================================================
    @property
    def viewport(self) -> SeismicViewport:
        """
        Retorna o viewport compartilhado pela Seismic Data Window.
        """
        return self._viewport

    @property
    def first_trace_position(self) -> int:
        """
        Primeira posição de visualização atualmente visível.
        """
        return self._viewport.first_trace_position

    @property
    def first_trace(self) -> int:
        """
        Índice global do primeiro traço atualmente visível.
        """
        return self.first_trace_position

    @property
    def last_trace_position(self) -> int:
        """
        Última posição de visualização atualmente visível.
        """
        if self.trace_count <= 0:
            return self.first_trace_position

        return self.first_trace_position + self.trace_count - 1

    @property
    def last_trace(self) -> int:
        """
        Alias temporário para compatibilidade.
        """
        return self.last_trace_position

    @property
    def trace_count(self) -> int:
        """
        Quantidade de traços atualmente visíveis.
        """
        return self._viewport.trace_count

    @property
    def selected_trace(self) -> int | None:
        """
        Retorna o índice global do traço selecionado.
        """

        return self._viewport.selected_trace

    # ======================================================================
    # Horizontal geometry
    # ======================================================================
    @property
    def left_margin(self) -> float:
        """
        Margem esquerda da área de plotagem.
        """
        return self._left_margin

    @property
    def right_margin(self) -> float:
        """
        Margem direita da área de plotagem.
        """
        return self._right_margin

    @property
    def plot_left(self) -> float:
        """
        Coordenada X onde começa a área útil de plotagem.
        """
        return self._left_margin

    @property
    def plot_right(self) -> float:
        """
        Coordenada X onde termina a área útil de plotagem.
        """

        return max(
            self.plot_left,
            self.width() - self._right_margin,
        )

    @property
    def plot_width(self) -> float:
        """
        Largura horizontal disponível para os traços.
        """

        return max(
            0.0,
            self.width()
            - self._left_margin
            - self._right_margin,
        )

    @property
    def trace_spacing(self) -> float:
        """
        Distância horizontal entre os centros de dois traços consecutivos.

        A divisão utiliza a quantidade de traços visíveis definida pelo
        SeismicViewport.
        """

        if self.trace_count <= 0:
            return 0.0

        return (
            self.plot_width
            / self.trace_count
        )

    @property
    def x_scale(self) -> float:
        """
        Escala horizontal em pixels por posição de visualização.
        """
        return self.trace_spacing

    # ======================================================================
    # Trace coordinates
    # ======================================================================
    def trace_position_to_x(self, trace_position: int) -> float:
        """
        Converte uma posição de visualização na coordenada X
        correspondente ao centro do traço.
        """
        local_position = (trace_position - self.first_trace_position)
        return (self.plot_left  + local_position * self.x_scale + self.x_scale / 2.0)


    def trace_to_x(self, trace_index: int) -> float:
        """
            Alias temporário para compatibilidade.
            """
        return self.trace_position_to_x(trace_index)

    def x_to_trace_position(self, x: float) -> int | None:
        """
        Converte uma coordenada X na posição de visualização
        correspondente.
        """
        if self.trace_count <= 0:
            return None

        if self.x_scale <= 0.0:
            return None

        if not self.plot_left <= x < self.plot_right:
            return None

        local_position = int(
            (x - self.plot_left) / self.x_scale
        )

        if not 0 <= local_position < self.trace_count:
            return None

        return self.first_trace_position + local_position

    def x_to_trace(self, x: float) -> int | None:
        """
            Alias temporário para compatibilidade.
        """
        return self.x_to_trace_position(x)

    # ======================================================================
    # Trace range
    # ======================================================================
    def visible_trace_range(self) -> range:
        return range(self.first_trace_position,
                     self.first_trace_position + self.trace_count)

    def is_trace_visible(self, trace_position: int) -> bool:
        return (self.first_trace_position
                <= trace_position
                <= self.last_trace_position
                )

    # ======================================================================
    # Margins
    # ======================================================================
    def set_horizontal_margins(self, left: float, right: float) -> None:
        """
        Define as margens horizontais utilizadas pela área de visualização.

        Os três widgets principais devem receber os mesmos valores.
        """
        self._left_margin = max(0.0, float(left))
        self._right_margin = max(0.0, float(right))
        self.update()

    # ======================================================================
    # Refresh
    # ======================================================================

    def refresh(self) -> None:
        """
        Solicita o redesenho do widget.

        A SeismicDataWindow pode chamar este método simultaneamente nos três
        componentes após alterações no SeismicViewport.
        """

        self.update()