# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 're-educ-ia-secret-key'
    JSON_SORT_KEYS = False
