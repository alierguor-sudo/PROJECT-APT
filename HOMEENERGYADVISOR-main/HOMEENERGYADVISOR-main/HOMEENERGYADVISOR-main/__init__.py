"""
Home Energy-Saving Advisor Package
A rule-based decision tree system for energy-saving recommendations
"""

__version__ = "1.0.0"
__author__ = "Energy Advisor Team"
__description__ = "Rule-based system for personalized home energy-saving recommendations"

from database import Database
from knowledge_base import KnowledgeBase
from rules_engine import RulesEngine
from test_scenarios import TestScenarios

__all__ = [
    'Database',
    'KnowledgeBase',
    'RulesEngine',
    'TestScenarios',
]
