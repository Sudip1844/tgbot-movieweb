# IntegratedServer/test_connection.py
"""
Test database connection and Supabase configuration
Run: python test_connection.py
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

def test_config():
    """Test if config loads correctly"""
    print("🔍 Testing configuration...")
    try:
        from config import (
            SUPABASE_URL, SUPABASE_DB_HOST,
            DATABASE_URL, OWNER_ID
        )
        
        print("✅ Config loaded successfully")
        print(f"   Supabase URL: {SUPABASE_URL}")
        print(f"   DB Host: {SUPABASE_DB_HOST}")
        print(f"   Bot Token: {'*' * 20}... (hidden)")
        print(f"   Owner ID: {OWNER_ID}")
        
        if not DATABASE_URL:
            print("❌ DATABASE_URL is empty!")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🔌 Testing database connection...")
    try:
        from database import engine
        
        with engine.connect() as conn:
            conn.exec_driver_sql("SELECT 1")
            print("✅ Database connection successful!")
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\n📋 Debugging info:")
        print(f"   Make sure .env file exists in IntegratedServer/")
        print(f"   Check database credentials:")
        from config import SUPABASE_DB_HOST, SUPABASE_DB_USER
        print(f"   Host: {SUPABASE_DB_HOST}")
        print(f"   User: {SUPABASE_DB_USER}")
        return False

def test_tables():
    """Test if database tables exist"""
    print("\n📊 Testing database tables...")
    try:
        from database import SessionLocal
        from database.models import AdminSetting
        
        session = SessionLocal()
        
        # Count admin settings
        admin_count = session.query(AdminSetting).count()
        print(f"✅ Database tables accessible")
        print(f"   Admin settings: {admin_count} record(s)")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Table access error: {e}")
        print("\n💡 Did you run SQL schema in Supabase?")
        print("   Go to: SQL Editor → Run SUPABASE_SQL_SCHEMA.sql")
        return False

def test_flask_app():
    """Test if Flask app can be created"""
    print("\n🌐 Testing Flask app...")
    try:
        from server.app import create_app
        
        app = create_app()
        print("✅ Flask app created successfully!")
        
        # Test health endpoint
        with app.test_client() as client:
            response = client.get('/api/health')
            if response.status_code == 200:
                print(f"✅ Health endpoint works: {response.status_code}")
                return True
            else:
                print(f"❌ Health endpoint failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        return False

def main():
    """Run all tests"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║           MovieZone Connection Test                        ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        ("Configuration", test_config),
        ("Database Connection", test_database_connection),
        ("Database Tables", test_tables),
        ("Flask App", test_flask_app),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Unexpected error in {name}: {e}")
            failed += 1
    
    print(f"""
    ╔════════════════════════════════════════════════════════════╗
    ║                      Test Results                          ║
    ├────────────────────────────────────────────────────────────┤
    ║  ✅ Passed: {passed}                                          ║
    ║  ❌ Failed: {failed}                                          ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    if failed == 0:
        print("🎉 All tests passed! Server is ready to run!")
        print("\n📌 Start server with: python main.py")
        return 0
    else:
        print("⚠️ Some tests failed. Check the errors above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
