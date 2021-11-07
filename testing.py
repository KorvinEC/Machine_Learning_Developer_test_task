from PuzzleSolver.Puzzle import Puzzle


def main():
    name = '0000_0000_0000'

    path = f'data/{name}/test_2'
    puzzle = Puzzle(path, 0.7)

    # puzzle.save_pickle(f'{name}.pkl')
    # puzzle = Puzzle.load_pickle(f'{name}.pkl')

    puzzle.solve()

    # puzzle.save_pickle(f'{name}.pkl')

    # puzzle = Puzzle.load_pickle(f'{name}.pkl')
    puzzle.save(name + '.ppm')


if __name__ == "__main__":
    main()
