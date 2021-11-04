import numpy as np
from matplotlib import pyplot as plt
from PuzzleSolver.Side import Side

CHANNEL_NUM = 3


class Cell:
    def __init__(self, image_name, image):
        self._image_name = image_name
        self._image = image

        self._sides = {}
        self._available_space = 0

        if self._image.any():
            self._get_sides()

    def get_cells_links_values(self):
        return [i for i in self.sides.values() if i.cell_link is not None]

    def has_same_side(self, other_cell):
        for side in self._sides.values():
            if side.cell_link == other_cell:
                return True
            else:
                False

    def has_available_space(self):
        if self._available_space > 0:
            return True
        else:
            return False

    @property
    def image(self):
        return self._image

    @property
    def sides(self):
        return self._sides

    def rotate(self, rot_val=1):
        self._image = np.rot90(self._image, -1 * rot_val)
        new_sides = {}

        for key, value in self._sides.items():
            new_sides[(key + rot_val) % 4] = value

        self._sides = new_sides

    def _get_sides(self):
        image = np.copy(self._image)

        for side_num in range(4):
            line_dot_list = []
            line_dot_color_list = []

            for i in range(image.shape[1]):
                for j in range(image[:, i:i + 1].shape[0]):
                    if np.all(image[j, i] != (0, 0, 0)):
                        line_dot_list.append([i, j])
                        line_dot_color_list.append(list(image[j, i]))
                        break
            side = Side(
                    line_dot_list=line_dot_list,
                    line_color=line_dot_color_list,
                )

            self._sides[side_num] = side

            if not side.border_side:
                self._available_space += 1

            image = np.rot90(image)

    def show_image(self):
        plt.imshow(self._image)
        plt.show()

    def show_sides(self):
        fig, ax = plt.subplots(len(self.sides))
        for i, side in self.sides:
            ax[i].plot(side[0], side[1])
        plt.show()

    def compare(self, other_cell):
        # self.show_image()
        # other_cell.show_image()

        for i, first_side in self._sides.items():

            # fig, ax = plt.subplots(5, 1)
            # ax[0].plot(first_side.line_np[0], first_side.line_np[1])

            for j, second_side in other_cell.sides.items():
                print(i, j)
                first_side.does_fit(second_side)
                print()

                # result, result_list, longest, shift  = first_side.does_fit(second_side)
                #
                # print(result, longest, shift)
                #
                # ax[j+1].plot(second_side.line_np[0], second_side.line_np[1][::-1])
                # ax[j+1].plot([i for i in range(len(result_list))], result_list)
                #
                # if result:
                #     print(f'found side for {self._image_name} {other_cell._image_name}')
                #     print(longest)
                #     self._sides[i].cell_link = other_cell
                #     other_cell.sides[j].cell_link = self
                #
                #     self._available_space -= 1
                #     other_cell._available_space -= 1
                #
                #     first_side.x_align = longest[2]
                #     first_side.y_align = longest[1]
                #
                #     print(shift)
                #
                #     second_side.x_align = longest[1]
                #     second_side.y_align = longest[2]
                #
                #     ax[j + 1].plot(longest[2], 0, 'bo')
                #     ax[j + 1].plot(longest[2] + longest[1], 0, 'bo')
                #
                #     ax[0].plot(longest[2], 0, 'bo')
                #     ax[0].plot(longest[2] + longest[1], 0, 'bo')

            # plt.show()

    def __repr__(self):
        return str(self._image_name)

    def __iter__(self):
        for side in self._sides:
            yield side

    def __getitem__(self, item):
        return self._sides[item % 4]


