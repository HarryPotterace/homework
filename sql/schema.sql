CREATE DATABASE IF NOT EXISTS mental_health_system
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE mental_health_system;

DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS behavior_logs;
DROP TABLE IF EXISTS vent_posts;
DROP TABLE IF EXISTS assessment_records;
DROP TABLE IF EXISTS scale_questions;
DROP TABLE IF EXISTS scales;
DROP TABLE IF EXISTS counselors_schedule;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  student_no VARCHAR(20) NOT NULL UNIQUE,
  name VARCHAR(50) NOT NULL,
  nickname VARCHAR(50) NOT NULL,
  contact VARCHAR(50) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE admins (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL UNIQUE,
  name VARCHAR(50) NOT NULL,
  role VARCHAR(20) NOT NULL DEFAULT 'consultant',
  contact VARCHAR(50) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE scales (
  id INT PRIMARY KEY AUTO_INCREMENT,
  code VARCHAR(20) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  description TEXT NOT NULL
);

CREATE TABLE scale_questions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  scale_code VARCHAR(20) NOT NULL,
  question_order INT NOT NULL,
  content TEXT NOT NULL,
  CONSTRAINT fk_scale_questions_scale_code
    FOREIGN KEY (scale_code) REFERENCES scales(code)
    ON DELETE CASCADE,
  UNIQUE KEY uk_scale_question_order (scale_code, question_order)
);

CREATE TABLE assessment_records (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  scale_code VARCHAR(20) NOT NULL,
  scale_name VARCHAR(100) NOT NULL,
  score INT NOT NULL,
  result_level VARCHAR(50) NOT NULL,
  advice TEXT NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_assessment_records_user_id
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE
);

CREATE TABLE vent_posts (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NULL,
  title VARCHAR(100) NOT NULL,
  content TEXT NOT NULL,
  emotion VARCHAR(20) NOT NULL,
  risk_level VARCHAR(20) NOT NULL,
  is_anonymous TINYINT(1) NOT NULL DEFAULT 1,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_vent_posts_user_id
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE SET NULL
);

CREATE TABLE behavior_logs (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NULL,
  page_name VARCHAR(50) NOT NULL,
  mouse_speed FLOAT NOT NULL DEFAULT 0,
  click_count INT NOT NULL DEFAULT 0,
  pause_count INT NOT NULL DEFAULT 0,
  emotion VARCHAR(20) NOT NULL,
  ui_mode VARCHAR(20) NOT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_behavior_logs_user_id
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE SET NULL
);

CREATE TABLE counselors_schedule (
  id INT PRIMARY KEY AUTO_INCREMENT,
  counselor_name VARCHAR(50) NOT NULL,
  title VARCHAR(50) NOT NULL,
  schedule_date VARCHAR(20) NOT NULL,
  slot VARCHAR(50) NOT NULL,
  is_available TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE appointments (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  schedule_id INT NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  note VARCHAR(255) NOT NULL DEFAULT '',
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_appointments_user_id
    FOREIGN KEY (user_id) REFERENCES users(id)
    ON DELETE CASCADE,
  CONSTRAINT fk_appointments_schedule_id
    FOREIGN KEY (schedule_id) REFERENCES counselors_schedule(id)
    ON DELETE CASCADE
);
