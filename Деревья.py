from collections import deque

# ------------------- Узел двоичного дерева -------------------
class Node:
    """Базовый класс узла дерева."""
    def __init__(self, key):
        self.left = None   # левый потомок(дочерний узел)
        self.right = None  # правый потомок(дочерний узел)
        self.val = key     # значение узла

# ------------------- Обычное двоичное дерево поиска (BST) -------------------
class BinaryTree:
    """Класс обычного (не сбалансированного) двоичного дерева поиска."""

    def __init__(self):
        """Инициализация: корень дерева изначально пуст."""
        self.root = None

    # ---------- Вставка ----------
    def insert(self, key):
        """Публичный метод вставки ключа в дерево (не балансирует)."""
        if self.root is None:
            # Если дерево пустое, создаём корень
            self.root = Node(key)
        else:
            # Иначе рекурсивно вставляем в подходящее место
            self._insert_recursively(self.root, key)

    def _insert_recursively(self, node, key):
        """
        Рекурсивная вставка.
        Алгоритм: идём влево, если ключ меньше, иначе вправо,
        пока не найдём свободное место.
        """
        if key < node.val:
            # Ключ должен быть в левом поддереве
            if node.left is None:
                node.left = Node(key)   # нашли место
            else:
                self._insert_recursively(node.left, key)
        else:
            # Ключ должен быть в правом поддереве
            if node.right is None:
                node.right = Node(key)
            else:
                self._insert_recursively(node.right, key)

    # ---------- Поиск ----------
    def search(self, key):
        """Поиск узла по значению. Возвращает узел или None."""
        return self._search_recursively(self.root, key)

    def _search_recursively(self, node, key):
        """Рекурсивный поиск с учётом свойств BST."""
        if node is None or node.val == key:
            return node
        if key < node.val:
            return self._search_recursively(node.left, key)
        return self._search_recursively(node.right, key)

    # ---------- Обходы дерева ----------
    # Все три обхода рекурсивно обходят дерево начиная с корня self.root

    def preorder(self):
        """Прямой (префиксный) обход: корень → левое → правое."""
        return self._preorder_recursively(self.root)

    def _preorder_recursively(self, node):
        if not node:
            return []
        return [node.val] + self._preorder_recursively(node.left) + self._preorder_recursively(node.right)

    def inorder(self):
        """Симметричный (инфиксный) обход: левое → корень → правое.
        Для BST даёт отсортированный список значений."""
        return self._inorder_recursively(self.root)

    def _inorder_recursively(self, node):
        if not node:
            return []
        return self._inorder_recursively(node.left) + [node.val] + self._inorder_recursively(node.right)

    def postorder(self):
        """Обратный (постфиксный) обход: левое → правое → корень."""
        return self._postorder_recursively(self.root)

    def _postorder_recursively(self, node):
        if not node:
            return []
        return self._postorder_recursively(node.left) + self._postorder_recursively(node.right) + [node.val]

# ---------- Обход в ширину (BFS) как отдельная функция ----------
def bfs(root):
    """
    Обход в ширину (уровень за уровнем) с использованием очереди.
    Возвращает список значений узлов в порядке BFS.
    """
    if not root:
        return []

    result = []
    queue = deque([root])      # начинаем с корня

    while queue:
        current = queue.popleft()   # извлекаем первый узел из очереди
        result.append(current.val)  # запоминаем его значение

        # Добавляем потомков в очередь (слева направо)
        if current.left:
            queue.append(current.left)
        if current.right:
            queue.append(current.right)

    return result

# ------------------- AVL-дерево (самобалансирующееся) -------------------
# Сначала определим узел AVL, у которого добавится высота
class AVLNode(Node):
    """Узел AVL-дерева: наследует left, right, val и добавляет height."""
    def __init__(self, key):
        super().__init__(key)   # вызываем конструктор родителя Node
        self.height = 1         # высота узла (лист имеет высоту 1)


