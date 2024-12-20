from tkinter import *
from tkinter import messagebox
import sqlite3
import log

def run_registration():
    root = Tk()
    root.geometry('400x300')
    root.title('Регистрация')
    root.configure(bg='#0a2239')

    def create_db():
        """Создает базу данных и таблицу пользователей, если она не существует."""
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            high_score INTEGER
        )
        ''')
        connection.commit()
        connection.close()

    def add_high_score_column():
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        try:
            cursor.execute('ALTER TABLE users ADD COLUMN high_score INTEGER DEFAULT 0')
            connection.commit()
        except sqlite3.OperationalError:
            pass # Столбец уже существует
        finally:
            connection.close()

    def registration():
       def save():
           login=registr_login.get()
           password=registr_password.get()
           if not login or not password:
               messagebox.showwarning('Ошибка','Логин и пароль не могут быть пустыми!')
               return
           try:
               connection=sqlite3.connect('users.db')
               cursor=connection.cursor()
               cursor.execute('INSERT INTO users (login,password) VALUES (?,?)',(login,password))
               connection.commit()
               messagebox.showinfo('Успех','Вы успешно зарегистрированы!')
               root.quit() # Закрываем окно регистрации и возвращаем управление в main.py
           except sqlite3.IntegrityError:
               messagebox.showwarning('Ошибка','Этот логин уже занят!')
           except Exception as e:
               messagebox.showerror('Ошибка',f'Произошла ошибка: {e}')
           finally:
               if connection:
                   connection.close()

       # Рамка для элементов регистрации
       frame=Frame(root,bg='#53a2be')
       frame.pack(fill=BOTH ,expand=True)

       # Элементы интерфейса для регистрации
       title_label=Label(frame,text='Регистрация',font=('Arial',20),bg='#53a2be',fg='#132e32')
       title_label.pack(pady=(30 ,10))

       text_log=Label(frame,text='Введите Ваш логин:',bg='#53a2be',fg='#132e32',font=('Arial',12))
       text_log.pack(anchor='w',padx=20)

       registr_login=Entry(frame,width=30)
       registr_login.pack(pady=(0 ,10),padx=20)

       text_password=Label(frame,text='Введите Ваш пароль:',bg='#53a2be',fg='#132e32',font=('Arial',12))
       text_password.pack(anchor='w',padx=20)

       registr_password=Entry(frame ,show='*',width=30)
       registr_password.pack(pady=(0 ,20),padx=20)

       button_registr=Button(frame,text='Зарегистрироваться',command=save,bg='#1d84b5',fg='white',font=('Arial',12))
       button_registr.pack(pady=10)

       # Кнопка для перехода к окну входа
       button_login_redirect=Button(frame,text='Уже зарегистрированы? Войти!',command=lambda: [root.quit(), log.run_login()],bg='#1d84b5',fg='white',font=('Arial',12))
       button_login_redirect.pack(pady=(10 ,0))

   # Создание базы данных и таблицы при запуске приложения
    create_db()
    add_high_score_column()

   # Вызов функции регистрации
    registration()

   # Запуск главного цикла приложения
    root.mainloop()

# Запуск функции регистрации при прямом исполнении этого скрипта
if __name__ == "__main__":
   run_registration()

