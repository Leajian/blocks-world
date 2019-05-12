from itertools import permutations
from copy import deepcopy


class State(object):
    """
        description
            A state's description dictionary looks like this...
            {'A': ['B', True], 'C': ['table', True], 'B': ['table', False]}

            And represents...
            'That cube': ['is on top of that', is it clear on top?]

            And if we visualize it, it looks like this...
             ___
            | A |
            |___|  ___
            | B | | C |
            |___| |___|
            ====================== <-- table

        parent
            The parent state object.

        move
            The move that was required to form that state from parent state.
            The list has the following format...
            ['A', 'B', 'C'] or ['A', 'B', 'table']
            ...which means, move cube A, from cube, on top of cube C or table.
    """

    def __init__(self, description=None, parent=None, move=None):
        super(State, self).__init__()
        self._parent = parent
        self._moveToForm = move

        # If no initial state description is given, try to create it,
        # by following the move that this state was given to form itself.
        if not description:
            self._stateDescription = deepcopy(self._parent._stateDescription)

            # If that move doesn't exists, it probably means, that it's a root state.
            if self._moveToForm is not None:
                self.__move(self._moveToForm[0], self._moveToForm[2])
        # Otherwise, just use the state given as argument.
        else:
            self._stateDescription = description

    # Overriding the equals method, so the comparison of the states is its
    # description dictionary.
    def __eq__(self, other):
        if other is None:
            return False
        return self._stateDescription == other._stateDescription

    # Overriding the representation method, for debugging purposes.
    def __repr__(self):
        return str(self._stateDescription) + '\n'

    def _generateStateChildren(self):
        """
            Generates all possible children (states) of itself (state).
            Each child state represents a possible move.
        """
        # Find all clear cubes of the state.
        clearCubes = [key for key in self._stateDescription if self._stateDescription[key][1] is True]

        # Calculate all possible move permutations and
        # add the special case of moving a cube onto table, if it's not already.
        possibleMoves = list(permutations(clearCubes, 2)) + [(cube, 'table') for cube in clearCubes if self._stateDescription[cube][0] != 'table']

        # Initialize the final generated children states list.
        states = []

        # For every possible move, create a child state, whose parent is this
        # very state and its move to form is given bt the move method.
        for cubeToMove, destinationCube in possibleMoves:
            states.append(State(parent=self, move=self.__move(cubeToMove, destinationCube, True)))

        return states

    def __move(self, object, destination, fake=False):
        """
            Moves the selected object to desired destination and
            returns the action in detail. Optionally,
            it only returns the hypothetical move, without actually doing it.
        """

        # Initialize the initial position of the cube.
        oldPosition = self._stateDescription[object][0]

        # Fake means, that the move is only recorded and not performed.
        # This is useful when we only want the move to form a state
        # from another and then passed as an argument to a new state object.
        if fake:
            return [object, oldPosition, destination]

        # The cube below is now clear, because the cube above it is lifted.
        # Unless it's the table, which is always something we can place on.
        if oldPosition != 'table':
            self._stateDescription[oldPosition][1] = True

        # Cube is now onto destination cube.
        self._stateDescription[object][0] = destination

        # The cube below is now unclear, because the cube above it is placed.
        # Unless it's the table, which is always something we can place on.
        if destination != 'table':
            self._stateDescription[destination][1] = False

        # [move a cube, from that cube, on top of another cube or on table]
        move = [object, oldPosition, destination]

        return move

    def __hash__(self):
        # Creating my own hashing method for the state, which is uniquely
        # identified by the cube, its position and a letter T(rue) or F(alse),
        # which denotes whether the cube is clear above or not.
        string = ''
        for key, value in self._stateDescription.items():
            string += "".join(key + value[0] + str(value[1])[0])
        return hash(string)

    def _tracePath(self):
        """
            Finds the moves required to solve the problem.
        """

        # Initialize the final path list.
        path = []
        # Initialize the current parent as this very state.
        currentParent = self

        # While there is a parent, we have not reached the root...
        while currentParent._parent is not None:
            # Add the move that the current parent required to form to the path.
            path.append(currentParent._moveToForm)
            # Set the current parent, the parent of the it, the grandparent.
            # So, we can go one vertex above, until there is no parent.
            # That means we have reached the root, because it has no parent.
            currentParent = currentParent._parent

        # Invert the order before you return, becase we need
        # the path from the root to the state,
        # but we have the path from this very state
        # (which is probably a solution) to the root.
        return path[::-1]

    def _tracePathDEBUG(self):
        # Just pretty printing the moves to solution.
        i = 0
        for move in self._tracePath():
            i += 1
            print('{}. Move({}, {}, {})' .format(i, move[0], move[1], move[2]))
