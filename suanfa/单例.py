class danli(object):
    __instance = None
    __is_first = True

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance=object.__new__(cls)
            print('hehe')
        return cls.__instance

    def __init__(self,age,name):
        if self.__is_first:
            self.age=age
            self.name=name
            danli.__is_first=False

a=danli(18,'习大大')
b=danli(28,'XIDADA')
