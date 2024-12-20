import unittest
import sqlite3
import os
from unittest.mock import patch
from tkinter import Tk
import reg
import log
import game

class TestGameApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Создаем временную базу данных для тестов
        cls.db_path = 'test_users.db'
        cls.connection = sqlite3.connect(cls.db_path)
        cls.cursor = cls.connection.cursor()
        cls.cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            high_score INTEGER
        )
        ''')
        cls.connection.commit()

    @classmethod
    def tearDownClass(cls):
        # Удаляем временную базу данных после тестов
        cls.connection.close()
        os.remove(cls.db_path)

    def setUp(self):
        # Очищаем таблицу перед каждым тестом
        self.cursor.execute('DELETE FROM users')
        self.connection.commit()

    def test_registration(self):
        # Тестируем регистрацию нового пользователя
        with patch('reg.messagebox.showinfo') as mock_showinfo, \
             patch('reg.messagebox.showwarning') as mock_showwarning, \
             patch('reg.Tk', return_value=Tk()):
            reg.run_registration()
            mock_showinfo.assert_called_with('Успех', 'Вы успешно зарегистрированы!')
            mock_showwarning.assert_not_called()

    def test_login(self):
        # Тестируем вход пользователя
        self.cursor.execute('INSERT INTO users (login, password) VALUES (?, ?)', ('testuser', 'testpass'))
        self.connection.commit()

        with patch('log.messagebox.showinfo') as mock_showinfo, \
             patch('log.messagebox.showwarning') as mock_showwarning, \
             patch('log.Tk', return_value=Tk()), \
             patch('game.start_game', return_value=None):  # Заменяем start_game на мок
            log.run_login()
            mock_showinfo.assert_called_with('Успех', 'Вы успешно вошли в систему!')
            mock_showwarning.assert_not_called()

    def test_update_score(self):
        # Тестируем обновление счета пользователя
        self.cursor.execute('INSERT INTO users (login, password, high_score) VALUES (?, ?, ?)', ('testuser', 'testpass', 100))
        self.connection.commit()

        game.user_login = 'testuser'
        game.add_or_update_user_score(150)

        self.cursor.execute('SELECT high_score FROM users WHERE login=?', ('testuser',))
        result = self.cursor.fetchone()
        self.assertEqual(result[0], 150)

    def test_leaderboard(self):
        # Тестируем получение таблицы лидеров
        self.cursor.execute('INSERT INTO users (login, password, high_score) VALUES (?, ?, ?)', ('user1', 'pass1', 200))
        self.cursor.execute('INSERT INTO users (login, password, high_score) VALUES (?, ?, ?)', ('user2', 'pass2', 150))
        self.connection.commit()

        leaderboard = game.get_leaderboard()
        self.assertEqual(len(leaderboard), 2)
        self.assertEqual(leaderboard[0][0], 'user1')
        self.assertEqual(leaderboard[0][1], 200)
        self.assertEqual(leaderboard[1][0], 'user2')
        self.assertEqual(leaderboard[1][1], 150)

if __name__ == '__main__':
    unittest.main()
