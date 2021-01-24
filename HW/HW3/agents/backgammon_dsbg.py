'''
Name(s):
UW netid(s):
'''

from game_engine import genmoves

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()

    # returns a string representing a unique nick name for your agent
    def nickname(self):
        # TODO: return a string representation of your UW netid(s)
        return ""

    # If prune==True, changes the search algorthm from minimax
    # to Alpha-Beta Pruning
    def useAlphaBetaPruning(self, prune=False):
        # TODO: use the prune flag to indiciate that your search
        # should use Alpha-Beta rather than minimax
        pass

    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        # TODO: return a tuple containig states and cutoff
        return (-1, -1)

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. If maxply==-1,
    # no limit is set
    def setMaxPly(self, maxply=-1):
        # TODO: set the max ply
        pass

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        # TODO: update your staticEval function appropriately
        pass

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move
    def move(self, state, die1=1, die2=6):
        # TODO: return a move for the current state and for the current player.
        # Hint: you can get the current player with state.whose_move
        return None


    # Given a state, returns an integer which represents how good the state is
    # for the two players (W and R) -- more positive numbers are good for W
    # while more negative numbers are good for R
    def staticEval(self, state):
        # TODO: return a number for the given state
        return -1