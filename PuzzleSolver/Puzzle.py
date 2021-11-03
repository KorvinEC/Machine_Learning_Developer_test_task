import numpy as np
import os
from PuzzleSolver.Cell import Cell

W = 1200
H = 900
CHANNEL_NUM = 3  # we work with rgb images
MAX_VALUE = 255  # max pixel value, required by ppm header


class Puzzle:
    def __init__(self, folder_path):
        self._cells_list = []
        self._load_cells_from_path(folder_path)
        self._init_dims()

    def __str__(self):
        return str([str(i) for i in self._cells_list])

    def _load_cells_from_path(self, folder_path):
        for image_name in sorted(os.listdir(folder_path)):
            path = os.path.join(os.path.abspath(folder_path), image_name)
            w, h = np.loadtxt(path, skiprows=1, max_rows=1, dtype=np.int32)

            # skip 3 lines reserved for header and read image
            image = np.loadtxt(path, skiprows=3, dtype=np.uint8).reshape((h, w, CHANNEL_NUM))

            self._cells_list.append(Cell(image_name, image))

    def _init_dims(self):
        dims = np.array([t.image.shape[:2] for t in self._cells_list])
        self._h, self._w = np.min(dims, axis=0)

        self._x_nodes = np.arange(0, W, self._w)
        self._y_nodes = np.arange(0, H, self._h)
        xx, yy = np.meshgrid(self._x_nodes, self._y_nodes)
        self._nodes = np.vstack((xx.flatten(), yy.flatten())).T

    def _simulate_solve(self):
        self._cells_list[0]._cells_links = {
            0: self._cells_list[5],
            1: self._cells_list[4],
            2: None,
            3: self._cells_list[10]
        }
        self._cells_list[1]._cells_links = {
            0: self._cells_list[9],
            1: None,
            2: self._cells_list[4],
            3: self._cells_list[5],
        }
        self._cells_list[2]._cells_links = {
            0: self._cells_list[11],
            1: self._cells_list[3],
            2: None,
            3: self._cells_list[7],
        }
        self._cells_list[3]._cells_links = {
            0: None,
            1: None,
            2: self._cells_list[2],
            3: self._cells_list[8],
        }
        self._cells_list[4]._cells_links = {
            0: self._cells_list[0],
            1: self._cells_list[1],
            2: None,
            3: None,
        }
        self._cells_list[5]._cells_links = {
            2: self._cells_list[0],
            1: self._cells_list[1],
            0: self._cells_list[7],
            3: self._cells_list[11],
        }
        self._cells_list[6]._cells_links = {
            0: None,
            1: self._cells_list[8],
            2: self._cells_list[10],
            3: None,
        }
        self._cells_list[7]._cells_links = {
            0: self._cells_list[2],
            1: None,
            2: self._cells_list[9],
            3: self._cells_list[5],
        }
        self._cells_list[8]._cells_links = {
            0: None,
            1: self._cells_list[3],
            2: self._cells_list[11],
            3: self._cells_list[6],
        }
        self._cells_list[9]._cells_links = {
            0: None,
            1: None,
            2: self._cells_list[1],
            3: self._cells_list[7],
        }
        self._cells_list[10]._cells_links = {
            0: self._cells_list[0],
            1: None,
            2: self._cells_list[6],
            3: self._cells_list[11],
        }
        self._cells_list[11]._cells_links = {
            0: self._cells_list[5],
            1: self._cells_list[10],
            2: self._cells_list[8],
            3: self._cells_list[2],
        }

    def _create_solved_graph(self):
        for first_cell in self._cells_list:
            if first_cell.has_available_space():
                for second_cell in self._cells_list:
                    if not first_cell.has_same_side(second_cell) and \
                            first_cell.has_available_space() and \
                            second_cell.has_available_space() and \
                            first_cell != second_cell:
                        first_cell.compare(second_cell)

    def solve(self):
        self._create_solved_graph()
        # self._simulate_solve()

        for cell in self._cells_list:
            print(cell, cell.cells_links)
        print()

        return_cells_list = []

        for cell in self._cells_list:
            if len(cell.get_cells_links_values()) == 2:

                while not (cell[0] is None and cell[3] is None):
                    cell.rotate(1)

                print('first-cell: ', cell, cell.cells_links)

                return_cells_list.append(cell)

                while 1:
                    previous_cell = cell
                    new_cell = cell[1]

                    while 1:
                        while new_cell[3] != previous_cell:
                            new_cell.rotate(1)


                        return_cells_list.append(new_cell)
                        print('new-cell: ', new_cell, new_cell.cells_links)

                        if new_cell[1]:
                            previous_cell = new_cell
                            new_cell = new_cell[1]
                        else:
                            print()
                            break

                    if cell[2]:
                        while cell[2][0] != cell:
                            cell[2].rotate(1)
                        cell = cell[2]
                        return_cells_list.append(cell)
                        print('next-row-cell: ', cell, cell.cells_links)
                    else:
                        break
                break
        self._cells_list = return_cells_list

    def save(self, path="image.ppm"):
        for cell in self._cells_list:
            print(cell, cell.cells_links)

        result_img = np.zeros((H, W, CHANNEL_NUM), dtype=np.uint8)

        for (x, y), cell in zip(self._nodes, self._cells_list):
            result_img[y: y + self._h, x: x + self._w] = cell.image[:self._h, :self._w]

        write_image_ppm(path, result_img)
        print(f'Saved image in {os.path.abspath(path)}')


def write_image_ppm(path, img):
    h, w = img.shape[:2]
    # ppm format requires header in special format
    header = f'P3\n{w} {h}\n{MAX_VALUE}\n'
    with open(path, 'w') as f:
        f.write(header)
        for r, g, b in img.reshape((-1, CHANNEL_NUM)):
            f.write(f'{r} {g} {b} ')


