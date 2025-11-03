import time
from contextlib import contextmanager

class cm_timer_1:
    def __enter__(self):
        self.start = time.perf_counter()
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.perf_counter()
        if exc_type is not None:
            print("Ошибка в блоке кода")
            return False

        print(f"time: {end - self.start}")

@contextmanager
def cm_timer_2():
    start = time.perf_counter()

    try:
        yield start
    except Exception as e:
        print("Ошибка в блоке кода")
        raise

    print(f"time: {time.perf_counter() - start}")


def test():
    print("cm_timer_1")
    with cm_timer_1():
        time.sleep(5.5)

    print("\ncm_timer_2")
    with cm_timer_2():
        time.sleep(5.5)

if __name__ == "__main__":
    test()
