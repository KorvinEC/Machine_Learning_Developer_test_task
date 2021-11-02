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

    def _load_cells_from_path(self, folder_path):
        for image_name in sorted(os.listdir(folder_path)):
            path = os.path.join(os.path.abspath(folder_path), image_name)
            w, h = np.loadtxt(path, skiprows=1, max_rows=1, dtype=np.int32)

            # skip 3 lines reserved for header and read image
            image = np.loadtxt(path, skiprows=3, dtype=np.uint8).reshape((h, w, CHANNEL_NUM))

            self._cells_list.append(Cell(image_name, image))

    def __str__(self):
        return str([str(i) for i in self._cells_list])

    def solve(self):
        for first_cell in self._cells_list:
            # first_cell.show_image()

            for second_cell in self._cells_list:
                # second_cell.show_image()
                first_cell.compare(second_cell)

        for cell in self._cells_list:
            print(cell._image_name, cell.cells_links)

    def save(self, path="image.ppm"):
        result_img = np.zeros((H, W, CHANNEL_NUM), dtype=np.uint8)

        dims = np.array([t.image.shape[:2] for t in self._cells_list])
        h, w = np.min(dims, axis=0)

        x_nodes = np.arange(0, W, w)
        y_nodes = np.arange(0, H, h)
        xx, yy = np.meshgrid(x_nodes, y_nodes)
        nodes = np.vstack((xx.flatten(), yy.flatten())).T

        for (x, y), cell in zip(nodes, self._cells_list):
            result_img[y: y + h, x: x + w] = cell.image[:h, :w]

        write_image(path, result_img)


def write_image(path, img):
    h, w = img.shape[:2]
    # ppm format requires header in special format
    header = f'P3\n{w} {h}\n{MAX_VALUE}\n'
    with open(path, 'w') as f:
        f.write(header)
        for r, g, b in img.reshape((-1, CHANNEL_NUM)):
            f.write(f'{r} {g} {b} ')


