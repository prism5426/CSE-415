'''Farmer_Fox.py
by Yijie Li
UWNetID: yijiel2
Student number: 1810605

Assignment 2, in CSE 415, Winter 2021.
 
This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''

# Put your formulation of the Farmer-Fox-Chicken-and-Grain problem here.
# Be sure your name, uwnetid, and 7-digit student number are given above in 
# the format shown.

# <METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "Farmer_Fox"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['Yijie Li']
PROBLEM_CREATION_DATE = "18-JAN-2021"

# The following field is mainly for the human solver, via either the Text_SOLUZION_Client.
# or the SVG graphics client.
PROBLEM_DESC = \
    '''This is the Farmer and Fox problem.'''

LEFT = 0
RIGHT = 1


class State:
    def __init__(self):
        self.d = {'bank': [['Fa', 'Fo', 'C', 'G'], []],
                  'boat': LEFT}
        self.d['bank'][LEFT].sort()
        self.d['bank'][RIGHT].sort()

    def __eq__(self, s2):
        for b in ['bank', 'boat']:
            if self.d[b] != s2.d[b]: return False
        return True

    def __str__(self):
        # Produces a textual description of a state

        # add objects on the left bank to a list
        left_bank_list = []
        for obj in self.d['bank'][0]:
            left_bank_list.append(obj)

        # add objects on the right bank to a list
        right_bank_list = []
        for obj in self.d['bank'][1]:
            right_bank_list.append(obj)

        txt = str(left_bank_list) + ' || ' + str(right_bank_list) + '\n'

        side = 'left'
        if self.d['boat'] == 1: side = 'right'
        txt += "Boat is on the " + side + ".\n"
        return txt

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State()
        news.d['bank'] = [self.d['bank'][l_or_r][:] for l_or_r in [LEFT, RIGHT]]
        news.d['boat'] = self.d['boat']
        return news

    def can_move(self, obj):
        # get current bank
        bk = self.d['boat']

        # check if farmer is in current bank
        if 'Fa' not in self.d['bank'][bk]:
            return False

        # check if obj is in current bank
        if obj != '' and obj not in self.d['bank'][bk]:
            return False

        left_temp = self.d['bank'][LEFT].copy()
        right_temp = self.d['bank'][RIGHT].copy()

        # if boat is currently on left bank
        if bk is LEFT:
            right_temp.append('Fa')
            if obj != '':
                right_temp.append(obj)
            left_temp.remove('Fa')
            if obj != '':
                left_temp.remove(obj)

        # if boat is currently on right bank
        if bk is RIGHT:
            left_temp.append('Fa')
            if obj != '':
                left_temp.append(obj)
            right_temp.remove('Fa')
            if obj != '':
                right_temp.remove(obj)

        if len(left_temp) == 2 and 'Fo' in left_temp and 'C' in left_temp:
            return False
        # chicken alone with grain
        elif len(left_temp) == 2 and 'C' in left_temp and 'G' in left_temp:
            return False
        # farmer alone
        elif len(left_temp) == 1 and 'Fa' in left_temp:
            return False

        if len(right_temp) == 2 and 'Fo' in right_temp and 'C' in right_temp:
            return False
        # chicken alone with grain
        elif len(right_temp) == 2 and 'C' in right_temp and 'G' in right_temp:
            return False
        # farmer alone
        elif len(right_temp) == 1 and 'Fa' in right_temp:
            return False

        return True

    def move(self, obj):
        news = self.copy()
        bk = self.d['boat']  # current farmer bank

        # remove farmer and obj from left bank, and add to right bank
        if bk == LEFT:
            # move farmer
            news.d['bank'][LEFT].remove('Fa')
            news.d['bank'][RIGHT].append('Fa')

            if obj in news.d['bank'][LEFT]:
                news.d['bank'][RIGHT].append(obj)
                news.d['bank'][LEFT].remove(obj)

        # remove farmer and obj from right bank, and add to left bank
        elif bk == RIGHT:
            # move farmer
            news.d['bank'][RIGHT].remove('Fa')
            news.d['bank'][LEFT].append('Fa')

            if obj in news.d['bank'][RIGHT]:
                news.d['bank'][LEFT].append(obj)
                news.d['bank'][RIGHT].remove(obj)

        # move boat to the other side
        if news.d['boat'] == LEFT:
            news.d['boat'] = RIGHT
        else:
            news.d['boat'] = LEFT

        news.d['bank'][LEFT].sort()
        news.d['bank'][RIGHT].sort()

        return news


def goal_test(s):
    # if LEFT bank is empty, then s is a goal state
    return len(s.d['bank'][LEFT]) == 0


def goal_message(s):
    return "You have solved the Farmer problem!"


class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


# </COMMON_CODE>

# <INITIAL_STATE>
CREATE_INITIAL_STATE = lambda: State()

# </INITIAL_STATE>

# <OPERATORS>
FF_combinations = ['', 'Fo', 'C', 'G']
OPERATORS = [Operator("Fa and " + who + " cross the river",
                      lambda s, obj=who: s.can_move(obj),
                      # The default value construct is needed
                      # here to capture the values of p&q separately
                      # in each iteration of the list comp. iteration.
                      lambda s, obj=who: s.move(obj))
             for who in FF_combinations]
# </OPERATORS>

# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>
