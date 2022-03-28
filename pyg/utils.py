from __future__ import annotations
from collections.abc import Sequence

import numpy as np


#: Represents a coordinate (x and y positions) in a plane.
Coord2D = tuple[float, float]

#: Represents a color (RGBA).
Color = tuple[float, float, float, float]


def normalize_array(
    v: Sequence[float | tuple[float, ...]] | np.ndarray,
) -> np.ndarray:
    if not isinstance(v, np.ndarray):
        return np.array(v, dtype=np.float32)
    elif v.dtype is not np.float32:
        return v.astype(np.float32)
    return v
