__author__ = "Katherine Lee"
__email__ = "khl2145"

#======================================================================#
#*#*#*# Optional: Import any allowed libraries you may need here #*#*#*#
#======================================================================#

#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#

import argparse
#imports i added
import time
import resource
from collections import deque
import heapq
import sys

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Robot Path Planning | HW 1 | COMS 4701')
	parser.add_argument('-bfs', action="store_true", default=False , help="Run BFS on the map")
	parser.add_argument('-dfs', action="store_true", default=False, help= "Run DFS on the map")
	parser.add_argument('-astar', action="store_true", default=False, help="Run A* on the map")
	parser.add_argument('-ida', action="store_true", default=False, help="Run Iterative Deepening A* on the map")
	parser.add_argument('-all', action="store_true", default=False, help="Run all the 4 algorithms")
	parser.add_argument('-m', action="store", help="Map filename")

	results = parser.parse_args()

	if results.m=="" or not(results.all or results.astar or results.bfs or results.dfs or results.ida):
		print("Check the parameters : >> python hw1_UNI.py -h")
		exit()

	if results.all:
		results.bfs = results.dfs = results.astar = results.ida = True

	# Reading of map given and all other initializations
	try:
		with open(results.m) as f:
			arena = f.read()
			arena = arena.split("\n")
	except:
		print("Error in reading the arena file.")
		exit()

	# Internal representation
	print(arena)

	print("The arena of size "+ str(len(arena)) + "x" + str(len(arena[0])))
	print("\n".join(arena))

