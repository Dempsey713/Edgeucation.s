
"""
Edgeucation -- An app designed to keep graph theory simple in the classroom

This app creates a simple, easy to use PyQt application with a NetworkX backend to help you
create, modify, and analyze graphs at the press of a button.


@author: Daniel Dempsey
@date: May 9, 2019
"""

import sys

import matplotlib.pyplot as plt
import networkx as nx
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from qtconsole.inprocess import QtInProcessKernelManager
from qtconsole.rich_jupyter_widget import RichJupyterWidget


class UI_MainWindow(QWidget):

    def __init__(self):
        super(UI_MainWindow, self).__init__()
        font = QFont()
        font.setPointSize(18)
        self.initialize_UI()

    # below sets up the UI

    def initialize_UI(self):
        self.the_graph = nx.Graph()

        self.setGeometry(100, 100, 1000, 800)
        self.setWindowTitle('Edgeucation')
        self.center()

        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.createVerticalBox()
        # self.createMenu()

        buttonBunch = QVBoxLayout()
        buttonBunch.addWidget(self.verticalButtonBox)

        consoleWidgetMaybe = createConsole(self)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.grid.addWidget(self.canvas, 0, 1, 11, 10)
        self.grid.addLayout(buttonBunch, 0, 0)
        self.grid.addWidget(consoleWidgetMaybe['widget'], 11, 1, 12, 10)

        self.color_map = [1000]
        self.houseGraphPlotTest()

        self.show()

    def createTabBox(self):
        """
        Creates a menu consisting of 2 tabs of buttons. This is where
        most of the functionality of the program will be accessed from

        :return:
        """
        self.tabBox = QTabWidget()
        self.tabBox.setObjectName("tabBox")

        self.tab1 = QWidget()
        self.tab1.setObjectName("tab1")
        self.tab2 = QWidget()
        self.tab2.setObjectName("tab2")

        self.tabBox.addTab(self.tab1, "")

    def createVerticalBox(self):
        self.verticalButtonBox = QGroupBox()
        layout = QVBoxLayout()

        self.addButtons(layout)


    def addButtons(self, layout):
        self.redrawGraphButton(layout)
        self.addNodeButton(layout)
        self.delNodeButton(layout)
        self.addEdgeButton(layout)
        self.delEdgeButton(layout)
        self.addPathButton(layout)
        self.trivialGraphButton(layout)
        self.pathGraphButton(layout)
        self.houseGraphButton(layout)
        self.regularGraphButton(layout)
        self.completeGraphButton(layout)
        self.exportGraphButton(layout)

    # Below defines the various buttons, each followed by their functional method

    def redrawGraphButton(self, layout):
        button = QPushButton('Redraw Graph')
        button.setObjectName("ButtonRedrawGraph")

        layout.addWidget(button)
        layout.setSpacing(10)
        self.verticalButtonBox.setLayout(layout)

        button.clicked.connect(self.redrawGraphNormal)

    def addNodeButton(self, layout):
        button = QPushButton('Add Node')
        button.setObjectName("ButtonAddNode")

        layout.addWidget(button)
        layout.setSpacing(10)
        self.verticalButtonBox.setLayout(layout)

        button.clicked.connect(self.addNodeToGraph)

    def addNodeToGraph(self):
        self.figure.clf()

        if nx.is_empty(self.the_graph):
            self.the_graph.add_node(0)
            # self.color_map[0] = 'blue'

        self.the_graph.add_node(list(self.the_graph.nodes)[-1] + 1)
        # self.color_map[list(self.the_graph.nodes)[-1]] = 'blue'

        nx.draw(self.the_graph,  with_labels=True)
        self.canvas.draw_idle()

    def delNodeButton(self, layout):
        button = QPushButton('Del Node')
        button.setObjectName("ButtonDelNode")

        layout.addWidget(button)
        layout.setSpacing(10)
        self.verticalButtonBox.setLayout(layout)

        button.clicked.connect(self.removeNodeFromGraph)

    def removeNodeFromGraph(self):
        if nx.is_empty(self.the_graph):
            return

        i, okPressed = QInputDialog.getInt(self, "Node to delete", "Delete which node?", list(self.the_graph.nodes)[0],
                                           list(self.the_graph.nodes)[0], list(self.the_graph.nodes)[-1], 1)
        if okPressed:
            self.figure.clf()
            try:
                self.the_graph.remove_node(i)
            except:
                pass
            nx.draw(self.the_graph, with_labels=True)
            self.canvas.draw_idle()

    def addEdgeButton(self, layout):
        button = QPushButton('Add Edge')
        button.setObjectName("ButtonAddEdge")

        layout.addWidget(button)
        layout.setSpacing(10)
        self.verticalButtonBox.setLayout(layout)

        button.clicked.connect(self.addEdgeToGraph)

    def addEdgeToGraph(self):
        i, okPressed = QInputDialog.getInt(self, "First Node", "Start at which node?", 0, 0,
                                           list(self.the_graph.nodes)[-1] + 1, 1)
        j, okPressed2 = QInputDialog.getInt(self, "Second Node", "End at which node?", 0, 0,
                                            list(self.the_graph.nodes)[-1] + 2, 1)

        if okPressed and okPressed2:
            self.figure.clf()
            self.the_graph.add_edge(i, j)
            nx.draw(self.the_graph, with_labels=True)
            self.canvas.draw_idle()

    def delEdgeButton(self, layout):
        button = QPushButton('Del Edge')
        button.setObjectName("ButtonDelEdge")

        layout.addWidget(button)
        layout.setSpacing(10)
        self.verticalButtonBox.setLayout(layout)

        button.clicked.connect(self.removeEdgeFromGraph)

    def removeEdgeFromGraph(self):
        if nx.is_empty(self.the_graph):
            return

        i, okPressed = QInputDialog.getInt(self, "First Node", "Start at which node?", list(self.the_graph.nodes)[0],
                                           list(self.the_graph.nodes)[0], list(self.the_graph.nodes)[-1], 1)
        j, okPressed2 = QInputDialog.getInt(self, "Second Node", "End at which node?", list(self.the_graph.nodes)[0],
                                            list(self.the_graph.nodes)[0], list(self.the_graph.nodes)[-1], 1)

        if okPressed and okPressed2:
            self.figure.clf()
            try:
                self.the_graph.remove_edge(i, j)
            except:
                pass
            nx.draw(self.the_graph, with_labels=True)
            self.canvas.draw_idle()

    def addPathButton(self, layout):
        button = QPushButton('Add Path')
        button.setObjectName("ButtonAddPath")

        layout.addWidget(button)
        layout.setSpacing(10)
        self.verticalButtonBox.setLayout(layout)

        button.clicked.connect(self.addPathToGraph)

    def addPathToGraph(self):
        i, okPressed = QInputDialog.getInt(self, "Path Generation", "How many nodes in path?", 1, 1, 100, 1)


        if okPressed:
            nodesToPath = []

            j, okPressed2 = QInputDialog.getInt(self, "Path Generation", "First node in path", 0, 0, list(self.the_graph.nodes)[-1] + 1, 1)
            nodesToPath.append(j)

            for k in range(1, i):
                q, okPressed3 = QInputDialog.getInt(self, "Path Generation", "Next node in path", 0, 0, list(self.the_graph.nodes)[-1] + i, 1)

                if okPressed3:
                    nodesToPath.append(q)

            self.figure.clf()
            for n in range (1, len(nodesToPath)):
                self.the_graph.add_edge(nodesToPath[n], nodesToPath[n - 1])

            nx.draw(self.the_graph, with_labels=True)
            self.canvas.draw_idle()

    def trivialGraphButton(self, layout):
        button = QPushButton('Trivial Graph')
        button.setObjectName("ButtonTrivialGraph")

        layout.addWidget(button)
        layout.setSpacing(10)
        self.verticalButtonBox.setLayout(layout)

        button.clicked.connect(self.trivialGraph)

    def trivialGraph(self):
        self.figure.clf()
        self.the_graph = nx.trivial_graph()

        nx.draw(self.the_graph, with_labels=True)
        self.canvas.draw_idle()

    def pathGraphButton(self, layout):
        button = QPushButton('Path Graph')
        button.setObjectName("ButtonPathGraph")

        layout.addWidget(button)
        layout.setSpacing(10)
        self.verticalButtonBox.setLayout(layout)

        button.clicked.connect(self.pathGraph)

    def pathGraph(self):
        i, okPressed = QInputDialog.getInt(self, "Path Graph", "How many nodes in the path?", 1, 1, 2000, 1)

        if okPressed:
            self.figure.clf()
            self.the_graph = nx.path_graph(i)

            nx.draw(self.the_graph, with_labels=True)
            self.canvas.draw_idle()

    def houseGraphButton(self, layout):
        button = QPushButton('House Graph')
        button.setObjectName("ButtonHouseGraph")

        layout.addWidget(button)
        layout.setSpacing(10)
        self.verticalButtonBox.setLayout(layout)

        button.clicked.connect(self.houseGraphPlotTest)

    def regularGraphButton(self, layout): #TODO
        button = QPushButton('Regular Graph')
        button.setObjectName("ButtonRegularGraph")

        layout.addWidget(button)
        layout.setSpacing(10)
        self.verticalButtonBox.setLayout(layout)

        button.clicked.connect(self.regularGraph)

    def regularGraph(self):
        i, okPressed = QInputDialog.getInt(self, "Regular Graph", "How many nodes in the graph?", 1, 1, 2000, 1)
        j, okPressed2 = QInputDialog.getInt(self, "Regular Graph", "Regularity:", 0, 0, i-1, 1)

        if okPressed and okPressed2:
            self.figure.clf()
            try:
                self.the_graph = nx.random_regular_graph(j, i)
            except:
                pass

            nx.draw(self.the_graph, with_labels=True)
            self.canvas.draw_idle()

    def completeGraphButton(self, layout): #TODO
        button = QPushButton('Complete Graph')
        button.setObjectName("ButtonCompleteGraph")

        layout.addWidget(button)
        layout.setSpacing(10)
        self.verticalButtonBox.setLayout(layout)

        button.clicked.connect(self.completeGraph)

    def completeGraph(self):
        i, okPressed = QInputDialog.getInt(self, "Complete Graph", "How many nodes in the graph?", 1, 1, 2000, 1)

        if okPressed:
            self.figure.clf()
            self.the_graph = nx.complete_graph(i)
            nx.draw(self.the_graph, with_labels=True)
            self.canvas.draw_idle()

    def exportGraphButton(self, layout):
        button = QPushButton('Export Graph to .png')
        button.setObjectName("ButtonExportGraph")

        layout.addWidget(button)
        layout.setSpacing(10)
        self.verticalButtonBox.setLayout(layout)

        button.clicked.connect(self.exportGraph)

    def exportGraph(self):
        plt.savefig("ExportedGraph.png", format="PNG")

    # below are some utility methods

    def center(self):
        """
        When the app is opened, this will make sure it is center-screen

        :return:
        """

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def houseGraphPlotTest(self):
        """
        Creates a simple house graph then draws it to the canvas.
        This method is intended for testing purposes.

        :return:
        """

        self.figure.clf()
        self.the_graph = nx.house_graph()

        nx.draw(self.the_graph, with_labels=True)
        self.canvas.draw_idle()

    def redrawGraphNormal(self):
        """
        clears the canvas, then draws the_graph with basic parameters

        :return:
        """

        self.figure.clf()
        nx.draw(self.the_graph, with_labels=True)
        self.canvas.draw_idle()


def createConsole(parent):
    """
    disclaimer: this code is not mine. I copied it to get an embedded console
    It will be modified at some point to attempt interactability

    source: https://stackoverflow.com/a/26676570

    :param parent:
    :return:
    """
    kernel_manager = QtInProcessKernelManager()
    kernel_manager.start_kernel()
    kernel = kernel_manager.kernel
    kernel.gui = 'qt4'

    kernel_client = kernel_manager.client()
    kernel_client.start_channels()
    kernel_client.namespace = parent

    def stop():
        kernel_client.stop_channels()
        kernel_manager.shutdown_kernel()

    layout = QVBoxLayout(parent)
    widget = RichJupyterWidget(parent=parent)
    layout.addWidget(widget, Qt.AlignRight)
    widget.kernel_manager = kernel_manager
    widget.kernel_client = kernel_client
    widget.exit_requested.connect(stop)
    ipython_widget = widget
    ipython_widget.show()
    kernel.shell.push({'widget': widget, 'kernel': kernel, 'parent': parent})
    return {'widget': widget, 'kernel': kernel}

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UI_MainWindow()

    window.show()
    app.exec_()
