from PuzzleSolver.Puzzle import Puzzle


def main():
    path = 'data/0001_0000_0000/test_dir'
    puzzle = Puzzle(path)
    puzzle.solve()
    # puzzle.save()


if __name__ == "__main__":
    main()