#Sample Functions to Run
# $python3 maze.py -m arena1.txt -bfs
# python3 maze.py -m arena2.txt -dfs -astar -ida
# $python3 maze.py -m arena3.txt -all
class MazeState:
	'''
	This class is an abstraction to store a maze state, which contains the following:
	- Maze configuration (arena)
	- Current Position (position in the the maze that the current state represents)
	- Parent (the state from which the current state came from)
	- Action (the action taken in the parent state, direction moved, which lead to the creation of the current state)
	- Cost (Cost  of the path taken from the start to the current state)
	- Children (a child of the current state is generated by moving in a direction)
	'''
	
	def get_start_index(self):
		'''
		Returns the start index of the maze based on the given arena
		returns (-1, -1) if no start index found
		'''
		#=======================================================================#
		#*#*#*# TODO: Write your code to find the start index of the maze #*#*#*#
		#=======================================================================#
		for row_idx, row in enumerate(self.arena):
			col_idx = row.find('s')
			if col_idx != -1:
				return (row_idx, col_idx)  # Return (row, col)
		return (-1, -1)  # If no start index found

		#=================================#
		#*#*#*# Your code ends here #*#*#*#
		#=================================#

	def get_goal_index(self):
		'''
		Returns the goal index of the maze based on the given arena
		returns (-1, -1) if no goal index found
		'''
		#======================================================================#
		#*#*#*# TODO: Write your code to find the goal index of the maze #*#*#*#
		#======================================================================#
		for row_idx, row in enumerate(self.arena):
			col_idx = row.find('g')
			if col_idx != -1:
				return (row_idx, col_idx)  # Return (row, col)
		return (-1, -1)
		#=================================#
		#*#*#*# Your code ends here #*#*#*#
		#=================================#

	def __init__(self, arena, parent=None, action='Start', cost=0, current_position=(-1,-1)):

		self.arena = arena
		self.parent = parent
		self.action = action
		self.cost = cost
		self.children = []

		self.start = self.get_start_index()
		self.goal = self.get_goal_index()

		if(current_position[0] == -1):
			self.current_position = self.start
		else:
			self.current_position = current_position

	def display(self):
		print("\n".join(self.arena))
	
		#=======================================================================#

	def move_up(self):
		'''
		This function checks if up is a valid move from the given state.
		If up is a valid move, returns a child in which the player has moved up
		Else returns None.
		'''
		
		#=================================================================#
		#*#*#*# TODO: Write your code to move up in the puzzle here #*#*#*#
		#=================================================================#
		# a 'o' represents an obstacle, empty spaces = ' ' 
		up_row = self.current_position[0] - 1
		cur_col = self.current_position[1]
		if up_row >= 0 and self.arena[up_row][cur_col] != 'o':
			new_position = (up_row, cur_col)
			return MazeState(self.arena, parent=self, action='up', current_position=new_position, cost=self.cost + 1)
		return None
		#=================================#
		#*#*#*# Your code ends here #*#*#*#
		#=================================#


	def move_down(self):
		'''
		This function checks if down is a valid move from the given state.
		If down is a valid move, returns a child in which the player has moved down.
		Else returns None.
		'''
		down_row = self.current_position[0] + 1
		cur_col = self.current_position[1]
		if down_row < len(self.arena) and self.arena[down_row][cur_col] != 'o':
			new_position = (down_row, cur_col)
			return MazeState(self.arena, parent=self, action='down', current_position=new_position, cost=self.cost + 1)
		return None
		#===================================================================#
		#*#*#*# TODO: Write your code to move down in the puzzle here #*#*#*#
		#===================================================================#
		
		#=================================#
		#*#*#*# Your code ends here #*#*#*#
		#=================================#

	def move_left(self):
		'''
		This function checks if left is a valid move from the given state.
		If left is a valid move, returns a child in which the player has moved left.
		Else returns None.
		'''
		#===================================================================#
		#*#*#*# TODO: Write your code to move left in the puzzle here #*#*#*#
		#===================================================================#
		cur_row = self.current_position[0]
		left_col = self.current_position[1] - 1
		if left_col >= 0 and self.arena[cur_row][left_col] != 'o':
			new_position = (cur_row, left_col)
			return MazeState(self.arena, parent=self, action='left', current_position=new_position, cost=self.cost + 1)
		return None

		#=================================#
		#*#*#*# Your code ends here #*#*#*#
		#=================================#


	def move_right(self):
		'''
		This function checks if left is a valid move from the given state.
		If left is a valid move, returns a child in which the player has moved left.
		Else returns None.
		'''
		
		#====================================================================#
		#*#*#*# TODO: Write your code to move right in the puzzle here #*#*#*#
		#====================================================================#
		cur_row = self.current_position[0]
		right_col = self.current_position[1] + 1
		if right_col < len(self.arena[0]) and self.arena[cur_row][right_col] != 'o':
			new_position = (cur_row, right_col)
			return MazeState(self.arena, parent=self, action='right', current_position=new_position, cost=self.cost + 1)
		return None
		#=================================#
		#*#*#*# Your code ends here #*#*#*#
		#=================================#

	def expand(self):
		""" 
		Generate the child nodes of this node 
		"""
		
		if(len(self.children) != 0):
			return self.children

		# Do not change the order in this function, since the grading script assumes this order of expansion when checking
		children = [self.move_up(), self.move_right(), self.move_down(), self.move_left()]

		self.children = [state for state in children if state is not None]
		return self.children
		
	def __hash__(self):
		'''
		Maze states hashed based on cost. 
		This function may be modified if required.
		'''
		#============================================================================================#
		#*#*#*# Optional: May be modified if your algorithm requires a different hash function #*#*#*#
		#============================================================================================#
		
		return self.cost
		
		#=================================#
		#*#*#*# Your code ends here #*#*#*#
		#=================================#
		
	def __eq__(self, other):
		'''
		Maze states are defined as equal if they have the same dimensions and the same current position. 
		This function may be modified if required.
		'''
		
		#=============================================================================================#
		#*#*#*# Optional: May be modified if your algorithm requires a different equality check #*#*#*#
		#=============================================================================================#
		
		m1 = self.arena
		m2 = other.arena

		if(len(m1) != len(m2)):
			return False

		for i in range(0, len(m1)):
			if(not (m1[i] == m2[i])):
				return False
				
		return self.current_position == other.current_position
		
		#=================================#
		#*#*#*# Your code ends here #*#*#*#
		#=================================#
		
	#=====================================================================================#
	#*#*#*# Optional: Write any other functions you may need in the MazeState Class #*#*#*#
	#=====================================================================================#
		
	#=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#



