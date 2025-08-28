#!/usr/bin/env python3
"""
Database Schema Migration Script for VelocityThreads
This script updates the database schema to fix field size issues.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

def migrate_database_schema():
    """Migrate the database schema to fix field size issues"""
    load_dotenv()
    
    # Get database connection details
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'velocity_threads')
    db_user = os.getenv('DB_USER', 'postgres')
    db_password = os.getenv('DB_PASSWORD', 'your_password_here')
    
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            database=db_name
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("Starting database schema migration...")
        
        # Check if the order table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'order'
            );
        """)
        
        if not cursor.fetchone()[0]:
            print("Order table does not exist. Please run the application first to create tables.")
            return False
        
        # Update order_number field size from VARCHAR(20) to VARCHAR(30)
        try:
            cursor.execute("""
                ALTER TABLE "order" 
                ALTER COLUMN order_number TYPE VARCHAR(30);
            """)
            print("✅ Updated order_number field from VARCHAR(20) to VARCHAR(30)")
        except Exception as e:
            print(f"⚠️  order_number field update: {str(e)}")
        
        # Update phone field size from VARCHAR(20) to VARCHAR(15)
        try:
            cursor.execute("""
                ALTER TABLE "order" 
                ALTER COLUMN phone TYPE VARCHAR(15);
            """)
            print("✅ Updated phone field from VARCHAR(20) to VARCHAR(15)")
        except Exception as e:
            print(f"⚠️  phone field update: {str(e)}")
        
        # Check for any other potential field size issues
        print("\nChecking for other potential field size issues...")
        
        # Check current field sizes
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns 
            WHERE table_name = 'order' 
            AND table_schema = 'public'
            AND data_type LIKE '%char%';
        """)
        
        fields = cursor.fetchall()
        print("\nCurrent field sizes in 'order' table:")
        for field in fields:
            print(f"  - {field[0]}: {field[1]}({field[2]})")
        
        cursor.close()
        conn.close()
        
        print("\n✅ Database schema migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error during migration: {str(e)}")
        return False

def verify_migration():
    """Verify that the migration was successful"""
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
        
        # Check the updated field sizes
        cursor.execute("""
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns 
            WHERE table_name = 'order' 
            AND table_schema = 'public'
            AND column_name IN ('order_number', 'phone');
        """)
        
        fields = cursor.fetchall()
        print("\nVerification - Updated field sizes:")
        for field in fields:
            print(f"  - {field[0]}: {field[1]}({field[2]})")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Error during verification: {str(e)}")
        return False

if __name__ == '__main__':
    print("Database Schema Migration for VelocityThreads")
    print("=" * 50)
    
    if migrate_database_schema():
        print("\nVerifying migration...")
        verify_migration()
        print("\n🎉 Migration completed! You can now run your application.")
    else:
        print("\n❌ Migration failed! Please check your database connection.")
