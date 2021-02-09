#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os
from search import * #for search engines
from snowman import SnowmanState, Direction, snowman_goal_state #for snowball specific classes
from test_problems import PROBLEMS #20 test problems

# my imports
import math
import numpy as np
import time
# (approx. 10 lines)
def heur_manhattan_distance(state):
#IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a snowman state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #We want an admissible heuristic, which is an optimistic heuristic.
    #It must never overestimate the cost to get from the current state to the goal.
    #The sum of the Manhattan distances between each snowball that has yet to be stored and the storage point is such a heuristic.
    #When calculating distances, assume there are no obstacles on the grid.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.

    m_distance = 0
    goal = state.destination
    for snowball in state.snowballs:
        if(snowball != goal):
            m_distance += abs(snowball[0] - goal[0]) + abs(snowball[1] - goal[1])

    return m_distance

#HEURISTICS 
def trivial_heuristic(state):
  '''trivial admissible snowball heuristic'''
  '''INPUT: a snowball state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''   
  return len(state.snowballs)

# (approx... its up to me...)
def heur_alternate(state):
#IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    #heur_manhattan_distance has flaws.
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.

    PENALTY = 1000000 # penalization weight
    
    # IDEA: since creating a new heuristic based on rewarding the best past results in worse runtimes, the approach below will penalize bad moves instead
    # This includes: deadlocks on edges, corners, and times when the order of snowballs is disrupted on the goal 'b' -> 'm' -> 's'

    # following are indicators to see if the goal is on an edge
    # otherwise we want to avoid edges to prevent deadlocks
    left_edge = False
    right_edge = False
    top_edge = False
    bottom_edge = False

    boardX = state.width
    boardY = state.height

    robot = state.robot
    goal = state.destination
    obstacles = state.obstacles

    cost = [] # find the cost representing the closes snowball to the robot (no need to accumilate all costs)

    # loop through each existing snowball for the deadlock states
 
    for snowball in state.snowballs:
        cost.append(abs(robot[0] - snowball[0]) + abs(robot[1] - snowball[1]))

        # snowball[0] == goal[0] somehow works! 
        if snowball[0] == goal[0]:
            continue
        
        if snowball[0] == boardX - 1:
            right_edge = True
        if snowball[0] == 0:
            left_edge = True
        if snowball[1] == 0:
            top_edge = True
        if snowball[1] == boardY - 1:
            bottom_edge = True

        # corner checks
        '''
        if not right_edge and not top_edge:
            if snowball[0] == boardX - 1 and snowball[1] == 0:
                return PENALTY

        elif not right_edge and not bottom_edge:
            if snowball[0] == boardX - 1 and snowball[1] == boardY - 1:
                return PENALTY

        elif not left_edge and not top_edge:
            if snowball[0] == 0 and snowball[1] == 0:
                return PENALTY

        elif not left_edge and not bottom_edge:
            if snowball[0] == 0 and snowball[1] == boardY - 1:
                return PENALTY
        '''
        # check against obstacles
        # top right
        if ((snowball[0] + 1, snowball[1]) or right_edge) in obstacles and ((snowball[0], snowball[1] + 1) in obstacles or top_edge) and goal[0] != snowball[0]:
            return PENALTY
        # top left
        if ((snowball[0] - 1, snowball[1]) or left_edge) in obstacles and ((snowball[0], snowball[1] + 1) in obstacles or top_edge) and goal[0] != snowball[0]:
            return PENALTY
        # bottom right
        if ((snowball[0], snowball[1] + 1) or bottom_edge) in obstacles and ((snowball[0] + 1, snowball[1]) in obstacles or right_edge) and goal[1] != snowball[1]:
            return PENALTY
        # bottom left
        if ((snowball[0], snowball[1] + 1) or bottom_edge) in obstacles and ((snowball[0] - 1, snowball[1]) in obstacles or left_edge) and goal[1] != snowball[1]:
            return PENALTY
        # edge checks
        if right_edge and goal[0] != snowball[0]:
            return PENALTY

        elif bottom_edge and goal[1] != snowball[1]:
            return PENALTY

        elif left_edge and goal[0] != snowball[0]:
            return PENALTY

        elif top_edge and goal[1] != snowball[1]:
            return PENALTY
    
    mini = min(cost)
    return mini + heur_manhattan_distance(state)

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

# (approx. 1 line)
def fval_function(sN, weight):
#IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
  
    #Many searches will explore nodes (or states) that are ordered by their f-value.
    #For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    #You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    #The function must return a numeric f-value.
    #The value will determine your state's position on the Frontier list during a 'custom' search.
    #You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + sN.hval*weight

# (approx. 20 lines)
def anytime_weighted_astar(initial_state, heur_fn, weight=1.0, timebound = 5):
#IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    # initialize searching engine from the given API
    start = os.times()[0]
    fval_fct = (lambda sN : fval_function(sN, weight))
    engine = SearchEngine('custom', 'full')
    engine.init_search(initial_state, snowman_goal_state, heur_fn, fval_fct)

    elapsed = 0
    costbound = (float('inf'), float('inf'), float('inf'))
    goal_state = False

    while elapsed < timebound - 0.5:
        # time remaining for the search will be timebound - elapsed   
        found_state = engine.search(timebound - elapsed, costbound)
        
        if found_state: 
            # for costbound we only consider the gvalues
            end = os.times()[0]
            elapsed = end - start
            costbound = (found_state.gval, float('inf'), float('inf'))
            # update the next best goal state
            goal_state = found_state 
        else:
            return goal_state

    return goal_state

# (approx. 20 lines) implement before anytime_weighted_astar
def anytime_gbfs(initial_state, heur_fn, timebound = 5):
#IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    # initialize searching engine from the given API
    engine = SearchEngine('best_first', 'full')
    engine.init_search(initial_state, snowman_goal_state, heur_fn)
    
    # The algorithm returns either when we have expanded all non-pruned nodes OR when it runs out of time.
    # create a costbound variable to allow for pruning (begin with inf cost so any gval is better at first)
    costbound = (float('inf'), float('inf'), float('inf'))
    goal_state = False
    # measure time elapsed so far
    elapsed = 0

    start = time.time()
    while elapsed < timebound - 3:
        # time remaining for the search will be timebound - elapsed      
        found_state = engine.search(timebound - elapsed, costbound)
        end = time.time()
        elapsed = end - start

        if found_state: 
            # for costbound we only consider the gvalues
            costbound = (found_state.gval, float('inf'), float('inf'))
            # update the next best goal state
            goal_state = found_state 
        else:
            return goal_state

    return goal_state
