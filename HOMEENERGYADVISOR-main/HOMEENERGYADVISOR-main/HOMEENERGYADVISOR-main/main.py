"""
Home Energy-Saving Advisor - Main Entry Point
"""

from database import Database
from rules_engine import RulesEngine
from knowledge_base import KnowledgeBase
from test_scenarios import TestScenarios
import sys


def print_banner():
    """Print welcome banner"""
    print("\n" + "🏠" * 35)
    print("""
    ╔════════════════════════════════════════════════════╗
    ║                                                    ║
    ║    🌱 HOME ENERGY-SAVING ADVISOR 🌱              ║
    ║    Your personal guide to energy efficiency       ║
    ║                                                    ║
    ╚════════════════════════════════════════════════════╝
    """)
    print("🏠" * 35 + "\n")


def print_menu():
    """Print main menu"""
    print("\n" + "─" * 70)
    print("WHAT WOULD YOU LIKE TO DO?")
    print("─" * 70)
    print("")
    print("  📊 1.  Run Demo with Sample Households")
    print("         (See the advisor in action with 5 test homes)")
    print("")
    print("  🔍 2.  Analyze Your Home")
    print("         (Get personalized recommendations)")
    print("")
    print("  🏡 3.  Register a New Household")
    print("         (Add your home to the system)")
    print("")
    print("  ⚡ 4.  Add Energy Usage Data")
    print("         (Update monthly electricity, gas, and water)")
    print("")
    print("  📚 5.  Explore Our Knowledge Base")
    print("         (Browse all 19 energy-saving rules and tips)")
    print("")
    print("  🌐 6.  Launch Web Dashboard")
    print("         (Open the beautiful web interface)")
    print("")
    print("  📈 7.  Compare Multiple Homes")
    print("         (See how your home measures up)")
    print("")
    print("  ❌ 0.  Exit")
    print("")
    print("─" * 70)


