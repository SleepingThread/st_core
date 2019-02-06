import time
import os


class TempDirectory(object):
    def __init__(self, root_dir, prefix = "",
        name_type = "datetime"):
        """
            name_type = datetime | int
        """

        self.root_dir = os.path.abspath(root_dir)
        self.prefix = prefix
        self.name_type = name_type

        return

    def get(self):
        _basename = self.root_dir+os.sep+self.prefix
        if self.name_type == "datetime":
            while True:
                _name = _basename+time.strftime("%Y%m%d%H%M%S")
                if os.path.exists(_name):
                    time.sleep(1)
                else:
                    break
        elif self.name_type == "int":
            _counter = 0
            while True:
                _name = _basename+str(_counter)
                if os.path.exists(_name):
                    _counter += 1
                else:
                    break
        else:
            raise Exception("Unknown name_type: '"+self.name_type+"'")

        return _name

    def create(self):
        _name = self.get()
        os.makedirs(_name)

        return _name


