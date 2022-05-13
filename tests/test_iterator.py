class MyIterable:
    """
    An iterator that returns an updated state of itself.
    
    In this case, it is a counter. In the `Planefinder` application,
    the `ListingPage` class does this. It updates its URL and page
    data.
    """

    def __init__(self):
        self.x = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.x > 10:
            raise StopIteration
        self.x += 1
        return self


def test_my_iterable():
    my_iter = MyIterable()
    expected_x = 0
    for state in my_iter:
        assert expected_x == state.x - 1
        expected_x += 1
