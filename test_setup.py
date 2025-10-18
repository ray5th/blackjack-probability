#!/usr/bin/env python3
"""
Quick test script to verify the Blackjack Pro setup
"""

import sys
import os
import sqlite3
from pathlib import Path

def test_database():
    """Test database connection and schema"""
    print("🔍 Testing database...")
    
    try:
        conn = sqlite3.connect("blackjack.db")
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        expected_tables = ['users', 'hands', 'analytics', 'alembic_version']
        missing_tables = [t for t in expected_tables if t not in tables]
        
        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
            return False
        
        print(f"✅ Database schema verified ({len(tables)} tables)")
        
        # Test inserting a sample user
        cursor.execute("""
            INSERT INTO users (username, email, hashed_password) 
            VALUES (?, ?, ?)
        """, ("test_user", "test@example.com", "hashed_password_123"))
        
        conn.commit()
        
        # Verify the insert
        cursor.execute("SELECT username FROM users WHERE username = ?", ("test_user",))
        result = cursor.fetchone()
        
        if result:
            print("✅ Database write/read test passed")
            
            # Clean up test data
            cursor.execute("DELETE FROM users WHERE username = ?", ("test_user",))
            conn.commit()
        else:
            print("❌ Database write/read test failed")
            return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_imports():
    """Test importing key modules"""
    print("🔍 Testing module imports...")
    
    try:
        # Test backend imports
        sys.path.append('.')
        from database.models import User, Hand, Analytics
        from database.database import get_db
        print("✅ Database models imported successfully")
        
        from analytics.monte_carlo import BlackjackAnalytics
        print("✅ Analytics module imported successfully")
        
        from privacy.telemetry import PrivacyManager, TelemetryCollector
        print("✅ Privacy modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_analytics():
    """Test analytics functionality"""
    print("🔍 Testing analytics...")
    
    try:
        from analytics.monte_carlo import BlackjackAnalytics
        
        analyzer = BlackjackAnalytics()
        
        # Test basic functionality
        deck = analyzer.create_deck()
        if len(deck) != 52:
            print(f"❌ Deck creation failed: expected 52 cards, got {len(deck)}")
            return False
        
        # Test hand value calculation
        test_hand = ['ace_of_hearts', '10_of_spades']
        value = analyzer.calculate_hand_value(test_hand)
        if value != 21:
            print(f"❌ Hand value calculation failed: expected 21, got {value}")
            return False
        
        print("✅ Analytics basic functionality verified")
        return True
        
    except Exception as e:
        print(f"❌ Analytics test failed: {e}")
        return False

def test_privacy():
    """Test privacy controls"""
    print("🔍 Testing privacy controls...")
    
    try:
        from privacy.telemetry import PrivacyManager, PrivacyMode, DataCategory
        
        # Test different privacy modes
        privacy = PrivacyManager(PrivacyMode.STANDARD)
        if not privacy.should_collect_data(DataCategory.GAMEPLAY):
            print("❌ Standard mode should allow gameplay data collection")
            return False
        
        privacy = PrivacyManager(PrivacyMode.EPHEMERAL)
        if privacy.should_collect_data(DataCategory.GAMEPLAY):
            print("❌ Ephemeral mode should not allow gameplay data collection")
            return False
        
        # Test anonymization
        user_id = "test_user_123"
        anon_id = privacy.anonymize_user_data(user_id)
        if anon_id == user_id:
            print("❌ User ID should be anonymized in ephemeral mode")
            return False
        
        print("✅ Privacy controls verified")
        return True
        
    except Exception as e:
        print(f"❌ Privacy test failed: {e}")
        return False

def test_file_structure():
    """Test that all required files exist"""
    print("🔍 Testing file structure...")
    
    required_files = [
        "requirements.txt",
        "backend/main.py",
        "database/models.py",
        "database/database.py",
        "analytics/monte_carlo.py",
        "privacy/telemetry.py",
        "wasm-engine/blackjack_engine.cpp",
        "frontend/game.html",
        "frontend/game.js",
        "frontend/game.css",
        "alembic.ini",
        "blackjack.db"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def main():
    """Run all tests"""
    print("🃏 Blackjack Pro - Setup Verification")
    print("=" * 50)
    
    tests = [
        ("File structure", test_file_structure),
        ("Module imports", test_imports),
        ("Database functionality", test_database),
        ("Analytics functionality", test_analytics),
        ("Privacy controls", test_privacy),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_function in tests:
        print(f"\n📋 {test_name}")
        if test_function():
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Your Blackjack Pro setup is ready.")
        print("\n🚀 Quick start:")
        print("1. cd backend && python main.py")
        print("2. Open frontend/enhanced_index.html in your browser")
    else:
        print("⚠️  Some tests failed. Please check the setup.")
        sys.exit(1)

if __name__ == "__main__":
    main()