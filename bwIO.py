import re


def openProblem(fileName):

    with open(fileName, 'r') as f:
        problem = f.read()

    # Fixing new line inconsistencies and removing excessive space, so that we can parse data easier.
    problem = re.sub('[ ]+', ' ', re.sub('[ ]*\)\(', ')\n(', re.sub('\n', '', problem)))

    # Spliting the input into keyword segments.
    segmentedList = re.compile('\(:objects.*\)\s*|\(:INIT.*\)\s*|\(:goal.*\)\s*', re.IGNORECASE).findall(problem)

    # Objects appear in a specific pattern. For example, (:objects A B C).
    # So, we search for a space and a word and we keep only the word,
    # thus, that group is inside '()'.
    objects = re.findall(' (\w*)', segmentedList[0])

    # Initial state appears in a specific pattern.
    # For example,
    # (:INIT (CLEAR B) (ONTABLE D) (ON B C) (ON C A) (ON A D) (HANDEMPTY))
    # We keep the status (CLEAR, ONTABLE, ON) and the cube name (A, B, C, etc).
    # So, we search inside parentheses for a word, a space and another word,
    # thus, these groups are inside '()'. If the status is 'ON', then there will
    # be a whitespace character and another word, because (ON A D) has 3 words.
    # That is why we use '?' qualifier, because it means 0 or 1 occurances.
    # This is how we cover both the cases of a pattern with 2 and 3 words.
    # (HANDEMPTY) is automatically ignored because it doesn't follow pattern.
    initTemp = re.findall('\((\w*) (\w*)\s?(\w*)?\)', segmentedList[1])

    # Goal state appears in a specific pattern.
    # For example,
    # (:goal (AND (ON D C) (ON C A) (ON A B)))
    # We keep the status (ON) and the cube name (A, B, C, etc).
    # So, we search inside parentheses for a word, a space and another word,
    # thus, these groups are inside '()'. We don't keep the status is 'ON',
    # because we only need which cube is on which one.
    # That is why we use don't include the first word inside '()'
    # (AND ...) is automatically ignored because it doesn't follow pattern.
    goalTemp = re.findall('\(\w* (\w*) (\w*)\)', segmentedList[2])

    # Initialize objects and their state (position, is clear).
    init = {i:['table', True] for i in objects}

    # For each item that's is on another, change it's location
    # and set to unclear.
    for item in initTemp:
        if item[0] == 'ON':
            init[item[1]][0] = item[2]
            init[item[2]][1] = False
        ##unessecary, but left for readability
        #elif item[0] == 'ONTABLE':
        #    state[item[1]][0] = 'table'
        #elif item[0] == 'CLEAR':
        #    state[item[1]][1] = True
        #####################################

    # Initialize goal and their state (position, is clear).
    goal = {i: ['table', True] for i in objects}

    # For each item that's is on another, change it's location
    # and set to unclear.
    for item in goalTemp:
        goal[item[0]][0] = item[1]
        goal[item[1]][1] = False

    return init, goal, objects


def writeSolution(solution, output):
    if output == '':
        output = 'solution.txt'

    with open(output, 'w') as file:
        i = 0
        for move in solution:
            i += 1
            file.write('{}. Move({}, {}, {})\n' .format(i, move[0], move[1], move[2]))
