class controller:
    def __init__(self):
        # print(f'Constructor {self.getName()}')
        pass

    def __del__(self):
        # print(f'Destructor {self.getName()}')
        pass

    def getName(self):
        return self.__class__.__name__
