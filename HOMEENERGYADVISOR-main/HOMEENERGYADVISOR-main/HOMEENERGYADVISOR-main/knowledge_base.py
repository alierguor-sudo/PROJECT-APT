"""
Knowledge Base for Energy-Saving Rules
Contains all the energy-saving rules and decision tree logic
"""

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Rule:
    """Represents an energy-saving rule"""
    id: str
    category: str
    condition: callable
    recommendation: str
    priority: str  # High, Medium, Low
    estimated_savings_percent: float
    implementation_cost: str
    description: str


class KnowledgeBase:
    """Energy-saving knowledge base with decision tree rules"""
    
    def __init__(self):
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self) -> List[Rule]:
        """Initialize all energy-saving rules"""
        return [
            # Electricity Rules
            Rule(
                id="ELEC_001",
                category="Lighting",
                condition=lambda h, e: e.get('electricity_kwh', 0) > 1000,
                recommendation="Switch to LED bulbs to reduce electricity consumption by 75%",
                priority="High",
                estimated_savings_percent=15,
                implementation_cost="$100-300",
                description="LED bulbs use significantly less energy than incandescent/CFL"
            ),
            
            Rule(
                id="ELEC_002",
                category="HVAC",
                condition=lambda h, e: h.get('square_feet', 0) > 3000 and e.get('electricity_kwh', 0) > 1200,
                recommendation="Install a programmable thermostat to optimize heating/cooling schedules",
                priority="High",
                estimated_savings_percent=10,
                implementation_cost="$150-300",
                description="Programmable thermostats can reduce HVAC energy use by 10-15%"
            ),
            
            Rule(
                id="ELEC_003",
                category="Appliances",
                condition=lambda h, e: e.get('electricity_kwh', 0) > 900,
                recommendation="Upgrade to ENERGY STAR certified appliances",
                priority="Medium",
                estimated_savings_percent=12,
                implementation_cost="$800-3000",
                description="ENERGY STAR appliances use 10-15% less energy than standard models"
            ),
            
            Rule(
                id="ELEC_004",
                category="Standby Power",
                condition=lambda h, e: True,  # Applicable to all households
                recommendation="Eliminate phantom power drain by using smart power strips",
                priority="Low",
                estimated_savings_percent=5,
                implementation_cost="$20-50",
                description="Phantom power accounts for 5-10% of home energy use"
            ),
            
            # Gas/Heating Rules
            Rule(
                id="GAS_001",
                category="Heating",
                condition=lambda h, e: e.get('gas_therms', 0) > 100,
                recommendation="Improve home insulation by adding weatherstripping and caulking",
                priority="High",
                estimated_savings_percent=8,
                implementation_cost="$100-200",
                description="Proper insulation and sealing reduces heating loss by 8-15%"
            ),
            
            Rule(
                id="GAS_002",
                category="Heating",
                condition=lambda h, e: e.get('gas_therms', 0) > 120 and h.get('square_feet', 0) > 2500,
                recommendation="Schedule annual HVAC maintenance and consider upgrading to a high-efficiency furnace",
                priority="High",
                estimated_savings_percent=12,
                implementation_cost="$3000-5000",
                description="High-efficiency furnaces (95%+ AFUE) save 10-20% on heating costs"
            ),
            
            Rule(
                id="GAS_003",
                category="Water Heating",
                condition=lambda h, e: h.get('members', 0) > 3 and e.get('gas_therms', 0) > 50,
                recommendation="Lower water heater temperature to 120°F and insulate pipes",
                priority="Medium",
                estimated_savings_percent=6,
                implementation_cost="$20-100",
                description="Reducing water heater temp and insulating pipes saves 3-5% of gas use"
            ),
            
            Rule(
                id="GAS_004",
                category="Water Heating",
                condition=lambda h, e: h.get('members', 0) > 4 and e.get('gas_therms', 0) > 80,
                recommendation="Consider upgrading to a tankless water heater for long-term savings",
                priority="Medium",
                estimated_savings_percent=15,
                implementation_cost="$1500-2500",
                description="Tankless water heaters save 24-34% on water heating costs"
            ),
            
            # Water Rules
            Rule(
                id="WATER_001",
                category="Water Usage",
                condition=lambda h, e: e.get('water_gallons', 0) > 10000,
                recommendation="Install low-flow showerheads and faucet aerators",
                priority="Medium",
                estimated_savings_percent=20,
                implementation_cost="$20-60",
                description="Low-flow fixtures reduce water usage by 20-30% without sacrificing comfort"
            ),
            
            Rule(
                id="WATER_002",
                category="Water Usage",
                condition=lambda h, e: h.get('square_feet', 0) > 3500,
                recommendation="Fix leaks promptly; a dripping faucet can waste 3,000 gallons per year",
                priority="Medium",
                estimated_savings_percent=10,
                implementation_cost="$0-200",
                description="Fixing leaks is one of the quickest ways to reduce water usage"
            ),
            
            # Behavioral/General Rules
            Rule(
                id="BEH_001",
                category="General",
                condition=lambda h, e: True,
                recommendation="Seal air leaks around doors, windows, and electrical outlets",
                priority="High",
                estimated_savings_percent=10,
                implementation_cost="$50-150",
                description="Air sealing can improve HVAC efficiency by 10-20%"
            ),
            
            Rule(
                id="BEH_002",
                category="General",
                condition=lambda h, e: True,
                recommendation="Increase natural ventilation and use ceiling fans in summer",
                priority="Low",
                estimated_savings_percent=5,
                implementation_cost="$50-200",
                description="Ceiling fans use less energy than AC and enable higher thermostat settings"
            ),
            
            Rule(
                id="BEH_003",
                category="Behavior",
                condition=lambda h, e: h.get('members', 0) > 2,
                recommendation="Educate household members about energy-saving practices and set goals",
                priority="Low",
                estimated_savings_percent=5,
                implementation_cost="$0",
                description="Behavioral changes can reduce energy use by 5-15% without investments"
            ),
            
            Rule(
                id="SOL_001",
                category="Renewable Energy",
                condition=lambda h, e: e.get('electricity_kwh', 0) > 800 and h.get('climate_zone', '').upper() in ['SUNNY', 'MODERATE'],
                recommendation="Evaluate solar panel installation for long-term electricity savings",
                priority="Medium",
                estimated_savings_percent=50,
                implementation_cost="$15000-25000",
                description="Solar panels can reduce electricity bills by 50-100% depending on usage"
            ),
        ]
    
    def evaluate_household(self, household: Dict[str, Any], energy_data: Dict[str, Any]) -> List[Rule]:
        """
        Evaluate a household against all rules
        Returns list of triggered rules
        """
        triggered_rules = []
        
        for rule in self.rules:
            try:
                if rule.condition(household, energy_data):
                    triggered_rules.append(rule)
            except Exception as e:
                print(f"Error evaluating rule {rule.id}: {e}")
        
        # Sort by priority
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        triggered_rules.sort(key=lambda r: priority_order.get(r.priority, 3))
        
        return triggered_rules
    
    def get_rule_by_id(self, rule_id: str) -> Rule:
        """Get a specific rule by ID"""
        for rule in self.rules:
            if rule.id == rule_id:
                return rule
        return None
    
    def get_rules_by_category(self, category: str) -> List[Rule]:
        """Get all rules in a specific category"""
        return [r for r in self.rules if r.category == category]
    
    def get_all_categories(self) -> List[str]:
        """Get list of all rule categories"""
        categories = set(r.category for r in self.rules)
        return sorted(list(categories))
