# this is for the database configuration for sqllite

import os

class Config:
    # SQLite (easy for development)
    SQLALCHEMY_DATABASE_URL = "sqlite:///books.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False