import importlib

class Builder:
    ''' Imports a class name equivalent to a string value '''
    def __init__(self):
        pass

    def construct(self, protocol):
        targetClass = None
        try:
            module = importlib.import_module('.protocols', "classes")
			# Import the class name contained in variable 'protocol' 
			# which resides in the classes.protocols module
            targetClass = getattr(module, protocol)
        except Exception as e:
            print(str(e))

        return targetClass