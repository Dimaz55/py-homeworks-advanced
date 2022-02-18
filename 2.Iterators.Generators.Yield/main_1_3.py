nested_list = [
    ['a', 'b', 'c'],
    ['d', 'e', 'f', 'g', False],
    [1, 2, [3, 4, ['h', 'i', 'j'], [[[[[6]]]]]], None],
]


class FlatIterator:
    def __init__(self, nest_list, depth=0):
        self.nest_list = nest_list
        self.flat_list = []
        self.pointer = -1
        self.depth = depth
        self.depth_level = self.depth
        self.list_flattener(self.nest_list)

    def list_flattener(self, nested):
        for el in nested:
            if isinstance(el, list) and self.depth_level > 0:
                self.depth_level -= 1
                self.list_flattener(el)
                self.depth_level = self.depth
            else:
                self.flat_list.append(el)

    def __iter__(self):
        return self

    def __next__(self):
        self.pointer += 1
        if self.pointer < len(self.flat_list):
            return self.flat_list[self.pointer]
        else:
            raise StopIteration


if __name__ == '__main__':
    # DEPTH - глубина раскрытия списков
    # 0 соответствует самому верхнему уровню списка
    # Для первого задания DEPTH = 1
    DEPTH = 1
    for item in FlatIterator(nested_list, DEPTH):
        print(item)

    flat_list = [item for item in FlatIterator(nested_list, DEPTH)]
    print('\n', flat_list)

    print(FlatIterator(nested_list, DEPTH).__sizeof__())
    print(list(FlatIterator(nested_list, DEPTH)).__sizeof__())