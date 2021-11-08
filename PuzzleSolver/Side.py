import numpy as np
# from matplotlib import pyplot as plt
from math import e, log


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

            x, y = longest[2], longest[2] + longest[1]

            self.x_align = x
            self.y_align = y

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

    def _check_colors(self, other_line):

        first_color = self.line_color.astype(np.int32)
        second_color = other_line.line_color[::-1].astype(np.int32)

        if first_color.shape != second_color.shape:
            return False

        sub = first_color - second_color

        # unique, counts = np.unique(first_color, return_counts=True)
        # unique_2, counts_2 = np.unique(second_color, return_counts=True)
        # print(f'unique       {[{i: j} for i, j in zip(unique, counts)]}')
        # print(f'len          {len(unique)}')
        # print(f'unique       {[{i: j} for i, j in zip(unique_2, counts_2)]}')
        # print(f'len          {len(unique_2)}')

        # mse_r = (sub[:, 0] ** 2) / len(first_color)
        # mse_g = (sub[:, 1] ** 2) / len(first_color)
        # mse_b = (sub[:, 2] ** 2) / len(first_color)

        # print(f'mse_r        {np.sum(mse_r)}')
        # print(f'max     min  {np.max(mse_r)} {np.min(mse_r)}')
        # print(f'mse_g        {np.sum(mse_g)}')
        # print(f'max     min  {np.max(mse_g)} {np.min(mse_g)}')
        # print(f'mse_b        {np.sum(mse_b)}')
        # print(f'max     min  {np.max(mse_b)} {np.min(mse_b)}')

        mse_test = [np.sum([i[0], i[1], i[2]]) / 3 for i in sub ** 2]
        mse_test_sum = sum(mse_test) / len(mse_test)

        print(f'mse chan     {mse_test}')
        print(f'avg          {np.average(mse_test)}')

        # print(f'avg abs      {np.average(abs(sub))}')

        # avg_r = np.average(abs(sub[:, 0]))
        # avg_g = np.average(abs(sub[:, 1]))
        # avg_b = np.average(abs(sub[:, 2]))
        # print(f'avg_r        {avg_r}')
        # print(f'avg_g        {avg_g}')
        # print(f'avg_b        {avg_b}')
        # print(f'avg          {np.average(mse_test)}')
        # print(f'mse chann    {[  for i in sub]}')

        print()

        thresh = 2000.

        # if mse_r < thresh and mse_b < thresh and mse_g < thresh:
        if np.average(mse_test) < thresh:
            return True
        else:
            return False

    def does_fit(self, other_line, threshold=0.70):
        # if other_line.border_side and self.border_side:
        #     return self._check_colors(other_line)

        # elif other_line.border_side or self.border_side:
        #     return False

        if other_line.border_side or self.border_side:
            return False

        if self._line_np[1].shape > other_line[1].shape:
            bigger_side = self
            smaller_side = other_line
        else:
            bigger_side = other_line
            smaller_side = self

        bigger_line = bigger_side.line_np[1]
        smaller_line = np.zeros(bigger_line.shape, dtype=np.uint8)
        smaller_line[:smaller_side.line_np[1].shape[0]] = smaller_side.line_np[1][::-1]

        for i in range(len(bigger_line)):
            line_sum = bigger_line + np.roll(smaller_line, i)

            seg_list = SegmentsList(line_sum)
            longest = seg_list.get_longest()

            # print(longest[1] / len(line_sum))
            if longest[1] / len(line_sum) >= threshold:

                x, y = longest[2], longest[2] + longest[1]

                bigger_side.x_align = x
                bigger_side.y_align = y

                size_bg, = bigger_side.line_np[1].shape
                size_sm, = smaller_side.line_np[1].shape

                smaller_side.x_align = (size_sm - y + i) % size_bg if size_bg != size_sm else (size_sm - y + i)
                smaller_side.y_align = (size_sm - x + i) % size_bg if size_bg != size_sm else (size_sm - x + i)

                # testing(
                #     bigger_side, smaller_side,
                #     i,
                #     bigger_line, smaller_line, line_sum,
                #     x, y
                # )

                return True
        # print(longest[1] / len(line_sum))
        return False


def testing(bigger_side, smaller_side, i, bigger_line, smaller_line, line_sum, x, y):
    big_size = bigger_side.line_np[0].shape[0]
    size, = smaller_side.line_np[1].shape

    print(' ' * 4, bigger_side.x_align, bigger_side.y_align)
    print(' ' * 4, big_size, size, i)
    print(' ' * 4, smaller_side.x_align, smaller_side.y_align)

    fig, ax = plt.subplots(4, 1)
    # ax[0].set_xlim([0, big_size])
    # ax[1].set_xlim([0, big_size])
    # ax[1].set_xlim([-1 * bigger_side.line_np[0].shape[0], bigger_side.line_np[0].shape[0]])
    # ax[2].set_xlim([2 * bigger_side.line_np[0].shape[0], bigger_side.line_np[0].shape[0]])
    # ax[3].set_xlim([0, big_size])

    ax[0].plot(np.arange(bigger_line.shape[0]), bigger_line)
    ax[0].set_ylabel('bigger')
    ax[1].plot(np.arange(smaller_line.shape[0]), smaller_line)
    ax[1].set_ylabel('line')
    ax[2].plot(smaller_side.line_np[0], smaller_side.line_np[1])
    ax[2].set_ylabel('side')

    ax[3].plot([i for i in range(len(smaller_line))], np.roll(smaller_line, i))
    ax[3].plot([i for i in range(len(line_sum))], line_sum)
    ax[3].set_ylabel('result')

    first_line = np.arange(x, y)
    second_line = np.arange((x - i) % big_size, (y - i) % big_size)

    third_line = np.arange(smaller_side.x_align, smaller_side.y_align)

    ax[0].plot(first_line, np.zeros(first_line.shape) - 10, 'b')
    ax[1].plot(second_line, np.zeros(second_line.shape) - 10, 'b')
    ax[2].plot(third_line, np.zeros(third_line.shape) - 10, 'g')

    plt.show()

    # if ret_val:
    #     longest = ret_seg.get_longest()

        # fig, ax = plt.subplots(3, 1)

        # ax[0].plot([i for i in range(len(bigger_line))], bigger_line)
        # ax[1].plot([i for i in range(len(smaller_line))], smaller_line)
        # ax[1].plot([i for i in range(len(ret_list))], ret_list)
        # ax[2].plot([i for i in range(len(smaller_line))], smaller_line)
        #
        # first_line = np.arange(longest[2], longest[2] + longest[1])
        # second_line = np.arange(longest[2] - shift, longest[2] + longest[1] - shift)
        # ax[0].plot(first_line, np.zeros(first_line.shape) - 10, 'b')
        # ax[1].plot(second_line, np.zeros(second_line.shape) - 10, 'b')

        # ax[1].plot(longest[2] - shift, 0, 'bo')
        # ax[1].plot(longest[2] + longest[1] - shift, 0, 'bo')

        # def animate(i):
        #     ax[2].clear()
        #     ax[2].plot([i for i in range(len(smaller_line))], np.roll(smaller_line, i))
        #     ax[2].plot([i for i in range(len(results[i]))], results[i])
        #
        # anim = animation.FuncAnimation(fig, animate, interval=50, frames=len(results))
        # anim.save(os.path.join(os.path.abspath('gifs'), f'{0}-{0}.gif'))

        # plt.show()

    # return ret_val
