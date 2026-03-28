from src.domain import Task
from src.exceptions import ValidationError, StateError
from src.enums import TaskStatus

if __name__ == '__main__':
    task = Task(task_id=101, description="Настроить базу данных", priority=2)

    print(f"ID задачи: {task.id} (read-only property)")
    print(f"Время создания: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Сводка: {task.summary} (non-data descriptor)")
    print(f"Готова к выполнению? {task.is_ready_for_execution}")
    try:
        print("Пробуем установить приоритет = 10")
        task.priority = 10
    except ValidationError as e:
        print(f"Поймана ошибка: {e}")
    try:
        print("Пробуем изменить ID задачи на 999")
        task.id = 999 # type: ignore
    except AttributeError as e:
        print(f"Поймана ошибка Python: {e}")
    print("ПРОВЕРКА МАШИНЫ СОСТОЯНИЙ")
    print(f"Текущий статус: {task.state.value}")
    task.state = TaskStatus.IN_PROGRESS
    print(f"Успешный переход в статус: {task.state.value}")
    print(f"Готова к выполнению? {task.is_ready_for_execution}")

    try:
        print("Пробуем вернуть статус назад в NEW")
        task.state = TaskStatus.NEW
    except StateError as e:
        print(f"Поймана ошибка состояний: {e}")
    print("ДЕМОНСТРАЦИЯ NON-DATA DESCRIPTOR")
    task.summary = "Дескриптор перетерт произвольной строкой"
    print(f"Новое значение summary: {task.summary}")
