import statistics
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import csv
import math
import numpy as np
from PyQt6 import QtWidgets as qtw
from functools import partial
import scipy
import scipy.stats
import transforming_functions as transform_func
import model_functions as model_func
import plotting_functions as plot_func


def mean(vals):
    return np.mean(vals), np.std(vals, ddof=1)


def multiply(vals, st_dev):
    return vals[0] * vals[1], math.sqrt(pow(st_dev[0]/vals[0], 2) + pow(st_dev[1]/vals[1], 2))


def divide(vals, st_dev):
    return vals[0] / vals[1], math.sqrt(pow(st_dev[0] / vals[0], 2) + pow(st_dev[1] / vals[1], 2))


def add(vals, st_dev):
    return vals[0] + vals[1], math.sqrt(pow(st_dev[0] / vals[0], 2) + pow(st_dev[1] / vals[1], 2))


def subtract(vals, st_dev):
    return vals[0] + vals[1], math.sqrt(pow(st_dev[0] / vals[0], 2) + pow(st_dev[1] / vals[1], 2))


operations_dict = {
    "Mean": (mean, 0, False),
    "Multiply": (multiply, 2, True),
    "Divide": (divide, 2, True),
    "Add": (add, 2, True),
    "Subtract": (subtract, 2, True)
}


