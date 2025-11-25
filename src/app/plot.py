import matplotlib.pyplot as plt


class Plot:
    def __init__(self, title="", xlabel="", ylabel=""):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.fig, self.ax = plt.subplots()

    def set_labels(self):
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)

    def show(self):
        plt.show()

    def save(self, filename):
        self.fig.savefig(filename)


class PoincarePlot(Plot):
    def __init__(
        self, det, tr, title="Diagramme de Poincaré", xlabel="Tr A", ylabel="Det A"
    ):
        super().__init__(title, xlabel, ylabel)
        self.det = det
        self.tr = tr

    def plot(self):
        self.ax.plot(self.tr, self.det)
        self.set_labels()
        # Continue personalizing the plot as needed
