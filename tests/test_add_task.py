import unittest
import bot_database

class TestAddTask(unittest.TestCase):
    def setUp(self):
        bot_database.init_db()

    def test_add_task(self):
        bot_database.add_task(1, "Test görevi")
        tasks = bot_database.get_tasks(1)
        self.assertIn("Test görevi", tasks)


if __name__ == '__main__':
    unittest.main()
