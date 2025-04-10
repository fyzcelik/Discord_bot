import unittest
import bot_database

class TestCompleteTask(unittest.TestCase):
    def setUp(self):
        bot_database.init_db()
        bot_database.add_task(1, "Tamamlanacak görev")
        self.task_id = 1

    def test_complete_task(self):
        bot_database.complete_task(self.task_id)
        tasks = bot_database.get_tasks(1)
        self.assertIn("[X]", tasks[0])

if __name__ == '__main__':
    unittest.main()
