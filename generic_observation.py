""" Super class of all collected data"""


class GenericObservation:

    def __init__(self):
        pass

    def convert_to_tuple(self, delete=[]):
        """
        gets values from object
        :param delete: list of attributes that are not needed not needed (ex: for sql select)
        :return: tuple of values for attributes
        """
        d_dict = self.__dict__.copy()
        for e in delete + ['parser']:
            d_dict.pop(e, None)
        return tuple(d_dict.values())