# scripts/pipline/database.py
from sqlalchemy import create_engine
import os

def get_db_path():
    """"get path"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, '/Users/linhao/tcga_sql_demo/database/tcga.db')

def get_engine():
    """"creat SQLite engine"""
    db_path = get_db_path()
    return create_engine(f'sqlite:///{db_path}')