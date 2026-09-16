import colorsys
import sys
import numpy as np
from PySide6.QtCore import Qt, QRect, QPoint, QPointF
from PySide6.QtGui import QPainter, QPen, QBrush, QColor, QFont
from PySide6.QtWidgets import QApplication, QWidget

class Function():
    def __init__(self, name: str, formation_law:str):
        self._name = name
        self._formation_law = formation_law

    @property
    def name(self):
        return self._name

    @property
    def formation_law(self):
        return self._formation_law


class Grafico(QWidget):
    def __init__(self, window_title: str, graf_title: str ):
        super().__init__()
        self.setMouseTracking(True)

        self.setWindowTitle(window_title)
        self._window_title = window_title
        self._graf_title = graf_title
        self._setMargins()

    def mouseMoveEvent(self, event):
        screen_point = event.position()
        inverse, ok = self._transform.inverted()
        if ok:
            point = inverse.map(screen_point)
            print(f"x = {point.x():.2f}, y = {point.y():.2f}")


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.begin(self)
        # Para desenhar este retangulo, ainda nao tenho meu sistema de coordenadas definidas
        painter.drawRect(self.centrimetro_to_pixels(self.left_margin),
                         self.centrimetro_to_pixels(self.top_margin),
                         self.centrimetro_to_pixels(self.draw_area_width),
                         self.centrimetro_to_pixels(self.draw_area_height))

        #Aqui crio o meu sistema de corrdenadas
        painter.save()
        self._create_cartesian_coord_system(painter)
        self._plot_cartesian_axis(painter)

        funcao1 = Function("f(X)",  "(6 * np.sin(X*2.7))/(1+0.08*X)")
        funcao2 = Function("g(X)", "3.5 + 3.5 * np.sin(X + 0.7 * np.sin(2.3*X) + 0.35 * np.cos(5.7*X))")
        funcao3 = Function("h(X)", "4*np.sin(X)*np.sin(0.3 * X)")
        funcao4 = Function("j(X)", "3*np.sin(X) + 2*np.cos(3 * X)")
        funcao5 = Function("k(X)", "6 * np.sin(X) * np.exp(-0.05 * X)")
        funcoes = [funcao1, funcao2, funcao3, funcao4,funcao5]
        colors = [Qt.blue, Qt.darkRed, Qt.darkGreen, Qt.darkYellow, Qt.darkGray]

        for i, funcao in enumerate(funcoes):
            self.funcao = funcao.formation_law
            self.plot_funcao(painter, colors[i] )


        painter.end()

    def _plot_cartesian_axis(self, painter):
        axis_pen = QPen(QColor("#232424"), 0.025, Qt.PenStyle.DashLine)
        painter.setPen(axis_pen)
        self.min_x, self.max_x = -13, 13
        self.min_y, self.max_y = -8, 9
        painter.drawLine(self.min_x, 0, self.max_x, 0)  #Eixo X
        painter.drawLine(0, self.min_y, 0, self.max_y)    #Eixo Y

        font = QFont("Arial", 12, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QPen(QColor("#2c3e50")))

        x_points=[]
        y_points=[]
        for x in range(self.min_x, self.max_x+1):
            screen_point = (x, painter.transform().map(QPointF(x, -0.5)))
            x_points.append(screen_point)

        for y in range(self.min_y, self.max_y+1):
            screen_point = (y, painter.transform().map(QPointF(-0.5, y)))
            y_points.append(screen_point)

        painter.restore()

        for x, screen_point in x_points:
            dash_point = screen_point + QPointF(-1, -10)
            text_point = screen_point + QPointF(-10, 5)
            painter.drawText(dash_point, "|")
            painter.drawText(text_point, f"{x:.2f}")

        for y, screen_point in y_points:
            dash_point = screen_point + QPointF(10, 4)
            text_point = screen_point + QPointF(-15, 4)
            painter.drawText(dash_point, "--")
            painter.drawText(text_point, f"{y:.2f}")

        painter.save()
        self._create_cartesian_coord_system(painter)


    def _create_cartesian_coord_system(self, painter):
        self._x_scale =  self._scale
        self._y_scale = -1 *  self._scale
        self.resize(self.centrimetro_to_pixels(self._width), self.centrimetro_to_pixels(self._height))

        h_y_axis = (self._height/2) * self._scale
        h_x_axis = (self._width/2) * self._scale
        painter.translate(h_x_axis, h_y_axis )  # define onde estara o 0 (zero) do meu sistema de coordenadas
        painter.scale(self._x_scale, self._y_scale)

        self._transform = painter.transform() # Guarda os parametros de trasformação


    def _setMargins(self):
        #Margens do "papel" ja em cm
        self._scale = 40
        self._width = 30
        self._height = 21
        self.left_margin = 1.5
        self.right_margin = 1.5
        self.top_margin = 1
        self.bottom_margin = 1.5
        self.draw_area_width=(self._width - (self.left_margin + self.right_margin))
        self.draw_area_height=(self._height - (self.left_margin + self.right_margin))


    def centrimetro_to_pixels(self, centrimetro: float) -> int:
        return int(centrimetro *  self._scale)

    def funcao_valor(self, X_value:float, funcao:str)->float:
        X = X_value
        Y = eval(funcao)
        return Y

    def plot_funcao(self, painter, color):
        pen = QPen(color, 3/self._scale)
        painter.setPen(pen)
        points=[]
        sample_interval=0.025/3   #FIZ ESTA CONTA PARA TER APROXIMADAMENTE 3000 AMOSTRAS
        for x_value in  np.arange(self.min_x, self.max_x+sample_interval, sample_interval):
            x_value = np.round(x_value, 3)
            y_value = self.funcao_valor(x_value, self.funcao)
            # print(f"f({x_value}) = {y_value}")
            point = QPointF(x_value, y_value)
            points.append(point)
            painter.drawPoint(point)

        line_pen = QPen(QColor("#232424"), 1/self._scale, Qt.PenStyle.SolidLine)
        painter.setPen(line_pen)
        # print(len(points))
        painter.drawPolyline(points)

    def plot_test_points(self, painter):
        pen = QPen(Qt.red, 0.1)
        painter.setPen(pen)
        point1 = QPoint(0, 0)
        painter.drawPoint(point1)

        pen = QPen(Qt.blue, 0.1)
        painter.setPen(pen)
        point2 = QPoint(1, 0)
        painter.drawPoint(point2)

        pen = QPen(Qt.black, 0.1)
        painter.setPen(pen)
        point3 = QPoint(0, 1)
        painter.drawPoint(point3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = Grafico("Gráfico de linha","Título do gráfico")
    janela.show()
    sys.exit(app.exec())