#!/usr/bin/env python3
"""
Simple Baccarat Predictor - Single File Version
Easy to run anywhere!
"""

import random
from collections import defaultdict, deque
from datetime import datetime

class SimpleBaccaratPredictor:
    def __init__(self):
        self.results = []
        self.correct_predictions = 0
        self.total_predictions = 0
        
    def predict_next_hand(self):
        """Make a prediction for the next hand"""
        if len(self.results) < 5:
            return {
                'prediction': 'Banker',
                'confidence': 51,
                'reason': 'Default banker advantage'
            }
        
        # Analyze recent results
        recent = self.results[-10:]
        banker_count = recent.count('Banker')
        player_count = recent.count('Player')
        
        # Check for streaks
        current_streak = 1
        if len(recent) >= 2:
            for i in range(len(recent)-1, 0, -1):
                if recent[i] == recent[i-1] and recent[i] != 'Tie':
                    current_streak += 1
                else:
                    break
        
        # Make prediction based on patterns
        confidence = 50
        prediction = 'Banker'
        reasons = []
        
        # Long streak - bet against it
        if current_streak >= 4:
            last_winner = recent[-1]
            prediction = 'Player' if last_winner == 'Banker' else 'Banker'
            confidence = 65
            reasons.append(f"Long {last_winner} streak ({current_streak}) - betting against")
        
        # Frequency imbalance
        elif banker_count > player_count * 1.5:
            prediction = 'Player'
            confidence = 58
            reasons.append("Banker overdue - frequency imbalance")
        
        elif player_count > banker_count * 1.5:
            prediction = 'Banker'
            confidence = 58
            reasons.append("Player overdue - frequency imbalance")
        
        else:
            # Default to banker with slight edge
            prediction = 'Banker'
            confidence = 52
            reasons.append("Balanced pattern - banker edge")
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'reason': '; '.join(reasons)
        }
    
    def simulate_hand(self):
        """Simulate dealing a baccarat hand"""
        # Simple simulation - you can replace with real results
        outcomes = ['Banker', 'Player', 'Tie']
        weights = [45.8, 44.6, 9.6]  # Realistic baccarat probabilities
        
        result = random.choices(outcomes, weights=weights)[0]
        self.results.append(result)
        return result
    
    def record_prediction(self, prediction, actual_result):
        """Record if prediction was correct"""
        self.total_predictions += 1
        if prediction == actual_result:
            self.correct_predictions += 1
    
    def get_accuracy(self):
        """Get prediction accuracy"""
        if self.total_predictions == 0:
            return 0
        return (self.correct_predictions / self.total_predictions) * 100
    
    def get_recent_pattern(self):
        """Get recent results pattern"""
        recent = self.results[-10:]
        return ' → '.join(recent) if recent else 'No results yet'

def main():
    print("🎰 Simple Baccarat Predictor")
    print("=" * 40)
    
    predictor = SimpleBaccaratPredictor()
    
    while True:
        print("\n📊 Options:")
        print("1. Get Prediction (p)")
        print("2. Simulate Hand (s)")
        print("3. Auto Test (a)")
        print("4. Show Stats (t)")
        print("5. Quit (q)")
        
        choice = input("\nChoose option: ").lower().strip()
        
        if choice in ['q', 'quit']:
            break
            
        elif choice in ['p', 'prediction']:
            prediction = predictor.predict_next_hand()
            print(f"\n🎯 PREDICTION: {prediction['prediction']}")
            print(f"📈 Confidence: {prediction['confidence']}%")
            print(f"💡 Reason: {prediction['reason']}")
            
        elif choice in ['s', 'simulate']:
            # Get prediction first
            prediction = predictor.predict_next_hand()
            print(f"\n🎯 Prediction: {prediction['prediction']} ({prediction['confidence']}%)")
            
            # Simulate result
            result = predictor.simulate_hand()
            print(f"🎲 Result: {result}")
            
            # Record accuracy
            predictor.record_prediction(prediction['prediction'], result)
            
            # Show if correct
            correct = prediction['prediction'] == result
            print(f"✅ {'Correct!' if correct else 'Incorrect'}")
            
        elif choice in ['a', 'auto']:
            hands = int(input("How many hands to test? (1-50): ") or 10)
            hands = min(hands, 50)
            
            print(f"\n🤖 Auto-testing {hands} hands...")
            correct = 0
            
            for i in range(hands):
                prediction = predictor.predict_next_hand()
                result = predictor.simulate_hand()
                predictor.record_prediction(prediction['prediction'], result)
                
                if prediction['prediction'] == result:
                    correct += 1
                
                print(f"Hand {i+1}: Predicted {prediction['prediction']}, Got {result} {'✅' if prediction['prediction'] == result else '❌'}")
            
            accuracy = (correct / hands) * 100
            print(f"\n📊 Test Results: {correct}/{hands} correct ({accuracy:.1f}%)")
            
        elif choice in ['t', 'stats']:
            print(f"\n📊 STATISTICS:")
            print(f"Total Predictions: {predictor.total_predictions}")
            print(f"Accuracy: {predictor.get_accuracy():.1f}%")
            print(f"Recent Pattern: {predictor.get_recent_pattern()}")
            print(f"Total Results: {len(predictor.results)}")
            
            if predictor.results:
                banker_wins = predictor.results.count('Banker')
                player_wins = predictor.results.count('Player')
                ties = predictor.results.count('Tie')
                print(f"Banker: {banker_wins}, Player: {player_wins}, Ties: {ties}")
        
        else:
            print("❌ Invalid choice. Try again.")
    
    print("\n👋 Thanks for using the Baccarat Predictor!")
    print(f"Final Accuracy: {predictor.get_accuracy():.1f}%")

if __name__ == "__main__":
    main()