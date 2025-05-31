"""
Test suite for SQL Assistant
Run this to verify that all components are working correctly
"""

import unittest
import sqlite3
import pandas as pd
import os
import sys
from pathlib import Path

# Add the current directory to the path
sys.path.append(str(Path(__file__).parent))

class TestSQLAssistant(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_db_path = "test_database.db"
        self.create_test_database()
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
    
    def create_test_database(self):
        """Create a simple test database"""
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE test_employees (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                department TEXT NOT NULL,
                salary REAL NOT NULL
            )
        ''')
        
        test_data = [
            (1, 'John Doe', 'Engineering', 75000),
            (2, 'Jane Smith', 'Marketing', 65000),
            (3, 'Bob Johnson', 'Sales', 55000)
        ]
        
        cursor.executemany('INSERT INTO test_employees VALUES (?, ?, ?, ?)', test_data)
        conn.commit()
        conn.close()
    
    def test_database_creation(self):
        """Test that database was created successfully"""
        self.assertTrue(os.path.exists(self.test_db_path))
        
        conn = sqlite3.connect(self.test_db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM test_employees")
        count = cursor.fetchone()[0]
        conn.close()
        
        self.assertEqual(count, 3)
    
    def test_sql_query_execution(self):
        """Test basic SQL query execution"""
        conn = sqlite3.connect(self.test_db_path)
        df = pd.read_sql_query("SELECT * FROM test_employees", conn)
        conn.close()
        
        self.assertEqual(len(df), 3)
        self.assertIn('name', df.columns)
        self.assertIn('department', df.columns)
        self.assertIn('salary', df.columns)
    
    def test_imports(self):
        """Test that all required packages can be imported"""
        try:
            import streamlit
            import langchain
            import pandas
            import plotly
            import sqlalchemy
            from langchain_groq import ChatGroq
            print("✅ All imports successful")
        except ImportError as e:
            self.fail(f"Import failed: {e}")
    
    def test_config_file(self):
        """Test that configuration file exists and is valid"""
        try:
            import config
            self.assertTrue(hasattr(config, 'DEFAULT_MODEL'))
            self.assertTrue(hasattr(config, 'CHART_TYPES'))
            self.assertTrue(hasattr(config, 'SAMPLE_QUERIES'))
            print("✅ Configuration file is valid")
        except ImportError:
            self.fail("Configuration file not found or invalid")
    
    def test_sample_database_creation(self):
        """Test the sample database creation script"""
        try:
            from create_sample_db import create_extended_sample_database
            
            # Remove existing sample db if it exists
            if os.path.exists('extended_sample_data.db'):
                os.remove('extended_sample_data.db')
            
            create_extended_sample_database()
            
            # Verify the database was created
            self.assertTrue(os.path.exists('extended_sample_data.db'))
            
            # Verify tables exist
            conn = sqlite3.connect('extended_sample_data.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            expected_tables = ['customers', 'products', 'employees', 'orders', 'order_details']
            for table in expected_tables:
                self.assertIn(table, tables)
            
            conn.close()
            print("✅ Sample database creation successful")
            
        except Exception as e:
            self.fail(f"Sample database creation failed: {e}")
    
    def test_visualization_functions(self):
        """Test visualization capabilities"""
        try:
            import plotly.express as px
            import plotly.graph_objects as go
            
            # Create test data
            test_data = pd.DataFrame({
                'category': ['A', 'B', 'C'],
                'values': [10, 20, 15]
            })
            
            # Test different chart types
            fig_bar = px.bar(test_data, x='category', y='values')
            fig_pie = px.pie(test_data, names='category', values='values')
            
            self.assertIsNotNone(fig_bar)
            self.assertIsNotNone(fig_pie)
            print("✅ Visualization functions working")
            
        except Exception as e:
            self.fail(f"Visualization test failed: {e}")

def run_comprehensive_test():
    """Run all tests and provide a summary"""
    print("🧪 Running SQL Assistant Test Suite")
    print("=" * 50)
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    print("\n" + "=" * 50)
    print("🔍 Additional System Checks")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    else:
        print(f"❌ Python version too old: {python_version}")
    
    # Check if environment file exists
    if os.path.exists('.env'):
        print("✅ Environment file exists")
        
        # Check if API key is set
        from dotenv import load_dotenv
        load_dotenv()
        
        if os.getenv('GROQ_API_KEY'):
            print("✅ Groq API key is configured")
        else:
            print("⚠️  Groq API key not set in environment")
    else:
        print("⚠️  Environment file not found")
    
    # Check if sample database exists
    if os.path.exists('sample_data.db') or os.path.exists('extended_sample_data.db'):
        print("✅ Sample database available")
    else:
        print("⚠️  Sample database not found")
    
    print("\n🎉 Test suite completed!")

if __name__ == "__main__":
    run_comprehensive_test()