class GraphWindow(qtw.QMainWindow):

    def __init__(self):

        self.filename = None

        self.min = None
        self.max = None

        plt.style.use("seaborn-whitegrid")

        self.handles = []
        self.lines = []

        self.fig, self.ax = plt.subplots(figsize=(14, 10), layout="constrained")
        plt.ion()
        plt.show()

        self.cycle = 0
        self.colours = [["mediumblue", "#084eff"],
                        ["orangered", "coral"],
                        ["maroon", "firebrick"],
                        ["#bd08ff", "orchid"],
                        ["green", "mediumseagreen"],
                        ["k", "grey"],
                        ["goldenrod", "gold"],
                        ["cyan", "lightskyblue"]
                        ]

        super().__init__()

        self.setFixedSize(250, 560)
        self.setWindowTitle("Graph Generator")

        self.layout = qtw.QFormLayout()

        self.ingest_button = qtw.QPushButton("Open")
        self.ingest_button.clicked.connect(self.ingest)
        self.layout.addWidget(self.ingest_button)

        self.drop_y_func = qtw.QComboBox()
        self.drop_y_func.addItems(transform_func.function_dict.keys())
        self.layout.addRow("y-func", self.drop_y_func)

        self.drop_y_vals = qtw.QComboBox()
        self.layout.addRow("y-val", self.drop_y_vals)

        self.drop_x_func = qtw.QComboBox()
        self.drop_x_func.addItems(transform_func.function_dict.keys())
        self.layout.addRow("x-func", self.drop_x_func)

        self.drop_x_vals = qtw.QComboBox()
        self.layout.addRow("x-val", self.drop_x_vals)

        self.drop_line_type = qtw.QComboBox()
        self.drop_line_type.addItems(plot_func.plotting_dict.keys())
        self.layout.addRow("Plot type: ", self.drop_line_type)

        self.line_button = qtw.QCheckBox("Line of Best Fit")
        self.layout.addWidget(self.line_button)

        self.rank_button = qtw.QCheckBox("Include Pearson's r")
        self.layout.addWidget(self.rank_button)

        self.scale_button = qtw.QCheckBox("Scale y-axis")
        self.layout.addWidget(self.scale_button)

        self.line_label = qtw.QLineEdit()
        self.layout.addRow("Label", self.line_label)

        self.add_button = qtw.QPushButton("Add Plot")
        self.add_button.clicked.connect(self.add_plot)
        self.layout.addWidget(self.add_button)

        self.clear_button = qtw.QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_graph)
        self.layout.addWidget(self.clear_button)

        self.title = qtw.QLineEdit()
        self.layout.addRow("Title", self.title)

        self.x_label = qtw.QLineEdit()
        self.layout.addRow("x-label", self.x_label)

        self.y_label = qtw.QLineEdit()
        self.layout.addRow("y-label", self.y_label)

        self.generate_button = qtw.QPushButton("Update Titles")
        self.generate_button.clicked.connect(self.generate_graph)
        self.layout.addWidget(self.generate_button)

        self.plot_drop_down = qtw.QComboBox()
        self.plot_drop_down.addItems(model_func.plotting_dict.keys())
        self.layout.addRow("Model Type: ", self.plot_drop_down)

        self.plot_button = qtw.QPushButton("Add Model")
        self.plot_button.clicked.connect(self.add_line_plot)
        self.layout.addWidget(self.plot_button)

        self.widget = qtw.QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def ingest(self):
        self.filename, _ = qtw.QFileDialog.getOpenFileName(self, "Open File", ".", "Csv Files (*.csv)")
        try:
            with open(self.filename, "r") as file:
                data_dict = csv.DictReader(file)

                self.drop_x_vals.clear()
                self.drop_y_vals.clear()

                self.drop_x_vals.addItems(data_dict.fieldnames)
                self.drop_y_vals.addItems(data_dict.fieldnames)
        except (FileNotFoundError, TypeError):
            pass

    def add_plot(self):
        try:
            if self.filename is None:
                qtw.QMessageBox.warning(
                    self, "No File", "You haven't selected a file or the file you selected has beem moved or deleted.",
                    qtw.QMessageBox.StandardButton.Ok)
            else:
                with open(self.filename, "r") as file:
                    data_dict = csv.DictReader(file)

                    flag = False

                    x = [[]]
                    x_list = []
                    y = [[]]
                    y_list = []
                    x_name = self.drop_x_vals.currentText()
                    y_name = self.drop_y_vals.currentText()
                    for row in data_dict:
                        try:
                            x_val = transform_func.function_dict[
                                             self.drop_x_func.currentText()](float(row[x_name]))
                            x[-1].append(x_val)
                            x_list.append(x_val)
                            try:
                                y_val = transform_func.function_dict[
                                    self.drop_y_func.currentText()](float(row[y_name]))
                                y[-1].append(y_val)
                                y_list.append(y_val)
                                flag = True
                            except (ValueError, ZeroDivisionError):
                                x[-1].pop()
                                x_list.pop()
                                if x[-1]:
                                    x.append([])
                                    y.append([])
                        except (ValueError, ZeroDivisionError):
                            if x[-1]:
                                x.append([])
                                y.append([])

                if flag:

                    if self.scale_button.isChecked():
                        y_bar = statistics.mean(y_list)
                        y_std_dev = statistics.stdev(y_list)
                        for section in y:
                            for i in range(len(section)):
                                if y_std_dev != 0:
                                    section[i] = (section[i] - y_bar) / y_std_dev
                                else:
                                    section[i] = (section[i] - y_bar)

                    if self.line_label.text():
                        name = self.line_label.text()
                    else:
                        name = f"{y_name} vs {x_name}"

                    colours = self.colours[self.cycle]
                    self.cycle = (self.cycle + 1) % len(self.colours)
                    self.lines.append([
                        x, y, self.line_button.isChecked(), self.rank_button.isChecked(),
                        colours, name, plot_func.plotting_dict[self.drop_line_type.currentText()], "data"])

                    if self.max is not None:
                        self.max = max(*x_list, self.max)
                        self.min = min(*x_list, self.min)
                    else:
                        self.max = max(*x_list)
                        self.min = min(*x_list)

                    self.ax.clear()
                    self.generate_graph()

                else:
                    qtw.QMessageBox.warning(
                        self, "Type Failure", "The data you selected is not numerical.",
                        qtw.QMessageBox.StandardButton.Ok)
        except FileNotFoundError:
            qtw.QMessageBox.warning(
                self, "No File", "You haven't selected a file or the file you selected has beem moved or deleted.",
                qtw.QMessageBox.StandardButton.Ok)
        except TypeError:
            qtw.QMessageBox.warning(
                self, "Type Failure", "The data you selected is not numerical.",
                qtw.QMessageBox.StandardButton.Ok)
        except ValueError:
            qtw.QMessageBox.warning(
                self, "Type Failure", "The data you selected is not numerical.",
                qtw.QMessageBox.StandardButton.Ok)

    def clear_graph(self):
        self.cycle = 0
        self.lines = []
        self.ax.clear()
        self.max = None
        self.min = None

    def add_line_plot(self):
        draw_func, label_func, args = model_func.plotting_dict[self.plot_drop_down.currentText()]
        plot_window = PlotWindow(self, draw_func, label_func, *args)
        plot_window.show()

    def generate_graph(self):
        self.handles = []

        for line in self.lines:
            if line[-1] == "data":
                self.handles += line[-2](*line[:-2])

            elif self.max is not None:
                label, draw_func, options, _ = line
                x, y = draw_func(*options, self.min, self.max)

                colours = self.colours[self.cycle]
                self.cycle = (self.cycle + 1) % len(self.colours)

                line, = plt.plot(x, y, color=colours[0], label=label)
                self.handles.append(line)

        self.ax.legend(handles=self.handles)

        self.ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
        self.ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
        self.ax.tick_params(which="minor", length=3, width=0.7)
        self.ax.tick_params(which="major", length=5, width=1.3)

        plt.grid(linewidth=0.8, color="darkgrey")
        plt.grid(linewidth=0.4, color="gainsboro", which="minor")

        self.ax.set_title(self.title.text())
        self.ax.set_xlabel(self.x_label.text())
        self.ax.set_ylabel(self.y_label.text())


class PlotWindow(qtw.QDialog):

    def __init__(self, parent, draw_func, label_func, *options):
        super().__init__()

        self.parent = parent

        self.layout = qtw.QFormLayout()

        self.input_boxes = []
        for option in options:
            self.input_boxes.append(qtw.QLineEdit())
            self.layout.addRow(option, self.input_boxes[-1])

        self.submit_button = qtw.QPushButton("Submit")
        self.submit_button.clicked.connect(partial(self.closeEvent, None))
        self.layout.addWidget(self.submit_button)

        self.widget = qtw.QWidget()
        self.setLayout(self.layout)

        self.plot_func, self.label_func = draw_func, label_func

    def closeEvent(self, event):
        options = []
        for input_box in self.input_boxes:
            options.append(model_func.convert_to_number(input_box.text()))

        self.parent.lines.append([self.label_func(*options), self.plot_func, options, "model"])
        self.parent.generate_graph()
        self.done(0)


app = qtw.QApplication([])
window = GraphWindow()
window.show()
app.exec()
