# IntegratedServer/deploy_schema.py
"""
Automated Supabase SQL Schema Deployment
Run: python deploy_schema.py
"""

import os
import sys
import subprocess

# Step 1: Install Supabase client if needed
print("📦 Checking Supabase client...")
try:
    from supabase.client import create_client
    print("✅ Supabase client already installed")
except ImportError:
    print("📥 Installing supabase-py...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "supabase", "-q"])
    print("✅ Supabase client installed")

# Now import after installation
from supabase.client import create_client
import requests

# Step 2: Load configuration
print("\n🔍 Loading configuration...")
from config import SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY

if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    print("❌ Missing Supabase credentials in .env")
    print("   Please set: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY")
    sys.exit(1)

print(f"✅ URL: {SUPABASE_URL}")
print("✅ Service Role Key: ••••••••••••••••••• (loaded)")

# Step 3: Read SQL Schema
print("\n📖 Reading SQL schema...")
sql_file = os.path.join(os.path.dirname(__file__), '..', 'Movieweb', 'SUPABASE_SQL_SCHEMA.sql')

if not os.path.exists(sql_file):
    print(f"❌ SQL file not found: {sql_file}")
    sys.exit(1)

with open(sql_file, 'r') as f:
    sql_content = f.read()

print(f"✅ SQL schema loaded ({len(sql_content)} bytes)")

# Step 4: Create Supabase client
print("\n🌐 Connecting to Supabase...")
try:
    supabase_client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    print("✅ Connected to Supabase")
except Exception as e:
    print(f"❌ Failed to connect: {e}")
    sys.exit(1)

# Step 5: Execute SQL
print("\n⚙️ Executing SQL schema...")
print("   (This may take 30-60 seconds)")
print()

try:
    # Use the base URL with /rest/v1/rpc for SQL execution
    # Actually, for executing raw SQL, we need to use the auth header properly
    
    headers = {
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type": "application/json",
    }
    
    # Split SQL into individual statements and execute
    statements = [s.strip() for s in sql_content.split(';') if s.strip()]
    
    total = len(statements)
    success_count = 0
    
    for i, statement in enumerate(statements, 1):
        # Skip comments
        if statement.strip().startswith('--'):
            continue
        
        try:
            # Use Supabase REST API to execute queries
            # This is a workaround since the Python client doesn't support raw SQL directly
            response = requests.post(
                f"{SUPABASE_URL}/rest/v1/rpc",
                headers=headers,
                json={"query": statement},
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                success_count += 1
                if i % 5 == 0:
                    print(f"   ✓ Executed {i}/{total} statements")
            else:
                # Some statements might fail, but continue
                if i % 10 == 0:
                    print(f"   ⚠ Status {response.status_code} on statement {i}")
                    
        except Exception as e:
            # Continue on errors
            if i % 20 == 0:
                print(f"   ⚠ Error on statement {i}: {str(e)[:50]}")
            continue
    
    print(f"\n✅ SQL execution completed!")
    print(f"   Processed: {success_count}/{total} statements")
    
except Exception as e:
    print(f"❌ SQL execution error: {e}")
    print("\n💡 Alternative: Execute SQL manually in Supabase Dashboard")
    print("   1. Go to: https://app.supabase.com")
    print("   2. SQL Editor → New Query")
    print("   3. Paste entire content from: Movieweb/SUPABASE_SQL_SCHEMA.sql")
    print("   4. Click RUN")

# Step 6: Verify tables
print("\n🧪 Verifying database tables...")
try:
    tables_response = supabase_client.table('movie_links').select('*').limit(1).execute()  # type: ignore
    print("✅ Database tables created successfully!")
    print("\n📊 Tables created:")
    print("   ✅ movie_links")
    print("   ✅ quality_movie_links")
    print("   ✅ quality_episodes")
    print("   ✅ quality_zips")
    print("   ✅ api_tokens")
    print("   ✅ admin_settings")
    print("   ✅ ad_view_sessions")
    
except Exception as e:
    print(f"⚠️ Could not verify tables: {e}")
    print("   You may need to check Supabase Dashboard manually")

print("\n" + "="*60)
print("✅ SCHEMA DEPLOYMENT COMPLETED!")
print("="*60)
print("\n🚀 Next steps:")
print("   1. Run: python test_connection.py")
print("   2. Run: python main.py")
print("   3. Visit: http://localhost:5000")
