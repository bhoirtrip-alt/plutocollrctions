#!/usr/bin/env python3
"""
Quick Start Script for VelocityThreads PostgreSQL Setup
This script automates the entire setup process for new users.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required!")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['flask', 'flask_sqlalchemy', 'flask_login', 'psycopg2', 'python-dotenv']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package}")
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ Dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True

def check_env_file():
    """Check if .env file exists and has correct format"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ .env file not found!")
        print("Creating .env file with default values...")
        
        env_content = """# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=velocity_threads
DB_USER=postgres
DB_PASSWORD=your_password_here

# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print("✅ .env file created!")
        print("⚠️  Please edit .env file with your actual PostgreSQL password!")
        return False
    
    print("✅ .env file found")
    
    # Check if password is still default
    with open('.env', 'r') as f:
        content = f.read()
        if 'your_password_here' in content:
            print("⚠️  Please update your PostgreSQL password in .env file!")
            return False
    
    return True

def setup_database():
    """Run database setup script"""
    print("\n🗄️  Setting up PostgreSQL database...")
    try:
        result = subprocess.run([sys.executable, 'setup_database.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Database setup completed!")
            return True
        else:
            print("❌ Database setup failed!")
            print("Error output:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error running database setup: {str(e)}")
        return False

def test_connection():
    """Test database connection"""
    print("\n🔌 Testing database connection...")
    try:
        result = subprocess.run([sys.executable, 'test_connection.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Database connection test passed!")
            return True
        else:
            print("❌ Database connection test failed!")
            print("Error output:", result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error testing connection: {str(e)}")
        return False

def start_application():
    """Start the Flask application"""
    print("\n🚀 Starting VelocityThreads application...")
    print("The application will be available at: http://localhost:5000")
    print("Admin credentials: admin / admin123")
    print("\nPress Ctrl+C to stop the application")
    
    try:
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {str(e)}")

def main():
    """Main setup function"""
    print("🚀 VelocityThreads PostgreSQL Quick Start")
    print("=" * 50)
    
    # Step 1: Check Python version
    if not check_python_version():
        return
    
    # Step 2: Check and install dependencies
    if not check_dependencies():
        return
    
    # Step 3: Check environment configuration
    if not check_env_file():
        print("\n📝 Please edit the .env file with your PostgreSQL credentials and run this script again.")
        return
    
    # Step 4: Setup database
    if not setup_database():
        return
    
    # Step 5: Test connection
    if not test_connection():
        return
    
    # Step 6: Start application
    start_application()

if __name__ == '__main__':
    main()
