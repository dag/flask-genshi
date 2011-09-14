from unittest import TestCase
from flaskext.genshi import Pipe


class TestPipe(TestCase):

    def test_no_args(self):
        length = Pipe(len)
        assert [1, 2, 3] | length == 3

    def test_decorator(self):
        @Pipe
        def length(x):
            return len(x)
        assert [1, 2, 3] | length == 3

    def test_with_args(self):
        @Pipe
        def take(x, n):
            return x[:n]
        assert range(10) | take(5) == range(5)
