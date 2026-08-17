"""Production WSGI entry point for Gunicorn.  Usage: gunicorn wsgi:app"""
from app import create_app

app = create_app()
