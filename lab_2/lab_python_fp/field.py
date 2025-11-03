goods = [
   {'title': 'Ковер', 'price': 2000, 'color': 'green'},
   {'title': 'Диван для отдыха', 'price': 5300, 'color': 'black'}
]

def field(items, *args):
    assert len(args) > 0
    if len(args) == 1:
        return [dct.get(args[0]) for dct in items if dct.get(args[0]) is not None]
    else:
        return [{key : dct.get(key) for key in args if dct.get(key) is not None} for dct in items]

if __name__ == "__main__":
    print(field(goods, 'title'))
    print(field(goods, 'title', 'price'))
