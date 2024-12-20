from tkinter import *
from tkinter import messagebox
import sqlite3
import game


def run_login():
    root = Tk()
    root.geometry('400x300')
    root.title('Вход')
    root.configure(bg='#0a2239')

    def login():
        login_name = login_entry.get()
        password = password_entry.get()
        if not login_name or not password:
            messagebox.showwarning('Ошибка', 'Логин и пароль не могут быть пустыми!')
            return

        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM users WHERE login=? AND password=?', (login_name, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo('Успех', 'Вы успешно вошли в систему!')
            root.quit()  # Закрываем окно входа

            # Запускаем игру после успешного входа с передачей логина текущего пользователя в start_game.
            game.start_game(login_name)
        else:
            messagebox.showwarning('Ошибка', 'Неверный логин или пароль!')

        connection.close()

    frame = Frame(root, bg='#53a2be')
    frame.pack(fill=BOTH, expand=True)

    # Элементы интерфейса для входа
    title_label = Label(frame, text='Вход', font=('Arial', 20), bg='#53a2be', fg='#132e32')
    title_label.pack(pady=(30, 10))

    text_log = Label(frame, text='Введите Ваш логин:', bg='#53a2be', fg='#132e32', font=('Arial', 12))
    text_log.pack(anchor='w', padx=20)

    login_entry = Entry(frame, width=30)
    login_entry.pack(pady=(0, 10), padx=20)

    text_password = Label(frame, text='Введите Ваш пароль:', bg='#53a2be', fg='#132e32', font=('Arial', 12))
    text_password.pack(anchor='w', padx=20)

    password_entry = Entry(frame, width=30)
    password_entry.pack(pady=(0, 20), padx=20)

    button_login = Button(frame, text='Войти', command=login, bg='#1d84b5', fg='white', font=('Arial', 12))
    button_login.pack(pady=(10, 5))

    # Запуск главного цикла приложения
    root.mainloop()


# Запуск функции входа при прямом исполнении этого скрипта
if __name__ == "__main__":
    run_login()
