# coding=utf-8


class TestClass1(object):
    """
    This is a test class 1
    """
    @classmethod
    def test_class_method(cls):
        """

        :return: test
        """
        pass

    def _protected_method(self):
        """
        should not be shown
        :return:
        """
        pass

    def instance_method(self, param1):
        """

        :param param1: any parameter
        :return: None
        """
        return None
