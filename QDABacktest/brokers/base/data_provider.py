class OHLCVT:
    open = "Open"
    high = "High"
    low = "Low"
    close = "Close"
    volume = "Volume"
    timestamp = "Date"

class DataProvider:
    def __init__(self):
        pass

    def current(self, *args, **kwargs):
        return self.historical(*args, **kwargs)[-1]

    def historical(self, *args, **kwargs):
        raise NotImplementedError


