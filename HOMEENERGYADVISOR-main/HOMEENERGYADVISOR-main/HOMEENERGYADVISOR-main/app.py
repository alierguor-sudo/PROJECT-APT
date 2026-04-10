"""
Flask Web Interface for Home Energy-Saving Advisor
Provides REST API and web dashboard for the energy advisor system
"""

from flask import Flask, render_template, request, jsonify
from database import Database
from rules_engine import RulesEngine
from knowledge_base import KnowledgeBase
import json


app = Flask(__name__)
db = Database()
engine = RulesEngine(db)
kb = KnowledgeBase()


# ============ API ENDPOINTS ============

@app.route('/api/household', methods=['POST'])
def create_household():
    """Create a new household profile"""
    data = request.json
    
    try:
        household_id = db.add_household(
            name=data['name'],
            members=data.get('members', 0),
            square_feet=data.get('square_feet', 0),
            climate_zone=data.get('climate_zone', 'Moderate')
        )
        
        return jsonify({
            'status': 'success',
            'household_id': household_id,
            'message': f'Household "{data["name"]}" created successfully'
        }), 201
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/household/<int:household_id>', methods=['GET'])
def get_household(household_id):
    """Get household profile"""
    try:
        household = db.get_household(household_id)
        if not household:
            return jsonify({'status': 'error', 'message': 'Household not found'}), 404
        
        return jsonify({
            'status': 'success',
            'household': dict(household)
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/energy-data/<int:household_id>', methods=['POST'])
def add_energy_data(household_id):
    """Add energy consumption data for a household"""
    data = request.json
    
    try:
        db.add_energy_data(
            household_id=household_id,
            month=data['month'],
            electricity_kwh=data.get('electricity_kwh', 0),
            gas_therms=data.get('gas_therms', 0),
            water_gallons=data.get('water_gallons', 0)
        )
        
        return jsonify({
            'status': 'success',
            'message': f'Energy data for {data["month"]} added successfully'
        }), 201
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/energy-data/<int:household_id>', methods=['GET'])
def get_energy_data(household_id):
    """Get energy consumption history"""
    try:
        energy_data = db.get_energy_data(household_id)
        
        return jsonify({
            'status': 'success',
            'household_id': household_id,
            'energy_data': energy_data
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/analyze/<int:household_id>', methods=['GET'])
def analyze_household(household_id):
    """Analyze household and generate recommendations"""
    try:
        analysis = engine.analyze_household(household_id)
        
        return jsonify({
            'status': 'success',
            'analysis': analysis
        }), 200
    
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/recommendations/<int:household_id>', methods=['GET'])
def get_recommendations(household_id):
    """Get stored recommendations for a household"""
    try:
        recommendations = db.get_recommendations(household_id)
        
        return jsonify({
            'status': 'success',
            'household_id': household_id,
            'recommendations': recommendations,
            'count': len(recommendations)
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/quick-wins/<int:household_id>', methods=['GET'])
def quick_wins(household_id):
    """Get quick, low-cost wins"""
    try:
        wins = engine.get_quick_wins(household_id)
        
        return jsonify({
            'status': 'success',
            'household_id': household_id,
            'quick_wins': wins,
            'count': len(wins)
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/strategic-investments/<int:household_id>', methods=['GET'])
def strategic_investments(household_id):
    """Get major investments with long-term savings"""
    try:
        investments = engine.get_strategic_investments(household_id)
        
        return jsonify({
            'status': 'success',
            'household_id': household_id,
            'strategic_investments': investments,
            'count': len(investments)
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/compare', methods=['POST'])
def compare_households_api():
    """Compare multiple households"""
    data = request.json
    
    try:
        household_ids = data.get('household_ids', [])
        comparison = engine.compare_households(household_ids)
        
        return jsonify({
            'status': 'success',
            'comparison': comparison
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/knowledge-base', methods=['GET'])
def get_knowledge_base():
    """Get all rules from knowledge base"""
    try:
        rules = []
        for rule in kb.rules:
            rules.append({
                'id': rule.id,
                'category': rule.category,
                'recommendation': rule.recommendation,
                'priority': rule.priority,
                'estimated_savings_percent': rule.estimated_savings_percent,
                'implementation_cost': rule.implementation_cost,
                'description': rule.description
            })
        
        return jsonify({
            'status': 'success',
            'rules': rules,
            'total_rules': len(rules),
            'categories': kb.get_all_categories()
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/decision-tree/<int:household_id>', methods=['GET'])
def decision_tree(household_id):
    """Get decision tree path for a household"""
    try:
        path = engine.get_decision_tree_path(household_id)
        
        return jsonify({
            'status': 'success',
            'decision_path': path
        }), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


# ============ WEB PAGES ============

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')


@app.route('/household/<int:household_id>')
def household_dashboard(household_id):
    """Household dashboard with recommendations"""
    try:
        household = db.get_household(household_id)
        if not household:
            return "Household not found", 404
        
        analysis = engine.analyze_household(household_id)
        return render_template('dashboard.html', analysis=analysis, household=household)
    
    except Exception as e:
        return f"Error: {str(e)}", 500


@app.route('/create-household')
def create_household_page():
    """Page to create a new household"""
    return render_template('create_household.html')

@app.route('/add-energy/<int:household_id>')
def add_energy_page(household_id):
    """Page to add energy data for a household"""
    from datetime import datetime
    household = db.get_household(household_id)
    if not household:
        return "Household not found", 404
    
    current_month = datetime.now().strftime("%Y-%m")
    return render_template('add_energy.html', household_id=household_id, current_month=current_month)



@app.route('/summary')
def summary():
    """Summary page showing knowledge base and rules"""
    rules_by_category = {}
    for category in kb.get_all_categories():
        rules_by_category[category] = kb.get_rules_by_category(category)
    
    return render_template('summary.html', rules_by_category=rules_by_category)


@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return jsonify({'status': 'error', 'message': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """500 error handler"""
    return jsonify({'status': 'error', 'message': 'Server error'}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)

