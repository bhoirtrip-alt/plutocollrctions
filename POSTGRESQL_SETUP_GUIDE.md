# PostgreSQL Setup Guide for VelocityThreads

This guide will help you set up PostgreSQL for the VelocityThreads e-commerce application and fix any database issues.

## Prerequisites

1. **PostgreSQL Server**: Make sure PostgreSQL is installed and running on your system
2. **Python Dependencies**: Install the required Python packages

## Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Configure Database Connection

### Create Environment File

Create a `.env` file in the project root with your PostgreSQL credentials:

```env
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=velocity_threads
DB_USER=postgres
DB_PASSWORD=your_actual_password_here

# Flask Configuration
SECRET_KEY=your-secret-key-here-change-this-in-production
FLASK_ENV=development
```

**Important**: Replace `your_actual_password_here` with your actual PostgreSQL password.

## Step 3: Create PostgreSQL Database

Run the database setup script:

```bash
python setup_database.py
```

This script will:
- Create the `velocity_threads` database if it doesn't exist
- Test the connection to ensure everything is working

## Step 4: Fix Database Schema Issues

### Run Database Migration (IMPORTANT!)

If you're experiencing field size errors like:
```
sqlalchemy.exc.DataError: (psycopg2.errors.StringDataRightTruncation) value too long for type character varying(20)
```

Run the migration script to fix field size issues:

```bash
python migrate_database_schema.py
```

This script will:
- Update `order_number` field from VARCHAR(20) to VARCHAR(30)
- Update `phone` field from VARCHAR(20) to VARCHAR(15)
- Check for other potential field size issues

## Step 5: Run Database Health Check

Run the comprehensive health check to ensure everything is working:

```bash
python database_health_check.py
```

This script will:
- Check database connection
- Verify table structure
- Identify field size issues
- Check data integrity
- Look for orphaned records

## Step 6: Start the Application

```bash
python app.py
```

The application will:
- Connect to PostgreSQL
- Create all necessary tables (if they don't exist)
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

### Common Errors and Solutions

#### 1. Field Size Errors
**Error**: `StringDataRightTruncation: value too long for type character varying(20)`

**Solution**: Run the migration script:
```bash
python migrate_database_schema.py
```

#### 2. Connection Issues
**Error**: `connection refused` or `authentication failed`

**Solutions**:
1. Check PostgreSQL service is running
2. Verify credentials in `.env` file
3. Ensure PostgreSQL accepts connections from your application
4. Check if the database exists

#### 3. Database Not Found
**Error**: `database "velocity_threads" does not exist`

**Solution**: Run the setup script:
```bash
python setup_database.py
```

### Reset Database

If you need to start fresh:

```sql
-- Connect to PostgreSQL and run:
DROP DATABASE IF EXISTS velocity_threads;
CREATE DATABASE velocity_threads;
```

Then run the application again to recreate tables.

### Manual Field Size Fixes

If the migration script doesn't work, you can manually fix field sizes:

```sql
-- Connect to your database and run:
ALTER TABLE "order" ALTER COLUMN order_number TYPE VARCHAR(30);
ALTER TABLE "order" ALTER COLUMN phone TYPE VARCHAR(15);
```

## Performance Optimization

### PostgreSQL Configuration

For better performance, consider these PostgreSQL settings in `postgresql.conf`:

```ini
# Memory settings
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB

# Connection settings
max_connections = 100

# Logging
log_statement = 'none'
log_min_duration_statement = 1000
```

### Indexes

The application automatically creates indexes for:
- Primary keys
- Foreign keys
- Unique constraints

## Monitoring

### Check Database Health Regularly

Run the health check script periodically:

```bash
python database_health_check.py
```

### Monitor Logs

Check PostgreSQL logs for errors:
- Windows: Event Viewer → Windows Logs → Application
- Linux: `/var/log/postgresql/`

## Backup and Recovery

### Create Backup

```bash
pg_dump -h localhost -U postgres -d velocity_threads > backup.sql
```

### Restore Backup

```bash
psql -h localhost -U postgres -d velocity_threads < backup.sql
```

## Security Best Practices

1. **Change Default Passwords**: Update admin and database passwords
2. **Use Environment Variables**: Never hardcode credentials
3. **Limit Database Access**: Use specific database users with minimal privileges
4. **Regular Updates**: Keep PostgreSQL and dependencies updated
5. **Backup Regularly**: Set up automated backups

## Support

If you encounter issues:

1. Run the health check script: `python database_health_check.py`
2. Check PostgreSQL logs
3. Verify your `.env` configuration
4. Ensure all dependencies are installed
5. Check that PostgreSQL is running and accessible

## Migration from SQLite

If you're migrating from SQLite:

1. Export data from SQLite database
2. Create PostgreSQL database
3. Import data to PostgreSQL
4. Update application configuration
5. Test all functionality

The application is designed to work seamlessly with PostgreSQL and includes all necessary migration tools.
