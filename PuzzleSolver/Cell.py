import numpy as np
from matplotlib import pyplot as plt
from PuzzleSolver.Side import Side

CHANNEL_NUM = 3


class Cell:
    def __init__(self, image_name, image):
        self._image_name = image_name
        self._image = image

        self._cells_links = {}
        self._sides = []

        if self._image.any():
            self._get_sides()

    @property
    def image(self):
        return self._image

    @property
    def cells_links(self):
        return self._cells_links

    @property
    def sides(self):
        return self._sides

    def rotate(self, rot_val=1):
        print(self._cells_links)
        self._image = np.rot90(self._image, -1 * rot_val)
        new_cells = {}

        for key, value in self._cells_links.items():
            new_cells[(key + rot_val) % 4] = value

        self._cells_links = new_cells
        print('rotated')
        print(self._cells_links)

    def _get_sides(self):
        image = np.copy(self._image)

        for side in range(4):
            line_dot_list = []
            line_dot_color_list = []

            for i in range(image.shape[1]):
                for j in range(image[:, i:i + 1].shape[0]):
                    if np.all(image[j, i] != (0, 0, 0)):
                        line_dot_list.append([i, j])
                        line_dot_color_list.append(list(image[j, i]))
                        break

            self._sides.append(
                Side(
                    line_dot_list=line_dot_list,
                    line_color=line_dot_color_list,
                )
            )

            image = np.rot90(image)

    def show_image(self):
        plt.imshow(self._image)
        plt.show()

    def show_sides(self):
        fig, ax = plt.subplots(len(self.sides))
        for i, side in enumerate(self.sides):
            ax[i].plot(side[0], side[1])
        plt.show()

    def compare(self, other_cell):
        for i, first_side in enumerate(self.sides):

            # fig, ax = plt.subplots(5)
            # ax[0].plot(first_side[0], first_side[1])

            for j, second_side in enumerate(other_cell.sides):
                result, result_list = first_side.does_fit(second_side)

                # ax[j+1].plot(second_side[0], second_side[1][::-1])
                if result:
                    print(f'found side for {self._image_name} {other_cell._image_name}')
                    self._cells_links[i] = other_cell
                    other_cell._cells_links[j] = self
                    # ax[j+1].plot([i for i in range(len(result_list))], result_list, 'g')
                # else:
                    # ax[j+1].plot([i for i in range(len(result_list))], result_list, 'r')

            # plt.show()

    def __repr__(self):
        return str(self._image_name)

    def __call__(self, *args, **kwargs):
        return self._sides

    def __iter__(self):
        for side in self._sides:
            yield side


