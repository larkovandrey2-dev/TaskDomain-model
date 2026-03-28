from src.descriptors import IntegerRangeValidator, StringValidator, TaskSummaryFormatter, StateValidator, TaskStatus
from datetime import datetime

class Task:
    priority = IntegerRangeValidator(min_value=1, max_value=5)
    description = StringValidator()
    state = StateValidator()
    summary = TaskSummaryFormatter()

    def __init__(self, task_id: int, description: str, priority: int) -> None:
        self._id = task_id
        self._created_at = datetime.now()
        self.description = description
        self.priority = priority
        self.state = TaskStatus.NEW

    @property
    def id(self) -> int:
        return self._id
    @property
    def created_at(self) -> datetime:
        return self._created_at
    @property
    def is_ready_for_execution(self) -> bool:
        return self.state == TaskStatus.NEW and bool(self.description)
