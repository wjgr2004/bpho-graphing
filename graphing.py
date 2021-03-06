import statistics
import csv
from PyQt6 import QtWidgets as qtw
from functools import partial
import transforming_functions as transform_func
import model_functions as model_func
import plotting_functions as plot_func
import graphing_colours as colours
from graphing_functions import convert_to_number
from graphing_interface import NormalGraph, PolarGraph


class GraphOptionsWindow(qtw.QMainWindow):

    def __init__(self):
        super().__init__()

        self.to_run = None

        # Window Widgets
        self.layout = qtw.QVBoxLayout()

        self.cartesian_button = qtw.QPushButton("Normal Graphing")
        self.cartesian_button.clicked.connect(self.run_cartesian)
        self.layout.addWidget(self.cartesian_button)

        self.polar_button = qtw.QPushButton("Polar Graphing")
        self.polar_button.clicked.connect(self.run_polar)
        self.layout.addWidget(self.polar_button)

        self.central_widget = qtw.QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def run_cartesian(self):
        self.to_run = "Cartesian"
        self.close()

    def run_polar(self):
        self.to_run = "Polar"
        self.close()


class GraphWindow(qtw.QMainWindow):
    """
    The main window to edit the graph
    """

    def __init__(self, polar=False):
        super().__init__()

        self.polar = polar

        self.filename = None

        self.min = None
        self.max = None

        self.in_window = False

        self.handles = []
        self.lines = []

        # Set up graph
        if polar:
            self.graph = PolarGraph()
        else:
            self.graph = NormalGraph()

        self.cycle = 0
        self.colours = colours.colours

        # Window Settings
        self.setFixedSize(230, 460)
        self.setWindowTitle("Graph Generator")

        # Window Widgets
        self.layout = qtw.QVBoxLayout()

        self.ingest_button = qtw.QPushButton("Open")
        self.ingest_button.clicked.connect(self.ingest)
        self.layout.addWidget(self.ingest_button)

        self.form_layout = qtw.QFormLayout()
        self.layout.addLayout(self.form_layout)

        if polar:
            name_1 = "Magnitude func"
            name_2 = "Magnitude"
            name_3 = "Angle func"
            name_4 = "Angle"
        else:
            name_1 = "y-func"
            name_2 = "y-val"
            name_3 = "x-func"
            name_4 = "x-val"

        self.drop_y_func = qtw.QComboBox()
        self.drop_y_func.addItems(transform_func.function_dict.keys())
        self.form_layout.addRow(name_1, self.drop_y_func)

        self.drop_y_vals = qtw.QComboBox()
        self.form_layout.addRow(name_2, self.drop_y_vals)

        self.drop_x_func = qtw.QComboBox()
        self.drop_x_func.addItems(transform_func.function_dict.keys())
        self.form_layout.addRow(name_3, self.drop_x_func)

        self.drop_x_vals = qtw.QComboBox()
        self.form_layout.addRow(name_4, self.drop_x_vals)

        self.line_label = qtw.QLineEdit()
        self.form_layout.addRow("Label", self.line_label)

        self.drop_line_type = qtw.QComboBox()
        self.drop_line_type.addItems(plot_func.plotting_dict.keys())
        self.form_layout.addRow("Plot type: ", self.drop_line_type)

        self.line_button = qtw.QCheckBox("Line of Best Fit")
        self.layout.addWidget(self.line_button)

        self.rank_button = qtw.QCheckBox("Include Pearson's r")
        self.layout.addWidget(self.rank_button)

        self.scale_button = qtw.QCheckBox("Scale y-axis")
        self.layout.addWidget(self.scale_button)

        self.options_layout = qtw.QGridLayout()
        self.layout.addLayout(self.options_layout)

        self.add_button = qtw.QPushButton("Add Plot")
        self.add_button.clicked.connect(self.add_plot)
        self.options_layout.addWidget(self.add_button, 0, 0)

        self.clear_button = qtw.QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_graph)
        self.options_layout.addWidget(self.clear_button, 0, 1)

        self.edit_button = qtw.QPushButton("Edit Lines")
        self.edit_button.clicked.connect(self.edit_lines)
        self.options_layout.addWidget(self.edit_button, 1, 0)

        if polar:
            self.edit_title_button = qtw.QPushButton("Edit Title")
            self.edit_title_button.clicked.connect(self.edit_title_polar)
        else:
            self.edit_title_button = qtw.QPushButton("Edit Titles")
            self.edit_title_button.clicked.connect(self.edit_titles)
        self.options_layout.addWidget(self.edit_title_button, 1, 1)

        self.model_layout = qtw.QHBoxLayout()
        self.layout.addLayout(self.model_layout)

        self.model_drop_down = qtw.QComboBox()
        self.model_drop_down.addItems(model_func.models_dict.keys())
        self.model_layout.addWidget(self.model_drop_down)

        self.model_button = qtw.QPushButton("Add Model")
        self.model_button.clicked.connect(self.add_model)
        self.model_layout.addWidget(self.model_button)

        self.range_button = qtw.QPushButton("Edit Range")
        self.range_button.clicked.connect(self.edit_range)
        self.layout.addWidget(self.range_button)

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

                    new_colours = self.colours[self.cycle]
                    self.cycle = (self.cycle + 1) % len(self.colours)

                    # add new line to lines
                    self.lines.insert(0, [
                        x, y, self.line_button.isChecked(), self.rank_button.isChecked(),
                        new_colours, name, self.drop_line_type.currentText(), "data"])

                    # update range for models
                    if self.max is not None:
                        self.max = max(*x_list, self.max)
                        self.min = min(*x_list, self.min)
                    else:
                        self.max = max(*x_list)
                        self.min = min(*x_list)

                    # redraw graph
                    self.graph.clear()
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
        self.graph.clear()
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

        draw_func, label_func, valid_input, args = model_func.models_dict[self.model_drop_down.currentText()]
        colours = self.colours[self.cycle]
        self.cycle = (self.cycle + 1) % len(self.colours)

        self.plot_window = ModelWindow(self, draw_func, label_func, valid_input, colours, *args)
        self.in_window = True
        self.plot_window.show()

    def generate_graph(self):
        """
        Draws the new plots on the graph and recalculates the models with the updated ranges.
        """

        self.handles = []

        for line in reversed(self.lines):
            if line[-1] == "data":  # if line is from data
                # plots data with function in plotting_functions
                self.graph.general_plot(*line[:-1])

            elif self.max is not None:
                label, draw_func, options, colours, _ = line
                x, y = draw_func(*options, self.min, self.max)

                self.graph.line_plot([list(x)], [list(y)], False, False, label, colour=colours)

    def edit_lines(self):
        """
        Edit the order of the plots and delete plots.
        Opens a window to allow the used to manage the plots.
        """

        # Prevent multiple popups appearing
        if self.in_window:
            return
        self.edit_window = LineEditWindow(self.lines, self)
        self.in_window = True
        self.edit_window.show()

    def edit_titles(self):
        # Prevent multiple popups appearing
        if self.in_window:
            return
        self.title_window = TitleWindow(self)
        self.in_window = True
        self.title_window.show()

    def edit_title_polar(self):
        # Prevent multiple popups appearing
        if self.in_window:
            return
        text, ok = qtw.QInputDialog.getText(self, "Change Title", "New Title:")
        if ok:
            self.graph.set_title(text)

    def edit_range(self):
        # Prevent multiple popups appearing
        if self.in_window:
            return
        self.range_window = RangeWindow(self)
        self.in_window = True
        self.range_window.show()


