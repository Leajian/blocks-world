from time import perf_counter


def __distanceFromGoal(currentStates, goalState):
    """ The H function. """

    # Initialize a list of each state's scores.
    statesScores = []

    # For each state in currently discovered states...
    for state in currentStates:

        # Initialize out place blocks.
        outOfPlaceBlocks = 0

        # For each block in every state...
        for block in state._stateDescription:

            # If that block is not positioned correctly, increase out of place
            # blocks for that state.
            if state._stateDescription[block] != goalState._stateDescription[block]:
                outOfPlaceBlocks += 1

        # Store the final score for that state.
        statesScores.append(outOfPlaceBlocks)

    # Return the index of the state with smallest distance from goal.
    return statesScores.index(min(statesScores))


def __distanceFromGoalWithLeastMoves(currentStates, goalState):
    """ The G + H function. """

    # Initialize a list of each state's scores.
    statesScores = []

    # For each state in currently discovered states...
    for state in currentStates:

        # Initialize out place blocks.
        outOfPlaceBlocks = 0

        # For each block in every state...
        for block in state._stateDescription:

            # If that block is not positioned correctly, increase out of place
            # blocks for that state.
            if state._stateDescription[block] != goalState._stateDescription[block]:
                outOfPlaceBlocks += 1

        # Store how many blocks are out of place plus the number of moves
        # needed to reach from root to each state.
        statesScores.append(outOfPlaceBlocks + len(state._tracePath()))

    # Return the index of the state with smallest distance
    # and least moves from goal.
    return statesScores.index(min(statesScores))


def heuristicSearch(initialState, goalState, algorithm='best', timeout=60):
    # Each algorithm uses a different heuristic function for the search.
    if algorithm == 'astar':
        function = __distanceFromGoalWithLeastMoves
    elif algorithm == 'best':
        function = __distanceFromGoal

    # Initialize iterations counter.
    iterations = 0

    # Initialize visited vertexes as set, because it's faster to check
    # if an item exists, due to O(1) searching complexity on average case.
    # The items here are hashable state objects.
    # A list, has O(n) on average case, when searching for an item existence.
    #
    # Initialize the search list.
    # A list has O(n) for popping items on average case.
    # We cannot improve it any further, since we may access items in the middle.
    #
    # source : https://wiki.python.org/moin/TimeComplexity
    visited, list = set(), [initialState]

    # Initialize timeout counter.
    t1 = perf_counter()

    # While there are elements to search for...
    while list:
        # Initialize on each iteration the performace of the previous.
        t2 = perf_counter()
        # If the the previous iteration has exceeded the allowed time,
        # then return, prematurely, nothing.
        if t2 - t1 > timeout:
            return None, iterations

        iterations += 1
        # Determine which item you pop, defined by the heuristic function of
        # the corresponding algorithm.
        item = function(list, goalState)
        vertex = list.pop(item)

        if vertex == goalState:
            return vertex._tracePath(), iterations

        for neighbour in vertex._generateStateChildren():
            if neighbour in visited:
                continue

            visited.add(neighbour)
            list.append(neighbour)
