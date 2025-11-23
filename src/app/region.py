from abc import ABC, abstractmethod
from typing import Sequence

import numpy as np


class Region(ABC):
    @abstractmethod
    def add_to_figure(self, fig):
        """Draw region on a bokeh figure (patch/line/etc)"""

    @abstractmethod
    def contains(self, x: float, y: float) -> bool:
        """(Optional) point-in-region test"""


class ParabolaRegion(Region):
    def __init__(
        self,
        tr_values: Sequence[float],
        det_values: Sequence[float],
        fill_color="#fff0d9",
        **patch_kwargs,
    ) -> None:
        self.tr_values = tr_values
        self.det_values = det_values
        self.fill_color = fill_color
        self.patch_kwargs = patch_kwargs

    def add_to_figure(self, fig):
        fig.patch(
            np.concatenate([self.tr_values, self.tr_values[::-1]]),
            np.concatenate(
                [
                    self.det_values,
                    np.full_like(
                        self.det_values,
                        fig.y_range.end
                        if self.fill_color == "#fff0d9"
                        else fig.y_range.start,
                    ),
                ]
            ),
            fill_color=self.fill_color,
            **self.patch_kwargs,
        )

    def contains(self, x: float, y: float) -> bool:
        # Point-in-region test for parabola region
        det_curve = x**2 / 4.0
        if self.fill_color == "#fff0d9":
            return y >= det_curve
        else:
            return y <= det_curve