class ModelWindow(qtw.QWidget):
    """
    Gets the information to plot a model.
    """

    def __init__(self, parent, draw_func, label_func, valid_input, model_colours, *options):
        super().__init__()

        self.parent = parent
        self.valid_input = valid_input

        self.setFixedWidth(230)

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

        self.colours = model_colours

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
            val = convert_to_number(input_box.text())
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

            # redraw graph
            self.parent.generate_graph()
            self.cancel()
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

        self.setFixedSize(430, 300)

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

        self.options_layout = qtw.QGridLayout()
        self.layout.addLayout(self.options_layout)

        self.move_up_button = qtw.QPushButton("Move Up")
        self.move_up_button.clicked.connect(partial(self.move_line, True))
        self.options_layout.addWidget(self.move_up_button, 0, 0)

        self.move_down_button = qtw.QPushButton("Move Down")
        self.move_down_button.clicked.connect(partial(self.move_line, False))
        self.options_layout.addWidget(self.move_down_button, 0, 1)

        self.delete_button = qtw.QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_line)
        self.options_layout.addWidget(self.delete_button, 0, 2)

        self.edit_colour_button = qtw.QPushButton("Edit Main Colour")
        self.edit_colour_button.clicked.connect(partial(self.edit_colour, True))
        self.options_layout.addWidget(self.edit_colour_button, 1, 0)

        self.edit_secondary_colour_button = qtw.QPushButton("Edit Second Colour")
        self.edit_secondary_colour_button.clicked.connect(partial(self.edit_colour, False))
        self.options_layout.addWidget(self.edit_secondary_colour_button, 1, 1)

        self.edit_label_button = qtw.QPushButton("Edit Label")
        self.edit_label_button.clicked.connect(self.edit_label)
        self.options_layout.addWidget(self.edit_label_button, 1, 2)

        self.close_button = qtw.QPushButton("Close")
        self.close_button.clicked.connect(self.custom_close)
        self.options_layout.addWidget(self.close_button, 2, 0, 1, 3)

    def edit_colour(self, main_colour):
        """
        Edits the line colour
        :param main_colour: Whether to edit the main colour or secondary colour.
        """

        currently_selected = self.list_widget.currentItem()
        current_row = self.list_widget.currentRow()

        if currently_selected is None or not currently_selected.isSelected():  # checks an item is selected
            return

        # Opens a colour picker
        self.colour = qtw.QColorDialog.getColor()
        if self.colour.isValid():
            r, g, b, _ = self.colour.getRgb()
            # Converts the colour to hex code
            colour = f"#{r:02x}{g:02x}{b:02x}"
            line = self.lines[current_row]
            if line[-1] == "data":
                index = 4
            else:
                index = 3

            if main_colour:
                line[index] = [colour, line[index][1]]
            else:
                line[index] = [line[index][0], colour]

            self.redraw_graph()

    def edit_label(self):

        currently_selected = self.list_widget.currentItem()
        current_row = self.list_widget.currentRow()

        if currently_selected is None or not currently_selected.isSelected():  # checks an item is selected
            return

        text, ok = qtw.QInputDialog.getText(self, "Change Label", "New Label:")

        if ok:
            line = self.lines[current_row]
            if line[-1] == "data":
                line[5] = text
            else:
                line[0] = text

        self.redraw_graph()

        self.list_widget.takeItem(current_row)
        self.list_widget.insertItem(current_row, text)

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
        self.parent.graph.clear()
        self.parent.generate_graph()

    def custom_close(self):
        self.parent.in_window = False
        self.close()

    def closeEvent(self, _):
        self.custom_close()


