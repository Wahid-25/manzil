class City:
    """
    Model representing a City entity.
    """
    def __init__(self, city_id, city_name, latitude, longitude):
        self.id = city_id
        self.name = city_name
        self.latitude = latitude
        self.longitude = longitude
    def __repr__(self):
        return f"<City {self.name} ({self.latitude}, {self.longitude})>"