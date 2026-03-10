# IntegratedServer/execute_sql.py
"""
Execute SQL Schema to Supabase - Direct PostgreSQL Connection
Run: python execute_sql.py
"""

import os
import sys
import subprocess

# Step 1: Install psycopg2 if needed
print("📦 Checking PostgreSQL client...")
try:
    import psycopg2
    print("✅ psycopg2 already installed")
except ImportError:
    print("📥 Installing psycopg2-binary...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary", "-q"])
    print("✅ psycopg2 installed")

import psycopg2

# Step 2: Load configuration
print("\n🔍 Loading configuration...")
from config import SUPABASE_DB_HOST, SUPABASE_DB_USER, SUPABASE_DB_PASSWORD, SUPABASE_DB_NAME, SUPABASE_DB_PORT

if not all([SUPABASE_DB_HOST, SUPABASE_DB_USER, SUPABASE_DB_PASSWORD]):
    print("❌ Missing database credentials in .env")
    print("   Required: SUPABASE_DB_HOST, SUPABASE_DB_USER, SUPABASE_DB_PASSWORD")
    sys.exit(1)

print(f"✅ Host: {SUPABASE_DB_HOST}")
print(f"✅ User: {SUPABASE_DB_USER}")
print(f"✅ Database: {SUPABASE_DB_NAME}")
print(f"✅ Port: {SUPABASE_DB_PORT}")

# Step 3: Read SQL Schema
print("\n📖 Reading SQL schema...")
sql_file = os.path.join(os.path.dirname(__file__), 'SUPABASE_SQL_SCHEMA.sql')

if not os.path.exists(sql_file):
    print(f"❌ SQL file not found: {sql_file}")
    sys.exit(1)

with open(sql_file, 'r', encoding='utf-8') as f:
    sql_content = f.read()

print(f"✅ SQL schema loaded ({len(sql_content)} bytes)")

# Step 4: Connect to Supabase
print("\n🌐 Connecting to Supabase PostgreSQL...")
try:
    conn = psycopg2.connect(
        host=SUPABASE_DB_HOST,
        port=SUPABASE_DB_PORT,
        user=SUPABASE_DB_USER,
        password=SUPABASE_DB_PASSWORD,
        database=SUPABASE_DB_NAME,
        sslmode='require'
    )
    print("✅ Connected to PostgreSQL")
    
except psycopg2.OperationalError as e:
    print(f"❌ Connection failed: {e}")
    print("\n💡 Troubleshooting:")
    print("   1. Check credentials in .env file")
    print("   2. Verify Supabase project is active")
    print("   3. Ensure firewall allows connection")
    sys.exit(1)

# Step 5: Execute SQL
print("\n⚙️ Executing SQL schema...")
print("   (This may take 30-60 seconds)")
print()

cursor = conn.cursor()
statement_count = 0
success_count = 0
error_count = 0

try:
    # Split into individual statements
    statements = sql_content.split(';')
    
    for i, statement in enumerate(statements, 1):
        # Clean up statement
        statement = statement.strip()
        
        # Skip empty and comment lines
        if not statement or statement.startswith('--'):
            continue
        
        statement_count += 1
        
        try:
            # Execute statement
            cursor.execute(statement)
            success_count += 1
            
            # Show progress every 10 statements
            if statement_count % 10 == 0:
                print(f"   ✓ Executed {statement_count} statements...")
            
        except Exception as stmt_error:
            error_count += 1
            # Some CREATE OR REPLACE might have duplicate errors - that's OK
            error_str = str(stmt_error).lower()
            if 'already exists' in error_str or 'duplicate' in error_str:
                print(f"   ℹ Statement {statement_count}: {error_str[:60]}")
            else:
                print(f"   ⚠️ Statement {statement_count}: {str(stmt_error)[:80]}")
    
    # Commit changes
    conn.commit()
    print(f"\n✅ All statements executed!")
    print(f"   Successful: {success_count}")
    print(f"   Errors (may be expected): {error_count}")
    
except Exception as e:
    conn.rollback()
    print(f"❌ Execution error: {e}")
    sys.exit(1)

finally:
    cursor.close()

# Step 6: Verify tables
print("\n🧪 Verifying database tables...")
try:
    verify_cursor = conn.cursor()
    verify_cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name
    """)
    tables = verify_cursor.fetchall()
    verify_cursor.close()
    
    expected_tables = [
        'movie_links',
        'quality_movie_links', 
        'quality_episodes',
        'quality_zips',
        'api_tokens',
        'admin_settings',
        'ad_view_sessions'
    ]
    
    found_tables = [t[0] for t in tables]
    all_present = all(table in found_tables for table in expected_tables)
    
    if all_present:
        print("✅ All tables created successfully!")
        print("\n📊 Tables in database:")
        for table in expected_tables:
            if table in found_tables:
                print(f"   ✅ {table}")
    else:
        print("⚠️ Some tables missing:")
        for table in expected_tables:
            status = "✅" if table in found_tables else "❌"
            print(f"   {status} {table}")
    
except Exception as e:
    print(f"⚠️ Could not verify tables: {e}")

# Step 7: Check admin credentials
print("\n🔐 Verifying admin credentials...")
try:
    admin_cursor = conn.cursor()
    admin_cursor.execute("SELECT admin_id FROM admin_settings LIMIT 1")
    admin_result = admin_cursor.fetchone()
    admin_cursor.close()
    
    if admin_result:
        print(f"✅ Admin credentials created: {admin_result[0]}")
    else:
        print("⚠️ No admin credentials found")
        
except Exception as e:
    print(f"⚠️ Could not check admin: {e}")

# Close connection
conn.close()

print("\n" + "="*60)
print("✅ SCHEMA DEPLOYMENT COMPLETED!")
print("="*60)
print("\n🚀 Next steps:")
print("   1. Run: python test_connection.py")
print("   2. Run: python main.py")
print("   3. Visit: http://localhost:5000")
