#!/usr/bin/env python3
"""
Database Setup Script for VelocityThreads PostgreSQL Migration
This script helps set up the PostgreSQL database and tables.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

def create_database():
    """Create the PostgreSQL database if it doesn't exist"""
    load_dotenv()
    
    # Get database connection details
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'velocity_threads')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'your_password_here')
    
    try:
        # Connect to PostgreSQL server (not to a specific database)
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database='postgres'  # Connect to default postgres database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        
        if not exists:
            # Create database
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"Database '{db_name}' created successfully!")
        else:
            print(f"Database '{db_name}' already exists!")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error creating database: {str(e)}")
        print("Please check your PostgreSQL connection details in .env file")
        return False

def test_connection():
    """Test connection to the newly created database"""
    load_dotenv()
    
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'velocity_threads')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'your_password_here')
    
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = conn.cursor()
        
        # Test a simple query
        cursor.execute('SELECT version();')
        version = cursor.fetchone()
        print(f"Successfully connected to PostgreSQL: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error testing connection: {str(e)}")
        return False

if __name__ == '__main__':
    print("Setting up PostgreSQL database for VelocityThreads...")
    print("=" * 50)
    
    # Create database
    if create_database():
        print("\nTesting connection...")
        if test_connection():
            print("\n✅ Database setup completed successfully!")
            print("\nNext steps:")
            print("1. Update your .env file with correct database credentials")
            print("2. Run 'python app.py' to create tables and start the application")
        else:
            print("\n❌ Database connection test failed!")
    else:
        print("\n❌ Database creation failed!")
