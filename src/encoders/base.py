from typing import IO, Callable


class Encoder:
    def __init__(self, data: str, writer: IO, progress_callback: Callable[[int, int], None]):
        self.data = data
        self.data_length = len(data)
        self.writer = writer

        self.progress_callback = progress_callback

    def write(self):
        raise NotImplementedError()


class Decoder:
    def __init__(self, reader: IO, writer: IO, progress_callback: Callable[[int, int], None]):
        self.reader = reader
        self.writer = writer

        self.progress_callback = progress_callback

    def read(self):
        raise NotImplementedError()
