from functools import wraps

def filter_tuples(func) -> tuple:
    @wraps(func)
    def wrapper(*args, **kwargs):
        return tuple(map(lambda x: x[-1], func(*args, **kwargs)))

    return wrapper


if __name__ == '__main__':
    @filter_tuples
    def dc():
        return [(1, 2), (10, 3)]


    print(dc())
