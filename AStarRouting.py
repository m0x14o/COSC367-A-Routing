from search import *

class MapGraph(Graph):
	def __init__(self, graph):
		self.graph = graph.splitlines()
		self.wall = []
		self.start_node = []
		self.goal_node = []
		self.possible_move = []
		
		for i in range(len(self.graph)):
			for j in range(len(self.graph[i])):
				if self.graph[i][j] in [' ', 'S', 's', 'G', 'g']:
					self.possible_move.append((i, j))
				if self.graph[i][j] in ['G', 'g']:
					self.goal_node.append((i, j))
				if self.graph[i][j] in ['S', 's']:
					self.start_node.append((i, j))
				if self.graph[i][j] in ['X', 'x']:
					self.wall.append((i, j))

	def starting_nodes(self):
		return self.start_node
		
	def is_goal(self, node):
		if (len(self.goal_node) > 0):
			return (node == self.goal_node[0])
		else:
			return False

	def outgoing_arcs(self, node):
		tail = node
		head = ''
		pos = ''
		cost = 0
		
		N = (tail[0]-1,tail[1])
		E = (tail[0],tail[1]+1)
		S = (tail[0]+1,tail[1])
		W = (tail[0],tail[1]-1)
		NE = (tail[0]-1,tail[1]+1)
		SE = (tail[0]+1,tail[1]+1)
		SW = (tail[0]+1,tail[1]-1)
		NW = (tail[0]-1,tail[1]-1)
		
		if (N in self.possible_move) and (N not in self.wall):
			pos = 'N'; cost = 1; head = (N)
			yield Arc(tail, head, pos, cost)
		if (NE in self.possible_move) and (NE not in self.wall):
			pos = 'NE'; cost = 1; head = (NE)
			yield Arc(tail, head, pos, cost)
		if (E in self.possible_move) and (E not in self.wall):
			pos = 'E'; cost = 1; head = (E)
			yield Arc(tail, head, pos, cost)
		if (SE in self.possible_move) and (SE not in self.wall):
			pos = 'SE'; cost = 1; head = (SE)
			yield Arc(tail, head, pos, cost)
		if (S in self.possible_move) and (S not in self.wall):
			pos = 'S'; cost = 1; head = (S)
			yield Arc(tail, head, pos, cost)
		if (SW in self.possible_move) and (SW not in self.wall):
			pos = 'SW'; cost = 1; head = (SW)
			yield Arc(tail, head, pos, cost)
		if (W in self.possible_move) and (W not in self.wall):
			pos = 'W'; cost = 1; head = (W)
			yield Arc(tail, head, pos, cost)
		if (NW in self.possible_move) and (NW not in self.wall):
			pos = 'NW'; cost = 1; head = (NW)
			yield Arc(tail, head, pos, cost)

	def estimated_cost_to_goal(self, node):
		if len(list(self.goal_node)) != 0:
			goal = self.goal_node[0]
			return max(abs(goal[0] - node[0]), abs(goal[1] - node[1]))
		else:
			return False
	
class LCFSFrontier(Frontier):
	def __init__(self):
		self.container = []
		self.visited = []

	def add(self, path):
		if (path[-1].head not in self.visited):
			self.container.append(path)
		
	def __iter__(self):
		while len(self.container) != 0:
			c = 0
			lowest_cost = 999
			
			for i in range(len(self.container)):
				self.arc_cost = 0
				
				for j in range(len(self.container[i])):
					self.arc_cost += self.container[i][j].cost
					
				self.node = self.container[i][-1].head
				if (self.arc_cost < lowest_cost):
					c = i;
					lowest_cost = self.arc_cost
					
			remove_node = self.container.pop(c)
			
			if (remove_node[-1].head not in self.visited):
				self.visited.append(remove_node[-1].head)
				yield remove_node

class AStarFrontier(MapGraph):
	def __init__(self, graph):
		self.container = []
		self.graph = graph
		self.visited = []
		if len(list(graph.starting_nodes())) != 0:
			self.node = sorted(graph.starting_nodes())[0]
			
	def add(self, path):
		if (path[-1].head not in self.visited):
			self.container.append(path)
		
	def __iter__(self):
		while len(self.container) != 0:
			c = 0
			lowest_cost = 999
			
			for i in range(len(self.container)):
				self.arc_cost = 0
				
				for j in range(len(self.container[i])):
					self.arc_cost += self.container[i][j].cost
					
				self.node = self.container[i][-1].head
				self.huristics = self.graph.estimated_cost_to_goal(self.node)
				self.total_cost = self.huristics + self.arc_cost
				if (self.total_cost < lowest_cost):
					c = i;
					lowest_cost = self.total_cost
					
			remove_node = self.container.pop(c)
			
			if (remove_node[-1].head not in self.visited):
				self.visited.append(remove_node[-1].head)
				yield remove_node

def print_map(map_graph, frontier, solution):
    for i in range(len(map_graph.graph)):
        for j in range(len(map_graph.graph[i])):
            if (solution != None) and ((i, j) in {k.tail for k in solution}) and (map_graph.graph[i][j] not in ['S', 's', 'G', 'g']):
                print('*', end='')
            elif ((i,j) in frontier.visited) and (map_graph.graph[i][j] not in ['S', 's', 'G', 'g']):
                print('.', end='')
            else:
                print(map_graph.graph[i][j], end='')
        print()
