CREATE DATABASE job_tracker;
USE job_tracker;
CREATE TABLE applications (
id INT AUTO_INCREMENT PRIMARY KEY,
company_name VARCHAR(100) NOT NULL,
role VARCHAR(100) NOT NULL,
applied_date DATE NOT NULL,
status VARCHAR(20) DEFAULT 'applied',
notes VARCHAR(255)
);
