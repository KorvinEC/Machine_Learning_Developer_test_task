import numpy as np
from matplotlib import pyplot as plt
from PuzzleSolver.Side import Side

CHANNEL_NUM = 3


class Cell:
    def __init__(self, image_name, image):
        self._image_name = image_name
        self._image = image

        self._cells_links = {
            0: None,
            1: None,
            2: None,
            3: None,
        }
        self._sides = []
        self._available_space = 0

        if self._image.any():
            self._get_sides()

    def get_cells_links_values(self):
        return [i for i in self.cells_links.values() if i is not None]

    def has_same_side(self, other_cell):
        values = [value for key, value in self.cells_links.items()]
        if other_cell in values:
            return True
        else:
            return False

    def has_available_space(self):
        if self._available_space > 0:
            return True
        else:
            return False

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
        self._image = np.rot90(self._image, -1 * rot_val)
        new_cells = {}

        for key, value in self._cells_links.items():
            new_cells[(key + rot_val) % 4] = value

        self._cells_links = new_cells

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
            side = Side(
                    line_dot_list=line_dot_list,
                    line_color=line_dot_color_list,
                )

            self._sides.append(side)

            if not side.border_side:
                self._available_space += 1

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

            for j, second_side in enumerate(other_cell.sides):
                result, result_list = first_side.does_fit(second_side)

                if result:
                    print(f'found side for {self._image_name} {other_cell._image_name}')
                    self._cells_links[i] = other_cell
                    other_cell._cells_links[j] = self
                    self._available_space -= 1
                    other_cell._available_space -= 1

    def __repr__(self):
        return str(self._image_name)

    def __iter__(self):
        for side in self._sides:
            yield side

    def __getitem__(self, item):
        return self.cells_links[item % 4]


