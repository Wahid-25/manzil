import bcrypt
from database import get_connection
def register_user(username, email, password):
    """
    Registers a new user in the database.
    Returns True if registration is successful, False otherwise.
    """
    if not username or not email or not password:
        return False
        
    try:
        conn = get_connection()
        cursor = conn.cursor()
        hashed = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        )
        sql = """
        INSERT INTO users
        (username, email, password_hash)
        VALUES (%s, %s, %s)
        """
        cursor.execute(
            sql,
            (
                username,
                email,
                hashed.decode('utf-8')
            )
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error in register_user: {e}")
        return False