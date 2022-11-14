SUCCESS_CODES = [200, 201]


class Response:

    def __init__(self, status_code, message=None, content=None):
        self.__status_code = status_code
        if not message:
            self.__message = ''
        else:
            self.__message = message
        if not content:
            self.__content = {}
        else:
            self.__content = content

    @property
    def status_code(self):
        return self.__status_code

    @property
    def messsage(self):
        return self.__status_code

    @property
    def content(self):
        return self.__status_code

    def __bool__(self):
        return self.__status_code in SUCCESS_CODES

    def as_json(self):
        return {'status_code': self.__status_code,
                'message': self.__message,
                'content': self.__content}
