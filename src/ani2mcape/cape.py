from ani2mcape.parser import CapePlist, Cursor, CURSOR_KEY, get_hotspot
from ani2mcape.cli import to_concated_image, get_zoomed_images
import os
from io import BytesIO
import numpy as np
import tifffile
import plistlib
from dataclasses import asdict
import click


def image2tiff(image) -> bytes:
    data = np.array(image.convert("rgb"))
    result = BytesIO()
    tifffile.imwrite(
        result,
        data,
        dtype='uint8',
        photometric='rgb',
        compression='lzw',
        extratags=[
            (274, 3, 1, 1, False)
        ]
    )
    return result.getvalue()


@click.command()
@click.argument("author")
@click.argument("name")
@click.argument("identifier")
@click.argument("dirpath")
@click.argument("outpath")
def make(author, name, identifier, dirpath, outpath):
    cursors = dict()
    for entry in os.scandir(dirpath):
        if not entry.name.endswith(".ani"):
            continue

        with open(entry, "rb") as f:
            raw = f.read()
            hotspot_x, hotspot_y = get_hotspot(raw)

            concated_image, frame_count = to_concated_image(raw)
            concated_image = concated_image.convert("rgb")
            concated_image.depth = 8
            w, h = concated_image.size
            h /= frame_count

            [s1, s2, s5, s10] = get_zoomed_images(concated_image)
            cursor = Cursor(FrameCount=frame_count,
                            FrameDuration=0.1,
                            HotSpotX=hotspot_x,
                            HotSpotY=hotspot_y,
                            PointsWide=w,
                            PointsHigh=h,
                            Representations=list(map(image2tiff, [s5, s10, s1, s2])))
            print(entry.name)
            match entry.name:
                case "Normal.ani":
                    cursors[CURSOR_KEY["Arrow"]] = cursor
                case "Busy.ani":
                    cursors[CURSOR_KEY["Wait"]] = cursor
                case "Unavailable.ani":
                    cursors[CURSOR_KEY["Forbidden"]] = cursor
                case "Text.ani":
                    cursors[CURSOR_KEY["IBeam"]] = cursor
                case "Link.ani":
                    cursors[CURSOR_KEY["Pointing"]] = cursor
                case "Diagonal1.ani":
                    cursors[CURSOR_KEY["Window NW-SE"]] = cursor
                case "Diagonal2.ani":
                    cursors[CURSOR_KEY["Window NE-SW"]] = cursor
                case "Horizontal.ani":
                    cursors[CURSOR_KEY["Window E-W"]] = cursor
                case "Vertical.ani":
                    cursors[CURSOR_KEY["Window N-S"]] = cursor
                case "Help.ani":
                    cursors[CURSOR_KEY["Help"]] = cursor
                case "Working.ani":
                    cursors[CURSOR_KEY["Busy"]] = cursor

    cape = CapePlist(
        Author=author,
        CapeName=name,
        CapeVersion=1,
        Cloud=False,
        Cursors=cursors,
        HiDPI=True,
        Identifier=identifier,
        MinimumVersion=2,
        Version=2
    )

    if not outpath.endswith(".cape"):
        outpath += ".cape"

    with open(outpath, "wb") as f:
        plistlib.dump(asdict(cape), f)
