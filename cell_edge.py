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


def get_sides(input_image):
    image = np.copy(input_image)

    all_sides = []

    for side in range(4):
        one_side = []

        for i in range(image.shape[1]):
            for j in range(image[:, i:i+1].shape[0]):
                if np.all(image[j, i] != (0, 0, 0)):
                    one_side.append([i, j])
                    break

        all_sides.append(one_side)

        image = np.rot90(image)

    return all_sides


def find_shift(first_side, second_side):
    max = 0

    for i in range(len(first_side[0])):
        result = [i + j for i, j in zip(np.roll(first_side[1], -i), second_side[1][::-1])]
        unique, counts = np.unique(result, return_counts=True)
        new_max = np.max(counts)
        if new_max > max:
            max = new_max
            shift_index = i
            ret_result = result
            entropy = entropy2(result)

    return shift_index, [[i for i in range(len(result))], ret_result], entropy


from math import e, log


def entropy2(labels, base=None):
  """ Computes entropy of label distribution. """

  n_labels = len(labels)

  if n_labels <= 1:
    return 0

  value,counts = np.unique(labels, return_counts=True)
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


def main():
    path = 'data/0001_0000_0000/tiles'
    sorted_dir = sorted(os.listdir(path))
    tile_1 = read_image(os.path.abspath(f'{path}/{sorted_dir[0]}'))
    tile_2 = read_image(os.path.abspath(f'{path}/{sorted_dir[4]}'))

    first_image_sides = get_sides(tile_1)
    second_image_sides = get_sides(tile_2)

    plt.imshow(tile_1)
    plt.show()
    plt.imshow(tile_2)
    plt.show()

    for first_side in first_image_sides:
        first_side_np = [[x for x, y in first_side], [y for x, y in first_side]]

        fig, ax = plt.subplots(5)
        ax[0].plot(first_side_np[0], first_side_np[1])

        for i, second_side in enumerate(second_image_sides):
            second_side_np = [[x for x, y in second_side], [y for x, y in second_side]]

            index, result, entropy = find_shift(first_side_np, second_side_np)

            # print(entropy)

            ax[i+1].plot(second_side_np[0], second_side_np[1])
            ax[i+1].plot(result[0], result[1][::-1])
            ax[i+1].text(0, 0, f'{entropy = }', fontsize=10)

        plt.show()


    # first_line = [[x for x, y in res[0]], [y for x, y in res[0]]]
    # second_line = [[x for x, y in res[2]], [y for x, y in res[2]]]

    # index, result = find_shift(first_line, second_line)
    #
    # print(index, result)
    #
    # fig, ax = plt.subplots(4)
    # ax[0].plot(first_line[0], first_line[1])
    # ax[1].plot(second_line[0], second_line[1])
    # ax[2].plot(second_line[0], second_line[1][::-1])
    # ax[3].plot(result[0], result[1])
    # plt.show()


        # print(i, dict(zip(unique, counts)))

        # fig, ax = plt.subplots(1)
        # ax.plot([i for i in range(len(result))], result)
        # plt.show()

    # result = [i + j for i, j in zip(first_line[1][11:], second_line[1][::-1])]
    # result = [[i for i in range(len(result))], result]

    # for i in range(len(first_line))

    # fig, ax = plt.subplots(4)
    # ax[0].plot(first_line[0], first_line[1])
    # ax[1].plot(second_line[0], second_line[1])
    # ax[2].plot(second_line[0], second_line[1][::-1])
    # ax[3].plot(result[0], result[1])
    # plt.show()

    # res_tile = np.copy(tile)

    # all_sides = []
    #
    # for color in range(4):
    #     result = []
    #
    #     for i in range(tile.shape[1]):
    #         for j in range(tile[:, i:i+1].shape[0]):
    #             if np.all(tile[j, i] != (0, 0, 0)):
    #                 result.append([i, j])
    #                 break
    #
    #     # for x, y in result:
    #     #     res_tile[y, x] = colors[color]
    #
    #     all_sides.append(result)
    #
    #     tile = np.rot90(tile)
    #     res_tile = np.rot90(res_tile)
    #
    # first_line = [[x for x, y in all_sides[0]], [y for x, y in all_sides[0]]]
    #
    # # fig, ax = plt.subplots(2)
    # # ax[0].imshow(res_tile, interpolation='nearest')
    # # ax[1].plot(first_line[0], first_line[1])
    # # plt.show()
    #
    # tile = read_image(os.path.abspath(f'data/0001_0000_0000/tiles/{sorted_dir[5]}'))
    #
    # res_tile = np.copy(tile)
    #
    # all_sides = []
    #
    # for color in range(4):
    #     result = []
    #
    #     for i in range(tile.shape[1]):
    #         for j in range(tile[:, i:i+1].shape[0]):
    #             if np.all(tile[j, i] != (0, 0, 0)):
    #                 result.append([i, j])
    #                 break
    #
    #     # for x, y in result:
    #     #     res_tile[y, x] = colors[color]
    #
    #     all_sides.append(result)
    #
    #     tile = np.rot90(tile)
    #     res_tile = np.rot90(res_tile)
    #
    # second_line = [[x for x, y in all_sides[2]], [y for x, y in all_sides[2]]]
    #
    # changed = [(i * -1) + np.amax(second_line[1]) for i in second_line[1][::-1]]
    #
    # while 1:
    #     result = [i + j for i, j in zip(first_line[1], changed)]

    # fig, ax = plt.subplots(2)
    # ax[0].imshow(res_tile, interpolation='nearest')
    # ax[1].plot(second_line[0], changed)
    # plt.show()

    # result = [i - j for i, j in zip(first_line[1], changed)]
    # result_0 = [i - j for i, j in zip(first_line[1][11:], changed)]
    #
    # unique, counts = np.unique(result, return_counts=True)
    # print(dict(zip(unique, counts)))
    #
    # unique, counts = np.unique(result_0, return_counts=True)
    # print(dict(zip(unique, counts)))

    # fig, ax = plt.subplots(4)
    # ax[0].plot(first_line[0], first_line[1])
    # ax[1].plot([i for i in range(len(changed))], changed)
    # ax[2].plot([i for i in range(len(result))], result)
    # ax[3].plot([i for i in range(len(result_0))], result_0)
    # plt.show()

    # print(first_line[1] - changed)

    # fig, ax = plt.subplots(2)
    # ax[0].imshow(res_tile, interpolation='nearest')

    # ax[1].plot(result_line[0], result_line[1])
    # plt.show()


if __name__ == "__main__":
    main()