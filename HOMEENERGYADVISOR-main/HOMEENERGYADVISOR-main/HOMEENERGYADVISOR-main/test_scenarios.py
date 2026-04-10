"""
Test scenarios with different household profiles
Used for Week 4: Testing with different household profiles
"""

from database import Database
from rules_engine import RulesEngine
import json


class TestScenarios:
    """Test scenarios with predefined household profiles"""
    
    @staticmethod
    def create_test_households(db: Database):
        """Create test households with different profiles"""
        
        test_households = [
            {
                'name': 'Urban Apartment (Small)',
                'members': 1,
                'square_feet': 600,
                'climate_zone': 'Moderate'
            },
            {
                'name': 'Family Home (Medium)',
                'members': 4,
                'square_feet': 2000,
                'climate_zone': 'Cold'
            },
            {
                'name': 'Large Suburban Home',
                'members': 5,
                'square_feet': 3500,
                'climate_zone': 'Hot'
            },
            {
                'name': 'Energy-Conscious Home',
                'members': 3,
                'square_feet': 1800,
                'climate_zone': 'Moderate'
            },
            {
                'name': 'Old Victorian House',
                'members': 2,
                'square_feet': 2500,
                'climate_zone': 'Cold'
            }
        ]
        
        household_ids = []
        for house in test_households:
            hid = db.add_household(
                name=house['name'],
                members=house['members'],
                square_feet=house['square_feet'],
                climate_zone=house['climate_zone']
            )
            household_ids.append(hid)
        
        return household_ids
    
    @staticmethod
    def populate_energy_data(db: Database, household_id: int, profile: str):
        """Populate energy data based on household profile"""
        
        profiles = {
            'low_consumption': {
                'electricity_kwh': 600,
                'gas_therms': 40,
                'water_gallons': 5000
            },
            'moderate_consumption': {
                'electricity_kwh': 900,
                'gas_therms': 70,
                'water_gallons': 8000
            },
            'high_consumption': {
                'electricity_kwh': 1300,
                'gas_therms': 120,
                'water_gallons': 12000
            },
            'very_high_consumption': {
                'electricity_kwh': 1800,
                'gas_therms': 150,
                'water_gallons': 15000
            }
        }
        
        data = profiles.get(profile, profiles['moderate_consumption'])
        
        db.add_energy_data(
            household_id=household_id,
            month='March 2026',
            electricity_kwh=data['electricity_kwh'],
            gas_therms=data['gas_therms'],
            water_gallons=data['water_gallons']
        )
    
    @staticmethod
    def run_all_tests(db: Database):
        """Run all test scenarios"""
        
        print("\n" + "="*70)
        print("🎬 DEMO: ANALYZING 5 DIFFERENT HOUSEHOLD PROFILES")
        print("="*70)
        print("""
You're about to see how our energy advisor analyzes different homes.
Each household has a unique profile - from compact apartments to large
suburban homes. Let's see what personalized recommendations each receives!
        """)
        
        engine = RulesEngine(db)
        
        # Create test households
        household_ids = TestScenarios.create_test_households(db)
        print(f"✅ Created {len(household_ids)} diverse household profiles\n")
        
        # Define test data for each household
        test_data = [
            ('low_consumption', 1),        # Urban Apartment
            ('high_consumption', 4),       # Family Home
            ('very_high_consumption', 5),  # Large Suburban
            ('moderate_consumption', 3),   # Energy-Conscious
            ('high_consumption', 2)        # Victorian House
        ]
        
        results = []
        
        for idx, (profile, hid) in enumerate(zip([d[0] for d in test_data], household_ids)):
            print("\n" + "─"*70)
            print(f"🏠 HOME #{idx + 1}: {db.get_household(hid)['name'].upper()}")
            print("─"*70)
            
            # Populate energy data
            TestScenarios.populate_energy_data(db, hid, profile)
            
            # Analyze household
            try:
                analysis = engine.analyze_household(hid)
                
                print(f"\n📋 HOME PROFILE:")
                print(f"   • Size: {analysis['household_profile']['square_feet']:,} sq ft")
                print(f"   • Occupants: {analysis['household_profile']['members']} people")
                print(f"   • Climate: {analysis['household_profile']['climate_zone']}")
                
                print(f"\n⚡ MONTHLY ENERGY USAGE:")
                print(f"   • Electricity: {analysis['current_usage']['electricity_kwh']:,} kWh")
                print(f"   • Natural Gas: {analysis['current_usage']['gas_therms']:,} therms")
                print(f"   • Water: {analysis['current_usage']['water_gallons']:,} gallons")
                
                print(f"\n✨ ANALYSIS RESULTS:")
                print(f"   • Total recommendations: {analysis['triggered_rules_count']}")
                print(f"   • Combined savings potential: {analysis['total_estimated_savings']}%")
                print(f"   • Avg per recommendation: {analysis['average_estimated_savings']}%")
                
                print(f"\n💡 TOP 5 PERSONALIZED RECOMMENDATIONS:")
                for i, rec in enumerate(analysis['recommendations'][:5], 1):
                    icon = "🔴" if rec['priority'] == "High" else "🟡" if rec['priority'] == "Medium" else "🟢"
                    print(f"\n   {i}. {icon} [{rec['priority'].upper()}] {rec['recommendation']}")
                    print(f"      💰 Cost: {rec['implementation_cost']} | 📈 Savings: {rec['estimated_savings_percent']}%")
                
                # Get quick wins
                quick_wins = engine.get_quick_wins(hid)
                if quick_wins:
                    print(f"\n⚡ QUICK WINS YOU CAN START TODAY ({len(quick_wins)} available):")
                    for win in quick_wins[:2]:
                        print(f"   ✓ {win['recommendation']}")
                        print(f"     (Cost: {win['implementation_cost']}, {win['estimated_savings_percent']}% savings)")
                
                # Get strategic investments
                investments = engine.get_strategic_investments(hid)
                if investments:
                    print(f"\n💰 STRATEGIC INVESTMENTS ({len(investments)} long-term options):")
                    for inv in investments[:2]:
                        print(f"   → {inv['recommendation']}")
                        print(f"     ({inv['estimated_savings_percent']}% potential savings)")
                
                results.append({
                    'household_id': hid,
                    'household_name': analysis['household_name'],
                    'recommendations': len(analysis['recommendations']),
                    'total_savings': analysis['total_estimated_savings'],
                    'avg_savings': analysis['average_estimated_savings']
                })
                
            except Exception as e:
                print(f"❌ Analysis error: {str(e)}")
        
        # Print comparison summary
        print(f"\n\n{'='*70}")
        print("📊 COMPARATIVE ANALYSIS - ALL HOMES AT A GLANCE")
        print(f"{'='*70}\n")
        
        comparison = engine.compare_households(household_ids)
        print(f"Total Homes Analyzed: {comparison['total_households']}\n")
        
        print(f"{'Home Name':<35} {'Recommendations':<20} {'Potential Savings':<15}")
        print("─" * 70)
        
        for comp in comparison['comparison_data']:
            print(f"{comp['name']:<35} {comp['recommendations_count']:<20} {comp['total_savings_potential']}%")
        
        if comparison['highest_savings_potential']:
            highest = comparison['highest_savings_potential']
            print(f"\n🏆 HIGHEST OPPORTUNITY: {highest['name']}")
            print(f"   This home has the most potential with {highest['total_savings_potential']}% in combined savings!")
        
        print("\n✅ Demo complete! Each home receives personalized advice based on:")
        print("   • Size and occupancy")
        print("   • Current energy consumption")
        print("   • Climate and location")
        print("   • Household characteristics")
        print("\n   Use the menu to create your own home and get YOUR personalized analysis!")
        
        return results


def run_demo():
    """Run a demo of the system"""
    db = Database()
    results = TestScenarios.run_all_tests(db)
    return results


if __name__ == '__main__':
    run_demo()
