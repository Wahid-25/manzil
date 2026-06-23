class User:
    """
    Model representing a User entity.
    """
    def __init__(self, user_id, username, email):
        self.id = user_id
        self.username = username
        self.email = email
    def __repr__(self):
        return f"<User {self.username}>"