#================================================================================#
#*#*#*# Optional: You may write helper functions in this space if required #*#*#*#
#================================================================================#

	def __lt__(self, other):
		'''
		Compares two states based on the sum of the cost and heuristic.
		'''
		return (self.cost + self.heuristic()) < (other.cost + other.heuristic())

	def heuristic(self):
		'''
		Returns the Manhattan distance between the current position and the goal.
		'''

		return abs(self.current_position[0] - self.goal[0]) + abs(self.current_position[1] - self.goal[1])

#=================================#
#*#*#*# Your code ends here #*#*#*#
#=================================#


'''
This function runs Breadth First Search on the input arena (which is a list of str)
Returns a ([], int) tuple where the [] represents the solved arena as a list of str and the int represents the cost of the solution
'''
def bfs(arena):
    # Start time and memory measurement
    start_time = time.time()
    start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    start_state = MazeState(arena)
    queue = deque([start_state])
    visited = set()  # Track only positions
    visited.add(start_state.current_position)

    nodes_expanded = 0  # Number of nodes expanded
    max_nodes_stored = len(queue) + len(visited)  # Initial max nodes stored (queue + visited)
    max_search_depth = 0  # Track max depth

    # LOG: Starting BFS
    print("Starting BFS...")

    while queue:
        current_state = queue.popleft()
        nodes_expanded += 1

        # LOG: Expanding node details
        print(f"Expanding node at position {current_state.current_position}, cost: {current_state.cost}")

        # Check if the goal is reached
        if current_state.current_position == current_state.goal:
            # End time and memory measurement
            end_time = time.time()
            end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

            total_time = end_time - start_time
            total_memory = (end_memory - start_memory) / 1024  # Convert to kB

            # LOG: Goal found and nodes expanded
            print(f"Goal found at {current_state.current_position}, cost: {current_state.cost}, nodes expanded: {nodes_expanded}")

            # Reconstruct path
            path = []
            cost = current_state.cost
            while current_state:
                path.append(current_state.current_position)
                current_state = current_state.parent
            path.reverse()

            # Mark path in arena
            solved_arena = [list(row) for row in arena]
            for (row, col) in path:
                if solved_arena[row][col] not in ['s', 'g']:
                    solved_arena[row][col] = '*'
            solved_arena = ["".join(row) for row in solved_arena]

            # LOG: BFS results summary
            print(f"BFS completed. Cost: {cost}, Nodes Expanded: {nodes_expanded}, Max Nodes Stored: {max_nodes_stored}, Max Search Depth: {max_search_depth}")

            return (solved_arena, cost, nodes_expanded, max_nodes_stored,
                    max_search_depth, total_time, total_memory)

        # Expand in URDL order
        for move_func in [current_state.move_up, current_state.move_right,
                          current_state.move_down, current_state.move_left]:
            child = move_func()
            if child and child.current_position not in visited:
                visited.add(child.current_position) 
                queue.append(child)
                max_search_depth = max(max_search_depth, child.cost)

                # LOG: Child added to queue
                print(f"Added child at position {child.current_position}, cost: {child.cost}")

        # Update max_nodes_stored based on the size of the queue and visited set
        max_nodes_stored = max(max_nodes_stored, len(queue) + len(visited))

        # LOG: Queue size and visited set
        print(f"Queue size: {len(queue)}, Visited nodes: {len(visited)}")

    # If no solution is found
    end_time = time.time()
    end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    total_time = end_time - start_time
    total_memory = (end_memory - start_memory) / 1024  

    # LOG: No solution found
    print(f"No solution found. Nodes Expanded: {nodes_expanded}, Max Nodes Stored: {max_nodes_stored}, Max Search Depth: {max_search_depth}")

    return ([], -1, nodes_expanded, max_nodes_stored,
            max_search_depth, total_time, total_memory)
