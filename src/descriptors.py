from src.exceptions import ValidationError,StateError
from src.enums import TaskStatus


class IntegerRangeValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)
    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise ValidationError("Значение должно быть числовым")
        if not (self.min_value <= value <= self.max_value):
            raise ValidationError(f"Атрибут '{self.name}' должен быть в промежутке {self.min_value} - {self.max_value}")
        instance.__dict__[self.name] = value


class StringValidator:
    def __set_name__(self, owner, name):
        self.name = name
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValidationError("Значение должно быть строкой")
        if len(value) == 0:
            raise ValidationError(f"Длина значения атрибута '{self.name}' должна быть > 0")
        instance.__dict__[self.name] = value

class StateValidator:
    ALLOWED_TRANSITIONS = {
        None: {TaskStatus.NEW},
        TaskStatus.NEW: {TaskStatus.IN_PROGRESS},
        TaskStatus.IN_PROGRESS: {TaskStatus.DONE},
        TaskStatus.DONE: set(),
    }


    def __set_name__(self, owner, name):
        self.name = name
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name, None)
    def __set__(self, instance, value):
        if not isinstance(value, TaskStatus):
            raise ValidationError("Статус должен быть экземпляром TaskStatus")

        cur_status = instance.__dict__.get(self.name)
        if value not in self.ALLOWED_TRANSITIONS[cur_status]:
            raise StateError(f"Переход статуса из {cur_status} в {value} невозможен")
        instance.__dict__[self.name] = value

class TaskSummaryFormatter:

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return f"Задача #{instance.id}: {instance.description} | Статус: {instance.state}"
