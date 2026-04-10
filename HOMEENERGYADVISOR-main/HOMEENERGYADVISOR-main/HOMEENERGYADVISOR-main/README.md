# Home Energy-Saving Advisor

A rule-based decision tree system for generating personalized energy-saving recommendations for households. Built with Python, SQLite, and Flask.

## 🎯 Overview

The Home Energy-Saving Advisor uses advanced rule-based logic to analyze household energy consumption patterns and provide targeted, prioritized recommendations for reducing energy use and saving money.

**Key Technologies:**
- **Python 3.x** - Core application logic
- **SQLite** - Household profiles and energy data storage
- **Flask** - Web interface and REST API
- **Decision Trees & Rule-Based Learning** - Recommendation engine

## 📊 Project Structure

```
HomeEnergyAdvisor/
├── main.py                      # Main entry point (CLI menu)
├── app.py                       # Flask web application
├── database.py                  # SQLite database manager
├── knowledge_base.py            # Energy-saving rules database
├── rules_engine.py              # Decision tree evaluation engine
├── test_scenarios.py            # Test households and scenarios
├── requirements.txt             # Python dependencies
├── energy_advisor.db            # SQLite database (generated)
└── templates/                   # Flask HTML templates
    ├── index.html              # Home page
    ├── create_household.html    # Household creation form
    ├── dashboard.html           # Household analysis dashboard
    └── summary.html             # Knowledge base display
```

## 🚀 Quick Start

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd HomeEnergyAdvisor
   ```

2. **Create a Python virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or source venv/bin/activate  # On Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the System

#### Option 1: Command-Line Interface
```bash
python main.py
```

This opens an interactive menu with options to:
- Run test scenarios (Week 4 testing)
- Analyze specific households
- Create new household profiles
- Add energy consumption data
- View the knowledge base
- Start the Flask web server

#### Option 2: Web Interface (Flask)
```bash
python app.py
```

Then open your browser to: `http://localhost:5000`

#### Option 3: Quick Test
```bash
python test_scenarios.py
```

This creates 5 test households and generates recommendations for each.

## 📋 Core Modules

### 1. **database.py** - Data Management
Handles all database operations using SQLite.

**Key Classes:**
- `Database` - Connection management and CRUD operations

**Tables:**
- `households` - Household profiles
- `energy_consumption` - Monthly energy usage data
- `recommendations` - Generated recommendations
- `rule_triggers` - Rule evaluation history

**Example Usage:**
```python
from database import Database

db = Database()
household_id = db.add_household("My Home", members=4, square_feet=2500, climate_zone="Cold")
db.add_energy_data(household_id, "March 2026", electricity_kwh=950, gas_therms=85, water_gallons=8500)
```

### 2. **knowledge_base.py** - Rule Database
Contains all energy-saving rules organized by category.

**Categories:**
- Lighting (LEDs, smart controls)
- HVAC (Thermostats, furnace upgrades)
- Appliances (ENERGY STAR ratings)
- Water Usage (Low-flow fixtures, leaks)
- Heating & Cooling (Insulation, weatherization)
- Renewable Energy (Solar panels)
- Behavioral changes

**Key Classes:**
- `Rule` - Individual energy-saving rule
- `KnowledgeBase` - Rule collection and evaluation

**Example Rule:**
```python
Rule(
    id="ELEC_001",
    category="Lighting",
    condition=lambda h, e: e.get('electricity_kwh', 0) > 1000,
    recommendation="Switch to LED bulbs to reduce electricity consumption by 75%",
    priority="High",
    estimated_savings_percent=15,
    implementation_cost="$100-300",
    description="LED bulbs use significantly less energy than incandescent/CFL"
)
```

### 3. **rules_engine.py** - Decision Tree Engine
Implements the decision-making logic for generating recommendations.

**Key Classes:**
- `RulesEngine` - Main evaluation engine

**Key Methods:**
- `analyze_household()` - Comprehensive household analysis
- `get_quick_wins()` - Low-cost, high-priority recommendations
- `get_strategic_investments()` - Major investments with long-term savings
- `compare_households()` - Multi-household comparison
- `get_decision_tree_path()` - Shows why rules were triggered

