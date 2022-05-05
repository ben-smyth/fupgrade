import sys


def str_to_class(classname):
    """
    Given a class str-name, return it as an actual class, not a string.
    :param: classname
    :return: actual class
    """
    return getattr(sys.modules[__name__],classname)