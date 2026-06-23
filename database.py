import os
import sys
import sqlite3
import mysql.connector
from mysql.connector import Error as MySQLError
import config
_use_sqlite = False
_sqlite_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "manzil.db")
class SQLiteCursor:
    def __init__(self, sqlite_cursor):
        self.cursor = sqlite_cursor
    def execute(self, sql, params=None):
        if params is None:
            params = ()
        # Convert %s to ? for SQLite
        sql_converted = sql.replace('%s', '?')
        self.cursor.execute(sql_converted, params)
        return self
    def fetchone(self):
        return self.cursor.fetchone()
    def fetchall(self):
        return self.cursor.fetchall()
    def close(self):
        self.cursor.close()
    @property
    def lastrowid(self):
        return self.cursor.lastrowid
class SQLiteConnection:
    def __init__(self, sqlite_conn):
        self.conn = sqlite_conn
    def cursor(self):
        return SQLiteCursor(self.conn.cursor())
    def commit(self):
        self.conn.commit()
    def rollback(self):
        self.conn.rollback()
    def close(self):
        self.conn.close()
def init_sqlite_db():
    """Initializes the SQLite database schema and seeds it if it doesn't exist."""
    db_exists = os.path.exists(_sqlite_path)
    conn = sqlite3.connect(_sqlite_path)
    cursor = conn.cursor()
    
    if not db_exists or True:
        # Create tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            city_id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_name TEXT UNIQUE,
            latitude REAL,
            longitude REAL
        );
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transport_companies (
            company_id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT UNIQUE,
            comfort_score INTEGER,
            safety_score INTEGER,
            speed_kmh REAL,
            price_per_km REAL
        );
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS searches (
            search_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            departure_city INTEGER,
            destination_city INTEGER,
            distance_km REAL,
            search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(departure_city) REFERENCES cities(city_id),
            FOREIGN KEY(destination_city) REFERENCES cities(city_id)
        );
        """)
        
        # Seed cities
        cities_data = [
            ('Islamabad', 33.6844, 73.0479),
            ('Rawalpindi', 33.5651, 73.0169),
            ('Lahore', 31.5204, 74.3587),
            ('Karachi', 24.8607, 67.0011),
            ('Peshawar', 34.0151, 71.5249),
            ('Quetta', 30.1798, 66.9750),
            ('Multan', 30.1575, 71.5249),
            ('Faisalabad', 31.4504, 73.1350),
            ('Sialkot', 32.4945, 74.5229),
            ('Gujranwala', 32.1877, 74.1945),
            ('Bahawalpur', 29.3956, 71.6836),
            ('Hyderabad', 25.3960, 68.3578),
            ('Sukkur', 27.7052, 68.8574),
            ('Abbottabad', 34.1688, 73.2215),
            ('Mardan', 34.1989, 72.0401),
            ('Sargodha', 32.0836, 72.6711),
            ('Dera Ghazi Khan', 30.0561, 70.6348),
            ('Gwadar', 25.1264, 62.3226),
            ('Murree', 33.9070, 73.3943),
            ('Skardu', 35.2971, 75.6337),
            ('Jhelum', 32.9405, 73.7276),
            ('Attock', 33.7667, 72.3667),
            ('Chakwal', 32.9329, 72.8539),
            ('Gujrat', 32.5731, 74.1005),
            ('Kasur', 31.1187, 74.4503),
            ('Sheikhupura', 31.7167, 73.9833),
            ('Okara', 30.8081, 73.4458),
            ('Sahiwal', 30.6682, 73.1114),
            ('Vehari', 30.0459, 72.3489),
            ('Rahim Yar Khan', 28.4212, 70.2989),
            ('Khanewal', 30.3017, 71.9321),
            ('Muzaffargarh', 30.0726, 71.1938),
            ('Layyah', 30.9697, 70.9428),
            ('Mianwali', 32.5853, 71.5436),
            ('Bhakkar', 31.6336, 71.0644),
            ('Jhang', 31.2781, 72.3317),
            ('Toba Tek Singh', 30.9720, 72.4827),
            ('Chiniot', 31.7200, 72.9789),
            ('Narowal', 32.1014, 74.8736),
            ('Nankana Sahib', 31.4500, 73.7065),
            ('Haripur', 33.9946, 72.9347),
            ('Mansehra', 34.3302, 73.1968),
            ('Swat', 34.7717, 72.3602),
            ('Mingora', 34.7795, 72.3629),
            ('Kohat', 33.5833, 71.4333),
            ('Bannu', 32.9854, 70.6027),
            ('Dera Ismail Khan', 31.8315, 70.9017),
            ('Khuzdar', 27.8119, 66.6100),
            ('Turbat', 26.0031, 63.0544),
            ('Chitral', 35.8510, 71.7864)
        ]
        for name, lat, lon in cities_data:
            try:
                cursor.execute("INSERT OR IGNORE INTO cities (city_name, latitude, longitude) VALUES (?, ?, ?)", (name, lat, lon))
            except sqlite3.Error:
                pass
                
        # Seed transport companies
        companies_data = [
            ('Daewoo', 9, 9, 80.0, 5.0),
            ('Faisal Movers', 8, 8, 85.0, 4.5),
            ('InDrive', 6, 7, 70.0, 10.0)
        ]
        for name, comfort, safety, speed, price in companies_data:
            try:
                cursor.execute("INSERT OR IGNORE INTO transport_companies (company_name, comfort_score, safety_score, speed_kmh, price_per_km) VALUES (?, ?, ?, ?, ?)", (name, comfort, safety, speed, price))
            except sqlite3.Error:
                pass
                
        conn.commit()
    conn.close()
# Try to connect to MySQL initially. Set _use_sqlite flag if database cannot be reached.
try:
    # First, let's verify if MySQL works
    temp_conn = mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        connect_timeout=2
    )
    # Check if DB exists or create it
    temp_cursor = temp_conn.cursor()
    temp_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config.DB_NAME}")
    temp_cursor.close()
    temp_conn.close()
    
    # Try fully connecting to the database
    db_conn = mysql.connector.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        connect_timeout=2
    )
    db_conn.close()
    _use_sqlite = False
    print("Database: Connected successfully to MySQL database 'manzil'.")
except Exception as e:
    print(f"Database Warning: Could not connect to MySQL server ({e}). Falling back to SQLite.", file=sys.stderr)
    _use_sqlite = True
    init_sqlite_db()
def get_connection():
    """Returns a connection object. Supports MySQL and falls back to SQLite."""
    if _use_sqlite:
        conn = sqlite3.connect(_sqlite_path)
        return SQLiteConnection(conn)
    else:
        return mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )