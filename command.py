from tkinter import END, messagebox as mb

from plan import Plan, parseXML, delete


# ФУНКЦИИ ОТВЕЧАЮЩИЕ ЗА НАВИГАЦИЮ

def create_plan(widget, sections):
    """Функция создает новый план"""
    text = widget.get()
    if not text:
        mb.showerror('Ошибка', 'Введите название плана')
        return

    sections.delete(0, END)

    widget['state'] = 'disabled'
    # Устанавливаем глобальную переменную чтобы использовать 
    # во всех функциях
    global mainplan
    # Создаем класс нашего плана
    mainplan = Plan(text)   # --> plan.py


def save_plan():
    """Функция отвечает за сохранения плана в xml"""
    try:
        mainplan.createXML()
    except Exception:
        mb.showerror('Ошибка', 'Нет созданного плана')


def download_plan(plan, sections):
    """Функция отвечает за загрузку плана из файла"""
    # Устанавливаем глобальную переменную чтобы использовать 
    # во всех функциях
    global mainplan

    try:
        mainplan = parseXML()   # Получаем план из файла. --> plan.parseXML
    except Exception:
        mb.showerror('Ошибка', 'Нет плана для загрузки')

    plan['state'] = 'normal'

    # Удаляем все значения из листбоксов
    plan.delete(0, END)
    sections.delete(0, END)
    # Вставляем название плана
    plan.insert(0, mainplan.getName())
    
    for section in mainplan.plan.items:
        sections.insert(0, section.data.name)
    
    # Устанавливаем выбранный элемент под индексом 0
    sections.selection_set(0)
    # Передаем действие, что листбокс выбран
    sections.event_generate("<<ListboxSelect>>")


def delete_plan(plan, sections, subjects, hours):
    """Функция отвечает за удаление плана"""
    # Возвращаем активное состояние плану
    plan['state'] = 'normal'
    # Очищаем листбоксы от значений
    plan.delete(0, END)
    sections.delete(0, END)
    subjects.delete(0, END)
    hours.delete(0, END)

    try:
        delete()
    except Exception:
        mb.showerror('Ошибка', 'План для удаления не существует')


# ФУНКЦИИ ОТВЕЧАЮЩИЕ ЗА РАЗДЕЛЫ

def create_section(widget, listbox):
    """Функция отвечает за создание разделов и отображение их в листбоксе"""
    text = widget.get()
    if not text:
        mb.showerror('Ошибка', 'Введите название раздела')
        return
    try:
        # Создаем новый элемент в нашем стеке-массиве
        mainplan.plan.push(text)
    except Exception:
        mb.showerror('Ошибка', 'Сначала создайте план')
        return
    # Добавляем в наш listbox новый элемент для отображения 
    # его в программе
    listbox.insert(0, text)


def delete_section(sections, subjects, hours):
    """Удаляем элемент из стека"""
    try:
        mainplan.plan.pop()
    except Exception:
        mb.showerror('Ошибка', 'Список разделов пуст')
        return

    # Поскольку удалили элемент из стека, не забываем удалить и 
    # из листбокса
    sections.delete(0)

    if sections.size() == 0:
        subjects.delete(0, END)
        hours.delete(0, END)

    # Очищаем все выделения в листбоксе
    sections.selection_clear(0, END)
    # Устанавливаем выбранный элемент под индексом 0
    sections.selection_set(0)
    # Передаем действие, что листбокс выбран
    sections.event_generate("<<ListboxSelect>>")


# ФУНКЦИИ ОТВЕЧАЮЩИЕ ЗА ПРЕДМЕТЫ

