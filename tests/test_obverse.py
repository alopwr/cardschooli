import sys


class TestObverse(object):
    def test_process_coords(self):
        print("\n\n\n\n\n{}\n\n\n\n\n".format(sys.path))
        from obverse import process_coords
        xy = [0, 0]
        assert process_coords(xy, 0, 0) == [0, 0]
