from approved_npo_data.huga import Huga


class TestHuga:
    def test_huga(self):
        assert Huga().piyo() == "piyo"
