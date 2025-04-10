import unittest
import bot_database

class TestDeleteTask(unittest.TestCase):
    def setUp(self):
        bot_database.init_db()
        bot_database.add_task(1, "Silinecek görev")
        self.task_id = 1

    def test_delete_task(self):
        bot_database.delete_task(self.task_id)
        tasks = bot_database.get_tasks(1)
        self.assertNotIn("Silinecek görev", tasks)


if __name__ == '__main__':
    unittest.main()
