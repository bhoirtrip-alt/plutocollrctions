#!/usr/bin/env python3
"""
Database Health Check Script for VelocityThreads
This script performs comprehensive checks on the database schema and data integrity.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

def check_database_connection():
    """Check if we can connect to the database"""
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
        
        # Test connection
        cursor.execute('SELECT version();')
        version = cursor.fetchone()
        print(f"✅ Database connection successful: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        return False

def check_table_structure():
    """Check the structure of all tables"""
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
        
        # Get all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"\n📋 Found {len(tables)} tables in database:")
        
        for table in tables:
            table_name = table[0]
            print(f"\n  Table: {table_name}")
            
            # Get column information
            cursor.execute("""
                SELECT column_name, data_type, character_maximum_length, is_nullable, column_default
                FROM information_schema.columns 
                WHERE table_name = %s 
                AND table_schema = 'public'
                ORDER BY ordinal_position;
            """, (table_name,))
            
            columns = cursor.fetchall()
            for col in columns:
                col_name, data_type, max_length, nullable, default_val = col
                length_info = f"({max_length})" if max_length else ""
                nullable_info = "NULL" if nullable == "YES" else "NOT NULL"
                default_info = f" DEFAULT {default_val}" if default_val else ""
                
                print(f"    - {col_name}: {data_type}{length_info} {nullable_info}{default_info}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error checking table structure: {str(e)}")
        return False

def check_field_size_issues():
    """Check for potential field size issues"""
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
        
        print("\n🔍 Checking for potential field size issues...")
        
        # Check order_number field
        cursor.execute("""
            SELECT column_name, character_maximum_length
            FROM information_schema.columns 
            WHERE table_name = 'order' 
            AND table_schema = 'public'
            AND column_name = 'order_number';
        """)
        
        result = cursor.fetchone()
        if result:
            field_name, max_length = result
            if max_length and max_length < 30:
                print(f"⚠️  {field_name} field size ({max_length}) may be too small for order numbers")
            else:
                print(f"✅ {field_name} field size ({max_length}) is adequate")
        
        # Check phone field
        cursor.execute("""
            SELECT column_name, character_maximum_length
            FROM information_schema.columns 
            WHERE table_name = 'order' 
            AND table_schema = 'public'
            AND column_name = 'phone';
        """)
        
        result = cursor.fetchone()
        if result:
            field_name, max_length = result
            if max_length and max_length < 15:
                print(f"⚠️  {field_name} field size ({max_length}) may be too small for phone numbers")
            else:
                print(f"✅ {field_name} field size ({max_length}) is adequate")
        
        # Check for any data that might exceed field limits
        print("\n📊 Checking for data that might exceed field limits...")
        
        # Check order_number lengths
        cursor.execute("""
            SELECT LENGTH(order_number) as length, COUNT(*) as count
            FROM "order"
            GROUP BY LENGTH(order_number)
            ORDER BY length;
        """)
        
        lengths = cursor.fetchall()
        if lengths:
            print("  Order number lengths in database:")
            for length, count in lengths:
                print(f"    - {length} characters: {count} orders")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error checking field size issues: {str(e)}")
        return False

def check_data_integrity():
    """Check data integrity"""
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
        
        print("\n🔍 Checking data integrity...")
        
        # Count records in each table
        tables = ['user', 'product', 'order', 'order_item', 'product_image']
        
        for table in tables:
            try:
                cursor.execute(f'SELECT COUNT(*) FROM "{table}";')
                count = cursor.fetchone()[0]
                print(f"  - {table}: {count} records")
            except Exception as e:
                print(f"  - {table}: Error - {str(e)}")
        
        # Check for orphaned records
        print("\n🔍 Checking for orphaned records...")
        
        # Check for orphaned order_items
        cursor.execute("""
            SELECT COUNT(*) 
            FROM order_item oi 
            LEFT JOIN "order" o ON oi.order_id = o.id 
            WHERE o.id IS NULL;
        """)
        
        orphaned_items = cursor.fetchone()[0]
        if orphaned_items > 0:
            print(f"⚠️  Found {orphaned_items} orphaned order items")
        else:
            print("✅ No orphaned order items found")
        
        # Check for orphaned product_images
        cursor.execute("""
            SELECT COUNT(*) 
            FROM product_image pi 
            LEFT JOIN product p ON pi.product_id = p.id 
            WHERE p.id IS NULL;
        """)
        
        orphaned_images = cursor.fetchone()[0]
        if orphaned_images > 0:
            print(f"⚠️  Found {orphaned_images} orphaned product images")
        else:
            print("✅ No orphaned product images found")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error checking data integrity: {str(e)}")
        return False

def run_comprehensive_health_check():
    """Run all health checks"""
    print("Database Health Check for VelocityThreads")
    print("=" * 50)
    
    checks = [
        ("Database Connection", check_database_connection),
        ("Table Structure", check_table_structure),
        ("Field Size Issues", check_field_size_issues),
        ("Data Integrity", check_data_integrity)
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n🔍 Running {check_name} check...")
        result = check_func()
        results.append((check_name, result))
    
    print("\n" + "=" * 50)
    print("HEALTH CHECK SUMMARY")
    print("=" * 50)
    
    all_passed = True
    for check_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{check_name}: {status}")
        if not result:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All health checks passed! Your database is healthy.")
    else:
        print("\n⚠️  Some health checks failed. Please review the issues above.")
    
    return all_passed

if __name__ == '__main__':
    run_comprehensive_health_check()