class TitleWindow(qtw.QWidget):
    """
    Window for editing the title of the graph.
    """

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setFixedSize(250, 170)

        # Window Widgets
        self.layout = qtw.QVBoxLayout()
        self.setLayout(self.layout)

        self.form_layout = qtw.QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.title = qtw.QLineEdit()
        self.form_layout.addRow("Title", self.title)

        self.y_label = qtw.QLineEdit()
        self.form_layout.addRow("y-label", self.y_label)

        self.x_label = qtw.QLineEdit()
        self.form_layout.addRow("x-label", self.x_label)

        self.options_layout = qtw.QHBoxLayout()
        self.layout.addLayout(self.options_layout)

        self.cancel_button = qtw.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.custom_close)
        self.options_layout.addWidget(self.cancel_button)

        self.update_button = qtw.QPushButton("Update Titles")
        self.update_button.clicked.connect(self.update_titles)
        self.options_layout.addWidget(self.update_button)

    def custom_close(self):
        self.parent.in_window = False
        self.close()

    def closeEvent(self, _):
        self.close()

    def update_titles(self):
        self.parent.graph.set_titles(self.title.text(), self.x_label.text(), self.y_label.text())


class RangeWindow(qtw.QWidget):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setFixedSize(250, 130)

        # Window Widgets
        self.layout = qtw.QVBoxLayout()

        self.form_layout = qtw.QFormLayout()
        self.layout.addLayout(self.form_layout)

        self.minimum_text = qtw.QLineEdit()
        self.form_layout.addRow("Minimum: ", self.minimum_text)

        self.maximum_text = qtw.QLineEdit()
        self.form_layout.addRow("Maximum: ", self.maximum_text)

        self.options_layout = qtw.QHBoxLayout()
        self.layout.addLayout(self.options_layout)

        self.cancel_button = qtw.QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.custom_close)
        self.options_layout.addWidget(self.cancel_button)

        self.submit_button = qtw.QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit)
        self.options_layout.addWidget(self.submit_button)

        self.setLayout(self.layout)

    def custom_close(self):
        self.parent.in_window = False
        self.close()

    def closeEvent(self, _):
        self.custom_close()

    def submit(self):
        val1, val2 = convert_to_number(self.minimum_text.text()), convert_to_number(self.maximum_text.text())
        if val1 is not False and val2 is not False:
            self.parent.min = val1
            self.parent.max = val2

            self.parent.graph.clear()
            self.parent.generate_graph()
            self.custom_close()
        else:
            qtw.QMessageBox.warning(
                self, "Input Failure", "You didn't input valid numbers.",
                qtw.QMessageBox.StandardButton.Ok)


def run_cartesian():
    app = qtw.QApplication([])
    window = GraphWindow()
    window.show()
    app.exec()


def run_polar():
    app = qtw.QApplication([])
    window = GraphWindow(polar=True)
    window.show()
    app.exec()


def main():
    app = qtw.QApplication([])
    window = GraphOptionsWindow()
    window.show()
    app.exec()
    match window.to_run:
        case "Cartesian":
            run_cartesian()
        case "Polar":
            run_polar()


if __name__ == "__main__":
    main()
