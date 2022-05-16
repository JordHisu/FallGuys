
from kivy.properties import NumericProperty, ListProperty
from graph import BarPlot
from props.graphs.base_graph import BaseGraph
from kivy.metrics import dp


class StepGraph(BaseGraph):
    number_of_bars = NumericProperty(7)
    plot_y = ListProperty([0] * number_of_bars.defaultvalue)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.plot = BarPlot(color=[1, 0, 0, 1], bar_width=dp(5))
        self.plot.points = [(i + 1, self.plot_y[i]) for i in range(self.number_of_bars)]
        self.graph.add_plot(self.plot)
        self.graph.xmax = self.number_of_bars + 1
        self.add_widget(self.graph)

    def add_value(self, value):
        # Shifts everything to the left and adds the new value at the end
        self.plot.points = [(x - 1, y) for x, y in self.plot.points[1:]] + [(self.number_of_bars, value)]
        max_value = max([y for x, y in self.plot.points])
        self.adjust(max_value)
