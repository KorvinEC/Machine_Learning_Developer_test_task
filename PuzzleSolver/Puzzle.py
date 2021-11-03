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
        self._cells_to_save = []
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
        self._cells_list[0].sides[0].cell_link = self._cells_list[5]
        self._cells_list[0].sides[1].cell_link = self._cells_list[4]
        self._cells_list[0].sides[2].cell_link = None
        self._cells_list[0].sides[3].cell_link = self._cells_list[10]

        self._cells_list[1].sides[0].cell_link = self._cells_list[9]
        self._cells_list[1].sides[1].cell_link = None
        self._cells_list[1].sides[2].cell_link = self._cells_list[4]
        self._cells_list[1].sides[3].cell_link = self._cells_list[5]

        self._cells_list[2].sides[0].cell_link = self._cells_list[11]
        self._cells_list[2].sides[1].cell_link = self._cells_list[3]
        self._cells_list[2].sides[2].cell_link = None
        self._cells_list[2].sides[3].cell_link = self._cells_list[7]

        self._cells_list[3].sides[0].cell_link = None
        self._cells_list[3].sides[1].cell_link = None
        self._cells_list[3].sides[2].cell_link = self._cells_list[2]
        self._cells_list[3].sides[3].cell_link = self._cells_list[8]

        self._cells_list[4].sides[0].cell_link = self._cells_list[0]
        self._cells_list[4].sides[1].cell_link = self._cells_list[1]
        self._cells_list[4].sides[2].cell_link = None
        self._cells_list[4].sides[3].cell_link = None

        self._cells_list[5].sides[0].cell_link = self._cells_list[0]
        self._cells_list[5].sides[1].cell_link = self._cells_list[1]
        self._cells_list[5].sides[2].cell_link = self._cells_list[7]
        self._cells_list[5].sides[3].cell_link = self._cells_list[11]

        self._cells_list[6].sides[0].cell_link = None
        self._cells_list[6].sides[1].cell_link = self._cells_list[8]
        self._cells_list[6].sides[2].cell_link = self._cells_list[10]
        self._cells_list[6].sides[3].cell_link = None

        self._cells_list[7].sides[0].cell_link = self._cells_list[2]
        self._cells_list[7].sides[1].cell_link = None
        self._cells_list[7].sides[2].cell_link = self._cells_list[9]
        self._cells_list[7].sides[3].cell_link = self._cells_list[5]

        self._cells_list[8].sides[0].cell_link = None
        self._cells_list[8].sides[1].cell_link = self._cells_list[3]
        self._cells_list[8].sides[2].cell_link = self._cells_list[11]
        self._cells_list[8].sides[3].cell_link = self._cells_list[6]

        self._cells_list[9].sides[0].cell_link = None
        self._cells_list[9].sides[1].cell_link = None
        self._cells_list[9].sides[2].cell_link = self._cells_list[1]
        self._cells_list[9].sides[3].cell_link = self._cells_list[7]

        self._cells_list[10].sides[0].cell_link = self._cells_list[0]
        self._cells_list[10].sides[1].cell_link = None
        self._cells_list[10].sides[2].cell_link = self._cells_list[6]
        self._cells_list[10].sides[3].cell_link = self._cells_list[11]

        self._cells_list[11].sides[0].cell_link = self._cells_list[5]
        self._cells_list[11].sides[1].cell_link = self._cells_list[10]
        self._cells_list[11].sides[2].cell_link = self._cells_list[8]
        self._cells_list[11].sides[3].cell_link = self._cells_list[2]

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
        # self._create_solved_graph()
        self._simulate_solve()

        # for cell in self._cells_list:
        #     print(cell, cell.sides)
        # print()

        for cell in self._cells_list:
            if len(cell.get_cells_links_values()) == 2:
                while not (cell.sides[0].cell_link is None and cell.sides[3].cell_link is None):
                    cell.rotate(1)

                print('first-cell: ', cell, cell.sides)

                self._cells_to_save.append(cell)

                while 1:
                    previous_cell = cell
                    new_cell = cell.sides[1].cell_link

                    while 1:
                        while new_cell.sides[3].cell_link != previous_cell:
                            new_cell.rotate(1)

                        self._cells_to_save.append(new_cell)
                        print('new-cell: ', new_cell, new_cell.sides)

                        if new_cell.sides[1].cell_link:
                            previous_cell = new_cell
                            new_cell = new_cell.sides[1].cell_link
                        else:
                            print()
                            break

                    if cell.sides[2].cell_link:
                        while cell.sides[2].cell_link.sides[0].cell_link != cell:
                            cell.sides[2].cell_link.rotate(1)
                        cell = cell.sides[2].cell_link
                        self._cells_to_save.append(cell)
                        print('next-row-cell: ', cell, cell.sides)
                    else:
                        break
                break

    def save(self, path="image.ppm"):

        result_img = np.zeros((H, W, CHANNEL_NUM), dtype=np.uint8)

        x, y = 0, 0
        cell = self._cells_to_save[0]

        i = 0
        while 1:
            if i == 2:
                break
            j = 0
            first_cell = cell
            while 1:
                # if i == 1 and j == 2:
                #     break
                img_y, img_x = cell.image.shape[:2]

                if i <= 0:
                    x -= cell.sides[3].line[-1][1]
                if i > 0:
                    temp_y = y - cell.sides[0].line[0][1]

                print(i, j, 'x', x, img_x, cell.sides[1].line[0][1], cell.sides[3].line[-1][1])
                print(i, j, 'y', y, img_y, cell.sides[0].line[0][1])
                print()

                result_img[y: y + img_y, x: x + img_x] = cell.image

                x += img_x - cell.sides[1].line[0][1]

                if cell.sides[1].cell_link:
                    cell = cell.sides[1].cell_link
                    j += 1
                else:
                    j = 0
                    break

            if first_cell.sides[2].cell_link:
                i += 1
                x = 0
                img_y, img_x = first_cell.image.shape[:2]

                print('in final', img_y, img_x)

                y = img_y - first_cell.sides[2].line[-1][1]

                first_cell = cell = first_cell.sides[2].cell_link
            else:
                i = 0
                break

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


