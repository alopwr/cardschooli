from .context import obverse


class TestObverse(object):
    def test_process_coords(self):
        xy = [0, 0]
        assert obverse.process_coords(xy, 0, 0) == [0, 0]
