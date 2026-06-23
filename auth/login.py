import bcrypt
from database import get_connection
def login_user(username, password):
    """
    Verifies user login credentials.
    Returns the user's ID if successful, False otherwise.
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, password_hash
            FROM users
            WHERE username=%s
            """,
            (username,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if not result:
            return False
        user_id = result[0]
        stored_hash = result[1]
        # Handle stored_hash as string or bytes
        if isinstance(stored_hash, str):
            stored_hash_bytes = stored_hash.encode('utf-8')
        else:
            stored_hash_bytes = stored_hash
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash_bytes):
            return user_id
        return False
    except Exception as e:
        print(f"Error in login_user: {e}")
        return False