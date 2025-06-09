#!/usr/bin/python
import sys
from PyQt5 import QtCore,QtGui,QtWidgets

class ColorPalette(QtWidgets.QWidget):
    def __init__(self, view):
        super().__init__()
        self.view = view
        layout = QtWidgets.QHBoxLayout(self)
        colors = ["red", "green", "blue", "yellow", "black"]
        for c in colors:
            btn = QtWidgets.QPushButton()
            btn.setFixedSize(30, 30)
            btn.setStyleSheet(f"background-color: {c};")
            btn.clicked.connect(lambda _, col=c: self.set_color(col))
            layout.addWidget(btn)

    def set_color_from_action(self):
        action = self.sender()
        color = action.data()
        self.view.set_pen_color(color)
        self.view.set_brush_color(color)

    def set_color(self, color):
        self.view.set_pen_color(color)
        self.view.set_brush_color(color)
        self.view.viewport().update()


class View (QtWidgets.QGraphicsView) :
    def __init__(self,position=(0,0),dimension=(600,400)):
        QtWidgets.QGraphicsView.__init__(self)
        x,y=position
        w,h=dimension
        self.setGeometry(x,y,w,h)

        self.begin,self.end=QtCore.QPoint(0,0),QtCore.QPoint(0,0)
        self.offset=QtCore.QPoint(0,0)
        self.pen,self.brush=None,None
        self.tool="line"
        self.item=None
        self.polygon_points = []
        self.undo_stack = []
        self.redo_stack = []

        self.create_style()

        # Enable multiple selection
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.setRubberBandSelectionMode(QtCore.Qt.IntersectsItemShape)

    def __repr__(self):
        return "<View({},{},{})>".format(self.pen,self.brush,self.tool)

    # Getters/Setters
    def get_pen(self) :
        return self.pen
    def set_pen(self,pen) :
        self.pen=pen
    def set_pen_color(self,color) :
        self.pen.setColor(QtGui.QColor(color))
    def set_pen_width(self, width):
        self.pen.setWidth(width)
    def set_pen_style(self, style):
        self.pen.setStyle(style)

    def get_brush(self) :
        return self.brush
    def set_brush(self,brush) :
        self.brush=brush
    def set_brush_color(self,color) :
        self.brush.setColor(QtGui.QColor(color))
    def set_brush_style(self, style):
        self.brush.setStyle(style)

    def get_tool(self) :
        return self.tool
    def set_tool(self,tool) :
        if tool == "polygon":
            self.polygon_points = []
        self.tool=tool


    def create_style(self) :
        self.pen=QtGui.QPen()
        self.pen.setColor(QtCore.Qt.red)
        self.brush=QtGui.QBrush()
        self.brush.setColor(QtCore.Qt.blue)
        self.brush.setStyle(QtCore.Qt.CrossPattern)

    def undo(self):
        if self.undo_stack:
            item = self.undo_stack.pop()
            self.scene().removeItem(item)
            self.redo_stack.append(item)

    def redo(self):
        if self.redo_stack:
            item = self.redo_stack.pop()
            self.scene().addItem(item)
            self.undo_stack.append(item)

    # Mouse Events
    def mousePressEvent(self, event):
        # Disable text editing when clicking elsewhere
        for item in self.scene().items():
            if isinstance(item, QtWidgets.QGraphicsTextItem):
                item.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

        if self.tool == "pencil":
            self.path = QtGui.QPainterPath(self.mapToScene(event.pos()))
            self.pencil_item = QtWidgets.QGraphicsPathItem(self.path)
            self.pencil_item.setPen(self.pen)
            self.add_item(self.pencil_item)

        if self.tool == "eraser":
            item = self.scene().itemAt(self.mapToScene(event.pos()), QtGui.QTransform())
            if item:
                self.scene().removeItem(item)
                if item in self.undo_stack:
                    self.undo_stack.remove(item)

        self.begin=self.end=event.pos()
        if self.scene() :
            self.item = self.scene().itemAt(self.mapToScene(self.begin), QtGui.QTransform())
            if self.item :
                self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
                self.item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
                self.offset = self.begin - self.mapFromScene(self.item.pos())
                self.item.setSelected(True)
            elif self.tool == "polygon":
                self.polygon_points.append(self.mapToScene(self.begin))
                if event.type() == QtCore.QEvent.MouseButtonDblClick and len(self.polygon_points) >= 3:
                    self.end_polygon()

    def mouseMoveEvent(self, event):
        self.end=event.pos()
        if self.scene() :
            if self.item :
                self.item.setPos(self.mapToScene(event.pos()) - self.offset)
            else :
                self.scene().update()

        if self.tool == "pencil" and hasattr(self, "path"):
            self.path.lineTo(self.mapToScene(event.pos()))
            self.pencil_item.setPath(self.path)
            self.scene().update()



    def mouseReleaseEvent(self, event):
        self.end=event.pos()
        if self.scene() :
            if self.item :
                self.item.setPos(self.mapToScene(event.pos()) - self.offset)
                self.item=None
            elif self.tool=="line" :
                self.create_line()
            elif self.tool=="rectangle" :
                self.create_rectangle()
            elif self.tool=="ellipse" :
                self.create_ellipse()
            elif self.tool=="text" :
                self.create_text()
            elif self.tool=="polygon" and len(self.polygon_points) > 1:
                self.draw_polygon_line()
            elif self.tool == "pencil":
                self.path = None
                self.pencil_item = None

    def mouseDoubleClickEvent(self, event):
        if self.tool == "polygon" and len(self.polygon_points) >= 3:
            self.end_polygon()

    # Shape creation methods
    def create_line(self):
        start_point = self.mapToScene(self.begin)
        end_point = self.mapToScene(self.end)
        line=QtWidgets.QGraphicsLineItem(start_point.x(), start_point.y(),
                                    end_point.x(), end_point.y())
        line.setPen(self.pen)
        self.add_item(line)

    def create_rectangle(self):
        start_point = self.mapToScene(self.begin)
        end_point = self.mapToScene(self.end)
        w = abs(end_point.x() - start_point.x())
        h = abs(end_point.y() - start_point.y())

        # Constrain to square if Shift is pressed
        if QtWidgets.QApplication.keyboardModifiers() & QtCore.Qt.ShiftModifier:
            size = min(w, h)
            w = h = size

        rect = QtWidgets.QGraphicsRectItem(
            min(start_point.x(), end_point.x()),
            min(start_point.y(), end_point.y()),
            w,
            h
        )
        rect.setPen(self.pen)
        rect.setBrush(self.brush)
        self.add_item(rect)

    def create_ellipse(self):
        start_point = self.mapToScene(self.begin)
        end_point = self.mapToScene(self.end)
        w = abs(end_point.x() - start_point.x())
        h = abs(end_point.y() - start_point.y())

        # Constrain to circle if Shift is pressed
        if QtWidgets.QApplication.keyboardModifiers() & QtCore.Qt.ShiftModifier:
            size = min(w, h)
            w = h = size

        ellipse = QtWidgets.QGraphicsEllipseItem(
            min(start_point.x(), end_point.x()),
            min(start_point.y(), end_point.y()),
            w,
            h
        )
        ellipse.setPen(self.pen)
        ellipse.setBrush(self.brush)
        self.add_item(ellipse)

    def create_text(self):
        item = self.scene().itemAt(self.mapToScene(self.begin), QtGui.QTransform())
        if isinstance(item, QtWidgets.QGraphicsTextItem):
            item.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
            item.setFocus()
        else:
            text = QtWidgets.QGraphicsTextItem("Double-cliquez pour éditer")
            text.setPos(self.mapToScene(self.begin))
            text.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
            self.add_item(text)

    def draw_polygon_line(self):
        if len(self.polygon_points) > 2:
            start_point = self.polygon_points[0]
            end_point = self.polygon_points[-1]
            distance = ((end_point.x() - start_point.x())**2 +
                        (end_point.y() - start_point.y())**2)**0.5
            if distance < 10:
                self.polygon_points[-1] = self.polygon_points[0]
                self.end_polygon()
                return

        start_point = self.polygon_points[-2]
        end_point = self.polygon_points[-1]
        line = QtWidgets.QGraphicsLineItem(start_point.x(), start_point.y(),
                                    end_point.x(), end_point.y())
        line.setPen(self.pen)
        self.scene().addItem(line)
        self.undo_stack.append(line)

    def end_polygon(self):
        if len(self.polygon_points) >= 3:
            poly = QtGui.QPolygonF()
            for point in self.polygon_points:
                poly.append(point)

            polygon = QtWidgets.QGraphicsPolygonItem(poly)
            polygon.setPen(self.pen)
            polygon.setBrush(self.brush)

            # Remove temporary lines
            temp_lines = [item for item in self.scene().items()
                        if isinstance(item, QtWidgets.QGraphicsLineItem)]
            for line in temp_lines:
                self.scene().removeItem(line)

            self.add_item(polygon)
            self.undo_stack = [item for item in self.undo_stack
                            if not isinstance(item, QtWidgets.QGraphicsLineItem)]

        self.polygon_points = []

    def add_item(self, item):
        """Add item to scene with common properties"""
        item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        item.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.scene().addItem(item)
        self.undo_stack.append(item)
        self.redo_stack.clear()

    def paintEvent(self, event):
        QtWidgets.QGraphicsView.paintEvent(self, event)

        if not self.item and self.begin != self.end and self.tool != "text":
            painter = QtGui.QPainter(self.viewport())
            painter.setRenderHint(QtGui.QPainter.Antialiasing)

            pen = QtGui.QPen(QtCore.Qt.gray)
            pen.setStyle(QtCore.Qt.DashLine)
            painter.setPen(pen)

            view_begin = self.mapFromScene(self.mapToScene(self.begin))
            view_end = self.mapFromScene(self.mapToScene(self.end))

            if self.tool == "line":
                painter.drawLine(view_begin, view_end)
            elif self.tool == "rectangle":
                painter.drawRect(QtCore.QRect(view_begin, view_end).normalized())
            elif self.tool == "ellipse":
                painter.drawEllipse(QtCore.QRect(view_begin, view_end).normalized())


    def resizeEvent(self,event):
        print("View.resizeEvent()")
        print("width : {}, height : {}".format(self.size().width(),self.size().height()))