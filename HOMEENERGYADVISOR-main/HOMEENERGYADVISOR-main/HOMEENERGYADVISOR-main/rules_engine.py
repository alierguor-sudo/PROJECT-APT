"""
Rules Engine for decision-making and recommendation generation
Implements the decision tree and rule evaluation logic
"""

from typing import List, Dict, Any
from knowledge_base import KnowledgeBase
from database import Database


class RulesEngine:
    """Decision tree-based rule engine for energy recommendations"""
    
    def __init__(self, db: Database = None):
        self.knowledge_base = KnowledgeBase()
        self.db = db or Database()
    
    def analyze_household(self, household_id: int) -> Dict[str, Any]:
        """
        Analyze a household and generate recommendations
        Returns analysis results with triggered rules and recommendations
        """
        # Retrieve household data
        household = self.db.get_household(household_id)
        if not household:
            raise ValueError(f"Household {household_id} not found")
        
        # Get latest energy data
                # Get latest energy data
        energy_data_list = self.db.get_energy_data(household_id)
        if not energy_data_list:
            # Return a friendly response instead of raising an error
            return {
                'household_id': household_id,
                'household_name': household['name'],
                'household_profile': dict(household),
                'current_usage': None,
                'triggered_rules_count': 0,
                'recommendations': [],
                'average_estimated_savings': 0,
                'total_estimated_savings': 0,
                'implementation_cost_range': [],
                'message': 'No energy data available yet. Please add energy consumption data to get recommendations.',
                'needs_energy_data': True
            }
        
        # Use most recent energy data (only reached if data exists)
        latest_energy = energy_data_list[0]
        # Use most recent energy data
        latest_energy = energy_data_list[0]
        
        # Evaluate all rules
        triggered_rules = self.knowledge_base.evaluate_household(household, latest_energy)
        
        # Clear old recommendations
        self.db.clear_recommendations(household_id)
        
        # Generate and store recommendations
        recommendations = []
        for rule in triggered_rules:
            recommendation_obj = {
                'rule_id': rule.id,
                'category': rule.category,
                'recommendation': rule.recommendation,
                'priority': rule.priority,
                'estimated_savings_percent': rule.estimated_savings_percent,
                'implementation_cost': rule.implementation_cost,
                'description': rule.description
            }
            
            # Store in database
            self.db.add_recommendation(
                household_id=household_id,
                rule_id=rule.id,
                category=rule.category,
                recommendation=rule.recommendation,
                priority=rule.priority,
                estimated_savings_percent=rule.estimated_savings_percent,
                implementation_cost=rule.implementation_cost,
                description=rule.description
            )
            
            # Log rule trigger
            self.db.log_rule_trigger(
                household_id,
                rule.id,
                {
                    'household': dict(household),
                    'energy_data': dict(latest_energy),
                    'recommendation': rule.recommendation
                }
            )
            
            recommendations.append(recommendation_obj)
        
        # Calculate aggregate metrics
        avg_savings = sum(r['estimated_savings_percent'] for r in recommendations) / len(recommendations) if recommendations else 0
        investment_categories = list(set(r['implementation_cost'] for r in recommendations))
        
        return {
            'household_id': household_id,
            'household_name': household['name'],
            'household_profile': dict(household),
            'current_usage': dict(latest_energy),
            'triggered_rules_count': len(triggered_rules),
            'recommendations': recommendations,
            'average_estimated_savings': round(avg_savings, 2),
            'total_estimated_savings': round(sum(r['estimated_savings_percent'] for r in recommendations), 2),
            'implementation_cost_range': investment_categories
        }
    
    def get_quick_wins(self, household_id: int) -> List[Dict[str, Any]]:
        """Get quick, low-cost wins for immediate energy savings"""
        analysis = self.analyze_household(household_id)
        
        # Filter for low cost and high priority
        quick_wins = [
            r for r in analysis['recommendations']
            if r['priority'] == 'High' and (
                '$0' in r['implementation_cost'] or 
                '$20' in r['implementation_cost'] or 
                '$50' in r['implementation_cost']
            )
        ]
        
        return quick_wins
    
    def get_strategic_investments(self, household_id: int) -> List[Dict[str, Any]]:
        """Get major investments that provide long-term savings"""
        analysis = self.analyze_household(household_id)
        
        # Filter for high savings and medium/high priority
        strategic = [
            r for r in analysis['recommendations']
            if r['estimated_savings_percent'] > 10 and r['priority'] in ['High', 'Medium']
        ]
        
        return sorted(strategic, key=lambda x: x['estimated_savings_percent'], reverse=True)
    
    def compare_households(self, household_ids: List[int]) -> Dict[str, Any]:
        """Compare energy profiles and recommendations across multiple households"""
        comparisons = []
        
        for hid in household_ids:
            try:
                analysis = self.analyze_household(hid)
                comparisons.append({
                    'household_id': hid,
                    'name': analysis['household_name'],
                    'recommendations_count': len(analysis['recommendations']),
                    'total_savings_potential': analysis['total_estimated_savings'],
                    'avg_savings': analysis['average_estimated_savings']
                })
            except ValueError:
                pass
        
        return {
            'comparison_data': comparisons,
            'total_households': len(comparisons),
            'highest_savings_potential': max(comparisons, key=lambda x: x['total_savings_potential']) if comparisons else None
        }
    
    def get_decision_tree_path(self, household_id: int) -> Dict[str, Any]:
        """
        Show the decision path taken for a household
        Useful for understanding why certain rules were triggered
        """
        household = self.db.get_household(household_id)
        if not household:
            raise ValueError(f"Household {household_id} not found")
            
        energy_data_list = self.db.get_energy_data(household_id)
        if not energy_data_list:
            raise ValueError(f"No energy data found for household {household_id}")
            
        energy_data = energy_data_list[0]
        
        decision_path = {
            'household_id': household_id,
            'decision_nodes': []
        }
        
        # Evaluate each rule category
        for category in self.knowledge_base.get_all_categories():
            category_rules = self.knowledge_base.get_rules_by_category(category)
            triggered = []
            
            for rule in category_rules:
                try:
                    if rule.condition(household, energy_data):
                        triggered.append(rule.id)
                except Exception:
                    pass
            
            decision_path['decision_nodes'].append({
                'category': category,
                'rules_evaluated': len(category_rules),
                'rules_triggered': len(triggered),
                'triggered_rule_ids': triggered
            })
        
        return decision_path
