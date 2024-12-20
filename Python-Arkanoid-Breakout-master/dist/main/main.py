import reg
import log
import game

def main():
    reg.run_registration()  # Открываем регистрацию или вход
    user_login = log.run_login()  # Запускаем вход и получаем имя пользователя
    if user_login:  # Проверяем, что вход успешен
        game.start_game(user_login)  # Передаем логин пользователя в игру

if __name__ == "__main__":
    main()
