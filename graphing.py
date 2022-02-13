import statistics
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import csv
from PyQt6 import QtWidgets as qtw
from functools import partial
import transforming_functions as transform_func
import model_functions as model_func
import plotting_functions as plot_func


class GraphWindow(qtw.QMainWindow):
    """
    The main window to edit the graph
    """

    def __init__(self):
        super().__init__()

        self.filename = None

        self.min = None
        self.max = None

        self.in_window = False

        self.handles = []
        self.lines = []

        # Set up graph
        plt.style.use("seaborn-whitegrid")
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

        # Window Settings
        self.setFixedSize(250, 600)
        self.setWindowTitle("Graph Generator")

        # Window Widgets
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

        self.edit_button = qtw.QPushButton("Edit Lines")
        self.edit_button.clicked.connect(self.edit_lines)
        self.layout.addWidget(self.edit_button)

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
        self.plot_drop_down.addItems(model_func.models_dict.keys())
        self.layout.addRow("Model Type: ", self.plot_drop_down)

        self.plot_button = qtw.QPushButton("Add Model")
        self.plot_button.clicked.connect(self.add_model)
        self.layout.addWidget(self.plot_button)

        self.widget = qtw.QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.generate_graph()

    def ingest(self):
        """
        Imports data from a csv file.
        """

        # Prevent multiple popups appearing
        if self.in_window:
            return
        self.filename, _ = qtw.QFileDialog.getOpenFileName(self, "Open File", ".", "Csv Files (*.csv)")
        try:
            with open(self.filename, "r") as file:
                data_dict = csv.DictReader(file)

                # Remove old headings
                self.drop_x_vals.clear()
                self.drop_y_vals.clear()

                # Add new headings
                self.drop_x_vals.addItems(data_dict.fieldnames)
                self.drop_y_vals.addItems(data_dict.fieldnames)
        except (FileNotFoundError, TypeError):
            pass

    def add_plot(self):
        """
        Adds a plot to the graph.
        """

        try:
            if self.filename is None:
                qtw.QMessageBox.warning(
                    self, "No File", "You haven't selected a file or the file you selected has beem moved or deleted.",
                    qtw.QMessageBox.StandardButton.Ok)
            else:
                with open(self.filename, "r") as file:
                    data_dict = csv.DictReader(file)

                    data_found = False

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
                                data_found = True

                            except (ValueError, ZeroDivisionError):  # If data is not numeric
                                # remove added x values
                                x[-1].pop()
                                x_list.pop()

                                # create new section
                                if x[-1]:
                                    x.append([])
                                    y.append([])
                        except (ValueError, ZeroDivisionError):  # If data is not numeric
                            # create new section
                            if x[-1]:
                                x.append([])
                                y.append([])

                if data_found:

                    if self.scale_button.isChecked():
                        # code y data so mean is 0 and 1 is one standard deviation
                        y_bar = statistics.mean(y_list)
                        y_std_dev = statistics.stdev(y_list)
                        for section in y:
                            for i in range(len(section)):
                                if y_std_dev != 0:
                                    section[i] = (section[i] - y_bar) / y_std_dev
                                else:
                                    section[i] = (section[i] - y_bar)

                    if self.line_label.text():
                        # Use custom line label
                        name = self.line_label.text()
                    else:
                        name = f"{y_name} vs {x_name}"

                    colours = self.colours[self.cycle]
                    self.cycle = (self.cycle + 1) % len(self.colours)

                    # add new line to lines
                    self.lines.insert(0, [
                        x, y, self.line_button.isChecked(), self.rank_button.isChecked(),
                        colours, name, plot_func.plotting_dict[self.drop_line_type.currentText()], "data"])

                    # update range for models
                    if self.max is not None:
                        self.max = max(*x_list, self.max)
                        self.min = min(*x_list, self.min)
                    else:
                        self.max = max(*x_list)
                        self.min = min(*x_list)

                    # redraw graph
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

    def clear_graph(self):
        """
        Removes all plots from the graph.
        """

        self.cycle = 0
        self.lines = []
        self.ax.clear()
        self.max = None
        self.min = None

    def add_model(self):
        """
        Adds a model from an equation to a graph.
        Gets information by opening a window.
        """

        # Prevent multiple popups appearing
        if self.in_window:
            return

        draw_func, label_func, valid_input, args = model_func.models_dict[self.plot_drop_down.currentText()]
        colours = self.colours[self.cycle]
        self.cycle = (self.cycle + 1) % len(self.colours)

        plot_window = ModelWindow(self, draw_func, label_func, valid_input, colours, *args)
        self.in_window = True
        plot_window.show()

    def generate_graph(self):
        """
        Draws the new plots on the graph and recalculates the models with the updated ranges.
        """

        self.handles = []

        for line in reversed(self.lines):
            if line[-1] == "data":  # if line is from data
                # plots data with function in plotting_functions
                self.handles += line[-2](*line[:-2])

            elif self.max is not None:
                label, draw_func, options, colours, _ = line
                x, y = draw_func(*options, self.min, self.max)

                line, = plt.plot(x, y, color=colours[0], label=label)
                self.handles.append(line)

        # add labels to key
        self.ax.legend(handles=self.handles)

        # Redraws gridlines and ticks
        self.ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
        self.ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
        self.ax.tick_params(which="minor", length=3, width=0.7)
        self.ax.tick_params(which="major", length=5, width=1.3)

        plt.grid(linewidth=0.8, color="darkgrey")
        plt.grid(linewidth=0.4, color="gainsboro", which="minor")

        # Updates titles and axis labels
        self.ax.set_title(self.title.text())
        self.ax.set_xlabel(self.x_label.text())
        self.ax.set_ylabel(self.y_label.text())

    def edit_lines(self):
        """
        Edit the order of the plots and delete plots.
        Opens a window to allow the used to manage the plots.
        """

        # Prevent multiple popups appearing
        if self.in_window:
            return
        edit_window = LineEditWindow(self.lines, self)
        self.in_window = True
        edit_window.show()


