class TaskDomainError(Exception):
    """Базовый класс ошибок доменной модели"""
class ValidationError(TaskDomainError):
    """Ошибка валидации"""
class StateError(TaskDomainError):
    """Ошибка перехода статуса"""
