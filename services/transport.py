from database import get_connection
# Local fallbacks for transport company information
FALLBACK_COMPANIES = [
    {"name": "Daewoo", "comfort": 9, "safety": 9, "speed": 80.0, "price": 5.0},
    {"name": "Faisal Movers", "comfort": 8, "safety": 8, "speed": 85.0, "price": 4.5},
    {"name": "InDrive", "comfort": 6, "safety": 7, "speed": 70.0, "price": 10.0}
]
def calculate_transport(distance):
    """
    Retrieves company profiles and computes fare and time for a given distance.
    """
    companies = []
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT company_name, comfort_score, safety_score, speed_kmh, price_per_km FROM transport_companies")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        
        for row in rows:
            companies.append({
                "name": row[0],
                "comfort": int(row[1]),
                "safety": int(row[2]),
                "speed": float(row[3]),
                "price": float(row[4])
            })
    except Exception as e:
        print(f"Error loading transport companies from database: {e}. Using fallback.")
        
    if not companies:
        companies = FALLBACK_COMPANIES
    results = []
    for c in companies:
        fare = round(c["price"] * distance, 2)
        time = round(distance / c["speed"], 2)  # Time in decimal hours
        results.append({
            "company": c["name"],
            "fare": fare,
            "time": time,
            "comfort": c["comfort"],
            "safety": c["safety"]
        })
    return results
def save_search(user_id, dep_city, des_city, distance):
    """
    Logs user travel query to database searches history table.
    """
    if not user_id:
        return False
    try:
        from services.city_service import get_city_id
        dep_id = get_city_id(dep_city)
        des_id = get_city_id(des_city)
        
        if dep_id is not None and des_id is not None:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO searches (user_id, departure_city, destination_city, distance_km)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, dep_id, des_id, distance)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
    except Exception as e:
        print(f"Error saving search log: {e}")
    return False