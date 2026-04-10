# Quick Start Guide

Get up and running with the Home Energy-Saving Advisor in 5 minutes!

## Installation (2 minutes)

```bash
# Navigate to project folder
cd HomeEnergyAdvisor

# Install Python dependencies
pip install -r requirements.txt
```

## Run Tests (1 minute)

Test the system with pre-defined household profiles:

```bash
python test_scenarios.py
```

This will:
- Create 5 test households with different profiles
- Generate energy data for each
- Analyze and display recommendations
- Show comparative analysis

## Try the CLI (2 minutes)

Launch the interactive menu:

```bash
python main.py
```

Options:
1. **Run Test Scenarios** - See the system in action
2. **Analyze Household** - Get recommendations for a specific household
3. **Create Household** - Add your own home profile
4. **Add Energy Data** - Input monthly energy consumption
5. **View Knowledge Base** - See all 19 rules
6. **Start Web Server** - Launch the Flask web interface

## Try the Web Interface

Start the Flask server:

```bash
python app.py
```

Then open your browser to: **http://localhost:5000**

Available pages:
- **Home** - Overview and navigation
- **Create Household** - Add a new household profile
- **Dashboard** - View detailed analysis and recommendations for a household
- **Knowledge Base** - Browse all energy-saving rules

## API Examples

### Create a Household

```bash
curl -X POST http://localhost:5000/api/household \
  -H "Content-Type: application/json" \
  -d {
    "name": "My Home",
    "members": 4,
    "square_feet": 2500,
    "climate_zone": "Cold"
  }
```

### Add Energy Data

```bash
curl -X POST http://localhost:5000/api/energy-data/1 \
  -H "Content-Type: application/json" \
  -d {
    "month": "March 2026",
    "electricity_kwh": 950,
    "gas_therms": 85,
    "water_gallons": 8500
  }
```

### Analyze Household

```bash
curl http://localhost:5000/api/analyze/1
```

### Get Recommendations

```bash
curl http://localhost:5000/api/recommendations/1
```

### Get Quick Wins

```bash
curl http://localhost:5000/api/quick-wins/1
```

### View Knowledge Base

```bash
curl http://localhost:5000/api/knowledge-base
```

## Understanding the Results

Each recommendation includes:
- **Category**: Type of energy-saving measure (Lighting, HVAC, etc.)
- **Priority**: High, Medium, or Low
- **Estimated Savings**: Percentage reduction in energy usage
- **Cost**: Estimated implementation cost range
- **Description**: Why this recommendation applies

## Example Household Analysis

Input:
- Family of 4
- 2,500 sq ft home
- Cold climate
- High electricity and gas usage

Output:
- 8 recommendations triggered
- ~115% cumulative savings potential
- Mix of quick wins and strategic investments

Recommendations include:
1. LED lighting upgrades (15% savings)
2. Programmable thermostat (10% savings)
3. Improved insulation (8% savings)
4. ... and more!

## Next Steps

1. **Run test scenarios** to understand the system
2. **Create your own household** with your actual data
3. **View recommendations** specific to your home
4. **Prioritize investments** based on cost and savings
5. **Track implementation** as you make changes

## Troubleshooting

**Flask not found?**
```bash
pip install Flask==2.3.0
```

**Database error?**
```bash
# Delete the old database and start fresh
rm energy_advisor.db
python main.py
```

**Port 5000 already in use?**
```bash
# Change the port in app.py or main.py
# Look for: app.run(debug=True, port=5000)
# Change 5000 to another port like 8000
```

## Project Files

- `main.py` - CLI interface
- `app.py` - Flask web server
- `database.py` - Database operations
- `knowledge_base.py` - Energy-saving rules (19 rules)
- `rules_engine.py` - Decision tree logic
- `test_scenarios.py` - Test households
- `templates/` - HTML templates
- `README.md` - Full documentation

## Learning Points

This project demonstrates:
- **Rule-based systems** and decision trees
- **SQLite database** design and operations
- **Flask web framework** (API + templates)
- **Data analysis** and comparative metrics
- **Software architecture** best practices

---

**Happy energy saving! 💚⚡**
