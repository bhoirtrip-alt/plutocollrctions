#!/usr/bin/env python3
"""
Data Migration Script for VelocityThreads
This script can help migrate data from SQLite to PostgreSQL if you have existing data.
Note: This is optional and only needed if you want to preserve existing data.
"""

import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import json

def connect_sqlite():
    """Connect to the old SQLite database"""
    try:
        sqlite_path = os.path.join(os.path.dirname(__file__), 'instance', 'ecommerce.db')
        if os.path.exists(sqlite_path):
            return sqlite3.connect(sqlite_path)
        else:
            print("SQLite database not found. No data to migrate.")
            return None
    except Exception as e:
        print(f"Error connecting to SQLite: {str(e)}")
        return None

def connect_postgresql():
    """Connect to PostgreSQL database"""
    load_dotenv()
    
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'your_password_here'),
            database=os.getenv('DB_NAME', 'velocity_threads')
        )
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {str(e)}")
        return None

def migrate_users(sqlite_conn, pg_conn):
    """Migrate user data"""
    try:
        sqlite_cursor = sqlite_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        # Get users from SQLite
        sqlite_cursor.execute("SELECT id, username, email, password_hash, is_admin, created_at FROM user")
        users = sqlite_cursor.fetchall()
        
        if not users:
            print("No users to migrate")
            return
        
        # Insert into PostgreSQL
        for user in users:
            pg_cursor.execute("""
                INSERT INTO "user" (id, username, email, password_hash, is_admin, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, user)
        
        pg_conn.commit()
        print(f"Migrated {len(users)} users")
        
    except Exception as e:
        print(f"Error migrating users: {str(e)}")
        pg_conn.rollback()

def migrate_products(sqlite_conn, pg_conn):
    """Migrate product data"""
    try:
        sqlite_cursor = sqlite_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        # Get products from SQLite
        sqlite_cursor.execute("""
            SELECT id, name, description, price, image_url, category, 
                   COALESCE(subcategory, ''), stock, 
                   COALESCE(colors, ''), COALESCE(sizes, ''), created_at 
            FROM product
        """)
        products = sqlite_cursor.fetchall()
        
        if not products:
            print("No products to migrate")
            return
        
        # Insert into PostgreSQL
        for product in products:
            pg_cursor.execute("""
                INSERT INTO product (id, name, description, price, image_url, category, 
                                   subcategory, stock, colors, sizes, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, product)
        
        pg_conn.commit()
        print(f"Migrated {len(products)} products")
        
    except Exception as e:
        print(f"Error migrating products: {str(e)}")
        pg_conn.rollback()

def migrate_orders(sqlite_conn, pg_conn):
    """Migrate order data"""
    try:
        sqlite_cursor = sqlite_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        # Get orders from SQLite
        sqlite_cursor.execute("""
            SELECT id, order_number, user_id, total_amount, 
                   COALESCE(advance_paid, 0.0), COALESCE(remaining_amount, total_amount),
                   status, shipping_address, phone, 
                   COALESCE(utr_number, ''), COALESCE(payment_screenshot, ''), created_at
            FROM "order"
        """)
        orders = sqlite_cursor.fetchall()
        
        if not orders:
            print("No orders to migrate")
            return
        
        # Insert into PostgreSQL
        for order in orders:
            pg_cursor.execute("""
                INSERT INTO "order" (id, order_number, user_id, total_amount, advance_paid, 
                                   remaining_amount, status, shipping_address, phone, 
                                   utr_number, payment_screenshot, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, order)
        
        pg_conn.commit()
        print(f"Migrated {len(orders)} orders")
        
    except Exception as e:
        print(f"Error migrating orders: {str(e)}")
        pg_conn.rollback()

def migrate_order_items(sqlite_conn, pg_conn):
    """Migrate order item data"""
    try:
        sqlite_cursor = sqlite_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        # Get order items from SQLite
        sqlite_cursor.execute("""
            SELECT id, order_id, product_id, quantity, price, 
                   COALESCE(selected_color, ''), COALESCE(selected_size, '')
            FROM order_item
        """)
        order_items = sqlite_cursor.fetchall()
        
        if not order_items:
            print("No order items to migrate")
            return
        
        # Insert into PostgreSQL
        for item in order_items:
            pg_cursor.execute("""
                INSERT INTO order_item (id, order_id, product_id, quantity, price, 
                                      selected_color, selected_size)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, item)
        
        pg_conn.commit()
        print(f"Migrated {len(order_items)} order items")
        
    except Exception as e:
        print(f"Error migrating order items: {str(e)}")
        pg_conn.rollback()

def main():
    """Main migration function"""
    print("VelocityThreads Data Migration Tool")
    print("=" * 40)
    
    # Check if SQLite database exists
    sqlite_conn = connect_sqlite()
    if not sqlite_conn:
        print("No SQLite database found. Starting fresh with PostgreSQL.")
        return
    
    # Connect to PostgreSQL
    pg_conn = connect_postgresql()
    if not pg_conn:
        print("Cannot connect to PostgreSQL. Please check your configuration.")
        return
    
    try:
        print("Starting data migration...")
        
        # Migrate data in order (respecting foreign key constraints)
        migrate_users(sqlite_conn, pg_conn)
        migrate_products(sqlite_conn, pg_conn)
        migrate_orders(sqlite_conn, pg_conn)
        migrate_order_items(sqlite_conn, pg_conn)
        
        print("\n✅ Data migration completed successfully!")
        print("\nNote: Product images and payment screenshots are not migrated.")
        print("You may need to re-upload these files manually.")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {str(e)}")
    
    finally:
        sqlite_conn.close()
        pg_conn.close()

if __name__ == '__main__':
    main()
