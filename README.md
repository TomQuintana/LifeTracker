<h2 align="center">
    This project consist in life tracker for manage my spends. 
</h2>
<h5 align="center">In the future I have a implement an interface but for now its only a backend</h5>

<div align="center">

## Project technologies

[![Python](https://img.shields.io/badge/Python-3178C6?style=for-the-badge&logo=python&logoColor=white&labelColor=101010)]()
[![FastApi](https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=101010)]()
[![FastApi](https://img.shields.io/badge/postgresql-4169E1?style=for-the-badge&logo=postgresql&logoColor=white&labelColor=101010)]()
[![FastApi](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white&labelColor=101010)]()

</div>

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Documentation Endpoints](#documentation-endpoints)
4. [Usage](#usage)
5. [Folder Structure](#folder-structure)

## Features

### Spends

- Add new spend
- Obtain all data of spends

## Usage
- Generate a virtual enviroment by `python3 -m venv <name>`
- Activate enviroment ` source .<name>/bin/activate`
- Then install a necesary package in your enviroment using `pip install -r requirements.txt`
- For the last run a server with `python3 runserver` in port 3000

### Set up database

- execute a terminal `docker compose up -d` for create a postgres database

## Documentation Endpoints

For see a different curl endpoints go to - `http://localhost:3000/docs`
