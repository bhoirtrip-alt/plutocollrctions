#!/usr/bin/env python3
"""
Simple connection test script for PostgreSQL
Run this to verify your database connection before starting the main application.
"""

import os
from dotenv import load_dotenv
import psycopg2

def test_postgresql_connection():
    """Test PostgreSQL connection using credentials from .env file"""
    load_dotenv()
    
    # Get database connection details
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'velocity_threads')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'your_password_here')
    
    print("Testing PostgreSQL Connection...")
    print("=" * 40)
    print(f"Host: {db_host}")
    print(f"Port: {db_port}")
    print(f"Database: {db_name}")
    print(f"User: {db_user}")
    print(f"Password: {'*' * len(db_password) if db_password else 'Not set'}")
    print()
    
    try:
        # Test connection
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
        
        print("✅ Connection successful!")
        print(f"PostgreSQL Version: {version[0]}")
        
        # Test if tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        tables = cursor.fetchall()
        if tables:
            print(f"\n📋 Existing tables: {[table[0] for table in tables]}")
        else:
            print("\n📋 No tables found (this is normal for a new database)")
        
        cursor.close()
        conn.close()
        
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Connection failed: {str(e)}")
        print("\n🔧 Troubleshooting tips:")
        print("1. Check if PostgreSQL is running")
        print("2. Verify your credentials in .env file")
        print("3. Ensure the database exists (run setup_database.py)")
        print("4. Check if PostgreSQL accepts connections from your IP")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

if __name__ == '__main__':
    success = test_postgresql_connection()
    
    if success:
        print("\n🎉 Your PostgreSQL connection is working!")
        print("You can now run 'python app.py' to start the application.")
    else:
        print("\n💥 Connection test failed. Please fix the issues above.")
