import numpy as np
import os
from matplotlib import pyplot as plt

from PIL import Image


# dimensions of result image
W = 1200
H = 900
CHANNEL_NUM = 3  # we work with rgb images
MAX_VALUE = 255  # max pixel value, required by ppm header

colors = (
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0)
)

def read_image(path):
    # second line of header contains image dimensions
    w, h = np.loadtxt(path, skiprows=1, max_rows=1, dtype=np.int32)
    # skip 3 lines reserved for header and read image
    image = np.loadtxt(path, skiprows=3, dtype=np.uint8).reshape((h, w, CHANNEL_NUM))
    return image


def main():
    path = 'data/0001_0000_0000/tiles'
    sorted_dir = sorted(os.listdir(path))
    tile = read_image(os.path.abspath(f'data/0001_0000_0000/tiles/{sorted_dir[0]}'))

    res_tile = np.copy(tile)

    all_sides = []

    for color in range(4):
        result = []

        for i in range(tile.shape[1]):
            for j in range(tile[:, i:i+1].shape[0]):
                if np.all(tile[j, i] != (0, 0, 0)):
                    result.append([i, j])
                    break

        # for x, y in result:
        #     res_tile[y, x] = colors[color]

        all_sides.append(result)

        tile = np.rot90(tile)
        res_tile = np.rot90(res_tile)

    first_line = [[x for x, y in all_sides[0]], [y for x, y in all_sides[0]]]

    # fig, ax = plt.subplots(2)
    # ax[0].imshow(res_tile, interpolation='nearest')
    # ax[1].plot(first_line[0], first_line[1])
    # plt.show()

    tile = read_image(os.path.abspath(f'data/0001_0000_0000/tiles/{sorted_dir[5]}'))

    res_tile = np.copy(tile)

    all_sides = []

    for color in range(4):
        result = []

        for i in range(tile.shape[1]):
            for j in range(tile[:, i:i+1].shape[0]):
                if np.all(tile[j, i] != (0, 0, 0)):
                    result.append([i, j])
                    break

        # for x, y in result:
        #     res_tile[y, x] = colors[color]

        all_sides.append(result)

        tile = np.rot90(tile)
        res_tile = np.rot90(res_tile)

    second_line = [[x for x, y in all_sides[2]], [y for x, y in all_sides[2]]]

    changed = [(i * -1) + np.amax(second_line[1]) for i in second_line[1][::-1]]

    # fig, ax = plt.subplots(2)
    # ax[0].imshow(res_tile, interpolation='nearest')
    # ax[1].plot(second_line[0], changed)
    # plt.show()

    result = [i - j for i, j in zip(first_line[1], changed)]
    result_0 = [i - j for i, j in zip(first_line[1][11:], changed)]

    fig, ax = plt.subplots(4)
    ax[0].plot(first_line[0], first_line[1])
    ax[1].plot([i for i in range(len(changed))], changed)
    ax[2].plot([i for i in range(len(result))], result)
    ax[3].plot([i for i in range(len(result_0))], result_0)
    plt.show()

    # print(first_line[1] - changed)
    # print()


    # fig, ax = plt.subplots(2)
    # ax[0].imshow(res_tile, interpolation='nearest')
    #
    #
    #
    # ax[1].plot(result_line[0], result_line[1])
    # plt.show()


if __name__ == "__main__":
    main()