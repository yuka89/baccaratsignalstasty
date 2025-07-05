#!/usr/bin/env python3
"""
Baccarat Predictor Demo
Demonstrates the key features of the baccarat prediction system
"""

from baccarat_predictor import BaccaratPredictor
from advanced_strategy import AdvancedBaccaratStrategy
import time

def demo_basic_functionality():
    """Demonstrate basic prediction functionality"""
    print("🎰 BACCARAT PREDICTOR DEMO")
    print("=" * 50)
    
    # Create predictor
    predictor = BaccaratPredictor()
    
    print("📊 Starting new 8-deck shoe...")
    predictor.new_shoe()
    print(f"   Cards remaining: {predictor.shoe.cards_remaining()}")
    print(f"   Shoe penetration: {predictor.shoe.penetration():.1f}%")
    
    print("\n🎯 PREDICTION DEMONSTRATION")
    print("-" * 30)
    
    # Demo 5 hands with predictions
    for hand_num in range(1, 6):
        print(f"\n🎲 Hand {hand_num}:")
        
        # Get prediction
        prediction = predictor.get_prediction()
        print(f"   Prediction: {prediction['prediction']} ({prediction['confidence']}%)")
        print(f"   Reasoning: {prediction['reasoning']}")
        print(f"   Strategy: {prediction['strategy']}")
        
        # Deal hand
        result = predictor.deal_hand()
        if result:
            print(f"   Result: {result.winner} wins")
            print(f"   Player: {result.player_hand.value()} | Banker: {result.banker_hand.value()}")
            
            # Record prediction
            predictor.record_prediction_result(prediction['prediction'], result.winner)
            
            # Show if correct
            correct = prediction['prediction'] == result.winner
            print(f"   Prediction: {'✅ Correct' if correct else '❌ Incorrect'}")
        
        time.sleep(0.5)  # Brief pause for readability
    
    # Show session stats
    print("\n📈 SESSION STATISTICS")
    print("-" * 30)
    stats = predictor.get_session_stats()
    print(f"   Hands Played: {stats['hands_played']}")
    print(f"   Prediction Accuracy: {stats['accuracy']:.1f}%")
    print(f"   Banker Wins: {stats['banker_wins']}")
    print(f"   Player Wins: {stats['player_wins']}")
    print(f"   Ties: {stats['ties']}")
    print(f"   Shoe Penetration: {stats['shoe_penetration']:.1f}%")
    
    return predictor

def demo_advanced_features(predictor):
    """Demonstrate advanced strategy features"""
    print("\n🧠 ADVANCED STRATEGY DEMONSTRATION")
    print("-" * 40)
    
    # Create advanced strategy instance
    advanced = AdvancedBaccaratStrategy()
    
    if len(predictor.results_history) >= 5:
        results = [r.winner for r in predictor.results_history]
        card_counts = predictor.card_counter.card_counts
        cards_remaining = predictor.shoe.cards_remaining()
        
        # Get advanced prediction
        advanced_prediction = advanced.get_advanced_prediction(results, card_counts, cards_remaining)
        
        print(f"🎯 Advanced Analysis:")
        print(f"   Prediction: {advanced_prediction['prediction']}")
        print(f"   Confidence: {advanced_prediction['confidence']}%")
        print(f"   Risk Level: {advanced_prediction['risk_level']}")
        print(f"   Reasoning: {advanced_prediction['reasoning']}")
        print(f"   Pattern Strength: {advanced_prediction['pattern_strength']}%")
        print(f"   Card Advantage: {advanced_prediction['card_advantage']:.1f}%")
        
        # Demo betting systems
        print(f"\n💰 BETTING SYSTEM RECOMMENDATIONS")
        print("-" * 40)
        
        systems = ['flat', 'martingale', 'fibonacci', 'paroli']
        for system in systems:
            bet_size = advanced.get_betting_recommendation(system, 10, 100)
            print(f"   {system.capitalize()}: ${bet_size:.2f}")
    
    else:
        print("   Need more hands for advanced analysis...")

def demo_pattern_recognition():
    """Demonstrate pattern recognition capabilities"""
    print("\n🔍 PATTERN RECOGNITION DEMO")
    print("-" * 35)
    
    # Create fresh predictor for pattern demo
    predictor = BaccaratPredictor()
    
    # Simulate a specific pattern (streak followed by chop)
    print("   Simulating streak pattern...")
    
    # Deal hands to create pattern
    for i in range(15):
        result = predictor.deal_hand()
        if result:
            print(f"   Hand {i+1}: {result.winner}")
    
    # Show pattern analysis
    patterns = predictor.pattern_analyzer.get_pattern_summary()
    if 'recent_results' in patterns:
        print(f"\n   Recent Pattern: {' → '.join(patterns['recent_results'][-10:])}")
        print(f"   Current Streak: {patterns.get('current_streak', 0)} ({patterns.get('current_streak_winner', 'None')})")
        print(f"   Banker Frequency: {patterns.get('banker_frequency', 0):.1%}")
        print(f"   Player Frequency: {patterns.get('player_frequency', 0):.1%}")

def main():
    """Main demonstration"""
    print("🎰 Welcome to the Baccarat Predictor Demo!")
    print("This demonstration showcases the key features of our advanced prediction system.\n")
    
    # Basic functionality demo
    predictor = demo_basic_functionality()
    
    # Advanced features demo
    demo_advanced_features(predictor)
    
    # Pattern recognition demo
    demo_pattern_recognition()
    
    print("\n🎉 DEMO COMPLETE!")
    print("=" * 50)
    print("Key Features Demonstrated:")
    print("✅ 8-deck shoe simulation with accurate card tracking")
    print("✅ Pattern recognition and streak analysis")
    print("✅ Card counting and composition effects")
    print("✅ Multiple betting system recommendations")
    print("✅ Advanced statistical analysis")
    print("✅ Real-time accuracy tracking")
    
    print("\n🚀 Ready to use the full application!")
    print("   Command Line: python3 baccarat_predictor.py")
    print("   Web Interface: python3 web_app.py")
    
    print("\n⚠️  Remember: This is for educational purposes only.")
    print("   Always gamble responsibly and within your means.")

if __name__ == "__main__":
    main()