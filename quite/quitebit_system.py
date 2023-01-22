from quitebit import QuiteBit


class QuiteBitSystem(object):
    def __init__(self, quitebits: list[QuiteBit] = [], algorithm: list = []):
        self.quitebits = quitebits
        self.algorithm = algorithm