def create_subject(subject, hour, sections, subjects, hours, after):
    """Функция отвечает за создание предметов и отображение их в листбоксе"""
    try:
        index = sections.curselection()[0]  # Индекс выбранного элемента в листбоксе
    except Exception:
        mb.showerror('Ошибка', 'Необходимо выбрать раздел для добавления предмета')
        return

    subject = subject.get()     # Получаем значение поля subject
    if not subject:
        mb.showerror('Ошибка', 'Введите название предмета')
        return
    hour = hour.get()   # Получаем значение поля hour
    if not hour:
        mb.showerror('Ошибка', 'Введите колличество часов')
        return
    
    # Находим индекс нужного элемента в листбоксе и двухсвязном списке
    isection = sections.size() - 1 - index

    dll = mainplan.plan.items[isection].data    # dll - doubly linked list. Получаем двухсвязный список
    position = 0    # Индекс выбранного элемента в листбоксе subjects

    # Проверяем пустой ли двухсвязный список, если пустой, push, иначе append
    if dll.isEmpty():
        dll.push(subject, hour)     # --> structure.DoublyLinkedList.push()
        # Добавляем в листбоксы новые элементы
        subjects.insert(0, subject)
        hours.insert(0, hour)
    else:
        if after.get():
            position = subjects.curselection()[0]
            # Если нашли позицию, то находим значение в списке по позиции
            element = subjects.get(position)
            # Проверяем, есть ли искомый элемент в двухсвязном списке, если есть, 
            # то получаем кортеж (True, объект) или False
            node = dll.contains(element)[1]
            # Вызываем функцию, которая вставляет элемент до выбранного нами
            dll.insertAfter(subject, hour, node)    # --> structure.DoublyLinkedList.insertAfter()
            subjects.insert(position, subject)
            hours.insert(position, hour)
        else:
            # Устанавливаем исключение, если получаем позицию элемента, то идем дальше, 
            # иначе добавляем новые элементы в конец двухсвязного списка
            try:
                position = subjects.curselection()[0]
            except Exception:
                # Добавляем в конец двухсвязного списка   
                dll.append(subject, hour)   # --> structure.DoublyLinkedList.append()
                # Т.к на графическом интерфейсе отображается рекурсивно, добавляем 
                # элементы в самое начало
                subjects.insert(0, subject)
                hours.insert(0, hour)
                return

            # Если нашли позицию, то находим значение в списке по позиции
            element = subjects.get(position)
            # Проверяем, есть ли искомый элемент в двухсвязном списке, если есть, 
            # то получаем кортеж (True, объект) или False
            node = dll.contains(element)[1]     # --> structure.DoublyLinkedList.contains()
            # Если элемент равен "голове", то вызываем функцию push, чтобы добавить элемент в голову
            if dll.head == node:
                dll.push(subject, hour)
            else:
                # Вызываем функцию, которая вставляет элемент до выбранного нами
                dll.insertBefore(subject, hour, node)      # --> structure.DoublyLinkedList.insertBefore()

            subjects.insert(position + 1, subject)
            hours.insert(position + 1, hour)
            

def on_selection(event, subjects, hours):
    """Функция учитывает выбор в первом листбоксе и обновляет результаты в другом"""
    try:
        index = event.widget.curselection()[0]      # Индекс выбранного элемента в листбоксе
    except Exception:
        return

    subjects.delete(0, END)     # Удаляем все элементы в листбоксе, чтобы заполнить заново
    hours.delete(0, END)    # Удаляем все элементы в листбоксе, чтобы заполнить заново
    
    # Находим индекс нужного элемента в листбоксе и двухсвязном списке
    isection = event.widget.size() - 1 - index
    node = mainplan.plan.items[isection].data.head      # Получаем "голову" из двухсвязного списка
    
    if node:
        # Добавляем в листбоксы новые элементы
        subjects.insert(0, node.name)
        hours.insert(0, node.hours)
        # Добавляем в листбокс все элементы из двухсвязного списка
        while node.next is not None:
            node = node.next
            subjects.insert(0, node.name)
            hours.insert(0, node.hours)


def delete_subject(sections, subjects, hours):
    """Функция отвечает за удаление предметов из двухсвязного списка"""
    try:
        index = sections.curselection()[0]
    except Exception:
        mb.showerror('Ошибка', 'Необходимо выбрать раздел из которого будем удалять')
        return

    dll = mainplan.plan.items[index].data
    try:
        position = subjects.curselection()[0]
    except Exception:
        mb.showerror('Ошибка', 'Необходимо выбрать предмет для удаления')
        return

    element = subjects.get(position)
    node = dll.contains(element)[1]     # --> structure.DoublyLinkedList.contains()
    
    dll.delete(node)    # --> structure.DoublyLinkedList.delete()
    # Удаляем элемент из листбокса
    subjects.delete(position)
    hours.delete(position)