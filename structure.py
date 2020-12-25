class Stack:
    """Класс реализующий структуру данных Стек"""
    def __init__(self, name):
        self.items = []
        self.name = name

    def isEmpty(self):
        # Проверка на пустоту
        return len(self.items) == 0

    def push(self, name):
        # Добавляет элемент в конец стека
        element = ElementStack(name)
        self.items.append(element)

    def pop(self):
        # Вынимает элемент из стека
        return self.items.pop()

    def clear(self):
        # Очищает весь стек
        self.items.clear()    


class ElementStack:
    """Класс реализующий элемент стека для нашей работы"""
    def __init__(self, name):
        # Создает элемент двухсвязного списка
        self.data = DoublyLinkedList(name)

    def getName(self):
        # Функция возвращает название двухсвязного списка
        return self.data.name


class Node:
    """Элемент двухсвязного списка"""
    def __init__(self, name, hours):
        # Ссылки на следующий и предыдущий элемент
        self.next = None
        self.prev = None

        # Обязательны данные по задаче
        self.name = name    # Название элемента(предмета)
        self.hours = hours      # Часы


class DoublyLinkedList:
    """Класс реализующий структуру двухсвязного списка"""
    def __init__(self, name):
        self.name = name    # Название двухсвязного списка
        self.head = None    # Стартовый элемент
        self.tail = None    # Последний элемент

    def isEmpty(self):
        # Проверка на пустоту
        return self.head is None and self.tail is None

    def contains(self, name):
        # Проверяем содержится ли элемент
        node = self.head
        
        while node:
            if name == node.name:
                #return True
                return (True, node)
            else:
                node = node.next
        return False

    def push(self, name, hours):
        # Метод добавляет элемент в начало двухсвязного списка
        new_node = Node(name, hours)
        # У нового элемента есть ссылка на следующий, ей даем текущее 
        # значение головы
        new_node.next = self.head

        # Если голова изначально не пустая, то предыдущему элементу 
        # головы, передаем ссылку на новый элемент
        if self.head is not None:
            self.head.prev = new_node
        # Голове присваеваем новый элемент
        self.head = new_node
        self.tail = new_node

    def insertAfter(self, name, hours, prev_node=None):
        # Метод вставляет новый элемент после указанного
        if prev_node is None:
            print('Полученный предыдущий элемент не может быть пустым')
            return

        new_node = Node(name, hours)
        # У нового элемента, ссылке на следующий элемент передаем 
        # значение, которое было у старого элемента на следующий элемент
        new_node.next = prev_node.next
        # Изменяем у предыдущего элемента ссылку на следующий элемент
        prev_node.next = new_node
        # Передаем новому элементу ссылку на предыдущий элемент
        new_node.prev = prev_node
        
        # Изменяем ссылку на предыдущий элемент у следующего элемента, 
        # после добавленного
        if new_node.next is not None:
            new_node.next.prev = new_node
        else:
            self.tail = new_node

    def insertBefore(self, name, hours, next_node=None):
        # Метод вставляет новый элемент до указанного
        if next_node is None:
            print('Полученный предыдущий элемент не может быть пустым')
            return

        new_node = Node(name, hours)
        # У нового элемента, ссылке на предыдущий элемент передаем 
        # значение, которое было у следующего элемента на прошлый элемент
        new_node.prev = next_node.prev
        # Изменяем у следующего элемента ссылку на предыдущий элемент
        next_node.prev = new_node
        # Новому элементу присваеваем ссылку на следующий элемент
        new_node.next = next_node

        # Изменяем ссылку на следующий элемент у предыдущего элемента 
        # после добавленного
        if next_node.prev is not None:
            new_node.prev.next = new_node

    def append(self, name, hours):
        # Метод вставляет элемент в конец двухсвязного списка
        new_node = Node(name, hours)
        # Устанавливаем новому элементу, ссылку на след. элемент None
        new_node.next = None
        # Если голова None, то ссылку на предыдущий элемент делаем None
        if self.head is None:
            new_node.prev = None
            self.head = new_node
            self.tail = new_node
            return

        last = self.head
        # Находим ссылку на следующий элемент, пока она не равна None
        while last.next is not None:
            last = last.next
        # Передаем последнюю ссылку на новый элемент
        last.next = new_node
        # Устанавливаем новому элементу ссылку на старый последний элемент
        new_node.prev = last
        # Присваеваем хвосту значение последнего элемента
        self.tail = new_node
        return

    def delete(self, node):
        # Функция отвечет за удаление элемента из двухсвязного списка
        if self.head is None or node is None:
            return

        if self.head == node:
            self.head = node.next

        if self.tail == node:
            self.tail = node.prev
        # Если есть следующий элемент после удаляемого, то ссылке у следующего 
        # элемента на прошлый элемент, делаем от удаляемого элемента на прошлый
        if node.next is not None:
            node.next.prev = node.prev
        # Если есть прошлый элемент у удаляемого, то ссылке у прошлого элемента 
        # на следующий, даем значение следующего элемента после удаляемого
        if node.prev is not None:
            node.prev.next = node.next

    def printList(self, node):
        print("\nTraversal in forward direction")
        while(node is not None):
            print(node.name)
            last = node
            node = node.next
 
        print("\nTraversal in reverse direction")
        while(last is not None):
            print(last.name)
            last = last.prev