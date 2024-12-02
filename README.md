# Book Management System with FastAPI and PostgreSQL

This project is an intelligent book management system built using FastAPI, SQLAlchemy, and PostgreSQL. It supports basic CRUD operations, generating book summaries, and managing user reviews. The system also integrates with an Llama3 model (or other generative models) to generate summaries for books and reviews.

## Features

- **Book Management**: Add, retrieve, update, and delete books.
- **User Reviews**: Add reviews and ratings for books.
- **Book Summaries**: Generate summaries for books and reviews using a locally running Llama3 model.
- **Book Recommendations**: Get book recommendations based on user preferences.
- **RESTful API**: Accessible via a RESTful API built with FastAPI.
- **Asynchronous Database Access**: Utilizes SQLAlchemy with asyncpg for asynchronous database access.

## Requirements

- Python 3.8+
- PostgreSQL 13+ (locally running)
- FastAPI
- SQLAlchemy (async support)
- `databases` package
- `asyncpg` (async PostgreSQL driver)

## Setup

### 1. Install Dependencies

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/your-repo/book-management-system.git
cd book-management-system
pip install -r requirements.txt
