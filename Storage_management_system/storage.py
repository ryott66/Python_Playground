

class Storage:
    def __init__(self, myu_store: float, myu_update: float):
        self.files = {}
        self.used = 0
        self.used_max = 0
        self.update_size = 0
        self.myu_store = myu_store
        self.myu_update = myu_update

    def get_status(self):
        return {
            "used": self.used,
            "used_max": self.used_max,
            "update_size": self.update_size,
            "myu_store": self.myu_store,
            "myu_update": self.myu_update
        }

    def update_status(self, status):
        self.used = status["used"]
        self.used_max = status["used_max"]
        self.update_size = status["update_size"]