**Example Usage:**
```python
from rules_engine import RulesEngine
from database import Database

db = Database()
engine = RulesEngine(db)
analysis = engine.analyze_household(household_id=1)

print(f"Triggered {analysis['triggered_rules_count']} rules")
print(f"Total estimated savings: {analysis['total_estimated_savings']}%")
```

### 4. **app.py** - Flask Web Application
REST API and web interface.

**API Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/household` | Create new household |
| GET | `/api/household/<id>` | Get household profile |
| POST | `/api/energy-data/<id>` | Add energy consumption data |
| GET | `/api/energy-data/<id>` | Get energy history |
| GET | `/api/analyze/<id>` | Analyze household |
| GET | `/api/recommendations/<id>` | Get recommendations |
| GET | `/api/quick-wins/<id>` | Get quick wins |
| GET | `/api/strategic-investments/<id>` | Get investments |
| GET | `/api/knowledge-base` | Get all rules |
| GET | `/api/decision-tree/<id>` | Get decision path |
| POST | `/api/compare` | Compare multiple households |

**Web Pages:**
- `/` - Home page
- `/household/<id>` - Household dashboard
- `/create-household` - New household form
- `/summary` - Knowledge base viewer

### 5. **test_scenarios.py** - Test Suite
Pre-defined household profiles for testing and evaluation.

**Test Profiles:**
1. **Urban Apartment (Small)** - 1 member, 600 sq ft, low consumption
2. **Family Home (Medium)** - 4 members, 2000 sq ft, moderate consumption
3. **Large Suburban Home** - 5 members, 3500 sq ft, high consumption
4. **Energy-Conscious Home** - 3 members, 1800 sq ft, moderate consumption
5. **Old Victorian House** - 2 members, 2500 sq ft, high consumption

**Run Tests:**
```bash
python test_scenarios.py
```

## 📈 Decision Tree Logic

The system evaluates each household against all 19 rules using a decision tree approach:

```
Household Profile
    ↓
Energy Consumption Data
    ↓
Rule Evaluation (by category)
    ├─ Electricity Rules
    ├─ Gas/Heating Rules
    ├─ Water Rules
    ├─ Behavioral Rules
    └─ Renewable Energy Rules
    ↓
Triggered Rules
    ↓
Prioritize (High → Medium → Low)
    ↓
Generate Recommendations
    ↓
