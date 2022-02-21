nested_list = [
    ['a', 'b', 'c'],
    ['d', 'e', 'f', 'g', False],
    [1, 2, [3, 4, ['h', 'i', 'j'], [[[[[6]]]]]], None],
]


class FlatIterator:
    def __init__(self, nest_list):
        self.nest_list = nest_list
        self.outer_pointer = 0
        self.inner_pointer = 0

    def __iter__(self):
        return self

    def __next__(self):
        while self.outer_pointer < len(self.nest_list):
            el = self.nest_list[self.outer_pointer]
            if isinstance(el, list):
                while self.inner_pointer < len(el):
                    inner_el = el[self.inner_pointer]
                    self.inner_pointer += 1
                    return inner_el
                self.inner_pointer = 0
                self.outer_pointer += 1
            else:
                return el
        raise StopIteration


if __name__ == '__main__':
    for item in FlatIterator(nested_list):
        print(f"'{item}'" if isinstance(item, str) else item)

    flat_list = [item for item in FlatIterator(nested_list)]
    print('\n', flat_list)
