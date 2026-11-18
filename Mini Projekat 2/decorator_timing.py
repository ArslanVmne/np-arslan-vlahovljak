# Decorator: @timed mjeri koliko dugo traje funkcija, bez mijenjanja njenog koda.
import time
from functools import wraps


def timed(func):
    @wraps(func)  # čuva originalno ime funkcije
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)  # pozovi pravu funkciju
        seconds = time.perf_counter() - start
        print(f"  [Decorator @timed] {func.__name__}() took {seconds:.4f} s")
        return result  # vrati isti rezultat kao original

    return wrapper
