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
        if initial_list is not None:
            self(*initial_list)

    def get_last(self):
        if len(self._list) == 0:
            return [[]]
        else:
            return self._list[-1]

    def get_longest(self):
        index = np.argmax([quan for val, quan, x in self._list])
        return self._list[index]

    def __call__(self, *args, **kwargs):
        for value in args:
            if self.get_last()[0] == value:
                self._list[-1][1] += 1
            else:
                if len(self._list) == 0:
                    self._list.append([value, 1, 0])
                else:
                    self._list.append([value, 1, self._list[-1][2] + self._list[-1][1]])

    def __repr__(self):
        return str(self._list)


class Side:
    def __init__(self, line_dot_list, line_color=None):
        self._line = line_dot_list
        self._border_side = False
        self._cell_link = None
        self._segments = SegmentsList()
        self._y_align, self._x_align = None, None

        self._line_color = line_color
        self._line_np = np.array([[x for x, y in self._line], [y for x, y in self._line]])

        self.create_segmentation()

    def create_segmentation(self):
        for index, value in self._line:
            self._segments(value)

        longest = self._segments.get_longest()
        if longest[1] / len(self._line) >= 0.70:
            self._border_side = True

    @property
    def x_align(self):
        return self._x_align

    @x_align.setter
    def x_align(self, value):
        self._x_align = value

    @property
    def y_align(self):
        return self._y_align

    @y_align.setter
    def y_align(self, value):
        self._y_align = value

    @property
    def line(self):
        return self._line

    @property
    def line_np(self):
        return self._line_np

    @property
    def line_color(self):
        return self._line_color

    @property
    def border_side(self):
        return self._border_side

    @property
    def cell_link(self):
        return self._cell_link

    @cell_link.setter
    def cell_link(self, value):
        self._cell_link = value

    def __getitem__(self, index):
        return self._line_np[index]

    def __repr__(self):
        return f'{self._cell_link}'

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
        if other_line.border_side or self.border_side:
            return False

        shape_diff = abs(self._line_np[1].shape[0] - other_line[1].shape[0])

        if self._line_np[1].shape > other_line[1].shape:
            bigger_line = self.line_np[1]
            smaller_line = np.zeros(bigger_line.shape, dtype=np.int16)
            smaller_line[:other_line[1].shape[0]] = other_line[1][::-1]
        else:
            bigger_line = other_line.line_np[1]
            smaller_line = np.zeros(bigger_line.shape, dtype=np.int16)
            smaller_line[:self.line_np[1].shape[0]] = self.line_np[1][::-1]

        max_val = 0

        for i in range(shape_diff):
            line_sum = bigger_line + np.roll(smaller_line, i)

            unique, counts = np.unique(line_sum, return_counts=True)

            new_max = np.max(counts)

            if new_max > max_val:
                max_val = new_max
                shift = i
                ret_result = line_sum

        seg_list = SegmentsList(ret_result)
        longest = seg_list.get_longest()

        if longest[1] / len(ret_result) >= 0.70:
            print('True')
        else:
            print('False')

        # lines_sum = [i + j for i, j in zip(np.roll(self._line_np[1], 13), other_line[1][::-1])]

        # fig, ax = plt.subplots(2, 1)
        # ax[0].plot(bigger_line[0], bigger_line[1])
        # ax[1].plot(smaller_line[0], smaller_line[1][::-1])
        # ax[1].plot(other_line.line_np[0], other_line.line_np[1][::-1])
        # plt.show()

        # max_val = 0
        #
        # if self._line_np[1].shape > other_line[1].shape:
        #     bigger_line = self._line_np[1]
        #     smaller_line = other_line[1][::-1]
        # else:
        #     bigger_line = other_line[1][::-1]
        #     smaller_line = self._line_np[1]
        #
        # for i in range(len(bigger_line)):
        #     bigger_line = np.roll(bigger_line, i)
        #     lines_sum = bigger_line
        #     lines_sum[:smaller_line.shape[0]] += smaller_line

            # lines_sum =
            # lines_sum = [i + j for i, j in zip(np.roll(self._line_np[1], i), other_line[1][::-1])]

            # print(self._line_np[1].shape, other_line[1].shape, self._line_np[1].shape > other_line[1].shape)

            # if self._line_np[1].shape > other_line[1].shape:
            #     lines_sum = np.roll(self._line_np[1], i)
            #     lines_sum[:len(other_line[1][::-1])] += other_line[1][::-1]
            # else:
            #     lines_sum = other_line[1][::-1]
            #     lines_sum[:len(np.roll(self._line_np[1], i))] += np.roll(self._line_np[1], i)

        #     unique, counts = np.unique(lines_sum, return_counts=True)
        #
        #     new_max = np.max(counts)
        #
        #     if new_max > max_val:
        #         max_val = new_max
        #         shift = i
        #         ret_result = lines_sum
        #
        # seg_list = SegmentsList(ret_result)
        # longest = seg_list.get_longest()
        #
        # if longest[1] / len(ret_result) >= 0.70:
        #     return True, ret_result, longest, shift
        # else:
        #     return False, ret_result, [None, None, None], shift

