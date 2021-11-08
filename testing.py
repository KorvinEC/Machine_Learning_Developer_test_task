from PuzzleSolver.Puzzle import Puzzle


def main():
    name = '0000_0000_0000'

    path = f'data/{name}/tiles'
    puzzle = Puzzle(path, 0.71)

    puzzle.create_solved_graph()

    puzzle.solve()

    puzzle.save(name + '.ppm')


if __name__ == "__main__":
    main()
