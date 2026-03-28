import unittest
from datetime import datetime


from src.enums import TaskStatus
from src.exceptions import ValidationError, StateError
from src.domain import Task
from src.descriptors import IntegerRangeValidator, StringValidator, StateValidator, TaskSummaryFormatter


class TestTaskDomainModel(unittest.TestCase):

    def setUp(self):
        self.task = Task(task_id=1, description="Тестовая задача", priority=3)

    def test_task_creation_success(self):
        self.assertEqual(self.task.id, 1)
        self.assertEqual(self.task.description, "Тестовая задача")
        self.assertEqual(self.task.priority, 3)
        self.assertEqual(self.task.state, TaskStatus.NEW)
        self.assertIsInstance(self.task.created_at, datetime)

    def test_id_and_created_at_are_readonly(self):
        with self.assertRaises(AttributeError):
            self.task.id = 2

        with self.assertRaises(AttributeError):
            self.task.created_at = datetime.now()

    def test_priority_valid_change(self):
        self.task.priority = 5
        self.assertEqual(self.task.priority, 5)

    def test_priority_invalid_type(self):
        with self.assertRaises(ValidationError) as context:
            self.task.priority = "высокий"
        self.assertIn("должно быть числовым", str(context.exception))

    def test_priority_out_of_bounds(self):
        with self.assertRaises(ValidationError):
            self.task.priority = 0
        with self.assertRaises(ValidationError):
            self.task.priority = 6


    def test_description_valid_change(self):
        self.task.description = "Новое описание"
        self.assertEqual(self.task.description, "Новое описание")

    def test_description_invalid_type(self):
        with self.assertRaises(ValidationError):
            self.task.description = 123

    def test_description_empty_string(self):
        with self.assertRaises(ValidationError):
            self.task.description = ""


    def test_state_valid_transitions(self):
        self.task.state = TaskStatus.IN_PROGRESS
        self.assertEqual(self.task.state, TaskStatus.IN_PROGRESS)

        self.task.state = TaskStatus.DONE
        self.assertEqual(self.task.state, TaskStatus.DONE)

    def test_state_invalid_type(self):
        with self.assertRaises(ValidationError):
            self.task.state = "IN_PROGRESS"

    def test_state_invalid_transitions(self):
        with self.assertRaises(StateError):
            self.task.state = TaskStatus.DONE
        self.task.state = TaskStatus.IN_PROGRESS
        with self.assertRaises(StateError):
            self.task.state = TaskStatus.NEW

    def test_is_ready_for_execution(self):
        self.assertTrue(self.task.is_ready_for_execution)
        self.task.state = TaskStatus.IN_PROGRESS
        self.assertFalse(self.task.is_ready_for_execution)

    def test_summary_formatter(self):
        expected_summary = "Задача #1: Тестовая задача | Статус: TaskStatus.NEW"
        self.assertEqual(self.task.summary, expected_summary)

    def test_non_data_descriptor_overwrite(self):
        """Демонстрация того, что Non-data дескриптор можно перетереть"""
        self.task.summary = "Взломано"
        self.assertEqual(self.task.summary, "Взломано")

    def test_class_level_descriptor_access(self):
        self.assertIsInstance(Task.priority, IntegerRangeValidator)
        self.assertIsInstance(Task.description, StringValidator)
        self.assertIsInstance(Task.state, StateValidator)
        self.assertIsInstance(Task.summary, TaskSummaryFormatter)


if __name__ == "__main__":
    unittest.main(verbosity=2)
