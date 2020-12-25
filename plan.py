import xml.etree.ElementTree as xml
from os import remove

from structure import Stack


class Plan:
    """Класс отвечающий за создание, сохранение, загрузку и удаления
    плана обучения
    """
    def __init__(self, name):
        self.plan = Stack(name)

    def getName(self):
        return self.plan.name

    def createXML(self):
        """Функция отвечает за сохранение плана в xml-документ"""
        # Создаем xml-элементы
        root = xml.Element('xml-document')
        plan = xml.Element('plan')
        # Добавляем атрибут элементу plan
        plan.attrib['name'] = self.plan.name
        # В основной элемент добавляем всю структуру plan
        root.append(plan)

        for section in self.plan.items:
            sections = xml.SubElement(plan, 'sections')
            sections.attrib['name'] = section.data.name

            head = section.data.head
            if head:
                subjects = xml.SubElement(sections, 'subjects')
                subjects.attrib['name'] = head.name
                subjects.attrib['hours'] = head.hours
            
                while head.next is not None:
                    head = head.next 
                    subjects = xml.SubElement(sections, 'subjects')
                    subjects.attrib['name'] = head.name
                    subjects.attrib['hours'] = head.hours
        # Получаем xml-дерево
        tree = xml.ElementTree(root)
        tree.write('AcademicPlan.xml')


def parseXML():
    """Функция отвечает за загрузку плана из xml-документа"""
    # Получаем древо из файла
    tree = xml.ElementTree(file='AcademicPlan.xml')
    # Получаем основной элемент
    root = tree.getroot()

    for child in root:
        # Создаем стек план
        mainplan = Plan(child.attrib['name'])

        for i, sections in enumerate(child):
            # Заполняем план разделами
            mainplan.plan.push(sections.attrib['name'])
            try:
                for subject in sections:
                    # Заполняем каждый раздел своими предметами
                    mainplan.plan.items[i].data.append(subject.get('name'), subject.get('hours'))
            except Exception:
                pass

    return mainplan


def delete():
    # Удаляем файл с планом
    remove('AcademicPlan.xml')