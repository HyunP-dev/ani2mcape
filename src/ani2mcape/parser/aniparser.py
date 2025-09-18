from ani2mcape.parser import RiffChunk
from io import BytesIO


def get_hotspot(raw: bytes) -> tuple[int, int]:
    riff = RiffChunk.load(BytesIO(raw))

    for chunk in riff.chunks:
        if chunk.signature == b"LIST":
            for element in chunk.chunks:
                return int.from_bytes(element.data[10:12], "little"), int.from_bytes(element.data[12:14], "little")
