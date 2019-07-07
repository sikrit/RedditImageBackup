import os


class Save:
    def __init__(self, base_dir, by_sub):
        self.base_dir = base_dir
        self.by_sub = by_sub

    def get_dir(self, author, sub):
        folder = os.path.join(self.base_dir, sub)
        if not os.path.exists(folder):
            os.makedirs(folder)
        return folder