class AVLTree(BinaryTree):
    """
    AVL-дерево – разновидность BST, которая после каждой вставки
    проверяет баланс (разницу высот левого и правого поддеревьев)
    и выполняет повороты для поддержания сбалансированности.
    """

    # Переопределяем метод вставки, так как нужна балансировка
    def insert(self, key):
        """Вставка ключа с последующей балансировкой AVL."""
        self.root = self._insert_avl(self.root, key)

    def _insert_avl(self, node, key):
        """
        Рекурсивная вставка по правилам BST + обновление высот + балансировка.
        Возвращает (возможно новый) корень поддерева после балансировки.
        """
        # 1. Обычная BST-вставка
        if not node:
            return AVLNode(key)          # создаём новый AVL-узел

        if key < node.val:
            node.left = self._insert_avl(node.left, key)
        else:
            node.right = self._insert_avl(node.right, key)

        # 2. Обновление высоты текущего узла
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))

        # 3. Получение фактора баланса (разность высот левого и правого)
        balance = self._get_balance(node)

        # 4. Балансировка (4 случая)

        # Случай LL: левое поддерево тяжелее, и новый ключ в левом поддереве левого потомка
        if balance > 1 and key < node.left.val:
            return self._right_rotate(node)

        # Случай RR: правое поддерево тяжелее, и новый ключ в правом поддереве правого потомка
        if balance < -1 and key > node.right.val:
            return self._left_rotate(node)

        # Случай LR: левое тяжелее, но ключ в правом поддереве левого потомка
        if balance > 1 and key > node.left.val:
            node.left = self._left_rotate(node.left)   # сначала малый левый поворот
            return self._right_rotate(node)            # затем большой правый

        # Случай RL: правое тяжелее, но ключ в левом поддереве правого потомка
        if balance < -1 and key < node.right.val:
            node.right = self._right_rotate(node.right) # сначала малый правый поворот
            return self._left_rotate(node)              # затем большой левый

        # Баланс не нарушен – возвращаем узел как есть
        return node

    # ---------- Вспомогательные методы для AVL ----------

    def _get_height(self, node):
        """Безопасное получение высоты узла (для None возвращаем 0)."""
        return node.height if node else 0

    def _get_balance(self, node):
        """Фактор баланса: высота левого минус высота правого."""
        return self._get_height(node.left) - self._get_height(node.right) if node else 0

    # ---------- Повороты ----------

    def _left_rotate(self, z):
        """
        Левый поворот вокруг узла z.
        Используется при правой тяжести (balance < -1).
        Возвращает новый корень поддерева после поворота.
        """
        y = z.right
        T2 = y.left

        # Выполняем поворот
        y.left = z
        z.right = T2

        # Обновляем высоты (сначала у z, затем у y)
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y   # y становится новым корнем

    def _right_rotate(self, z):
        """
        Правый поворот вокруг узла z.
        Используется при левой тяжести (balance > 1).
        Возвращает новый корень поддерева.
        """
        y = z.left
        T3 = y.right

        # Поворот
        y.right = z
        z.left = T3

        # Обновление высот
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))

        return y

# ------------------- Пример использования -------------------
# Создаём AVL-дерево и вставляем последовательность ключей
avl_tree = AVLTree()
keys = [10, 20, 30, 40, 50, 25]   # эта последовательность вызовет несколько поворотов

print("\n--- Построение AVL-дерева ---")
for key in keys:
    avl_tree.insert(key)
    print(f"Вставлен {key}, текущий корень = {avl_tree.root.val}")

# Вывод различных обходов
print("\n--- Обходы полученного дерева ---")
print("Обход в ширину (BFS - Breadth-First Search):", bfs(avl_tree.root))
print("Прямой обход (preorder):", avl_tree.preorder())
print("Симметричный обход (inorder):", avl_tree.inorder())
print("Обратный обход (postorder):", avl_tree.postorder())

# Небольшое пояснение: inorder для AVL всегда даёт отсортированную последовательность,
# так как дерево остаётся корректным BST.
print("\nПримечание: симметричный обход выводит значения в порядке возрастания – это свойство любого BST, включая AVL.")