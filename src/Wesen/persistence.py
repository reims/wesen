from functools import wraps


def persistence(func, static, dynamic):
    """decorator for handling persistence.
    static fields are fields that are set only once in the constructor and
    thus only need to be stored. Dynamic fields are part of the dynamic state
    of the object and are set during restoring in addition to being stored."""
    for entry in static.keys():
        if static[entry] is None:
            static[entry] = lambda self: self.__getattribute__(entry)
    for entry in dynamic.keys():
        if dynamic[entry] is None:
            dynamic[entry] = (lambda self: self.__getattribute__(entry),
                              lambda self, v: self.__setattr__(entry, v))
        else:
            getter, setter = dynamic[entry]
            getter = getter or lambda self: self.__getattribute__(entry)
            setter = setter or lambda self, v: self.__setattr__(entry, v)
            dynamic[entry] = (getter, setter)

    @wraps(func)
    def wrapper(self, obj=None):
        if obj is None:  # setter case
            d = dict()
            for entry, f in static.items():
                d[entry] = f(self)
            for entry, (f, _) in dynamic.items():
                d[entry] = f(self)
            return d
        else:  # getter case
            for entry, (_, f) in dynamic.items():
                f(self, obj[entry])
    return wrapper