#=================================#
	#*#*#*# Your code ends here #*#*#*#
	#=================================#

'''
This function runs Depth First Search on the input arena (which is a list of str)
Returns a ([], int) tuple where the [] represents the solved arena as a list of str and the int represents the cost of the solution
'''
def dfs(arena):
    """
    This function runs Depth First Search on the input arena.
    Returns a ([], int) tuple where the [] represents the solved arena as a list of str
    and the int represents the cost of the solution.
    """
    import time
    import resource

    # Start time and memory measurement
    start_time = time.time()
    start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    start_state = MazeState(arena)
    stack = [start_state]
    visited = set()  # Use this to track visited nodes
    visited.add(start_state)

    nodes_expanded = 0  # Number of nodes expanded
    max_nodes_stored = len(stack) + len(visited)  # Initial nodes in memory
    max_search_depth = 0  # Maximum depth achieved

    while stack:
        current_state = stack.pop()
        nodes_expanded += 1  # Increment when a node is expanded

        # Check if the goal is reached
        if current_state.current_position == current_state.goal:
            # End time and memory measurement
            end_time = time.time()
            end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

            total_time = end_time - start_time
            total_memory = (end_memory - start_memory) / 1024  # Convert to kB

            # Reconstruct the path
            path = []
            cost = current_state.cost
            while current_state:
                path.append(current_state.current_position)
                current_state = current_state.parent
            path.reverse()

            # Modify the arena to mark the path with '*'
            solved_arena = [list(row) for row in arena]
            for (row, col) in path:
                if solved_arena[row][col] not in ['s', 'g']:
                    solved_arena[row][col] = '*'
            solved_arena = ["".join(row) for row in solved_arena]

            return (solved_arena, cost, nodes_expanded, max_nodes_stored,
                    max_search_depth, total_time, total_memory)

        # Reverse URDL order to maintain proper DFS order
        moves = [current_state.move_left, current_state.move_down,
                 current_state.move_right, current_state.move_up]

        for move_func in moves:
            child = move_func()
            if child and child.current_position not in visited:
                visited.add(child.current_position)  # Mark the child node as visited
                stack.append(child)
                max_search_depth = max(max_search_depth, child.cost)

        # Update max_nodes_stored
        total_nodes_stored = len(stack) + len(visited)
        max_nodes_stored = max(max_nodes_stored, total_nodes_stored)

    # If no solution is found
    end_time = time.time()
    end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    total_time = end_time - start_time
    total_memory = (end_memory - start_memory) / 1024  # Convert to kB

    return ([], -1, nodes_expanded, max_nodes_stored,
            max_search_depth, total_time, total_memory)

