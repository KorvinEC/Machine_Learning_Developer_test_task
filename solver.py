import os
import sys
from PuzzleSolver.Puzzle import Puzzle


if __name__ == "__main__":
    directory = sys.argv[1]
    path = os.path.abspath(directory)
    directory = path

    puzzle = Puzzle(path, 0.71)

    puzzle.create_solved_graph()

    puzzle.solve()

    save_path = os.path.join(path, 'image.ppm')

    puzzle.save(save_path)