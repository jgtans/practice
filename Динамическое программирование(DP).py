def knapsack_01(W, wt, val):
    n = len(val)
    # dp[i][w] — максимум ценности для первых i предметов и вместимости w
    # Инициализация нулями (базовые случаи: i=0 или w=0 дают 0)
    dp = [[0] * (W + 1) for _ in range(n + 1)]

    # Заполняем таблицу
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            # Вес текущего предмета (индекс i-1, так как i начинается с 1)
            weight_i = wt[i - 1]
            value_i = val[i - 1]

            if weight_i <= w:
                # Вариант 1: берём предмет -> value_i + dp[i-1][w - weight_i]
                # Вариант 2: не берём -> dp[i-1][w]
                dp[i][w] = max(value_i + dp[i - 1][w - weight_i], dp[i - 1][w])
            else:
                # Предмет слишком тяжёлый, только не брать
                dp[i][w] = dp[i - 1][w]

    return dp[n][W]

# Пример использования
val = [10, 500, 150]
wt = [50, 500, 30]
W = 580
print(knapsack_01(W, wt, val))  # 660

def lcs_length(s1, s2):
    m, n = len(s1), len(s2)
    # dp[i][j] – длина LCS для префиксов s1[:i] и s2[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                # Символы совпадают – увеличиваем LCS
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # Иначе берём максимум из двух вариантов (без одного символа)
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    return dp[m][n]

# Пример
print(lcs_length("ABCDGH", "AEDFHR"))  # 3 (A,D,H)
print(lcs_length("AGGTAB", "GXTXAYB"))  # 4 (G,T,A,B)

def count_partitions(n):
    # dp[i][j] – количество разбиений числа i с использованием слагаемых не больше j
    # Инициализация: dp[0][j] = 1 (пустое разбиение числа 0)
    dp = [[0] * (n + 1) for _ in range(n + 1)]

    for j in range(n + 1):
        dp[0][j] = 1  # один способ разбить 0 – не брать ничего

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            # Количество разбиений числа i с максимальным слагаемым j =
            # (разбиения, где максимальное слагаемое < j) +
            # (разбиения, где есть хотя бы одно j)
            dp[i][j] = dp[i][j - 1]
            if j <= i:
                dp[i][j] += dp[i - j][j]

    return dp[n][n]

# Более экономная версия (одномерный массив) для разбиений без ограничения на максимум:
def count_partitions_compact(n):
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            dp[j] += dp[j - i]
    return dp[n]

print(count_partitions(5))  # 7 (5, 4+1, 3+2, 3+1+1, 2+2+1, 2+1+1+1, 1+1+1+1+1)
print(count_partitions_compact(5))  # 7

def floyd_warshall(graph):
    V = len(graph)
    # Копируем исходную матрицу, чтобы не изменять входную
    dist = [row[:] for row in graph]

    # Инициализация: расстояние до самой себя должно быть 0
    for i in range(V):
        dist[i][i] = 0

    # Основной цикл алгоритма: пробуем улучшить пути через промежуточную вершину k
    for k in range(V):
        for i in range(V):
            for j in range(V):
                # Если путь i -> k -> j короче, чем текущий dist[i][j], обновляем
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist

# Пример использования
INF = float('inf')
graph = [
    [0, 3, INF, 7],
    [8, 0, 2, INF],
    [5, INF, 0, 1],
    [2, INF, INF, 0]
]

shortest = floyd_warshall(graph)
print("Кратчайшие расстояния:")
for row in shortest:
    print(row)

# Вывод:
# [0, 3, 5, 6]
# [5, 0, 2, 3]
# [3, 6, 0, 1]
# [2, 5, 7, 0]

    #Полный вывод:
# 660
# 3
# 4
# 7
# 7
# Кратчайшие расстояния:
# [0, 3, 5, 6]
# [5, 0, 2, 3]
# [3, 6, 0, 1]
# [2, 5, 7, 0]


















