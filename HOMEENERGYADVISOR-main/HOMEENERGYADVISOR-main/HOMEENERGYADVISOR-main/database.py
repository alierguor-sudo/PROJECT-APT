"""
Database module for Home Energy-Saving Advisor
Handles SQLite database setup and CRUD operations
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "energy_advisor.db"


class Database:
    """SQLite database manager for energy advisor"""
    
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get a database connection"""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Household table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS households (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                members INTEGER,
                square_feet INTEGER,
                climate_zone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Energy consumption table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS energy_consumption (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                household_id INTEGER NOT NULL,
                month TEXT,
                electricity_kwh REAL,
                gas_therms REAL,
                water_gallons REAL,
                recorded_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (household_id) REFERENCES households(id)
            )
        ''')
        
        # Recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                household_id INTEGER NOT NULL,
                rule_id TEXT,
                category TEXT,
                recommendation TEXT,
                priority TEXT,
                estimated_savings_percent REAL,
                description TEXT,
                implementation_cost TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (household_id) REFERENCES households(id)
            )
        ''')
        
        # Rule tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rule_triggers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                household_id INTEGER NOT NULL,
                rule_id TEXT NOT NULL,
                triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                rule_details TEXT,
                FOREIGN KEY (household_id) REFERENCES households(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_household(self, name, members, square_feet, climate_zone):
        """Add a new household profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO households (name, members, square_feet, climate_zone)
            VALUES (?, ?, ?, ?)
        ''', (name, members, square_feet, climate_zone))
        
        conn.commit()
        household_id = cursor.lastrowid
        conn.close()
        return household_id
    
    def get_household(self, household_id):
        """Retrieve household profile"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM households WHERE id = ?', (household_id,))
        household = cursor.fetchone()
        conn.close()
        return dict(household) if household else None
    
    def add_energy_data(self, household_id, month, electricity_kwh, gas_therms, water_gallons):
        """Add energy consumption data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO energy_consumption 
            (household_id, month, electricity_kwh, gas_therms, water_gallons)
            VALUES (?, ?, ?, ?, ?)
        ''', (household_id, month, electricity_kwh, gas_therms, water_gallons))
        
        conn.commit()
        conn.close()
    
    def get_energy_data(self, household_id):
        """Get all energy consumption data for a household"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM energy_consumption 
            WHERE household_id = ? 
            ORDER BY recorded_date DESC
        ''', (household_id,))
        data = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return data
    
    def add_recommendation(self, household_id, rule_id, category, recommendation, 
                          priority, estimated_savings_percent, implementation_cost, description):
        """Add a recommendation for a household"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO recommendations 
            (household_id, rule_id, category, recommendation, priority, 
             estimated_savings_percent, implementation_cost, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (household_id, rule_id, category, recommendation, priority,
              estimated_savings_percent, implementation_cost, description))
        
        conn.commit()
        conn.close()
    
    def get_recommendations(self, household_id):
        """Get all recommendations for a household"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM recommendations 
            WHERE household_id = ? 
            ORDER BY 
                CASE priority 
                    WHEN 'High' THEN 1 
                    WHEN 'Medium' THEN 2 
                    WHEN 'Low' THEN 3 
                END, created_at DESC
        ''', (household_id,))
        recommendations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return recommendations
    
    def clear_recommendations(self, household_id):
        """Clear old recommendations for re-evaluation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM recommendations WHERE household_id = ?', (household_id,))
        conn.commit()
        conn.close()
    
    def log_rule_trigger(self, household_id, rule_id, rule_details):
        """Log when a rule is triggered"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO rule_triggers (household_id, rule_id, rule_details)
            VALUES (?, ?, ?)
        ''', (household_id, rule_id, json.dumps(rule_details)))
        conn.commit()
        conn.close()
