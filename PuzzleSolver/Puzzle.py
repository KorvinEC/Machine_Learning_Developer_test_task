import numpy as np
import os
from PuzzleSolver.Cell import Cell
import pickle

W = 1200
H = 900
CHANNEL_NUM = 3  # we work with rgb images
MAX_VALUE = 255  # max pixel value, required by ppm header


class Puzzle:
    def __init__(self, folder_path, threshold=0.7):
        self._cells_list = []
        self._cells_to_save = np.array([])
        self._load_cells_from_path(folder_path)
        self._threshold = threshold
        # self._graph_shape = [0, 0, CHANNEL_NUM]

    def __str__(self):
        return str([str(i) for i in self._cells_list])

    @property
    def cells_list(self):
        return self._cells_list

    def save_pickle(self, name):

        with open(name, 'wb') as outp:
            pickle.dump(self, outp, pickle.HIGHEST_PROTOCOL)

        print(f'Saved {name}')

    @staticmethod
    def load_pickle(name):
        with open(name, 'rb') as inp:
            obj = pickle.load(inp)
        print(f'Loaded {name}')
        return obj

    def _load_cells_from_path(self, folder_path):
        for image_name in sorted(os.listdir(folder_path)):
            path = os.path.join(os.path.abspath(folder_path), image_name)
            w, h = np.loadtxt(path, skiprows=1, max_rows=1, dtype=np.int32)

            # skip 3 lines reserved for header and read image
            image = np.loadtxt(path, skiprows=3, dtype=np.uint8).reshape((h, w, CHANNEL_NUM))

            self._cells_list.append(Cell(image_name, image))

    def _create_solved_graph(self):
        for first_cell in self._cells_list:
            if first_cell.has_available_space():
                # print(f'{first_cell} {first_cell.has_available_space() = }')
                for second_cell in self._cells_list:
                    # print(f'{second_cell} {second_cell.has_available_space() = }')
                    # print(f'{first_cell != second_cell = }')
                    # print(f'{first_cell.has_same_side(second_cell) = }')

                    if first_cell != second_cell and not first_cell.has_same_side(second_cell) and \
                            first_cell.has_available_space() and \
                            second_cell.has_available_space():
                        print(first_cell, second_cell)
                        res = first_cell.compare(second_cell, self._threshold)
                        # print('*' * 16)
                        if res:
                            print(f'Found side for {first_cell} and {second_cell}')
                    # print('-'*16)
            # print()
        print(f'Ended solving')
        for cell in self._cells_list:
            print(cell, cell.sides)

    def solve(self):
        self._create_solved_graph()

        result = []

        for cell in self._cells_list:

            if len(cell.get_cells_links_values()) == 2:
                for i in range(4):
                    if not (cell.sides[0].cell_link is None and cell.sides[3].cell_link is None):
                        cell.rotate(1)
                    elif i == 3:
                        break

                row_results = []

                print('first-cell: ', cell, cell.sides)

                row_results.append(cell)

                while 1:
                    previous_cell = cell
                    new_cell = cell.sides[1].cell_link

                    while 1:
                        while new_cell.sides[3].cell_link != previous_cell:
                            new_cell.rotate(1)

                        row_results.append(new_cell)
                        print('new-cell: ', new_cell, new_cell.sides)

                        if new_cell.sides[1].cell_link:
                            previous_cell = new_cell
                            new_cell = new_cell.sides[1].cell_link
                        else:
                            print()
                            break

                    result.append(row_results)

                    if cell.sides[2].cell_link:

                        while cell.sides[2].cell_link.sides[0].cell_link != cell:
                            cell.sides[2].cell_link.rotate(1)

                        row_results = []
                        cell = cell.sides[2].cell_link
                        row_results.append(cell)

                        print('next-row-cell: ', cell, cell.sides)
                    else:
                        break
                break

        self._cells_to_save = np.array(result)

    def save(self, path="image.ppm"):
        result_img = np.zeros((H, W, CHANNEL_NUM), dtype=np.uint8)

        if len(self._cells_to_save.shape) != 2:
            raise IndexError(f'Wrong shape {self._cells_to_save.shape}')

        if self._cells_to_save.shape[0] > self._cells_to_save.shape[1]:
            result_img = np.rot90(result_img)

        x, y = 0, 0
        cell = self._cells_to_save[0][0]
        try:
            i = 0
            while 1:
                first_cell = cell
                j = 0
                while 1:

                    img_y, img_x = cell.image.shape[:2]

                    x_a = cell.sides[3].x_align
                    y_a = cell.sides[3].y_align
                    x_d = cell.sides[3].line[x_a: y_a][-1][1]

                    x_a = cell.sides[0].x_align
                    y_a = cell.sides[0].y_align
                    y_d = cell.sides[0].line[x_a: y_a][0][1]

                    x -= x_d

                    print(i, j, cell)
                    print(' ' * 4, 'coords:', x, y)
                    print(' ' * 4, 'img   :', img_x, img_y)
                    print(' ' * 4, 'delta :', x_d, y_d)

                    result_img[y - y_d: y - y_d + img_y, x: x   + img_x] += cell.image

                    x_a = cell.sides[1].x_align
                    y_a = cell.sides[1].y_align
                    x_d = cell.sides[1].line[x_a: y_a][0][1]

                    print(' ' * 4, 'delta :', x_d)

                    x += img_x - x_d

                    j += 1

                    if cell.sides[1].cell_link:
                        cell = cell.sides[1].cell_link
                    else:
                        break

                i += 1

                if first_cell.sides[2].cell_link:
                    print('-' * 16)
                    x = 0

                    img_y, img_x = first_cell.image.shape[:2]

                    x_a = first_cell.sides[2].x_align
                    y_a = first_cell.sides[2].y_align
                    y_d = first_cell.sides[2].line[x_a: y_a][-1][1]

                    y += img_y - y_d

                    cell = first_cell.sides[2].cell_link

                    x_a = first_cell.sides[0].x_align
                    y_a = first_cell.sides[0].y_align
                    y_d = first_cell.sides[0].line[x_a: y_a][0][1]

                    y -= y_d

                else:
                    break
        except Exception as e:
            raise e
        finally:
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