Store in Database
```

## 🔍 Rule Categories & Examples

### Electricity (3 rules)
- Switch to LED bulbs: 15% savings
- Install programmable thermostat: 10% savings
- Upgrade to ENERGY STAR appliances: 12% savings

### Gas/Heating (4 rules)
- Improve insulation: 8% savings
- Upgrade furnace: 12% savings
- Lower water heater temp: 6% savings
- Install tankless water heater: 15% savings

### Water (2 rules)
- Install low-flow fixtures: 20% savings
- Fix leaks: 10% savings

### General/Behavioral (6 rules)
- Seal air leaks: 10% savings
- Use ceiling fans: 5% savings
- Educate household: 5% savings
- Install solar panels: 50% savings

## 💾 Database Schema

### households table
```sql
CREATE TABLE households (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    members INTEGER,
    square_feet INTEGER,
    climate_zone TEXT,
    created_at TIMESTAMP
);
```

### energy_consumption table
```sql
CREATE TABLE energy_consumption (
    id INTEGER PRIMARY KEY,
    household_id INTEGER,
    month TEXT,
    electricity_kwh REAL,
    gas_therms REAL,
    water_gallons REAL,
    recorded_date TIMESTAMP
);
```

### recommendations table
```sql
CREATE TABLE recommendations (
    id INTEGER PRIMARY KEY,
    household_id INTEGER,
    rule_id TEXT,
    category TEXT,
    recommendation TEXT,
    priority TEXT,
    estimated_savings_percent REAL,
    implementation_cost TEXT,
    created_at TIMESTAMP
);
```

## 📅 Project Timeline (5-Week Plan)

### Week 1: Research & Foundation ✓
- [x] Research home energy-saving techniques
- [x] Design database schema
- [x] Create knowledge base structure
- [x] Implement core modules

### Week 2: Knowledge Base & Rules ✓
- [x] Build rule database (19 rules)
- [x] Organize rules by category
- [x] Implement rule evaluation logic
- [x] Create decision tree engine

### Week 3: Web Interface ✓
- [x] Develop Flask REST API
- [x] Create HTML templates
- [x] Build household dashboard
- [x] Implement knowledge base viewer

### Week 4: Testing with Profiles ✓
- [x] Create test households
- [x] Generate test scenarios
- [x] Run comparative analysis
- [x] Validate recommendations

### Week 5: Presentation & Finalization ✓
- [x] Complete documentation
- [x] Create comprehensive README
- [x] Prepare test results
- [x] Final system testing

## 🧪 Example: Analyzing a Household

**Scenario:** Family of 4 in a 2500 sq ft cold climate home

**Input Energy Data:**
- Electricity: 1,200 kWh/month
- Gas: 110 therms/month
- Water: 10,000 gallons/month

**Evaluated Rules (19 total):**
- High electricity → LED recommendation
- Large home + high electricity → Programmable thermostat
- High gas usage → Insulation improvement
- High gas + family → Water heater upgrade
- Water usage → Low-flow fixtures
- General rules → Air sealing

**Generated Recommendations:**
1. **HIGH: LED Bulbs** (15% savings, $100-300)
2. **HIGH: Programmable Thermostat** (10% savings, $150-300)
3. **HIGH: Insulation** (8% savings, $100-200)
4. **MEDIUM: ENERGY STAR Appliances** (12% savings, $800-3000)
5. **MEDIUM: Tankless Water Heater** (15% savings, $1500-2500)
6. **MEDIUM: Low-Flow Fixtures** (20% savings, $20-60)
7. **LOW: Air Sealing** (10% savings, $50-150)
8. **LOW: Smart Power Strips** (5% savings, $20-50)

**Total Estimated Savings: ~115%** (cumulative effect)

## 🔧 Customization

### Add a New Rule

Edit `knowledge_base.py`:

```python
Rule(
    id="CUSTOM_001",
    category="Custom Category",
    condition=lambda h, e: e.get('electricity_kwh', 0) > 1500,
    recommendation="Your recommendation text",
    priority="High",
    estimated_savings_percent=20,
    implementation_cost="$500-1000",
    description="Detailed description of the recommendation"
)
```

### Modify Rule Conditions

Rules use lambda functions for flexible condition evaluation:

```python
# Simple threshold
condition=lambda h, e: e.get('electricity_kwh', 0) > 1000

# Combined conditions
condition=lambda h, e: h.get('square_feet', 0) > 3000 and e.get('electricity_kwh', 0) > 1200

# Multiple data points
condition=lambda h, e: h.get('members', 0) > 4 and e.get('gas_therms', 0) > 100
```

## 📊 Interpreting Results

### Priority Levels
- **HIGH**: Immediate recommendations, often low cost with quick ROI
- **MEDIUM**: Important upgrades with good long-term savings
- **LOW**: Optional improvements or ongoing practices

### Savings Estimates
- Based on industry standards and real-world data
- Cumulative when multiple recommendations are implemented
- Actual savings vary by region, usage patterns, and implementation quality

### Cost Ranges
- **$0-100**: Quick wins (weatherstripping, power strips)
- **$100-500**: Medium investments (LED, thermostat)
- **$500-2500**: Major upgrades (furnace, water heater, insulation)
- **$15000+**: Long-term investments (solar, major renovations)

## 🎓 Learning Outcomes

This project demonstrates:
1. **Decision Tree Logic** - Rule-based decision making
2. **Database Design** - SQLite schema and relationships
3. **Web Development** - Flask REST API and templates
4. **Data Analysis** - Comparative analysis and metrics
5. **Software Architecture** - Modular, maintainable code

## 📝 License

This project is created for educational purposes.

## 👥 Support

For questions or improvements, refer to the code comments and docstrings throughout the project.

---

**Built with ❤️ for energy efficiency**
