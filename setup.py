#!/usr/bin/env python3
"""
Blackjack Pro Setup Script
Initializes the development environment and database
"""

import os
import sys
import subprocess
import sqlite3
from pathlib import Path

def run_command(command, description):
    """Run a shell command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_virtual_environment():
    """Create and activate virtual environment"""
    if not os.path.exists("venv"):
        return run_command("python -m venv venv", "Creating virtual environment")
    else:
        print("✅ Virtual environment already exists")
        return True

def install_dependencies():
    """Install Python dependencies"""
    activate_script = "venv/bin/activate" if os.name != 'nt' else "venv\\Scripts\\activate"
    
    if os.name == 'nt':
        pip_command = "venv\\Scripts\\pip install -r requirements.txt"
    else:
        pip_command = "source venv/bin/activate && pip install -r requirements.txt"
    
    return run_command(pip_command, "Installing Python dependencies")

def setup_database():
    """Initialize the database"""
    print("🔄 Setting up database...")
    
    # Create database directory if it doesn't exist
    os.makedirs("database", exist_ok=True)
    
    # Initialize Alembic if not already done
    if not os.path.exists("alembic"):
        if not run_command("alembic init alembic", "Initializing Alembic"):
            return False
    
    # Create initial migration if needed
    if not os.path.exists("alembic/versions"):
        os.makedirs("alembic/versions", exist_ok=True)
    
    # Check if database exists, create if not
    db_path = "blackjack.db"
    if not os.path.exists(db_path):
        print("📊 Creating initial database...")
        try:
            # Create empty database file
            conn = sqlite3.connect(db_path)
            conn.close()
            print("✅ Database file created")
        except Exception as e:
            print(f"❌ Failed to create database: {e}")
            return False
    
    # Run migrations
    return run_command("alembic upgrade head", "Running database migrations")

def build_wasm_engine():
    """Build WebAssembly engine if Emscripten is available"""
    print("🔄 Checking for Emscripten...")
    
    try:
        subprocess.run("emcc --version", shell=True, check=True, capture_output=True)
        print("✅ Emscripten found, building WebAssembly engine...")
        
        os.chdir("wasm-engine")
        success = run_command("chmod +x build.sh && ./build.sh", "Building WASM engine")
        os.chdir("..")
        
        return success
    except subprocess.CalledProcessError:
        print("⚠️  Emscripten not found, skipping WebAssembly build")
        print("   Install from: https://emscripten.org/docs/getting_started/downloads.html")
        return True  # Not a critical failure

def create_sample_config():
    """Create sample configuration files"""
    print("🔄 Creating sample configuration...")
    
    # Create .env file if it doesn't exist
    env_content = """# Blackjack Pro Configuration
DATABASE_URL=sqlite:///./blackjack.db
API_HOST=0.0.0.0
API_PORT=8000
DEFAULT_PRIVACY_MODE=standard
TELEMETRY_ENABLED=true
"""
    
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Created .env configuration file")
    else:
        print("✅ Configuration file already exists")
    
    return True

def run_tests():
    """Run basic tests to verify setup"""
    print("🔄 Running basic tests...")
    
    # Test database connection
    try:
        conn = sqlite3.connect("blackjack.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        if tables:
            print(f"✅ Database connection successful, {len(tables)} tables found")
        else:
            print("⚠️  Database connected but no tables found")
        
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🃏 Blackjack Pro Setup")
    print("=" * 50)
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Creating virtual environment", create_virtual_environment),
        ("Installing dependencies", install_dependencies),
        ("Setting up database", setup_database),
        ("Building WebAssembly engine", build_wasm_engine),
        ("Creating configuration", create_sample_config),
        ("Running tests", run_tests),
    ]
    
    failed_steps = []
    
    for step_name, step_function in steps:
        if not step_function():
            failed_steps.append(step_name)
    
    print("\n" + "=" * 50)
    
    if not failed_steps:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Activate virtual environment:")
        if os.name == 'nt':
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        print("2. Start the backend server:")
        print("   cd backend && python main.py")
        print("3. Open frontend/enhanced_index.html in your browser")
        print("\n📚 See README.md for detailed usage instructions")
    else:
        print("⚠️  Setup completed with some issues:")
        for step in failed_steps:
            print(f"   - {step}")
        print("\n🔧 Please resolve these issues and run setup again")
        sys.exit(1)

if __name__ == "__main__":
    main()