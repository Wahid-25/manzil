CREATE DATABASE IF NOT EXISTS manzil;
USE manzil;
CREATE TABLE IF NOT EXISTS users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS cities(
    city_id INT AUTO_INCREMENT PRIMARY KEY,
    city_name VARCHAR(50) UNIQUE,
    latitude DOUBLE,
    longitude DOUBLE
);
INSERT INTO cities(city_name,latitude,longitude)
VALUES
('Islamabad',33.6844,73.0479),
('Rawalpindi',33.5651,73.0169),
('Lahore',31.5204,74.3587),
('Karachi',24.8607,67.0011),
('Peshawar',34.0151,71.5249),
('Quetta',30.1798,66.9750),
('Multan',30.1575,71.5249),
('Faisalabad',31.4504,73.1350),
('Sialkot',32.4945,74.5229),
('Gujranwala',32.1877,74.1945),
('Bahawalpur',29.3956,71.6836),
('Hyderabad',25.3960,68.3578),
('Sukkur',27.7052,68.8574),
('Abbottabad',34.1688,73.2215),
('Mardan',34.1989,72.0401),
('Sargodha',32.0836,72.6711),
('Dera Ghazi Khan',30.0561,70.6348),
('Gwadar',25.1264,62.3226),
('Murree',33.9070,73.3943),
('Skardu',35.2971,75.6337),
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
ON DUPLICATE KEY UPDATE city_name=city_name;
CREATE TABLE IF NOT EXISTS transport_companies(
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) UNIQUE,
    comfort_score INT,
    safety_score INT,
    speed_kmh FLOAT,
    price_per_km FLOAT
);
INSERT INTO transport_companies
(company_name,comfort_score,safety_score,speed_kmh,price_per_km)
VALUES
('Daewoo',9,9,80,5),
('Faisal Movers',8,8,85,4.5),
('InDrive',6,7,70,10)
ON DUPLICATE KEY UPDATE company_name=company_name;
CREATE TABLE IF NOT EXISTS searches(
    search_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    departure_city INT,
    destination_city INT,
    distance_km FLOAT,
    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id)
    REFERENCES users(id),
    FOREIGN KEY(departure_city)
    REFERENCES cities(city_id),
    FOREIGN KEY(destination_city)
    REFERENCES cities(city_id)
);