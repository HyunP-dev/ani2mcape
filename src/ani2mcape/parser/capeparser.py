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


CURSOR_KEY = dict([("Resize N-S", "com.apple.cursor.23"),
                   ("Camera 2", "com.apple.cursor.9"),
                   ("IBeam H.", "com.apple.cursor.26"),
                   ("Window NE", "com.apple.cursor.29"),
                   ("Busy", "com.apple.cursor.4"),
                   ("Ctx Arrow", "com.apple.coregraphics.ArrowCtx"),
                   ("Open", "com.apple.cursor.12"),
                   ("Window N-S", "com.apple.cursor.32"),
                   ("Window SE", "com.apple.cursor.35"),
                   ("Counting Down", "com.apple.cursor.15"),
                   ("Window W", "com.apple.cursor.38"),
                   ("Resize E", "com.apple.cursor.18"),
                   ("Cell", "com.apple.cursor.41"),
                   ("Resize N", "com.apple.cursor.21"),
                   ("Copy Drag", "com.apple.cursor.5"),
                   ("Ctx Menu", "com.apple.cursor.24"),
                   ("Window E", "com.apple.cursor.27"),
                   ("Window NE-SW", "com.apple.cursor.30"),
                   ("Camera", "com.apple.cursor.10"),
                   ("Window NW", "com.apple.cursor.33"),
                   ("Pointing", "com.apple.cursor.13"),
                   ("IBeamXOR", "com.apple.coregraphics.IBeamXOR"),
                   ("Copy", "com.apple.coregraphics.Copy"),
                   ("Arrow", "com.apple.coregraphics.Arrow"),
                   ("Counting Up/Down", "com.apple.cursor.16"),
                   ("Window S", "com.apple.cursor.36"),
                   ("Resize Square", "com.apple.cursor.39"),
                   ("Resize W-E", "com.apple.cursor.19"),
                   ("Zoom In", "com.apple.cursor.42"),
                   ("Resize S", "com.apple.cursor.22"),
                   ("IBeam", "com.apple.coregraphics.IBeam"),
                   ("Move", "com.apple.coregraphics.Move"),
                   ("Crosshair", "com.apple.cursor.7"),
                   ("Poof", "com.apple.cursor.25"),
                   ("Wait", "com.apple.coregraphics.Wait"),
                   ("Link", "com.apple.cursor.2"),
                   ("Window E-W", "com.apple.cursor.28"),
                   ("Window N", "com.apple.cursor.31"),
                   ("Closed", "com.apple.cursor.11"),
                   ("Alias", "com.apple.coregraphics.Alias"),
                   ("Empty", "com.apple.coregraphics.Empty"),
                   ("Counting Up", "com.apple.cursor.14"),
                   ("Window NW-SE", "com.apple.cursor.34"),
                   ("Crosshair 2", "com.apple.cursor.8"),
                   ("Window SW", "com.apple.cursor.37"),
                   ("Resize W", "com.apple.cursor.17"),
                   ("Help", "com.apple.cursor.40"),
                   ("Forbidden", "com.apple.cursor.3"),
                   ("Cell XOR", "com.apple.cursor.20"),
                   ("Zoom Out", "com.apple.cursor.43")])
