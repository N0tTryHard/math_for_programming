import numpy as np
import heapq
import matplotlib.pyplot as plt

# Создаем лабиринт в виде двумерной матрицы
maze = np.array([
    [0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
])

# Определяем стартовую и целевую точки
start = (0, 0)
goal = (4, 4)


# Функция эвристики (Манхэттенское расстояние)
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


# Алгоритм A*
def astar(maze, start, goal):
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_cell = (current[0] + dx, current[1] + dy)
            if next_cell[0] < 0 or next_cell[0] >= maze.shape[0] or next_cell[1] < 0 or next_cell[1] >= maze.shape[1]:
                continue
            if maze[next_cell[0], next_cell[1]] != 0:
                continue

            new_cost = cost_so_far[current] + 1
            if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                cost_so_far[next_cell] = new_cost
                priority = new_cost + heuristic(goal, next_cell)
                heapq.heappush(frontier, (priority, next_cell))
                came_from[next_cell] = current

    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path


# Находим путь
path = astar(maze, start, goal)
print("Path found:", path)


# Симуляция движения
def simulate_movement(maze, path):
    real_path = []
    current = start
    for step in path:
        if maze[step[0], step[1]] == 0:
            real_path.append(step)
            current = step
        else:
            break
    return real_path


# Симулируем движение
real_path = simulate_movement(maze, path)
print("Real path:", real_path)


# Анализ производительности
def analyze_performance(path, real_path):
    path_length = len(path)
    real_path_length = len(real_path)
    deviation = abs(path_length - real_path_length)
    efficiency = (real_path_length / path_length) * 100 if path_length > 0 else 0
    return path_length, real_path_length, deviation, efficiency


path_length, real_path_length, deviation, efficiency = analyze_performance(path, real_path)
print(f"Path Length: {path_length}")
print(f"Real Path Length: {real_path_length}")
print(f"Deviation: {deviation}")
print(f"Efficiency: {efficiency:.2f}%")

# Выводы
print("Conclusion:")
print(f"The A* algorithm found a path of length {path_length}.")
print(f"The real path length was {real_path_length}.")
print(f"The deviation between the model and real path was {deviation}.")
print(f"The efficiency of the algorithm was {efficiency:.2f}%.")


# Визуализация лабиринта и пути
def visualize_maze(maze, path, real_path, start, goal):
    plt.figure(figsize=(10, 5))
    plt.imshow(maze, cmap='binary', interpolation='nearest')

    # Рисуем стартовую и целевую точки
    plt.plot(start[1], start[0], 'go', markersize=10)  # Стартовая точка (зеленый)
    plt.plot(goal[1], goal[0], 'ro', markersize=10)  # Целевая точка (красный)

    # Рисуем путь
    if path:
        path_x, path_y = zip(*path)
        plt.plot(path_y, path_x, 'b-', linewidth=2)  # Путь (синий)

    # Рисуем реальный путь
    if real_path:
        real_path_x, real_path_y = zip(*real_path)
        plt.plot(real_path_y, real_path_x, 'y-', linewidth=2)  # Реальный путь (желтый)

    plt.xticks([])
    plt.yticks([])
    plt.title('Maze with A* Path')
    plt.show()


# Визуализируем лабиринт и путь
visualize_maze(maze, path, real_path, start, goal)
