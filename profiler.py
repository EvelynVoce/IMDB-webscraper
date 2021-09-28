from cProfile import Profile
from pstats import Stats
from io import StringIO


def profile(fnc):
    
    """A decorator that uses cProfile to profile a function"""
    
    def inner(*args, **kwargs):
        pr = Profile()
        pr.enable()
        return_val = fnc(*args, **kwargs)
        pr.disable()
        s = StringIO()
        ps = Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        print(s.getvalue())
        return return_val

    return inner
