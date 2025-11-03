data = [4, -30, 100, -100, 123, 1, 0, -1, -4]

def abs_sort_key(x):
    return abs(x)

if __name__ == '__main__':
    print(sorted(data, key = abs_sort_key, reverse=True))
    print(sorted(data, key = lambda x: abs(x), reverse=True))
