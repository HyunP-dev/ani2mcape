from __future__ import annotations
from dataclasses import dataclass
import plistlib
import dacite


@dataclass
class Cursor:
    FrameCount: int
    FrameDuration: float
    HotSpotX: float
    HotSpotY: float
    PointsHigh: float
    PointsWide: float
    Representations: list[bytes]


@dataclass
class CapePlist:
    Author: str
    CapeName: str
    CapeVersion: float
    Cloud: bool
    Cursors: dict[str, Cursor]
    HiDPI: bool
    Identifier: str
    MinimumVersion: float
    Version: float

    @staticmethod
    def load(path: str) -> CapePlist:
        with open(path, "rb") as f:
            return dacite.from_dict(CapePlist, plistlib.load(f))
