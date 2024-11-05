<div align="center">
<h1 align="center">
    LifeTracker
</h1>

<img src="./image/proyecto_logo.jpeg" alt="Personal Logo" width="150" height="150">

</div>

<h4 align="left">
    This project consist in life tracker for manage my expenses and keep a record of my books.
</h4>

<div align="center">


## Project Technologies

[![Python](https://img.shields.io/badge/Python-3178C6?style=for-the-badge&logo=python&logoColor=white&labelColor=101010)]()
[![FastApi](https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=101010)]()
[![FastApi](https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white&labelColor=101010)]()
[![FastApi](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white&labelColor=101010)]()

</div>

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Usage](#usage)
4. [Folder Structure](#folder-structure)
5. [Documentation Endpoints](#documentation-endpoints)


## Introduction

This project is a backend service designed to help manage personal expenses, track users, and keep a record of books read or to be read. It was developed using Python with FastAPI for the backend, PostgreSQL for the database, and Docker for containerization.


## Features

### Spends

- **Add New Spend**: Users can add new spend records with details like amount, description, and date.
- **Retrieve All Spends**: Users can fetch all their spend records.
- **Calculate Total Spends**: Users can calculate the total spends for a specific period.

### Users

- **Create User**: Users can create an account by providing a username and password.
- **Authentication**: Users can log in and receive a JSON Web Token (JWT) for authentication.
- **Get User Details**: Users can fetch their profile details.

### Books

- **List All Books**: Users can list all books they have read or plan to read.
- **Add New Book**: Users can add books to their reading list.
- **Update Book Status**: Users can update the status of a book (e.g., read, unread).


## Usage
- Install a necesary librarys `poetry install`
- Activate enviroment `poetry shell`
- Setup database execute a terminal `docker compose up -d` for create a postgres database
- For the last run a server with `make run` in port 3000


## Documentation Endpoints
For see a different curl endpoints go to - `http://localhost:3000/docs`
