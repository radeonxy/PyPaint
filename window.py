import os, sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QColor


from view import View


class Window(QtWidgets.QMainWindow):
    def __init__(self, position=(0, 0), dimension=(500, 300)):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("CAI  2425P: Drawing Application")
        self.setWindowIcon(QtGui.QIcon("Icons/app.png"))
        x, y = position
        w, h = dimension
        self.filename = None

        self.view = View()
        self.scene = QtWidgets.QGraphicsScene()
        self.view.setScene(self.scene)
        self.setCentralWidget(self.view)

        self.view.setGeometry(x, y, w, h)
        self.scene.setSceneRect(x, y, w, h)

        self.create_actions()
        self.connect_actions()
        self.create_menus()

    def set_color_from_action(self):
        action = self.sender()
        color = action.data()
        self.view.set_pen_color(color)  # line color
        self.view.set_brush_color(color)  # fill color

    def get_view(self):
        return self.view

    def get_scene(self):
        return self.scene

    def use_pencil_tool(self, checked):
        if checked:
            self.view.set_tool("pencil")
            #self.action_tools_eraser.setChecked(False)
        else:
            self.view.set_tool("line")  # or default

    def use_eraser_tool(self, checked):
        if checked:
            self.view.set_tool("eraser")
            #self.action_tools_eraser.setChecked(False)
            # Uncheck other tools if any, to keep only one active
        else:
            # Optionally reset to default tool when unchecked
            self.view.set_tool("line")

    def create_actions(self):
        # File actions
        self.action_file_new = QtWidgets.QAction(QtGui.QIcon('Icons/new.png'), "New", self)
        self.action_file_new.setShortcut("Ctrl+N")
        self.action_file_new.setStatusTip("Create a new file")

        self.action_file_open = QtWidgets.QAction(QtGui.QIcon('Icons/open.png'), "Open", self)
        self.action_file_open.setShortcut("Ctrl+O")
        self.action_file_open.setStatusTip("Open a saved file")

        self.action_file_save = QtWidgets.QAction(QtGui.QIcon('Icons/save.png'), "Save", self)
        self.action_file_save.setShortcut("Ctrl+S")
        self.action_file_save.setStatusTip("Save this file")

        self.action_file_saveas = QtWidgets.QAction(QtGui.QIcon('Icons/save_as.png'), "Save As", self)
        self.action_file_saveas.setShortcut("Ctrl+Shift+S")
        self.action_file_saveas.setStatusTip("Save this file as")

        self.action_file_export = QtWidgets.QAction(QtGui.QIcon('Icons/export.png'), "Export as Image", self)
        self.action_file_export.setShortcut("Ctrl+E")
        self.action_file_export.setStatusTip("Export drawing as png")

        self.action_file_exit = QtWidgets.QAction(QtGui.QIcon('Icons/exit.png'), "Exit", self)
        self.action_file_exit.setShortcut("Ctrl+Q")
        self.action_file_exit.setStatusTip("Exit")

        self.action_color_red = QtWidgets.QAction(QtGui.QIcon('Icons/red.png'), "Red", self)
        self.action_color_red.setData(QColor('#FF0000'))
        self.action_color_red.setStatusTip("Set color to Red")

        self.action_color_green = QtWidgets.QAction(QtGui.QIcon('Icons/green.png'), "green", self)
        self.action_color_green.setData(QColor('#00FF00'))
        self.action_color_green.setStatusTip("Set color to green")

        self.action_color_blue = QtWidgets.QAction(QtGui.QIcon('Icons/blue.png'), "blue", self)
        self.action_color_blue.setData(QColor('#0000FF'))
        self.action_color_blue.setStatusTip("Set color to blue")

        self.action_color_yellow = QtWidgets.QAction(QtGui.QIcon('Icons/yellow.png'), "yellow", self)
        self.action_color_yellow.setData(QColor('#FFFF00'))
        self.action_color_yellow.setStatusTip("Set color to yellow")

        self.action_color_black = QtWidgets.QAction(QtGui.QIcon('Icons/black.png'), "black", self)
        self.action_color_black.setData(QColor('#000000'))
        self.action_color_black.setStatusTip("Set color to black")

        # Tools actions
        self.action_tools = QtWidgets.QActionGroup(self)

        self.action_tools_pencil = QtWidgets.QAction(QtGui.QIcon('Icons/pencil.png'), self.tr("&Pencil"), self)
        self.action_tools_pencil.setCheckable(True)
        self.action_tools.addAction(self.action_tools_pencil)

        self.action_tools_eraser = QtWidgets.QAction(QtGui.QIcon('Icons/eraser.png'), self.tr("&Eraser"), self)
        self.action_tools_eraser.setCheckable(True)
        self.action_tools.addAction(self.action_tools_eraser)

        self.action_tools_line = QtWidgets.QAction(QtGui.QIcon('Icons/tool_line.png'), self.tr("&Line"), self)
        self.action_tools_line.setCheckable(True)
        self.action_tools_line.setChecked(True)
        self.action_tools.addAction(self.action_tools_line)

        self.action_tools_rect = QtWidgets.QAction(QtGui.QIcon('Icons/tool_rectangle.png'), self.tr("&Rectangle"), self)
        self.action_tools_rect.setCheckable(True)
        self.action_tools.addAction(self.action_tools_rect)

        self.action_tools_ellipse = QtWidgets.QAction(QtGui.QIcon('Icons/ellipse.png'), self.tr("&Ellipse"), self)
        self.action_tools_ellipse.setCheckable(True)
        self.action_tools.addAction(self.action_tools_ellipse)

        self.action_tools_polygon = QtWidgets.QAction(QtGui.QIcon('Icons/tool_polygon.png'), self.tr("&Polygon"), self)
        self.action_tools_polygon.setCheckable(True)
        self.action_tools.addAction(self.action_tools_polygon)

        self.action_tools_text = QtWidgets.QAction(QtGui.QIcon('Icons/tool_text.png'), self.tr("Te&xt"), self)
        self.action_tools_text.setCheckable(True)
        self.action_tools.addAction(self.action_tools_text)

        # Edit actions
        self.action_edit_undo = QtWidgets.QAction(QtGui.QIcon('Icons/undo.png'), "Undo", self)
        self.action_edit_undo.setShortcut("Ctrl+Z")
        self.action_edit_undo.setStatusTip("Undo last action")

        self.action_edit_redo = QtWidgets.QAction(QtGui.QIcon('Icons/redo.png'), "Redo", self)
        self.action_edit_redo.setShortcut("Ctrl+Y")
        self.action_edit_redo.setStatusTip("Redo last action")

        # Style actions
        self.action_style_pen_color = QtWidgets.QAction(QtGui.QIcon('Icons/colorize.png'), self.tr("&Color"), self)
        self.action_style_pen_width = QtWidgets.QAction(QtGui.QIcon('Icons/width.png'), self.tr("&Width"), self)
        self.action_style_pen_style = QtWidgets.QAction(QtGui.QIcon('Icons/style.png'), self.tr("&Style"), self)

        self.action_style_brush_color = QtWidgets.QAction(QtGui.QIcon('Icons/colorize.png'), self.tr("&Color"), self)
        self.action_style_brush_style = QtWidgets.QAction(QtGui.QIcon('Icons/brush.png'), self.tr("&Pattern"), self)

        # Clear action
        self.action_edit_clear = QtWidgets.QAction(QtGui.QIcon('Icons/clear.png'), "Clear All", self)
        self.action_edit_clear.setShortcut("Ctrl+Delete")
        self.action_edit_clear.setStatusTip("Clear all items")

        # Help actions
        self.action_help_about = QtWidgets.QAction(QtGui.QIcon('Icons/aboutus.png'),"About Us", self)
        self.action_help_aboutqt = QtWidgets.QAction(QtGui.QIcon('Icons/aboutqt.png'),"About Qt", self)
        self.action_help_aboutapp = QtWidgets.QAction(QtGui.QIcon('Icons/aboutapp.png'),"About the Application", self)

    def connect_actions(self):
        self.action_file_new.triggered.connect(self.file_new)
        self.action_file_open.triggered.connect(self.file_open)
        self.action_file_save.triggered.connect(self.file_save)
        self.action_file_saveas.triggered.connect(self.file_saveas)
        self.action_file_export.triggered.connect(self.file_export)
        self.action_file_exit.triggered.connect(self.file_exit)

        self.action_tools_line.triggered.connect(lambda: self.view.set_tool("line"))
        self.action_tools_rect.triggered.connect(lambda: self.view.set_tool("rectangle"))
        self.action_tools_ellipse.triggered.connect(lambda: self.view.set_tool("ellipse"))
        self.action_tools_polygon.triggered.connect(lambda: self.view.set_tool("polygon"))
        self.action_tools_text.triggered.connect(lambda: self.view.set_tool("text"))
        self.action_tools_pencil.triggered.connect(lambda: self.view.set_tool("pencil"))
        self.action_tools_eraser.triggered.connect(lambda: self.view.set_tool("eraser"))
        self.action_color_red.triggered.connect(self.set_color_from_action)
        self.action_color_green.triggered.connect(self.set_color_from_action)
        self.action_color_blue.triggered.connect(self.set_color_from_action)
        self.action_color_yellow.triggered.connect(self.set_color_from_action)
        self.action_color_black.triggered.connect(self.set_color_from_action)

        self.action_edit_undo.triggered.connect(self.view.undo)
        self.action_edit_redo.triggered.connect(self.view.redo)
        self.action_edit_clear.triggered.connect(self.edit_clear)

        self.action_style_pen_color.triggered.connect(self.style_pen_color_selection)
        self.action_style_pen_width.triggered.connect(self.style_pen_width_selection)
        self.action_style_pen_style.triggered.connect(self.style_pen_style_selection)
        self.action_style_brush_color.triggered.connect(self.style_brush_color_selection)
        self.action_style_brush_style.triggered.connect(self.style_brush_style_selection)

        self.action_help_about.triggered.connect(self.help_about_us)
        self.action_help_aboutqt.triggered.connect(self.help_about_qt)
        self.action_help_aboutapp.triggered.connect(self.help_about_app)



    # File actions implementation
    def file_new(self):
        reply = QtWidgets.QMessageBox.warning(self, "Warning",
                                              "Do you want to create a new file? All unsaved changes will be lost.",
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.clear_scene()
            self.filename = None

    def file_open(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", os.getcwd(), "JSON Files (*.json)")
        if filename:
            self.clear_scene()

            try:
                with open(filename, 'r') as file:
                    data = json.load(file)

                self.load_items_from_data(data)

                self.filename = filename
                QtWidgets.QMessageBox.information(self, "Open Successful",
                                                  f"File successfully opened from {filename}")
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Open Failed",
                                              f"Failed to open file: {str(e)}")

    def load_items_from_data(self, data):
        """Load items from JSON data"""
        for item_data in data:
            item = None

            if item_data["type"] == "line":
                x1, y1, x2, y2 = item_data["x1"], item_data["y1"], item_data["x2"], item_data["y2"]
                item = QtWidgets.QGraphicsLineItem(x1, y1, x2, y2)
            elif item_data["type"] == "rectangle":
                x, y, width, height = item_data["x"], item_data["y"], item_data["width"], item_data["height"]
                item = QtWidgets.QGraphicsRectItem(x, y, width, height)
            elif item_data["type"] == "ellipse":
                x, y, width, height = item_data["x"], item_data["y"], item_data["width"], item_data["height"]
                item = QtWidgets.QGraphicsEllipseItem(x, y, width, height)
            elif item_data["type"] == "polygon":
                points = []
                for point in item_data["points"]:
                    points.append(QtCore.QPointF(point[0], point[1]))
                item = QtWidgets.QGraphicsPolygonItem(QtGui.QPolygonF(points))
            elif item_data["type"] == "text":
                item = QtWidgets.QGraphicsTextItem(item_data["text"])
                item.setPos(item_data["x"], item_data["y"])
                if "font_family" in item_data and "font_size" in item_data:
                    font = QtGui.QFont(item_data["font_family"], item_data["font_size"])
                    item.setFont(font)
                if "pen_color" in item_data:
                    item.setDefaultTextColor(QtGui.QColor(item_data["pen_color"]))

            if item and hasattr(item, 'setPen'):
                pen = QtGui.QPen()
                if "pen_color" in item_data:
                    pen.setColor(QtGui.QColor(item_data["pen_color"]))
                if "pen_width" in item_data:
                    pen.setWidth(item_data["pen_width"])
                item.setPen(pen)

            if item and hasattr(item, 'setBrush'):
                brush = QtGui.QBrush()
                if "brush_color" in item_data:
                    brush.setColor(QtGui.QColor(item_data["brush_color"]))
                if "brush_fill" in item_data:
                    brush.setStyle(item_data["brush_fill"])
                item.setBrush(brush)

            if item:
                self.scene.addItem(item)
                self.view.undo_stack.append(item)

    def file_save(self):
        if self.filename is None:
            self.file_saveas()
        else:
            self.save_to_json(self.filename)

    def file_saveas(self):
        filters = "JSON Files (*.json);;PNG Files (*.png);;JPEG Files (*.jpg *.jpeg)"
        filename, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save File As", os.getcwd(), filters)

        if filename:
            if '.' not in filename:
                if 'JSON' in selected_filter:
                    filename += '.json'
                elif 'PNG' in selected_filter:
                    filename += '.png'
                elif 'JPEG' in selected_filter:
                    filename += '.jpg'

            file_extension = filename.split('.')[-1].lower()

            if file_extension == 'json':
                self.save_to_json(filename)
                self.filename = filename
            elif file_extension in ['png', 'jpg', 'jpeg']:
                self.save_to_image(filename)

    def file_export(self):
        filters = "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;BMP Files (*.bmp)"
        filename, selected_filter = QtWidgets.QFileDialog.getSaveFileName(
            self, "Export Image", os.getcwd(), filters)

        if filename:
            if '.' not in filename:
                if 'PNG' in selected_filter:
                    filename += '.png'
                elif 'JPEG' in selected_filter:
                    filename += '.jpg'
                elif 'BMP' in selected_filter:
                    filename += '.bmp'

            self.save_to_image(filename)

    def info_file(self):
        items = []

        for item in self.scene.items():
            item_data = self.get_item_data(item)
            if item_data:
                items.append(item_data)

        return items

    def get_item_data(self, item):
        """Extract data from a graphics item"""
        item_data = {}

        if isinstance(item, QtWidgets.QGraphicsLineItem):
            line = item.line()
            position = item.pos()

            item_data = {
                "type": "line",
                "x1": line.x1() + position.x(),
                "y1": line.y1() + position.y(),
                "x2": line.x2() + position.x(),
                "y2": line.y2() + position.y(),
                "pen_color": item.pen().color().name(),
                "pen_width": item.pen().width(),
            }
        elif isinstance(item, QtWidgets.QGraphicsEllipseItem):
            rect = item.rect()
            position = item.pos()
            item_data = {
                "type": "ellipse",
                "x": rect.x() + position.x(),
                "y": rect.y() + position.y(),
                "width": rect.width(),
                "height": rect.height(),
                "pen_color": item.pen().color().name(),
                "pen_width": item.pen().width(),
                "brush_color": item.brush().color().name(),
                "brush_fill": item.brush().style()
            }
        elif isinstance(item, QtWidgets.QGraphicsRectItem) and not isinstance(item, QtWidgets.QGraphicsEllipseItem):
            rect = item.rect()
            position = item.pos()
            item_data = {
                "type": "rectangle",
                "x": rect.x() + position.x(),
                "y": rect.y() + position.y(),
                "width": rect.width(),
                "height": rect.height(),
                "pen_color": item.pen().color().name(),
                "pen_width": item.pen().width(),
                "brush_color": item.brush().color().name(),
                "brush_fill": item.brush().style()
            }
        elif isinstance(item, QtWidgets.QGraphicsPolygonItem):
            position = item.pos()
            points = [(point.x() + position.x(), point.y() + position.y()) for point in item.polygon()]
            item_data = {
                "type": "polygon",
                "points": points,
                "pen_color": item.pen().color().name(),
                "pen_width": item.pen().width(),
                "brush_color": item.brush().color().name(),
                "brush_fill": item.brush().style()
            }
        elif isinstance(item, QtWidgets.QGraphicsTextItem):
            item_data = {
                "type": "text",
                "text": item.toPlainText(),
                "x": item.x(),
                "y": item.y(),
                "font_family": item.font().family(),
                "font_size": item.font().pointSize(),
                "pen_color": item.defaultTextColor().name()
            }

        return item_data

    def save_to_json(self, filename):
        try:
            items = self.info_file()
            with open(filename, 'w') as file:
                json.dump(items, file, indent=4)

            QtWidgets.QMessageBox.information(self, "Save Successful",
                                              f"File successfully saved to {filename}")
        except Exception as e:
            QtWidgets.QMessageBox.warning(self, "Save Failed",
                                          f"Failed to save file: {str(e)}")

    def save_to_image(self, filename):
        rect = self.scene.sceneRect()
        image = QtGui.QImage(int(rect.width()), int(rect.height()), QtGui.QImage.Format_ARGB32_Premultiplied)
        image.fill(QtCore.Qt.white)

        painter = QtGui.QPainter(image)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        self.scene.render(painter)
        painter.end()

        success = image.save(filename)

        if success:
            QtWidgets.QMessageBox.information(self, "Export Successful",
                                              f"Image successfully exported to {filename}")
        else:
            QtWidgets.QMessageBox.warning(self, "Export Failed",
                                          "Failed to save the image! Try again.")

    def file_exit(self):
        reply = QtWidgets.QMessageBox.question(self, "Exit",
                                               "Are you sure you want to exit?",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            QtWidgets.qApp.quit()

    # Style actions implementation
    def style_pen_color_selection(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.yellow, self)
        if color.isValid():
            self.view.set_pen_color(color)

    def style_pen_width_selection(self):
        width, ok = QtWidgets.QInputDialog.getInt(self, "Line Width", "Enter width (1-20px):",
                                                  self.view.get_pen().width(), 1, 20)
        if ok:
            self.view.set_pen_width(width)

    def style_pen_style_selection(self):
        styles = {
            "Solid": QtCore.Qt.SolidLine,
            "Dash": QtCore.Qt.DashLine,
            "Dot": QtCore.Qt.DotLine,
            "Dash Dot": QtCore.Qt.DashDotLine,
            "Dash Dot Dot": QtCore.Qt.DashDotDotLine
        }
        style, ok = QtWidgets.QInputDialog.getItem(self, "Pen Style",
                                                   "Select style:", styles.keys(), 0, False)
        if ok and style:
            self.view.set_pen_style(styles[style])

    def style_brush_color_selection(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.blue, self)
        if color.isValid():
            self.view.set_brush_color(color)

    def style_brush_style_selection(self):
        styles = {
            "None": QtCore.Qt.NoBrush,
            "Solid": QtCore.Qt.SolidPattern,
            "Backward Diagonal": QtCore.Qt.BDiagPattern,
            "Forward Diagonal": QtCore.Qt.FDiagPattern,
            "Cross": QtCore.Qt.CrossPattern,
            "Cross Striped": QtCore.Qt.DiagCrossPattern,
            "Horizontal": QtCore.Qt.HorPattern,
            "Vertical": QtCore.Qt.VerPattern,

            #"Linear Gradient": QtGui.QBrush(QtGui.QLinearGradient(0, 0, 100, 100)),
            #"Radial Gradient": QtGui.QBrush(QtGui.QRadialGradient(50, 50, 50)),
            #"Conical Gradient": QtGui.QBrush(QtGui.QConicalGradient(50, 50, 0)),

            "Pattern 1": QtCore.Qt.Dense1Pattern,
            "Pattern 2": QtCore.Qt.Dense2Pattern,
            "Pattern 3": QtCore.Qt.Dense3Pattern,
            "Pattern 4": QtCore.Qt.Dense4Pattern,
            "Pattern 5": QtCore.Qt.Dense5Pattern,
            "Pattern 6": QtCore.Qt.Dense6Pattern,
            "Pattern 7": QtCore.Qt.Dense7Pattern

        }
        style, ok = QtWidgets.QInputDialog.getItem(self, "Brush Style",
                                                   "Select style:", styles.keys(), 0, False)
        if ok and style:
            self.view.set_brush_style(styles[style])

    # Edit actions implementation
    def edit_clear(self):
        reply = QtWidgets.QMessageBox.warning(self, "Warning",
                                              "Are you sure you want to clear everything?",
                                              QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.clear_scene()

    def clear_scene(self):
        self.scene.clear()
        self.view.undo_stack.clear()
        self.view.redo_stack.clear()

    # Help actions implementation
    def help_about_us(self):
        QtWidgets.QMessageBox.information(self, "About Us",
                                          "Cette application a été créée par l'étudiant en quatrième année Abdel Halim FAWAZ, dans le module CAI du semestre 7 en 2025 à l'ENIB.\n\n"
                                          "Contact: a24fawaz@enib.fr\n"
                                          "Prof: M. Alexis Nédélec\n\n"
                                          "No copyright !© 2025. No rights reserved."
                                           )

    def help_about_qt(self):
        QtWidgets.QApplication.aboutQt()

    def help_about_app(self):
        QtWidgets.QMessageBox.information(self, "À propos de l'application",
                                          "Dans cette application, vous pouvez dessiner à l'aide des outils fournis, "
                                          "modifier le remplissage, la largeur et les couleurs.\n"
                                          "Pour dessiner un carré ou un cercle exact, appuyez sur la touche Shift en dessinant.\n"
                                          'Vous pouvez utiliser le menu "Style" pour modifier les caractéristiques de style.\n'
                                          "Vous pouvez aussi utiliser les fonctionnalités 'Undo ou ctrl+Z' et 'Redo ou ctrl+Y' avec les raccourcis du clavier.\n"
                                          "Vous pouvez sauvegarder votre travail pour l'ouvrir plus tard, et quand vous terminez, vous pouvez l'exporter comme une image.\n"
                                          "Amusez-vous bien !")

    def toggle_dark_mode(self, checked):
        if checked:
            dark_style = """
            QWidget {
                background-color: #121212;
                color: #e0e0e0;
            }
            QToolButton {
                background-color: #696868;
                color: #e0e0e0;
                border-radius: 6px;
                padding: 6px;
            }
            QToolButton:hover {
                background-color: #264a24;
            }
            QToolButton:pressed {
                background-color: #12d406;
            }
            QToolButton:checked {
                background-color: #12d406;
            }
            """

            QtWidgets.QApplication.instance().setStyleSheet(dark_style)
        else:
            QtWidgets.QApplication.instance().setStyleSheet("")

    def create_menus(self):
        # Menubar actions
        menubar = self.menuBar()

        # File menu
        menu_file = menubar.addMenu('&File')
        menu_file.addAction(self.action_file_new)
        menu_file.addSeparator()
        menu_file.addAction(self.action_file_open)
        menu_file.addAction(self.action_file_save)
        menu_file.addAction(self.action_file_saveas)
        menu_file.addAction(self.action_file_export)
        menu_file.addSeparator()
        menu_file.addAction(self.action_file_exit)

        # Edit menu
        menu_edit = menubar.addMenu('&Edit')
        menu_edit.addAction(self.action_edit_undo)
        menu_edit.addAction(self.action_edit_redo)
        menu_edit.addSeparator()
        menu_edit.addAction(self.action_edit_clear)

        # Tools menu
        menu_tool = menubar.addMenu('&Tools')
        menu_tool.addAction(self.action_tools_line)
        menu_tool.addAction(self.action_tools_rect)
        menu_tool.addAction(self.action_tools_ellipse)
        menu_tool.addAction(self.action_tools_polygon)
        menu_tool.addSeparator()
        menu_tool.addAction(self.action_tools_text)

        # Colors submenu or direct actions
        color_menu = menu_tool.addMenu('Colors')

        colors = {
            'Red': '#FF0000',
            'Green': '#00FF00',
            'Blue': '#0000FF',
            'Yellow': '#FFFF00',
            'Black': '#000000'
        }

        for name, hex_color in colors.items():
            action = QtWidgets.QAction(name, self)
            action.setData(hex_color)  # store color code in action
            action.triggered.connect(self.set_color_from_action)
            color_menu.addAction(action)

        # Style menu
        menu_style = menubar.addMenu('&Style')
        menu_style_pen = menu_style.addMenu(QtGui.QIcon('Icons/line.png'),'&Line')
        menu_style_pen.addAction(self.action_style_pen_color)
        menu_style_pen.addAction(self.action_style_pen_width)
        menu_style_pen.addAction(self.action_style_pen_style)


        self.action_toggle_dark = QtWidgets.QAction(QtGui.QIcon('Icons/dark.png'),"Switch to Dark Mode", self)
        self.action_toggle_dark.setCheckable(True)
        self.action_toggle_dark.triggered.connect(self.toggle_dark_mode)
        menu_view = menubar.addMenu('&Dark Mode')

        menu_view.addAction(self.action_toggle_dark)



        menu_style_brush = menu_style.addMenu(QtGui.QIcon('Icons/colorandfill.png'),'&Color and Fill')
        menu_style_brush.addAction(self.action_style_brush_color)
        menu_style_brush.addAction(self.action_style_brush_style)

        # Help menu
        menu_help = menubar.addMenu('&Help')
        menu_help.addAction(self.action_help_about)
        menu_help.addAction(self.action_help_aboutqt)
        menu_help.addAction(self.action_help_aboutapp)

        # Toolbar actions
        toolbar = self.addToolBar("File")
        toolbar.addAction(self.action_file_new)
        toolbar.addAction(self.action_file_open)
        toolbar.addAction(self.action_file_save)
        toolbar.addAction(self.action_file_saveas)
        toolbar.addAction(self.action_file_export)
        toolbar.addSeparator()
        toolbar.addAction(self.action_edit_undo)
        toolbar.addAction(self.action_edit_redo)



        toolbar.repaint()

        # Toolbar for tools
        toolbar_tools = self.addToolBar("Tools")
        toolbar_tools.addAction(self.action_tools_pencil)
        toolbar_tools.addAction(self.action_tools_eraser)
        toolbar_tools.addAction(self.action_tools_line)
        toolbar_tools.addAction(self.action_tools_rect)
        toolbar_tools.addAction(self.action_tools_ellipse)
        toolbar_tools.addAction(self.action_tools_polygon)
        toolbar_tools.addAction(self.action_tools_text)
        toolbar_tools.addAction(self.action_color_red)
        toolbar_tools.addAction(self.action_color_green)
        toolbar_tools.addAction(self.action_color_blue)
        toolbar_tools.addAction(self.action_color_yellow)
        toolbar_tools.addAction(self.action_color_black)



        # Statusbar
        statusbar = self.statusBar()



    def resizeEvent(self, event):
        print("MainWindow.resizeEvent() : View")
        if self.view:
            print("dx : ", self.size().width() - self.view.size().width())
            print("dy : ", self.size().height() - self.view.size().height())
        else:
            print("Error : View is None")
        print("Menubar size : ", self.menuBar().size())

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu()

        # Tools submenu - reuse existing actions
        tools_menu = menu.addMenu("Tools")
        tools_menu.addAction(self.action_tools_line)
        tools_menu.addAction(self.action_tools_rect)
        tools_menu.addAction(self.action_tools_ellipse)
        tools_menu.addAction(self.action_tools_polygon)
        tools_menu.addAction(self.action_tools_text)

        # Style submenu - reuse existing actions
        style_menu = menu.addMenu("Style")
        pen_menu = style_menu.addMenu("Pen")
        pen_menu.addAction(self.action_style_pen_color)
        pen_menu.addAction(self.action_style_pen_width)
        pen_menu.addAction(self.action_style_pen_style)

        brush_menu = style_menu.addMenu("Brush")
        brush_menu.addAction(self.action_style_brush_color)
        brush_menu.addAction(self.action_style_brush_style)

        # Export option - reuse existing action
        menu.addSeparator()
        menu.addAction(self.action_file_export)

        # Clear action - reuse existing action
        menu.addSeparator()
        menu.addAction(self.action_edit_clear)

        # Execute menu
        menu.exec_(event.globalPos())