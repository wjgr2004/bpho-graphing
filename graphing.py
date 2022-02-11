import statistics
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import csv
import math
import numpy as np
from PyQt6 import QtWidgets as qtw
import scipy
import scipy.stats
import graphing_functions as graph_func


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

        self.setFixedSize(250, 490)
        self.setWindowTitle("Graph Generator")

        self.layout = qtw.QFormLayout()

        self.ingest_button = qtw.QPushButton("Open")
        self.ingest_button.clicked.connect(self.ingest)
        self.layout.addWidget(self.ingest_button)

        self.drop_x_func = qtw.QComboBox()
        self.drop_x_func.addItems(graph_func.function_dict.keys())
        self.drop_x_func.setEditable(False)
        self.layout.addRow("x-func", self.drop_x_func)

        self.drop_x_vals = qtw.QComboBox()
        self.layout.addRow("x-val", self.drop_x_vals)

        self.drop_y_func = qtw.QComboBox()
        self.drop_y_func.addItems(graph_func.function_dict.keys())
        self.layout.addRow("y-func", self.drop_y_func)

        self.y_val_widget = qtw.QWidget()
        self.y_val_layout = qtw.QHBoxLayout()

        self.drop_y_vals = qtw.QComboBox()
        self.layout.addRow("y-val", self.drop_y_vals)

        self.line_button = qtw.QCheckBox("Line of Best Fit")
        self.layout.addWidget(self.line_button)

        self.rank_button = qtw.QCheckBox("Include Pearson's r")
        self.layout.addWidget(self.rank_button)

        self.scale_button = qtw.QCheckBox("Scale y-axis")
        self.layout.addWidget(self.scale_button)

        self.scatter_button = qtw.QCheckBox("Force Scatter")
        self.layout.addWidget(self.scatter_button)

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
                    flag = False
                    data_dict = csv.DictReader(file)

                    x = []
                    y = []
                    x_name = self.drop_x_vals.currentText()
                    y_name = self.drop_y_vals.currentText()
                    for row in data_dict:
                        try:
                            x.append(graph_func.function_dict[self.drop_x_func.currentText()](float(row[x_name])))
                            try:
                                y.append(graph_func.function_dict[self.drop_y_func.currentText()](float(row[y_name])))
                                flag = True
                            except (ValueError, ZeroDivisionError):
                                x.pop()
                        except (ValueError, ZeroDivisionError):
                            pass

                if flag:

                    if self.scale_button.isChecked():
                        y_bar = statistics.mean(y)
                        print(y_bar)
                        y_std_dev = statistics.stdev(y)
                        y = list(map(lambda y: (y - y_bar) / y_std_dev, y))

                    if self.line_label.text():
                        name = self.line_label.text()
                    else:
                        name = f"{y_name} vs {x_name}"

                    self.lines.append([x, y, self.line_button.isChecked(), name, self.rank_button.isChecked()])

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
        self.lines = []
        self.ax.clear()

    def generate_graph(self):
        self.cycle = 0
        self.handles = []

        for x, y, show_best_fit, label, show_rank in self.lines:
            x2 = np.array(x)
            y2 = np.array(y)

            if show_rank:
                r, p = scipy.stats.pearsonr(x, y)
                rank_text = f"\nr = {r:.4}, p = {p:.4}"
            else:
                rank_text = ""

            colours = self.colours[self.cycle]
            self.cycle = (self.cycle + 1) % 5
            if len(x) > 300 and not self.scatter_button.isChecked():
                line, = plt.plot(x, y, color=colours[0], label=label + rank_text)
            elif len(x) > 300:
                line, = plt.plot(x, y, "x", color=colours[0], label=label + rank_text, alpha=.1)
            elif len(x2) > 50:
                line, = plt.plot(x, y, "x", color=colours[0], label=label + rank_text, alpha=.7)
            else:
                line, = plt.plot(x, y, "x", color=colours[0], label=label + rank_text)
            self.handles.append(line)

            if show_best_fit:
                min_val = None
                max_val = None
                for x_val in x2:
                    if min_val is None:
                        min_val = x_val
                    else:
                        min_val = min(min_val, x_val)
                    if max_val is None:
                        max_val = x_val
                    else:
                        max_val = max(max_val, x_val)

                # noinspection PyTupleAssignmentBalance
                m, c = np.polyfit(x2, y2, 1)

                points = np.array([min_val, max_val])
                best_fit, = plt.plot(points, m * points + c, label=f"y = {m:.5}x + {c:.5}", color=colours[1])
                self.handles.append(best_fit)

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


app = qtw.QApplication([])
window = GraphWindow()
window.show()
app.exec()
