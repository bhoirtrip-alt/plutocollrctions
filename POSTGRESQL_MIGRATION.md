# PostgreSQL Migration Guide for VelocityThreads

This guide will help you migrate from SQLite to PostgreSQL for the VelocityThreads e-commerce application.

## Prerequisites

1. **PostgreSQL Server**: Make sure PostgreSQL is installed and running on your system
2. **Python Dependencies**: Install the required Python packages

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Database Connection

Edit the `.env` file with your PostgreSQL credentials:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=velocity_threads
DB_USER=postgres
DB_PASSWORD=your_actual_password_here

# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

**Important**: Replace `your_actual_password_here` with your actual PostgreSQL password.

### 3. Create PostgreSQL Database

Run the database setup script:

```bash
python setup_database.py
```

This script will:
- Create the `velocity_threads` database if it doesn't exist
- Test the connection to ensure everything is working

### 4. Start the Application

```bash
python app.py
```

The application will:
- Connect to PostgreSQL
- Create all necessary tables
- Create an admin user (username: `admin`, password: `admin123`)

## Database Schema

The application will automatically create the following tables:

- **user**: User accounts and authentication
- **product**: Product information
- **product_image**: Product images
- **order**: Customer orders
- **order_item**: Individual items in orders

## Admin Access

After the first run, you can access the admin panel with:
- **Username**: `admin`
- **Password**: `admin123`

**Important**: Change the admin password after first login for security.

## Troubleshooting

### Connection Issues

1. **Check PostgreSQL Service**: Ensure PostgreSQL is running
2. **Verify Credentials**: Double-check username, password, and database name in `.env`
3. **Check Port**: Default PostgreSQL port is 5432
4. **Network Access**: Ensure PostgreSQL accepts connections from your application

### Common Errors

- **"connection refused"**: PostgreSQL service not running
- **"authentication failed"**: Wrong username/password
- **"database does not exist"**: Run `setup_database.py` first

### Reset Database

If you need to start fresh:

```sql
-- Connect to PostgreSQL and run:
DROP DATABASE IF EXISTS velocity_threads;
CREATE DATABASE velocity_threads;
```

Then run the application again to recreate tables.

## Features Preserved

All original functionality is preserved:
- User registration and authentication
- Product management
- Shopping cart
- Order processing
- Admin dashboard
- Payment handling
- Image management

## Performance Benefits

PostgreSQL provides:
- Better concurrent user handling
- Advanced indexing capabilities
- ACID compliance
- Better scalability
- Advanced data types and constraints

## Support

If you encounter issues:
1. Check the PostgreSQL logs
2. Verify your `.env` configuration
3. Ensure all dependencies are installed
4. Check that PostgreSQL is running and accessible
