'''AStar.py
partner 1 firstname and lastname: Yijie Li
partner 1 student number: 1810605
partner 1 uwnetid: yijiel2

partner 2 firstname and lastname: Junqi Ye
partner 2 student number: 1833403
partner 2 uwnetid: jy98

Assignment 2, part2, in CSE 415, Winter 2021.

This file contains EightPuzzleWithHamming Heuristic.
'''

from EightPuzzle import *

goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]


def h(s):
    count = 0
    for i in range(3):
        for j in range(3):
            if s.b[i][j] != goal[i][j] and s.b[i][j] != 0:
                count += 1

    return count


# A simple test:
# print(h([[0,8,2],[1,7,4],[3,6,5]]))
