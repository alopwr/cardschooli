from obverse import process_coords


class TestObverse(object):
    def test_process_coords(self):
        xy = [0, 0]
        assert process_coords(xy, 0, 0) == 0
