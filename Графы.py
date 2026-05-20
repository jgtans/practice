from collections import deque

class DirectedGraph:
    def __init__(self):
        # Инициализация пустого графа
        self.graph = {}

    def add_vertex(self, vertex):
        # Добавление вершины в граф
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, from_vertex, to_vertex):
        # Добавление направленного ребра
        if from_vertex not in self.graph:
            self.add_vertex(from_vertex)
        if to_vertex not in self.graph:
            self.add_vertex(to_vertex)
        self.graph[from_vertex].append(to_vertex)

    def __str__(self):
        return str(self.graph)

# Тестирование
dg = DirectedGraph()
dg.add_edge('A', 'B')
dg.add_edge('A', 'C')
dg.add_edge('B', 'D')
dg.add_edge('C', 'D')
print("Ориентированный граф:", dg)

def bfs(graph, start):
    visited = set()
    queue = deque([start])
    result = []

    while queue:
        vertex = queue.popleft()
        if vertex not in visited:
            visited.add(vertex)
            result.append(vertex)
            # Добавляем соседей в очередь
            for neighbor in graph.graph[vertex]:
                if neighbor not in visited:
                    queue.append(neighbor)
    return result

# Пример использования
print("BFS обход:", bfs(dg, 'A'))

class AdjacencyMatrix:
    def __init__(self):
        self.matrix = {}
        self.vertices = []

    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices.append(vertex)
            # Обновляем матрицу
            for row in self.matrix:
                self.matrix[row][vertex] = 0
            self.matrix[vertex] = {v: 0 for v in self.vertices}

    def add_edge(self, from_vertex, to_vertex):
        if from_vertex not in self.matrix:
            self.add_vertex(from_vertex)
        if to_vertex not in self.matrix:
            self.add_vertex(to_vertex)
        self.matrix[from_vertex][to_vertex] = 1

    def __str__(self):
        return str(self.matrix)

# Пример использования
am = AdjacencyMatrix()
am.add_edge('A', 'B')
am.add_edge('A', 'C')
am.add_edge('B', 'D')
print("Матрица смежности:", am)

class AdjacencyList:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, from_vertex, to_vertex):
        if from_vertex not in self.graph:
            self.add_vertex(from_vertex)
        if to_vertex not in self.graph:
            self.add_vertex(to_vertex)
        self.graph[from_vertex].append(to_vertex)

    def __str__(self):
        return str(self.graph)

# Пример использования
al = AdjacencyList()
al.add_edge('A', 'B')
al.add_edge('A', 'C')
al.add_edge('B', 'D')
print("Список смежности:", al)
