# SQL_MINIPROJECT


# Book Rental Management System

This project is a Book Rental Management System that allows users to register, login, and rent books from a library collection. The system is implemented in Python with a MySQL database backend. This README provides an overview of the project and instructions for setup and usage.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [To-Do](#to-do)

## Introduction

The Book Rental Management System is designed to provide a platform for users to register, log in, and rent books from a library. The system is built using Python and MySQL for the database storage. The project is aimed at providing a simple and user-friendly interface for managing book rentals.

## Features

- User Registration: New users can create accounts by providing a username and password.
- User Login: Registered users can log in using their credentials.
- Book Rental: Users can rent books from the available collection.
- Database Management: The system utilizes a MySQL database to store user information, books, and rental records.

## Setup

To run the Book Rental Management System on your local machine, follow these steps:

1. Clone the repository to your local machine.
2. Ensure that Python and MySQL are installed.
3. Install the required Python packages using `pip install -r requirements.txt`.
4. Configure the MySQL database connection details in the `bookrent.py` file.
5. Create the necessary tables in the MySQL database using the provided SQL scripts.

## Usage

After setting up the project, you can run the `bookrent.py` script to start the Book Rental Management System. This will initiate the system and prompt you to register, login, and rent books.

To register a new user, follow the on-screen instructions to provide a username and password.

To login as an existing user, enter the registered username and password when prompted.

To rent a book, navigate through the available collection and follow the prompts to complete the rental process.

## To-Do

- Add a table to show the books rented by the currently logged-in user and the rental duration.
- Implement a feature for users to offer their own books for rent.
- Enhance the user interface and provide clear feedback during registration, login, and rental processes.

