import numpy as np
from matplotlib import pyplot as plt
from math import e, log


def entropy(labels, base=None):
    """ Computes entropy of label distribution. """

    n_labels = len(labels)

    if n_labels <= 1:
        return 0

    value, counts = np.unique(labels, return_counts=True)
    probs = counts / n_labels
    n_classes = np.count_nonzero(probs)

    if n_classes <= 1:
        return 0

    ent = 0.

    # Compute entropy
    base = e if base is None else base
    for i in probs:
        ent -= i * log(i, base)

    return ent


class SegmentsList:
    def __init__(self, initial_list=None):
        self._list = []
        if initial_list:
            self(*initial_list)

    def get_last(self):
        if len(self._list) == 0:
            return [[]]
        else:
            return self._list[-1]

    def get_longest(self):
        index = np.argmax([quan for val, quan in self._list])
        return self._list[index]

    def __call__(self, *args, **kwargs):
        for value in args:
            # print(value)
            # if isinstance(value, int):
            if self.get_last()[0] == value:
                self._list[-1][1] += 1
            else:
                self._list.append([value, 1])

    def __repr__(self):
        return str(self._list)


class Side:
    def __init__(self, line_dot_list, line_color=None):
        self._line = line_dot_list
        self._border_side = False
        self._segments = SegmentsList()

        self._line_color = line_color
        self._line_np = [[x for x, y in self._line], [y for x, y in self._line]]

        self.create_segmentation()

    def create_segmentation(self):
        for index, value in self._line:
            self._segments(value)

        longest = self._segments.get_longest()
        if longest[1] / len(self._line) >= 0.70:
            self._border_side = True

    @property
    def line_color(self):
        return self._line_color

    @property
    def border_side(self):
        return self._border_side

    def __getitem__(self, index):
        return self._line_np[index]

    def __repr__(self):
        return str(self._line_np)

    def check_border_side(self):
        unique, counts = np.unique(self._line_np[1], return_counts=True)
        if len(counts) == 1:
            self._border_side = True

    def show(self, with_color=False):
        plt.plot(self._line_np[0], self._line_np[1])

        if with_color:
            for x, y, color in zip(
                    self._line_np[0],
                    self._line_np[1],
                    list(map(lambda x: (x.astype(float)) / 255, self._line_color))
            ):
                plt.scatter(x, y, c=color)

        plt.show()

    def does_fit(self, other_line):
        if other_line.border_side:
            return False, []

        max_val = 0

        for i in range(len(self._line_np[0])):
            lines_sum = [i + j for i, j in zip(np.roll(self._line_np[1], i), other_line[1][::-1])]

            unique, counts = np.unique(lines_sum, return_counts=True)

            new_max = np.max(counts)

            if new_max > max_val:
                max_val = new_max
                shift_index = i
                ret_result = lines_sum

        seg_list = SegmentsList(ret_result)

        if seg_list.get_longest()[1] / len(ret_result) >= 0.70:
            return True, ret_result
        else:
            return False, ret_result

