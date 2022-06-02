
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

    def adjust(self, min_value, max_value, should_round=False):
        self.graph.ymax = max_value + 1
        self.graph.ymin = min_value - 1
        if self.graph.ymin <= 0:
            self.graph.ymin = 0
        self.graph.y_ticks_major = float(f"{(self.graph.ymax - self.graph.ymin - .01) / 4:.2f}")
        if should_round:
            self.graph.y_ticks_major = floor(self.graph.y_ticks_major)

