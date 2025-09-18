from ani2mcape.parser import RiffChunk


def get_hotspot(path: str) -> tuple[int]:
    with open(path, "rb") as f:
        riff = RiffChunk.load(f)

        for chunk in riff.chunks:
            if chunk.signature == b"LIST":
                for element in chunk.chunks:
                    return int.from_bytes(element.data[10:12], "little"), int.from_bytes(element.data[12:14], "little")
