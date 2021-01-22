import importlib

class Builder:
    def __init__(self):
        pass

    def construct(self, protocol):
        targetClass = None
        try:
            module = importlib.import_module('.protocols', "classes")
            targetClass = getattr(module, protocol)
        except Exception as e:
            print(str(e))

        #print("Protocol: {0}".format(protocol))
        return targetClass