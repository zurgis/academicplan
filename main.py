import tkinter as tk

from widgets import label, button, entry, listbox
from command import (
    create_plan, create_section, delete_section, create_subject, 
    on_selection, delete_subject, save_plan, download_plan, delete_plan
    )
    

# ОСНОВНЫЕ НАСТРОЙКИ
root = tk.Tk()  # Точка входа приложения, создаем само приложение
root.title('Учебный план на основе "Стек-массив двунаправленных списков"')
root.geometry('1280x720')   # Задаем размеры окна
root.resizable(False, False)    # Запрещаем изменение окна


# ПОЛЯ ДЛЯ ТЕКСТА

plan = entry(root, 350, 100, width=40)      # Название плана
section = entry(root, 350, 510, width=40)    # Название нового раздела
subject = entry(root, 735, 510, width=40)    # Название нового предмета
hour = entry(root, 855, 540, width=20)    # Количество часов


# СПИСКИ ЭЛЕМЕНТОВ

sections = listbox(root, 350, 155, height=20, width=40, selectmode=tk.SINGLE, exportselection=0)    # Список разделов
subjects = listbox(root, 700, 155, height=20, width=40, selectmode=tk.SINGLE, exportselection=0)    # Список предметов
hours = listbox(root, 960, 155, height=20, width=8, selectmode=tk.SINGLE)    # Список часов


# БИНДЫ НА ЛИСТБОКСЫ

sections.bind('<<ListboxSelect>>', lambda e, x=subjects, y=hours: on_selection(e, x, y))


# ЧЕКБАТТОН НА ПРОВЕРКУ ДОБАВИТЬ ПОСЛЕ ИЛИ НЕТ, НОВЫЙ ЭЛЕМЕНТ

cvar = tk.BooleanVar()  # Переменная для значений чек баттона
checkbutton = tk.Checkbutton(root, text='После выбранного предмета',
    variable=cvar, onvalue=1, offvalue=0, font='arial 10').place(x=730, y=560)


# ВСЕ НЕОБХОДИМЫЕ КНОПКИ

button(root, 'Создать учебный план', 50, 200, width=30, command=lambda x=plan, y=sections: create_plan(x, y))
button(root, 'Загрузить из файла', 50, 250, width=30, command=lambda x=plan, y=sections: download_plan(x, y))
button(root, 'Сохранить в файл', 50, 300, width=30, command=save_plan)
button(root, 'Удалить учебный план', 50, 350, width=30, 
    command=lambda x=plan, y=sections, z=subjects, a=hours: delete_plan(x, y, z, a))
button(root, 'Выход', 1005, 670, width=30, command=root.destroy)
button(root, 'Создать раздел', 362, 535, width=30, command=lambda x=section, y=sections: create_section(x, y))
button(root, 'Удалить раздел', 362, 570, width=30, 
    command=lambda x=sections, y=subjects, z=hours: delete_section(x, y, z))
button(root, 'Создать предмет', 749, 590, width=30, command=lambda x=subject, y=hour, z=sections,
    a=subjects, b=hours, c=cvar: create_subject(x, y, z, a, b, c))
button(root, 'Удалить выбранный предмет', 749, 625, width=30, 
    command=lambda x=sections, y=subjects, z=hours: delete_subject(x, y, z))


# ВСЕ НЕОБХОДИМЫЕ ПОДПИСИ

label(root, 'Название учебного плана:', 390, 78, font='arial 10')
label(root, 'Управление:', 100, 150, font='arial 14')
label(root, 'Разделы:', 435, 130, font='arial 10')
label(root, 'Название нового раздела:', 390, 488, font='arial 10')
label(root, 'Предметы:', 780, 130, font='arial 10')
label(root, 'Название нового предмета:', 770, 488, font='arial 10')
label(root, 'Количество часов:', 730, 535, font='arial 10')
label(root, 'Часы:', 964, 130, font='arial 10')
label(root, 'Реализация Объекта-контейнера "Учебный план" \
    на основе структуры "Стек-массив двунаправленных списков"',
    x=30, y=690)


root.mainloop()