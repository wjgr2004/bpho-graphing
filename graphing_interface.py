import random
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import matplotlib.cm as cm
import numpy as np
import graphing_colours as colours
import plotting_functions as plot_func


class NormalGraph:
    def __init__(self):
        plt.style.use("seaborn-whitegrid")
        self.fig, self.ax = plt.subplots(figsize=(14, 10), layout="constrained")
        self.cycle = 0
        self.colours = colours.colours

        self.title = ""
        self.x_label = ""
        self.y_label = ""

        self.redraw_graph()
        self.handles = []
        plt.draw()
        plt.pause(0.01)

    def redraw_graph(self):
        self.ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
        self.ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
        self.ax.tick_params(which="minor", length=3, width=0.7)
        self.ax.tick_params(which="major", length=5, width=1.3)
        plt.grid(linewidth=0.8, color="darkgrey")
        plt.grid(linewidth=0.4, color="gainsboro", which="minor")

        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)

        plt.pause(0.01)

    def set_titles(self, title, x_label, y_label):
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.redraw_graph()

    def general_plot(self, x, y, lobf, rank, colour, label, plot_name):
        match plot_name:
            case "Scatter":
                self.scatter_plot(x, y, lobf, rank, label, colour=colour)
            case "Line":
                self.line_plot(x, y, lobf, rank, label, colour=colour)
            case "Smoothed Line":
                self.smooth_plot(x, y, lobf, rank, label, colour=colour)

    def scatter_plot(self, x, y, lobf, rank, label, colour=None):
        if colour is None:
            self.handles += plot_func.scatter_plot(x, y, lobf, rank, self.colours[self.cycle], label, False)
            self.cycle += 1
        else:
            self.handles += plot_func.scatter_plot(x, y, lobf, rank, colour, label, False)
        self.ax.legend(handles=self.handles)
        self.redraw_graph()

    def line_plot(self, x, y, lobf, rank, label, colour=None):
        if colour is None:
            self.handles += plot_func.line_plot(x, y, lobf, rank, self.colours[self.cycle], label, False)
            self.cycle += 1
        else:
            self.handles += plot_func.line_plot(x, y, lobf, rank, colour, label, False)
        self.ax.legend(handles=self.handles)
        self.redraw_graph()

    def smooth_plot(self, x, y, lobf, rank, label, colour=None):
        if colour is None:
            self.handles += plot_func.smoothed_plot(x, y, lobf, rank, self.colours[self.cycle], label, False)
            self.cycle += 1
        else:
            self.handles += plot_func.smoothed_plot(x, y, lobf, rank, colour, label, False)
        self.ax.legend(handles=self.handles)
        self.redraw_graph()

    def clear(self):
        self.ax.clear()
        self.cycle = 0
        self.handles = []
        self.redraw_graph()

    def freeze(self):
        while True:
            self.redraw_graph()


class PolarGraph:
    def __init__(self):
        plt.style.use("seaborn-whitegrid")
        self.fig, self.ax = plt.subplots(figsize=(11, 11), layout="constrained", subplot_kw={"projection": "polar"})
        self.cycle = 0
        self.colours = colours.colours

        self.title = ""

        self.handles = []
        self.redraw_graph()
        plt.draw()
        plt.pause(0.01)

    def set_title(self, title):
        self.title = title
        self.redraw_graph()

    def redraw_graph(self):
        plt.thetagrids(range(0, 360, 15))
        self.ax.set_theta_zero_location("N")
        self.ax.set_theta_direction(-1)
        self.ax.xaxis.set_minor_locator(tck.AutoMinorLocator(3))
        self.ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
        self.ax.tick_params(which="minor", length=3, width=0.7)
        self.ax.tick_params(which="major", length=5, width=1.3)

        self.ax.set_title(self.title)

        plt.grid(linewidth=0.8, color="darkgrey")
        plt.grid(linewidth=0.4, color="gainsboro", which="minor")

        plt.pause(0.01)

    def general_plot(self, x, y, lobf, rank, colour, label, plot_name):
        match plot_name:
            case "Scatter":
                self.scatter_plot(x, y, lobf, rank, label, colour=colour)
            case "Line":
                self.line_plot(x, y, lobf, rank, label, colour=colour)
            case "Smoothed Line":
                self.smooth_plot(x, y, lobf, rank, label, colour=colour)

    def scatter_plot(self, x, y, lobf, rank, label, colour=None):
        if colour is None:
            self.handles += plot_func.scatter_plot(x, y, lobf, rank, self.colours[self.cycle], label, True)
            self.cycle += 1
        else:
            self.handles += plot_func.scatter_plot(x, y, False, False, colour, label, True)
        self.ax.legend(handles=self.handles)
        self.redraw_graph()

    def line_plot(self, x, y, lobf, rank, label, colour=None):
        if colour is None:
            self.handles += plot_func.line_plot(x, y, lobf, rank, self.colours[self.cycle], label, True)
            self.cycle += 1
        else:
            self.handles += plot_func.line_plot(x, y, lobf, rank, colour, label, True)
        self.ax.legend(handles=self.handles)
        self.redraw_graph()

    def smooth_plot(self, x, y, lobf, rank, label, colour=None):
        if colour is None:
            self.handles += plot_func.smoothed_plot(x, y, lobf, rank, self.colours[self.cycle], label, True)
            self.cycle += 1
        else:
            self.handles += plot_func.smoothed_plot(x, y, lobf, rank, colour, label, True)
        self.ax.legend(handles=self.handles)
        self.redraw_graph()

    def clear(self):
        self.ax.clear()
        self.cycle = 0
        self.handles = []
        self.redraw_graph()

    def freeze(self):
        while True:
            self.redraw_graph()


class Animation2DWindow:
    def __init__(self, size, object_count):
        self.circles = []
        self.size = size

        plt.style.use("seaborn-whitegrid")
        self.fig, self.ax = plt.subplots(figsize=(10, 10), layout="constrained")
        plt.gca().set_aspect('equal')
        self.cycle = 0
        self.colours = colours.colours

        self.ax.set(xlim=(-size, size), ylim=(-size, size))
        self.redraw_graph()

        x = [0] * object_count
        y = [0] * object_count
        c = np.linspace(0, 1, object_count)
        s = [1] * object_count
        self.ln = self.ax.scatter(x, y, c=c, s=s, animated=True, cmap=cm.jet)
        plt.show(block=False)
        plt.pause(0.01)
        self.bg = self.fig.canvas.copy_from_bbox(self.fig.bbox)
        self.fig.canvas.blit(self.fig.bbox)

    def redraw_graph(self):
        self.ax.xaxis.set_minor_locator(tck.AutoMinorLocator())
        self.ax.yaxis.set_minor_locator(tck.AutoMinorLocator())
        self.ax.tick_params(which="minor", length=3, width=0.7)
        self.ax.tick_params(which="major", length=5, width=1.3)
        plt.grid(linewidth=0.8, color="darkgrey")
        plt.grid(linewidth=0.4, color="gainsboro", which="minor")

    def draw_circles(self, xy, r):
        self.fig.canvas.restore_region(self.bg)
        r = (r / self.size * 680) ** 2
        self.ln.set_offsets(xy)
        self.ln.set_sizes(r)
        self.ax.draw_artist(self.ln)
        self.fig.canvas.blit(self.fig.bbox)
        self.fig.canvas.flush_events()
        plt.pause(0.01)

    def process_frame(self, xy, r):
        self.draw_circles(xy, r)

    def freeze(self):
        while True:
            plt.pause(0.01)
