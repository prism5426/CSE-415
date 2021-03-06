'''backgammon.py
partner 1 firstname and lastname: Yijie Li
partner 1 student number: 1810605
partner 1 uwnetid: yijiel2

partner 2 firstname and lastname: Junqi Ye
partner 2 student number: 1833403
partner 2 uwnetid: jy98
Assignment 3, part1, in CSE 415, Winter 2021.

This file contains deterministic backgammon agent.
'''

from game_engine import genmoves
import math

W = 0
R = 1


class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.se_func = None
        self.usePrune = True
        self.stateExplored = 0
        self.cutoff = 0
        self.die1 = 1
        self.die2 = 6
        self.MaxDepth = 3

    # returns a string representing a unique nick name for your agent
    def nickname(self):
        return "Yijie Li:1810605, Junqi Ye: 1833403"

    # If prune==True, changes the search algorithm from minimax
    # to Alpha-Beta Pruning
    def useAlphaBetaPruning(self, prune=False):
        self.usePrune = prune
        self.stateExplored = 0
        self.cutoff = 0

    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        return self.stateExplored, self.cutoff

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. If maxply==-1,
    # no limit is set
    def setMaxPly(self, maxply=-1):
        self.MaxDepth = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        self.se_func = func

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move
    def move(self, state, die1=1, die2=6):
        self.die1 = die1
        self.die2 = die2
        # self.setMaxPly(3)
        # update the move_generator to current state/position
        # self.initialize_move_gen_for_state(state, state.whose_move, self.die1, self.die2)
        # get all possible moves in current position
        # pm_list = self.get_all_possible_moves()
        # print(self.usePrune)
        if self.usePrune is True:
            _, best_move = self.alphaBeta(state, self.MaxDepth, -math.inf, math.inf, state.whose_move)
        else:
            _, best_move = self.minimax(state, self.MaxDepth, state.whose_move)
        # print("state explored = " + str(self.stateExplored) + ", number of cutoff = " + str(self.cutoff))
        return best_move

    # Given a state, returns an integer which represents how good the state is
    # for the two players (W and R) -- more positive numbers are good for W
    # while more negative numbers are good for R
    # staticEval function checks index of checker, checker on bar, double checker, blocking opponent etc.
    def staticEval(self, state):
        if self.se_func is None:
            pts = 0
            for index in range(6, 18):
                white_count = 0
                red_count = 0
                for checker in state.pointLists[index]:
                    if checker == W:
                        white_count += 1
                        pts += index
                    elif checker == R:
                        red_count += 1
                        pts -= (23 - index)
                if white_count >= 2:
                    pts += 15
                if red_count >= 2:
                    pts -= 15

            for index in range(0, 6):
                white_count = 0
                red_count = 0
                for checker in state.pointLists[index]:
                    if checker == W:
                        white_count += 1
                        if index == 0 or index == 5:
                            pts += 25
                        pts += 5
                    elif checker == R:
                        red_count += 1
                        if index == 0 or index == 5:
                            pts -= 25
                        pts -= 25
                if white_count >= 2:
                    pts += 15
                if red_count >= 2:
                    pts -= 15

            for index in range(18, 24):
                white_count = 0
                red_count = 0
                for checker in state.pointLists[index]:
                    if checker == W:
                        white_count += 1
                        if index == 18 or index == 23:
                            pts += 25
                        pts += 25
                    elif checker == R:
                        red_count += 1
                        if index == 18 or index == 23:
                            pts -= 25
                        pts -= 5
                if white_count >= 2:
                    pts += 15
                if red_count >= 2:
                    pts -= 15

            for checker in state.bar:
                if checker == W:
                    pts -= 5
                elif checker == R:
                    pts += 5

            pts += len(state.white_off) * 100
            pts -= len(state.red_off) * 100
            return pts

        else:  # update static eval function to func
            return self.se_func(state)

    # returns the best move's staticEval
    def minimax(self, state, depth, maximizing_player):
        if state is None:
            return 0, 'p'
        # check for leaf node or game over
        if depth == 0 or self.gameover(state, maximizing_player):
            self.stateExplored += 1
            return self.staticEval(state), None

        # update the move_generator to current state/position
        self.initialize_move_gen_for_state(state, maximizing_player, self.die1, self.die2)
        # get all possible moves in current position
        pm_list = self.get_all_possible_moves()

        self.stateExplored += 1

        if maximizing_player is W:
            maxEval = -math.inf
            for s in pm_list:
                if len(pm_list) == 1:
                    best_move = s[0]

                eval, _ = self.minimax(s[1], depth - 1, not maximizing_player)
                # maxEval = max(maxEval, eval)
                if eval > maxEval:
                    maxEval = eval
                    best_move = s[0]

            return maxEval, best_move

        else:
            minEval = math.inf
            for s in pm_list:
                if len(pm_list) == 1:
                    best_move = s[0]

                eval, _ = self.minimax(s[1], depth - 1, not maximizing_player)
                # inEval = min(minEval, eval)
                if eval < minEval:
                    minEval = eval
                    best_move = s[0]

            return minEval, best_move

    def alphaBeta(self, state, depth, alpha, beta, maximizing_player):
        if state is None:
            return 0, 'p'
        # check for leaf node or game over
        if depth == 0 or self.gameover(state, maximizing_player):
            self.stateExplored += 1
            return self.staticEval(state), None

        # update the move_generator to current state/position
        self.initialize_move_gen_for_state(state, maximizing_player, self.die1, self.die2)
        # get all possible moves in current position
        pm_list = self.get_all_possible_moves()

        self.stateExplored += 1

        if maximizing_player is W:
            maxEval = -math.inf
            for s in pm_list:
                # only move is best move
                if len(pm_list) == 1:
                    best_move = s[0]

                alpha = max(alpha, maxEval)
                if beta <= alpha:
                    self.cutoff += 1
                    # when branching factor is greater than 2, still need to check remaining branches
                    if len(pm_list) > 2:
                        continue
                    else:
                        break

                eval, _ = self.alphaBeta(s[1], depth - 1, alpha, beta, not maximizing_player)
                if eval > maxEval:
                    maxEval = eval
                    best_move = s[0]

            return maxEval, best_move

        else:
            minEval = math.inf
            for s in pm_list:
                # only move is best move
                if len(pm_list) == 1:
                    best_move = s[0]

                beta = min(beta, minEval)
                if beta <= alpha:
                    self.cutoff += 1
                    if len(pm_list) > 2:
                        # when branching factor is greater than 2, still need to check remaining branches
                        continue
                    else:
                        break

                eval, _ = self.alphaBeta(s[1], depth - 1, alpha, beta, not maximizing_player)
                # inEval = min(minEval, eval)
                if eval < minEval:
                    minEval = eval
                    best_move = s[0]

            return minEval, best_move

    def initialize_move_gen_for_state(self, state, who, die1, die2):
        self.move_generator = self.GenMoveInstance.gen_moves(state, who, die1, die2)

    # gameover if in current state, either player has no checker on the board
    def gameover(self, state, maximizing_player):
        if maximizing_player == 0:  # maximizing player is white
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
                m = next(self.move_generator)  # Gets a (move, state) pair.
                # print("next returns: ",m[0]) # Prints out the move.    For debugging.
                if m[0] != 'p':
                    any_non_pass_moves = True
                    move_list.append(m)  # Add the move to the list.
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            move_list.append(('p', None))
        # move_list know contains (move, state) pair
        return move_list
