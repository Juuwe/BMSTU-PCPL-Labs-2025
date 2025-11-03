from typing import List, Any

class Unique(object):
    def __init__(self, items, **kwargs):
        self._items = iter(items)
        self._ignore_case = kwargs.get('ignore_case', False)
        self._seen = set()

    def __next__(self):
        while True:
            try:
                cur_item = next(self._items)
            except StopIteration:
                raise StopIteration

            key = cur_item

            if self._ignore_case and isinstance(cur_item, str):
                key = cur_item.lower()

            if key not in self._seen:
                self._seen.add(key)
                return cur_item

    def __iter__(self):
        return self

def test():
    data = [1, 4, 3, 2, 2, 1, 10]
    print([item for item in Unique(data)])

if __name__ == "__main__":
    test()

