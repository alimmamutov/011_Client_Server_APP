class ContextManager(object):
    def __init__(self, input_str):
        self.string = input_str

    def __enter__(self):
        print('Enter')
        print(self.string)
        return True

    def __exit__(self, type, value, traceback):
        print('exit')

