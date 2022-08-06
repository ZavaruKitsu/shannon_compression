from typing import IO, Callable

from src.encoders.shannon import ShannonEncoder, ShannonDecoder


class CaesarCipher(ShannonEncoder):
    def __init__(self, data: str, writer: IO, progress_callback: Callable[[int, int], None], key: int = 0):
        super().__init__(data, writer, progress_callback)
        self.key = key

    def write_symbol(self, symbol):
        symbol += self.key

        super(CaesarCipher, self).write_symbol(symbol)

    def write(self):
        super(CaesarCipher, self).write()


class CaesarDecoder(ShannonDecoder):
    def __init__(self, reader: IO, writer: IO, progress_callback: Callable[[int, int], None], key: int = 0):
        super().__init__(reader, writer, progress_callback)
        self.key = key

    def get_char(self, n: int):
        n -= self.key

        return super(CaesarDecoder, self).get_char(n)

    def read(self):
        super(CaesarDecoder, self).read()
