import unittest
import bot_database

class TestShowTasks(unittest.TestCase):
    def setUp(self):
        bot_database.init_db()
        bot_database.add_task(1, "Görev 1")
        bot_database.add_task(1, "Görev 2")

    def test_show_tasks(self):
        tasks = bot_database.get_tasks(1)
        self.assertEqual(tasks, ["Görev 1", "Görev 2"])


if __name__ == '__main__':
    unittest.main()