class ModelWindow(qtw.QWidget):
    """
    Gets the information to plot a model.
    """

    def __init__(self, parent, draw_func, label_func, valid_input, colours, *options):
        super().__init__()

        self.parent = parent
        self.valid_input = valid_input

        # window widgets
        self.layout = qtw.QVBoxLayout()

        self.form_layout = qtw.QFormLayout()

        self.input_boxes = []
        for option in options:
            self.input_boxes.append(qtw.QLineEdit())
            self.form_layout.addRow(option, self.input_boxes[-1])

        self.layout.addLayout(self.form_layout)

        self.h_box = qtw.QHBoxLayout()

        self.cancel_button = qtw.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel)
        self.h_box.addWidget(self.cancel_button)

        self.submit_button = qtw.QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.h_box.addWidget(self.submit_button)

        self.layout.addLayout(self.h_box)

        self.widget = qtw.QWidget()
        self.setLayout(self.layout)

        self.colours = colours

        self.plot_func, self.label_func = draw_func, label_func

    def cancel(self):
        self.parent.in_window = False
        self.close()

    def closeEvent(self, _):
        self.cancel()

    def submit(self):
        """
        Adds the new model to the graph.
        """

        options = []
        for input_box in self.input_boxes:
            val = model_func.convert_to_number(input_box.text())
            if val is not False:  # check if data is numeric
                options.append(val)
            else:
                qtw.QMessageBox.warning(
                    self, "Input Failure", "You didn't input a number.",
                    qtw.QMessageBox.StandardButton.Ok)
                return

        if self.valid_input(*options):
            # add line
            self.parent.lines.insert(0, [self.label_func(*options), self.plot_func, options, self.colours, "model"])

            #redraw graph
            self.parent.generate_graph()
            self.parent.in_window = False
            self.close()
        else:
            qtw.QMessageBox.warning(
                self, "Input Failure", "You input invalid numbers.",
                qtw.QMessageBox.StandardButton.Ok)


class LineEditWindow(qtw.QWidget):
    """
    Allows the user to reorder and delete plots.
    """

    def __init__(self, lines, parent):
        super().__init__()

        self.setFixedWidth(400)

        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        self.lines = lines
        self.parent = parent

        # window widgets
        self.line_layouts = []

        self.list_widget = qtw.QListWidget()

        for i, line in enumerate(self.lines):
            self.line_layouts.append(qtw.QHBoxLayout())

            if line[-1] == "data":
                name = line[5]
            else:
                name = line[0]

            self.list_widget.addItem(name)

        self.layout.addWidget(self.list_widget)

        self.options_layout = qtw.QHBoxLayout()
        self.layout.addLayout(self.options_layout)

        self.delete_button = qtw.QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_line)
        self.options_layout.addWidget(self.delete_button)

        self.move_up_button = qtw.QPushButton("Move Up")
        self.move_up_button.clicked.connect(partial(self.move_line, True))
        self.options_layout.addWidget(self.move_up_button)

        self.move_down_button = qtw.QPushButton("Move Down")
        self.move_down_button.clicked.connect(partial(self.move_line, False))
        self.options_layout.addWidget(self.move_down_button)

        self.close_button = qtw.QPushButton("Close")
        self.close_button.clicked.connect(self.custom_close)
        self.options_layout.addWidget(self.close_button)

    def move_line(self, up):
        """
        Reorders how the plots appear on the graph.
        :param up: If the line should be moved up or down.
        """

        # select up or down
        current_row = self.list_widget.currentRow()
        if up:
            new_row = current_row - 1
        else:
            new_row = current_row + 1
        if new_row < 0 or new_row >= len(self.lines):
            return

        # swap items in self.lines
        self.lines[current_row], self.lines[new_row] = self.lines[new_row], self.lines[current_row]

        # deletes item then reinserts it in new location
        item = self.list_widget.item(current_row)
        self.list_widget.takeItem(current_row)
        self.list_widget.insertItem(new_row, item)
        self.list_widget.setCurrentRow(new_row)

        self.redraw_graph()

    def delete_line(self):
        """
        Remove a plot from the graph.
        """

        currently_selected = self.list_widget.currentItem()
        current_row = self.list_widget.currentRow()

        if currently_selected is None or not currently_selected.isSelected():  # checks an item is selected
            return

        self.lines.pop(current_row)
        self.list_widget.takeItem(current_row)

        self.redraw_graph()

    def redraw_graph(self):
        self.parent.ax.clear()
        self.parent.generate_graph()

    def custom_close(self):
        self.parent.in_window = False
        self.close()

    def closeEvent(self, _):
        self.custom_close()


if __name__ == "__main__":
    # shows the graphing options and graph
    app = qtw.QApplication([])
    window = GraphWindow()
    window.show()
    app.exec()
