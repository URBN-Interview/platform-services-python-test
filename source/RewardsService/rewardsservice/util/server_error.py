class ServerError():
    def __init__ (self, type, context):
        self.type = type
        self.context = context
    
class ValidationError(ServerError):
    def __init__(self, context):
        super().__init__('ValidationError', context)