'''
This function runs A* Search on the input arena (which is a list of str)
Returns a ([], int) tuple where the [] represents the solved arena as a list of str and the int represents the cost of the solution
'''
def astar(arena):
    """
    This function runs A* Search on the input arena.
    Returns a ([], int) tuple where the [] represents the solved arena as a list of str
    and the int represents the cost of the solution.
    """
    import time
    import resource
    import heapq

    # Start time and memory measurement
    start_time = time.time()
    start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    start_state = MazeState(arena)
    open_set = []
    heapq.heappush(open_set, (start_state.cost + start_state.heuristic(), start_state))
    visited = {}

    nodes_expanded = 0
    max_nodes_stored = len(open_set) + len(visited)
    max_search_depth = 0

    while open_set:
        _, current_state = heapq.heappop(open_set)
        nodes_expanded += 1

        # Check if the goal is reached
        if current_state.current_position == current_state.goal:
            # End time and memory measurement
            end_time = time.time()
            end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

            total_time = end_time - start_time
            total_memory = (end_memory - start_memory) / 1024  # Convert to kB

            # Reconstruct the path
            path = []
            cost = current_state.cost
            while current_state:
                path.append(current_state.current_position)
                current_state = current_state.parent
            path.reverse()

            # Modify the arena to mark the path with '*'
            solved_arena = [list(row) for row in arena]
            for (row, col) in path:
                if solved_arena[row][col] not in ['s', 'g']:
                    solved_arena[row][col] = '*'
            solved_arena = ["".join(row) for row in solved_arena]

            return (solved_arena, cost, nodes_expanded, max_nodes_stored,
                    max_search_depth, total_time, total_memory)

        visited[current_state.current_position] = current_state.cost

        # URDL order
        for move_func in [current_state.move_up, current_state.move_right,
                          current_state.move_down, current_state.move_left]:
            child = move_func()
            if child:
                child_pos = child.current_position
                child_cost = child.cost

                if child_pos not in visited or visited[child_pos] > child_cost:
                    heapq.heappush(open_set, (child.cost + child.heuristic(), child))
                    visited[child_pos] = child_cost
                    max_search_depth = max(max_search_depth, child.cost)

        # Update max_nodes_stored
        total_nodes_stored = len(open_set) + len(visited)
        max_nodes_stored = max(max_nodes_stored, total_nodes_stored)

    # If no solution is found
    end_time = time.time()
    end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    total_time = end_time - start_time
    total_memory = (end_memory - start_memory) / 1024  # Convert to kB

    return ([], -1, nodes_expanded, max_nodes_stored,
            max_search_depth, total_time, total_memory)
	
'''
This function runs Iterative Deepening A* Search on the input arena (which is a list of str)
Returns a ([], int) tuple where the [] represents the solved arena as a list of str and the int represents the cost of the solution
'''
def ida(arena):
    """
    This function runs Iterative Deepening A* Search on the input arena.
    Returns a ([], int) tuple where the [] represents the solved arena as a list of str
    and the int represents the cost of the solution.
    """
    import time
    import resource

    # Start time and memory measurement
    start_time = time.time()
    start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    start_state = MazeState(arena)

    threshold = start_state.heuristic()
    nodes_expanded = 0
    max_nodes_stored = 0
    max_search_depth = 0

    while True:
        temp = float('inf')
        found, t, nodes, max_nodes, max_depth, path = dfs_ida(start_state, 0, threshold, set())

        nodes_expanded += nodes
        max_nodes_stored = max(max_nodes_stored, max_nodes)
        max_search_depth = max(max_search_depth, max_depth)

        if found:
            # End time and memory measurement
            end_time = time.time()
            end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

            total_time = end_time - start_time
            total_memory = (end_memory - start_memory) / 1024  # Convert to kB

            # Modify the arena to mark the path with '*'
            solved_arena = [list(row) for row in arena]
            for (row, col) in path:
                if solved_arena[row][col] not in ['s', 'g']:
                    solved_arena[row][col] = '*'
            solved_arena = ["".join(row) for row in solved_arena]

            return (solved_arena, t, nodes_expanded, max_nodes_stored,
                    max_search_depth, total_time, total_memory)
        if t == float('inf'):
            # No solution
            return ([], -1, nodes_expanded, max_nodes_stored,
                    max_search_depth, 0, 0)
        threshold = t

