from __future__ import annotations
from io import BytesIO


class RiffChunk:
    signature: bytes
    size: int
    type: bytes
    chunks: list[RiffChunk]
    data: bytes

    @staticmethod
    def load(io: BytesIO) -> RiffChunk | None:
        result = RiffChunk()
        result.signature = io.read(4)
        if not result.signature:
            return None

        result.size = int.from_bytes(io.read(4), "little")
        if result.signature in [b"RIFF", b"LIST"]:
            result.type = io.read(4)
            result.data = io.read(result.size)
            result.chunks = list(
                RiffChunk.__split_chunks(BytesIO(result.data)))
        else:
            result.data = io.read(result.size)
        return result

    @staticmethod
    def __split_chunks(io: BytesIO):
        while True:
            chunk = RiffChunk.load(io)
            if chunk is None:
                break
            yield chunk
