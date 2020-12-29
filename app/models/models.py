class Fire:
    def __init__(self, symbol: str, fourplay: 'FourPlay' = None):
        self.fourplay = fourplay
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def play(self) -> 'FourPlay.Disc':
        raise NotImplementedError()
