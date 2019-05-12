from collections import deque
from time import perf_counter


def breadthFirstSearch(initialState, goalState, timeout=60):
    # Initialize iterations counter.
    iterations = 0

    # Initialize visited vertexes as set, because it's faster to check
    # if an item exists, due to O(1) searching complexity on average case.
    # The items here are hashable state objects.
    # A list, has O(n) on average case, when searching for an item existence.
    #
    # Initialize the search queue which is a double-ended queue and has O(1)
    # complexity on average case when popping an item from it's left.
    # A list has O(n) on average case, when popping from the left,
    # so a deque, improves performance for both ends accesses.
    #
    # source : https://wiki.python.org/moin/TimeComplexity
    visited, queue = set(), deque([initialState])

    # Initialize timeout counter.
    t1 = perf_counter()
    # While there are elements to search for...
    while queue:
        # Initialize on each iteration the performace of the previous.
        t2 = perf_counter()
        # If the the previous iteration has exceeded the allowed time,
        # then return, prematurely, nothing.
        if t2 - t1 > timeout:
            return None, iterations

        iterations += 1
        vertex = queue.popleft()

        if vertex == goalState:
            return vertex._tracePath(), iterations

        for neighbour in vertex._generateStateChildren():
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)


def depthFirstSearch(initialState, goalState, timeout=60):
    # Initialize iterations counter.
    iterations = 0

    # Initialize visited vertexes as set, because it's faster to check
    # if an item exists, due to O(1) searching complexity on average case.
    # The items here are hashable state objects.
    # A list, has O(n) on average case, when searching for an item existence.
    #
    # Initialize the search queue which is a double-ended queue and has O(1)
    # complexity on average case when popping an item from it's right.
    # A list has O(1) on average case, when popping from the right,
    # which is the same, but we leave it the same as BFS for readability reasons.
    #
    # source : https://wiki.python.org/moin/TimeComplexity
    visited, stack = set(), deque([initialState])

    # Initialize timeout counter.
    t1 = perf_counter()

    # While there are elements to search for...
    while stack:
        # Initialize on each iteration the performace of the previous.
        t2 = perf_counter()
        # If the the previous iteration has exceeded the allowed time,
        # then return, prematurely, nothing.
        if t2 - t1 > timeout:
            return None, iterations

        iterations += 1
        vertex = stack.pop()  # right

        if vertex == goalState:
            return vertex._tracePath(), iterations

        if vertex in visited:
            continue

        for neighbour in vertex._generateStateChildren():
            stack.append(neighbour)

        visited.add(vertex)
