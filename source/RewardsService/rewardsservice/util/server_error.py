class ServerError:
    def __init__(self, type, context):
        self.error = True
        self.type = type
        self.context = context


class ValidationError(ServerError):
    def __init__(self, context):
        super().__init__('ValidationError', context)


class UnknownError(ServerError):
    def __init__(self):
        super().__init__('UnkownError', 'An error have occur during your request')