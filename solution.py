from bwIO import openProblem, writeSolution
from bwStateObject import State
from bwUninformedSearchingAlgorithms import breadthFirstSearch, depthFirstSearch
from bwInformedSearchingAlgorithms import heuristicSearch

from sys import argv, exit
from time import perf_counter


def main(argv):
    if len(argv) > 4:
        print('Usage:\npython3 {} <algorithm> <problem_file_name.pddl> [solution_file_name]' .format(argv[0]))
        exit(1)

    problemFile = argv[2]
    outputFile = ''
    if len(argv) == 4:
        outputFile = argv[3]

    init, goal, cubes = openProblem(problemFile)

    # Initialize inital and goal states.
    initialState = State(init)
    goalState = State(goal)

    algorithm = argv[1]

    t1 = perf_counter()

    if algorithm == 'breadth':
        solution, iters = breadthFirstSearch(initialState, goalState)
    elif algorithm == 'depth':
        solution, iters = depthFirstSearch(initialState, goalState)
    elif algorithm == 'best' or algorithm == 'astar':
        solution, iters = heuristicSearch(initialState, goalState, algorithm)
    else:
        raise Exception('Unknown algorithm. Available : breadth, depth, best, astar')

    t2 = perf_counter()

    print('| Problem name: {}' .format(' ' * 10 + problemFile))
    print('| Algorithm used: {}' .format(' ' * 8 + algorithm))
    print('| Number of cubes: {}' .format(' ' * 7 + str(len(cubes))))
    print('| Cubes: {}' .format(' ' * 17 + str(' '.join(cubes))))
    if solution:
        print('| Solved in: {}' .format(' ' * 13 + str(t2-t1)))
        print('| Algorithm iterations: {}' .format(' ' * 2 + str(iters)))
        print('| Moves: {}' .format(' ' * 17 + str(len(solution))))

        print('| Solution:' + ' ' * 15 + 'Found!')
        writeSolution(solution, outputFile)
    else:
        print('| Solution:' + ' ' * 15 + 'NOT found, search timed out.')


if __name__ == '__main__':
    main(argv)
