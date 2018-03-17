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
    def test_reverse_path(self):
        cardreverse = reverse.CardReverse("unittests1")
        assert cardreverse.project_location == "unittests1"

    def test_change_color(self):
        cardreverse = reverse.CardReverse("unittests2")
        cardreverse.change_color("#ef2929")
        path = os.path.join(os.pardir, "cards", "unittests2", "reverse_preview.png")
        with open(path, "rb") as f:
            sha1sum = sha1()
            data = f.read()
            sha1sum.update(data)
            assert sha1sum.hexdigest() == "58fda18bb194ca7ced890ee2d1d2f6208a9ec641"

    def test_paste(self):
        cardreverse = reverse.CardReverse("unittests3")
        cardreverse.paste(os.path.join("tests", "data", "leaf.png"), [43, 282])
        path = os.path.join(os.pardir, "cards", "unittests3", "reverse_preview.png")
        with open(path, "rb") as f:
            sha1sum = sha1()
            data = f.read()
            sha1sum.update(data)
            assert sha1sum.hexdigest() == "7a171e8949c6a384c483b2fe76d99b62a62b6070"

    def test_add_text(self):
        cardreverse = reverse.CardReverse("unittests4")
        cardreverse.add_text([0, 12], "SPQR", 34, "#194769", os.path.join("res", "fonts", "font.ttf"))
        path = os.path.join(os.pardir, "cards", "unittests4", "reverse_preview.png")
        with open(path, "rb") as f:
            sha1sum = sha1()
            data = f.read()
            sha1sum.update(data)
            assert sha1sum.hexdigest() == "5fe384bdcc80ed8522dac1c3d9a1f84eda603819"

    def test_save_reverses(self):
        cardreverse = reverse.CardReverse("unittests4")
        cardreverse.paste(os.path.join("tests", "data", "leaf.png"), [43, 282])
        cardreverse.add_text([0, 12], "SPQR", 34, "#194769", os.path.join("res", "fonts", "font.ttf"))
        cardreverse.change_color("#ef2929")
        cardreverse.save_reverses()
        path = os.path.join(os.pardir, "cards", cardreverse.project_location, "reverse.png")
        old_path = os.path.join(os.pardir, "cards", cardreverse.project_location, "reverse_preview.png")
        print(path)
        assert os.path.isfile(path) is True
        assert os.path.isfile(old_path) is False
        with open(path, "rb") as f:
            sha1sum = sha1()
            data = f.read()
            sha1sum.update(data)
            assert sha1sum.hexdigest() == "a3ccfe4c3c63a8d176133219605dee245da6a89c"