def dfs_ida(node, g, threshold, visited):
    f = g + node.heuristic()
    if f > threshold:
        return False, f, 0, len(visited), g, []
    if node.current_position == node.goal:
        return True, g, 1, len(visited), g, [node.current_position]
    min_threshold = float('inf')
    nodes_expanded = 1
    max_nodes_stored = len(visited)
    max_search_depth = g

    visited.add(node.current_position)

    # URDL order
    for move_func in [node.move_up, node.move_right, node.move_down, node.move_left]:
        child = move_func()
        if child and child.current_position not in visited:
            found, t, nodes, max_nodes, depth, path = dfs_ida(child, g + 1, threshold, visited)
            nodes_expanded += nodes
            max_nodes_stored = max(max_nodes_stored, max_nodes)
            max_search_depth = max(max_search_depth, depth)
            if found:
                return True, t, nodes_expanded, max_nodes_stored, max_search_depth, [node.current_position] + path
            if t < min_threshold:
                min_threshold = t

    visited.remove(node.current_position)
    return False, min_threshold, nodes_expanded, max_nodes_stored, max_search_depth, []
if __name__ == "__main__":
	if results.bfs:
		print("\nBFS algorithm called")
		print("\nBFS algorithm called")
		bfs_arena, bfs_cost, bfs_nodes_expanded, bfs_max_nodes_stored, bfs_max_search_depth, bfs_time, bfs_ram = bfs(arena)
		#print("\n".join(bfs_arena))
		print("\n".join([str(pos) for pos in bfs_arena]))
		print("BFS:")
		print("Cost: " + str(bfs_cost))
		print("Nodes Expanded: " + str(bfs_nodes_expanded))
		print("Max Nodes Stored: " + str(bfs_max_nodes_stored))
		print("Max Search Depth: " + str(bfs_max_search_depth))
		print("Time: " + str(bfs_time) + "s")
		print("RAM Usage: " + str(bfs_ram) + "kB\n")

		maze_state = MazeState(arena)
		# Print the start and goal indices, 0 indexes
		start_index = maze_state.get_start_index()
		goal_index = maze_state.get_goal_index()

		print(f"Start index: {start_index}")  # Prints the start coordinates
		print(f"Goal index: {goal_index}")    # Prints the goal coordinates


	if results.dfs:
		print("\nDFS algorithm called")
		dfs_arena, dfs_cost, dfs_nodes_expanded, dfs_max_nodes_stored, dfs_max_search_depth, dfs_time, dfs_ram = dfs(arena)
		print("\n".join(dfs_arena))
		print("DFS:")
		print("Cost: " + str(dfs_cost))
		print("Nodes Expanded: " + str(dfs_nodes_expanded))
		print("Max Nodes Stored: " + str(dfs_max_nodes_stored))
		print("Max Search Depth: " + str(dfs_max_search_depth))
		print("Time: " + str(dfs_time) + "s")
		print("RAM Usage: " + str(dfs_ram) + "kB\n")

	if results.astar:
		print("\nA* algorithm called")
		astar_arena, astar_cost, astar_nodes_expanded, astar_max_nodes_stored, astar_max_search_depth, astar_time, astar_ram = astar(arena)
		print("\n".join(astar_arena))
		print("A*:")
		print("Cost: " + str(astar_cost))
		print("Nodes Expanded: " + str(astar_nodes_expanded))
		print("Max Nodes Stored: " + str(astar_max_nodes_stored))
		print("Max Search Depth: " + str(astar_max_search_depth))
		print("Time: " + str(astar_time) + "s")
		print("RAM Usage: " + str(astar_ram) + "kB\n")
	
	if results.ida:
		print("\nIterative Deepening A* algorithm called")
		ida_arena, ida_cost, ida_nodes_expanded, ida_max_nodes_stored, ida_max_search_depth, ida_time, ida_ram = ida(arena)
		print("\n".join(ida_arena))
		print("Iterative Deepening A*:")
		print("Cost: " + str(ida_cost))
		print("Nodes Expanded: " + str(ida_nodes_expanded))
		print("Max Nodes Stored: " + str(ida_max_nodes_stored))
		print("Max Search Depth: " + str(ida_max_search_depth))
		print("Time: " + str(ida_time) + "s")
		print("RAM Usage: " + str(ida_ram) + "kB\n")