def main():
    """Main application entry point"""
    
    db = Database()
    engine = RulesEngine(db)
    kb = KnowledgeBase()
    
    print_banner()
    print("Welcome! 👋 I'm here to help you save energy and money on your utility bills.")
    print("Let's get started with personalized energy-saving recommendations for your home.\n")
    
    while True:
        print_menu()
        choice = input("\n> Enter your choice (0-7): ").strip()
        
        if choice == '0':
            print("\n" + "─" * 70)
            print("💚 Thank you for choosing Energy-Saving Advisor!")
            print("Remember: Every small change adds up to big savings! 🌱")
            print("─" * 70 + "\n")
            break
        
        elif choice == '1':
            print("\n" + "=" * 70)
            print("🎬 RUNNING DEMO WITH SAMPLE HOUSEHOLDS")
            print("=" * 70)
            print("\nI'll analyze 5 different household profiles and show you")
            print("personalized recommendations for each. This may take a moment...\n")
            TestScenarios.run_all_tests(db)
        
        elif choice == '2':
            try:
                print("\n" + "─" * 70)
                household_id = input("📍 Which household would you like to analyze? (Enter ID): ").strip()
                household_id = int(household_id)
                
                analysis = engine.analyze_household(household_id)
                
                print(f"\n{'='*70}")
                print(f"✨ PERSONALIZED ANALYSIS FOR: {analysis['household_name'].upper()}")
                print(f"{'='*70}")
                
                print(f"\n📋 YOUR HOME PROFILE:")
                print(f"   • Occupants: {analysis['household_profile']['members']} people")
                print(f"   • Square footage: {analysis['household_profile']['square_feet']:,} sq ft")
                print(f"   • Climate: {analysis['household_profile']['climate_zone']}")
                
                print(f"\n⚡ CURRENT ENERGY USAGE:")
                print(f"   • Electricity: {analysis['current_usage']['electricity_kwh']:,} kWh/month")
                print(f"   • Natural Gas: {analysis['current_usage']['gas_therms']:,} therms/month")
                print(f"   • Water: {analysis['current_usage']['water_gallons']:,} gallons/month")
                
                print(f"\n🎯 RECOMMENDATIONS SUMMARY:")
                print(f"   • Total recommendations: {analysis['triggered_rules_count']}")
                print(f"   • Combined savings potential: {analysis['total_estimated_savings']}%")
                print(f"   • Average savings per improvement: {analysis['average_estimated_savings']}%")
                
                print(f"\n💡 TOP RECOMMENDATIONS FOR YOU:\n")
                for i, rec in enumerate(analysis['recommendations'], 1):
                    priority_emoji = "🔴" if rec['priority'] == "High" else "🟡" if rec['priority'] == "Medium" else "🟢"
                    print(f"   {priority_emoji} #{i} [{rec['priority'].upper()}] {rec['recommendation']}")
                    print(f"       Field: {rec['category']} | Potential Savings: {rec['estimated_savings_percent']}%")
                    print(f"       Cost: {rec['implementation_cost']}")
                    print()
                
                # Quick wins highlight
                quick_wins = engine.get_quick_wins(household_id)
                if quick_wins:
                    print(f"⚡ QUICK WINS (You could start today!):")
                    for win in quick_wins[:3]:
                        print(f"   ✓ {win['recommendation']}")
                        print(f"     ({win['implementation_cost']}, {win['estimated_savings_percent']}% savings)\n")
                
                # Strategic investments
                investments = engine.get_strategic_investments(household_id)
                if investments:
                    print(f"💰 STRATEGIC INVESTMENTS (Long-term value):")
                    for inv in investments[:3]:
                        print(f"   → {inv['recommendation']}")
                        print(f"     ({inv['estimated_savings_percent']}% savings)\n")
            
            except ValueError:
                print("❌ Oops! That doesn't look like a valid household ID. Please try again.")
            except Exception as e:
                print(f"❌ Something went wrong: {str(e)}\n   Please make sure you've added energy data for this household.")
        
        elif choice == '3':
            print("\n" + "─" * 70)
            print("🏡 LET'S ADD YOUR HOME")
            print("─" * 70)
            print("\nTell me about your home so I can give you the best advice:\n")
            
            try:
                name = input("💬 What would you like to call your home? (e.g., 'My House', 'Cottage'): ").strip()
                if not name:
                    name = "My Home"
                
                members = input("   How many people live there? (default: 2): ") or "2"
                members = int(members)
                
                size = input("   What's the size in square feet? (default: 2000): ") or "2000"
                size = int(size)
                
                print("\n   What region describes your climate best?")
                print("   1) Cold (Northern climate, long winters)")
                print("   2) Moderate (Mild winters and summers)")
                print("   3) Hot (Warm year-round, intense summers)")
                print("   4) Sunny (Excellent solar potential)")
                climate_choice = input("   Your choice (1-4, default: 2): ") or "2"
                
                climate_map = {"1": "Cold", "2": "Moderate", "3": "Hot", "4": "Sunny"}
                climate = climate_map.get(climate_choice, "Moderate")
                
                hid = db.add_household(name, members, size, climate)
                print(f"\n✅ Excellent! I've registered '{name}'")
                print(f"   (Household ID: {hid})")
                print(f"\n   Next, add your energy usage data so I can analyze it!")
                
            except ValueError:
                print("❌ Please enter valid numbers for members and square footage.")
        
        elif choice == '4':
            print("\n" + "─" * 70)
            print("⚡ ADD ENERGY USAGE DATA")
            print("─" * 70)
            print("\nI need your monthly energy bills to give recommendations.\n")
            
            try:
                household_id = input("📍 Household ID (which home is this for?): ").strip()
                household_id = int(household_id)
                
                household = db.get_household(household_id)
                if not household:
                    print(f"❌ Household {household_id} not found. Maybe create it first?")
                    continue
                
                print(f"\n   Adding data for: {household['name']}")
                
                month = input("   What month? (e.g., 'March 2026'): ") or "March 2026"
                
                electricity = input("   Monthly electricity (kWh, e.g., 900): ") or "900"
                electricity = float(electricity)
                
                gas = input("   Monthly gas (therms, e.g., 70): ") or "70"
                gas = float(gas)
                
                water = input("   Monthly water (gallons, e.g., 8000): ") or "8000"
                water = float(water)
                
                db.add_energy_data(household_id, month, electricity, gas, water)
                print(f"\n✅ Got it! I've recorded your {month} data.")
                print(f"   Now analyze your home to get personalized recommendations!")
                
            except ValueError:
                print("❌ Please enter valid numbers for energy usage.")
        
        elif choice == '5':
            print("\n" + "=" * 70)
            print("📚 OUR KNOWLEDGE BASE")
            print("=" * 70)
            print("\nHere are all the energy-saving strategies I can recommend:\n")
            
            for category in kb.get_all_categories():
                print(f"\n{'─' * 70}")
                print(f"📁 {category.upper()}")
                print(f"{'─' * 70}")
                
                rules = kb.get_rules_by_category(category)
                for rule in rules:
                    print(f"\n  {rule.id}: {rule.recommendation}")
                    print(f"      💡 Why: {rule.description}")
                    print(f"      Priority: {rule.priority} | Savings: {rule.estimated_savings_percent}% | Cost: {rule.implementation_cost}")
        
        elif choice == '6':
            print("\n" + "─" * 70)
            print("🌐 LAUNCHING WEB DASHBOARD")
            print("─" * 70)
            print("\n✨ Opening your beautiful web interface!")
            print("\n   📍 Server running at: http://localhost:5000")
            print("   ⌨️  Press Ctrl+C to stop the server\n")
            print("   Here's what you'll find:")
            print("   • 🏠 Home page with quick navigation")
            print("   • 🏡 Add new households")
            print("   • 📊 Interactive dashboards with personalized advice")
            print("   • 📚 Explore all energy-saving rules")
            print("   • 🔗 REST API for automation\n")
            
            try:
                from app import app
                app.run(debug=True, port=5000)
            except ImportError:
                print("❌ Flask not installed. Run: pip install Flask==2.3.0")
        
        elif choice == '7':
            print("\n" + "─" * 70)
            print("📈 COMPARE MULTIPLE HOMES")
            print("─" * 70)
            print("\nLet's see how different homes compare!\n")
            
            try:
                hids_input = input("Enter household IDs (comma-separated, e.g., '1,2,3'): ").strip()
                hids = [int(h.strip()) for h in hids_input.split(',') if h.strip()]
                
                if not hids:
                    print("❌ Please enter at least one household ID.")
                    continue
                
                comparison = engine.compare_households(hids)
                
                print(f"\n{'='*70}")
                print("HOUSEHOLD COMPARISON REPORT")
                print(f"{'='*70}\n")
                
                print(f"{'Household':<35} {'Recommendations':<18} {'Savings Potential':<15}")
                print("─" * 70)
                
                for comp in comparison['comparison_data']:
                    print(f"{comp['name']:<35} {comp['recommendations_count']:<18} {comp['total_savings_potential']}%")
                
                if comparison['highest_savings_potential']:
                    highest = comparison['highest_savings_potential']
                    print(f"\n🏆 TOP OPPORTUNITY:")
                    print(f"   {highest['name']} has the highest savings potential at {highest['total_savings_potential']}%")
                    print(f"   ({highest['recommendations_count']} personalized recommendations)")
            
            except ValueError:
                print("❌ Please enter valid household IDs separated by commas.")
        
        else:
            print("\n❌ Hmm, that's not an option. Please choose 0-7.")
        
        input("\n💬 Press Enter to continue...")


if __name__ == '__main__':
    main()
