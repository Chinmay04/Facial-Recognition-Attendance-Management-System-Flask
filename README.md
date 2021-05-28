# Facial-Recognition-Attendance-Management-System Flask
## With provided visual analytics

## Working

This Webapp allows organization to create account, upload the details of their members/employee/students, set up their sessions(for eg lectures, workshop, etc.) and take attendance session-wise. Admin will select a session, webacam will start and members will show their face one by one, when a members is recognized, his/her name will be displayed.
Attendance records can be viewd with filters, stats will be displayed with help of graphics, excel sheet of records can be downloaded.

Live Webcam Attendance

Installation:
[face_recognition](url) api

Create database named rootdb with following query

CREATE DATABASE `rootdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

Create table roottable with following query

CREATE TABLE `roottable` (
  `id` int NOT NULL AUTO_INCREMENT,
  `accname` varchar(50) DEFAULT NULL,
  `accpassword` varchar(100) DEFAULT NULL,
  `accmail` varchar(50) DEFAULT NULL,
  `acccontact` mediumtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


