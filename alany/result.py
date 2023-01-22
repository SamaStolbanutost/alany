class Result(object):
    def __init__(self, status=1, value=None):
        self.status = status
        self.value = value

    def is_success(self) -> bool:
        return self.status in self.positive

    positive = [1, 2]
