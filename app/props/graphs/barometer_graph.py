
from typing import Type
from kivy.properties import NumericProperty
from graph import LinePlot
from props.graphs.base_graph import BaseGraph
from kivy.metrics import dp


class BarometerGraph(BaseGraph):
    number_of_points = NumericProperty(10)
    plots = {
        'base': Type[LinePlot],
        'anklet': Type[LinePlot],
        'necklace': Type[LinePlot],
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plots['base'] = LinePlot(color=[1, 0, 0, .8], line_width=dp(1.2))
        self.plots['anklet'] = LinePlot(color=[0, 1, 0, .8], line_width=dp(1.5))
        self.plots['necklace'] = LinePlot(color=[0, 0, 1, .8], line_width=dp(1.5))
        self.graph.add_plot(self.plots['base'])
        self.graph.add_plot(self.plots['anklet'])
        self.graph.add_plot(self.plots['necklace'])
        self.add_widget(self.graph)
        self.graph.xlabel = "Barometer data per measurement"
        self.y_ticks_minor = .01
        self.y_ticks_major = .1

    def add_value(self, source, value):
        plot = self.plots[source]
        # exclude the leftmost value if needed
        points = plot.points if len(plot.points) <= self.number_of_points else plot.points[1:]
        # Shifts everything to the left and adds the new value at the end
        plot.points = [(x - 1, y) for x, y in points] + [(self.number_of_points, value)]
        min_value = min([y for plot in self.plots.values() for x, y in plot.points])
        max_value = max([y for plot in self.plots.values() for x, y in plot.points])
        self.adjust(min_value, max_value)


