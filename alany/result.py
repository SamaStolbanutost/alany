class Result(object):
    def __init__(self, status=1, value=None):
        self.status = status
        self.value = value
        
    def is_success(self) -> bool:
        if self.status in [1, 2]:
            return True
        else:
            return False