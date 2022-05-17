
from kivy.uix.relativelayout import RelativeLayout
from graph import Graph as GardenGraph
from math import floor


class BaseGraph(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.graph = GardenGraph(
            x_ticks_minor=0, x_ticks_major=1,
            y_ticks_minor=0, y_ticks_major=5,
            y_grid_label=True, x_grid_label=False,
            x_grid=False, y_grid=True,
            xmin=0, xmax=10, ymin=0, ymax=10,
            padding=5
        )

    def adjust(self, max_value):
        self.graph.ymax = max(max_value + 1, 10)
        self.graph.y_ticks_major = floor(self.graph.ymax / 4)

