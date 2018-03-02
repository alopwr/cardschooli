from .context import obverse
from random import randint


class TestObverse(object):
    def test_process_coords(self):
        xy = [0, 0]
        assert obverse.process_coords(xy, 0, 0) == [0, 0]
        xy = [-1, 100]
        assert obverse.process_coords(xy, [1000, 1000], [54, 75]) == [473, 100]
        xy = [-1, -1]
        assert obverse.process_coords(xy, [100, 100], [10, 5]) == [45, 47]
        xy = [randint(0, 1500), randint(0, 2100)]
        size = [randint(1500, 3000), randint(2100, 3000)]
        psize = [randint(0, 500), randint(0, 500)]
        assert obverse.process_coords(xy, size, psize) == xy
