def get_all_users():
    # Заглушка для пользователей
    class User:
        def __init__(self, id, username):
            self.id = id
            self.username = username

    return [User(1, "testuser"), User(2, "exampleuser")]