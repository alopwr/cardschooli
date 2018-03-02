import os
from hashlib import sha1
from random import randint

from .context import reverse



def test_process_coords():
    xy = [0, 0]
    assert reverse.process_coords(xy, 0, 0) == [0, 0]
    xy = [-1, 100]
    assert reverse.process_coords(xy, [1000, 1000], [54, 75]) == [473, 100]
    xy = [-1, -1]
    assert reverse.process_coords(xy, [100, 100], [10, 5]) == [45, 47]
    xy = [randint(0, 1500), randint(0, 2100)]
    size = [randint(1500, 3000), randint(2100, 3000)]
    psize = [randint(0, 500), randint(0, 500)]
    assert reverse.process_coords(xy, size, psize) == xy


class TestCardReverse(object):
    def test_change_color(self):
        cardreverse = reverse.CardReverse("unittests")
        cardreverse.change_color("#ef2929")
        path = os.path.join(os.pardir, "cards", "unittests", "reverse_preview.png")
        with open(path, "rb") as f:
            sha1sum = sha1()
            data = f.read()
            sha1sum.update(data)
            assert sha1sum.hexdigest() == "7fabbec978b5cedad4a87c285cf5b93134b9a8fb"
