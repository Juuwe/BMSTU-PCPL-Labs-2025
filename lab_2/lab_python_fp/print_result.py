from typing import List, Any, Dict

def print_in_column(data):
    for el in data:
        print(el)

def print_result(func):
    def wrapper(*args, **kwargs):
        print("function name:", func.__name__)
        result = func(*args, **kwargs)
        if isinstance(result, List):
            print("result:")
            print_in_column(result)
        elif isinstance(result, Dict):
            print("result:")
            print_in_column([f'{key} = {value}' for key, value in result.items()])
        else:
            print(f"result: {result}")
        return result
    return wrapper

@print_result
def test_1():
    return 1

@print_result
def test_2():
    return 'iu5'

@print_result
def test_3():
    return {'a': 1, 'b': 2}

@print_result
def test_4():
    return [1, 2]

if __name__ == '__main__':
    test_1()
    test_2()
    test_3()
    test_4()
