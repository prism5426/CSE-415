'''
Name(s):
UW netid(s):
'''

from game_engine import genmoves
import math


class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()

    # returns a string representing a unique nick name for your agent
    def nickname(self):
        return "Yijie Li:1810605\nJunqi Ye: 1833403"

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
        self.setMaxPly = maxply

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
        self.die1 = die1
        self.die2 = die2

        # update the move_generator to current state/position
        self.initialize_move_gen_for_state(state, 0, self.die1, self.die2)
        # get all possible moves in current position
        pm_list = self.get_all_possible_moves()



        return None

    # Given a state, returns an integer which represents how good the state is
    # for the two players (W and R) -- more positive numbers are good for W
    # while more negative numbers are good for R
    def staticEval(self, state):
        pts = 0
        for index in range(24):
            for checker in state.pointLists[index]:
                if checker == 'W':
                    pts += index
                elif checker == 'R':
                    pts -= (23 - index)

        return pts

    # returns the best move's staticEval
    def minimax(self, state, depth, maximizing_player):
        if depth == 0 or self.gameover(state, maximizing_player):
            return self.staticEval(state)

        if maximizing_player:
            maxEval = -math.inf

            # update the move_generator to current state/position
            self.initialize_move_gen_for_state(state, maximizing_player, self.die1, self.die2)
            # get all possible moves in current position
            pm_list = self.get_all_possible_moves()

            for s in pm_list:
                eval = self.minimax(s, depth - 1, not maximizing_player)
                maxEval = max(maxEval, eval)
            return maxEval

        else:
            minEval = math.inf

            # update the move_generator to current state/position
            self.initialize_move_gen_for_state(state, maximizing_player, self.die1, self.die2)
            # get all possible moves in current position
            pm_list = self.get_all_possible_moves()

            for s in pm_list:
                eval = self.minimax(s, depth - 1, not maximizing_player)
                minEval = min(minEval, eval)
            return minEval


    def initialize_move_gen_for_state(self, state, who, die1, die2):
        self.move_generator = self.GenMoveInstance.gen_moves(state, who, die1, die2)

    # gameover if in current state, either player has no checker on the board
    def gameover(self, state, maximizing_player):
        if maximizing_player == 0: # maximizing player is white
            return len(state.white_off) == 15
        else:
            return len(state.red_off) == 15

    def get_all_possible_moves(self):
        """Uses the mover to generate all legal moves. Returns an array of move commands"""
        move_list = []
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(self.move_generator)    # Gets a (move, state) pair.
                # print("next returns: ",m[0]) # Prints out the move.    For debugging.
                if m[0] != 'p':
                    any_non_pass_moves = True
                    move_list.append(m[0])    # Add the move to the list.
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            move_list.append('p')
        return move_list
