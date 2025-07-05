#!/usr/bin/env python3
"""
Baccarat Predictor App
Advanced pattern analysis and strategy recommendations for baccarat gameplay
"""

import random
import json
import statistics
from datetime import datetime
from typing import List, Dict, Tuple, Optional
from collections import defaultdict, deque
from dataclasses import dataclass, asdict
import math

@dataclass
class Card:
    """Represents a playing card"""
    suit: str
    value: int
    
    def __str__(self):
        face_cards = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
        value_str = face_cards.get(self.value, str(self.value))
        return f"{value_str}{self.suit}"

@dataclass
class Hand:
    """Represents a baccarat hand"""
    cards: List[Card]
    
    def value(self) -> int:
        """Calculate baccarat hand value (0-9)"""
        total = sum(min(card.value, 10) for card in self.cards)
        return total % 10
    
    def __str__(self):
        return f"Cards: {', '.join(str(card) for card in self.cards)} | Value: {self.value()}"

@dataclass
class GameResult:
    """Represents the result of a baccarat hand"""
    player_hand: Hand
    banker_hand: Hand
    winner: str  # 'Player', 'Banker', or 'Tie'
    timestamp: datetime
    
    def to_dict(self):
        return {
            'player_value': self.player_hand.value(),
            'banker_value': self.banker_hand.value(),
            'winner': self.winner,
            'timestamp': self.timestamp.isoformat()
        }

class BaccaratShoe:
    """Represents a baccarat shoe with 8 decks"""
    
    def __init__(self, start_from_card: int = 10):
        self.decks = 8
        self.start_from_card = start_from_card
        self.cards = []
        self.used_cards = []
        self.reset_shoe()
    
    def reset_shoe(self):
        """Create a new 8-deck shoe"""
        suits = ['♠', '♥', '♦', '♣']
        self.cards = []
        
        # Create 8 decks
        for _ in range(self.decks):
            for suit in suits:
                for value in range(1, 14):
                    self.cards.append(Card(suit, value))
        
        # Shuffle the shoe
        random.shuffle(self.cards)
        
        # Remove cards before start position
        self.used_cards = self.cards[:self.start_from_card]
        self.cards = self.cards[self.start_from_card:]
    
    def deal_card(self) -> Optional[Card]:
        """Deal a card from the shoe"""
        if not self.cards:
            return None
        
        card = self.cards.pop()
        self.used_cards.append(card)
        return card
    
    def cards_remaining(self) -> int:
        """Number of cards remaining in shoe"""
        return len(self.cards)
    
    def penetration(self) -> float:
        """Percentage of cards dealt"""
        total_cards = self.decks * 52
        return (len(self.used_cards) / total_cards) * 100

class PatternAnalyzer:
    """Analyzes patterns in baccarat results"""
    
    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self.results_history = deque(maxlen=max_history)
        self.patterns = {
            'streaks': defaultdict(int),
            'alternating': 0,
            'doubles': 0,
            'choppy': 0
        }
    
    def add_result(self, result: GameResult):
        """Add a new result to the analysis"""
        self.results_history.append(result)
        self._analyze_patterns()
    
    def _analyze_patterns(self):
        """Analyze patterns in the results history"""
        if len(self.results_history) < 2:
            return
        
        # Reset counters
        self.patterns = {
            'streaks': defaultdict(int),
            'alternating': 0,
            'doubles': 0,
            'choppy': 0
        }
        
        # Analyze streaks
        current_streak = 1
        current_winner = None
        
        for i, result in enumerate(self.results_history):
            if result.winner == 'Tie':
                continue
                
            if current_winner == result.winner:
                current_streak += 1
            else:
                if current_winner:
                    self.patterns['streaks'][f"{current_winner}_{current_streak}"] += 1
                current_winner = result.winner
                current_streak = 1
        
        # Record final streak
        if current_winner:
            self.patterns['streaks'][f"{current_winner}_{current_streak}"] += 1
    
    def get_pattern_summary(self) -> Dict:
        """Get a summary of current patterns"""
        recent_results = [r.winner for r in list(self.results_history)[-10:] if r.winner != 'Tie']
        
        if len(recent_results) < 3:
            return {"message": "Not enough data for pattern analysis"}
        
        # Calculate various metrics
        banker_count = recent_results.count('Banker')
        player_count = recent_results.count('Player')
        
        # Check for streaks
        current_streak = 1
        for i in range(1, len(recent_results)):
            if recent_results[i] == recent_results[i-1]:
                current_streak += 1
            else:
                break
        
        return {
            'recent_results': recent_results,
            'banker_frequency': banker_count / len(recent_results),
            'player_frequency': player_count / len(recent_results),
            'current_streak': current_streak,
            'current_streak_winner': recent_results[-1] if recent_results else None,
            'total_hands_analyzed': len(self.results_history)
        }

class CardCounter:
    """Tracks card composition for strategic advantage"""
    
    def __init__(self):
        self.card_counts = {
            'A': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, '10': 0
        }
        self.total_cards_seen = 0
    
    def count_card(self, card: Card):
        """Count a dealt card"""
        value = min(card.value, 10)
        if value == 1:
            self.card_counts['A'] += 1
        else:
            self.card_counts[str(value)] += 1
        self.total_cards_seen += 1
    
    def get_remaining_distribution(self, total_decks: int = 8) -> Dict:
        """Calculate remaining card distribution"""
        total_cards = total_decks * 52
        remaining_cards = {}
        
        for value in ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            expected_total = total_decks * 4 if value != '10' else total_decks * 16
            remaining = expected_total - self.card_counts[value]
            remaining_cards[value] = remaining
        
        return remaining_cards
    
    def get_shoe_bias(self) -> Dict:
        """Calculate shoe bias based on remaining cards"""
        remaining = self.get_remaining_distribution()
        total_remaining = sum(remaining.values())
        
        if total_remaining == 0:
            return {"bias": "neutral", "confidence": 0}
        
        # Calculate bias towards banker or player
        # High cards (6-10) favor banker slightly
        # Low cards (A-5) favor player slightly
        high_cards = remaining['6'] + remaining['7'] + remaining['8'] + remaining['9'] + remaining['10']
        low_cards = remaining['A'] + remaining['2'] + remaining['3'] + remaining['4'] + remaining['5']
        
        high_ratio = high_cards / total_remaining
        low_ratio = low_cards / total_remaining
        
        bias_strength = abs(high_ratio - low_ratio)
        
        if high_ratio > low_ratio:
            return {"bias": "banker", "confidence": min(bias_strength * 100, 100)}
        else:
            return {"bias": "player", "confidence": min(bias_strength * 100, 100)}

class BaccaratPredictor:
    """Main baccarat predictor class"""
    
    def __init__(self):
        self.shoe = BaccaratShoe()
        self.pattern_analyzer = PatternAnalyzer()
        self.card_counter = CardCounter()
        self.results_history = []
        self.session_stats = {
            'hands_played': 0,
            'correct_predictions': 0,
            'banker_wins': 0,
            'player_wins': 0,
            'ties': 0
        }
    
    def new_shoe(self):
        """Start a new shoe"""
        self.shoe.reset_shoe()
        self.card_counter = CardCounter()
        print("🔄 New shoe started! Cards remaining: {}".format(self.shoe.cards_remaining()))
    
    def deal_hand(self) -> GameResult:
        """Deal a complete baccarat hand"""
        if self.shoe.cards_remaining() < 6:
            print("⚠️  Running low on cards. Consider new shoe.")
            return None
        
        # Deal initial cards
        player_cards = [self.shoe.deal_card(), self.shoe.deal_card()]
        banker_cards = [self.shoe.deal_card(), self.shoe.deal_card()]
        
        # Count dealt cards
        for card in player_cards + banker_cards:
            self.card_counter.count_card(card)
        
        player_hand = Hand(player_cards)
        banker_hand = Hand(banker_cards)
        
        # Apply drawing rules
        player_total = player_hand.value()
        banker_total = banker_hand.value()
        
        # Player drawing rule
        if player_total <= 5:
            third_card = self.shoe.deal_card()
            if third_card:
                player_hand.cards.append(third_card)
                self.card_counter.count_card(third_card)
                player_total = player_hand.value()
        
        # Banker drawing rule (simplified)
        if len(player_hand.cards) == 3:
            # Complex banker drawing rules based on player's third card
            player_third = player_hand.cards[2].value % 10
            if self._banker_draws(banker_total, player_third):
                third_card = self.shoe.deal_card()
                if third_card:
                    banker_hand.cards.append(third_card)
                    self.card_counter.count_card(third_card)
        else:
            # No third card for player
            if banker_total <= 5:
                third_card = self.shoe.deal_card()
                if third_card:
                    banker_hand.cards.append(third_card)
                    self.card_counter.count_card(third_card)
        
        # Determine winner
        final_player = player_hand.value()
        final_banker = banker_hand.value()
        
        if final_player > final_banker:
            winner = 'Player'
        elif final_banker > final_player:
            winner = 'Banker'
        else:
            winner = 'Tie'
        
        result = GameResult(player_hand, banker_hand, winner, datetime.now())
        
        # Update statistics
        self.results_history.append(result)
        self.pattern_analyzer.add_result(result)
        self.session_stats['hands_played'] += 1
        self.session_stats[f"{winner.lower()}_wins" if winner != 'Tie' else 'ties'] += 1
        
        return result
    
    def _banker_draws(self, banker_total: int, player_third: int) -> bool:
        """Determine if banker draws based on complex rules"""
        if banker_total <= 2:
            return True
        elif banker_total == 3:
            return player_third != 8
        elif banker_total == 4:
            return player_third in [2, 3, 4, 5, 6, 7]
        elif banker_total == 5:
            return player_third in [4, 5, 6, 7]
        elif banker_total == 6:
            return player_third in [6, 7]
        return False
    
    def get_prediction(self) -> Dict:
        """Generate prediction based on patterns and card counting"""
        if len(self.results_history) < 5:
            return {
                'prediction': 'Banker',
                'confidence': 51,
                'reasoning': 'Default banker bet (house edge advantage)',
                'strategy': 'conservative'
            }
        
        # Get pattern analysis
        patterns = self.pattern_analyzer.get_pattern_summary()
        
        # Get card counting bias
        shoe_bias = self.card_counter.get_shoe_bias()
        
        # Combine factors for prediction
        confidence = 50
        prediction = 'Banker'  # Default
        reasoning = []
        
        # Factor 1: Current streak analysis
        if 'current_streak' in patterns and patterns['current_streak'] >= 3:
            if patterns['current_streak'] >= 5:
                # Long streak - bet against it
                prediction = 'Player' if patterns['current_streak_winner'] == 'Banker' else 'Banker'
                confidence += 15
                reasoning.append(f"Long {patterns['current_streak_winner']} streak ({patterns['current_streak']}) - betting against")
            else:
                # Medium streak - continue
                prediction = patterns['current_streak_winner']
                confidence += 10
                reasoning.append(f"Medium {patterns['current_streak_winner']} streak ({patterns['current_streak']}) - continuing")
        
        # Factor 2: Shoe composition
        if shoe_bias['confidence'] > 20:
            if shoe_bias['bias'] == prediction:
                confidence += min(shoe_bias['confidence'] * 0.3, 15)
            else:
                confidence -= min(shoe_bias['confidence'] * 0.2, 10)
            reasoning.append(f"Shoe bias: {shoe_bias['bias']} ({shoe_bias['confidence']:.1f}%)")
        
        # Factor 3: Recent frequency
        if 'banker_frequency' in patterns and 'player_frequency' in patterns:
            if patterns['banker_frequency'] > 0.65:
                prediction = 'Player'
                confidence += 12
                reasoning.append("Banker overdue - frequency imbalance")
            elif patterns['player_frequency'] > 0.65:
                prediction = 'Banker'
                confidence += 12
                reasoning.append("Player overdue - frequency imbalance")
        
        # Cap confidence
        confidence = min(confidence, 85)
        
        # Determine strategy
        if confidence >= 70:
            strategy = 'aggressive'
        elif confidence >= 60:
            strategy = 'moderate'
        else:
            strategy = 'conservative'
        
        return {
            'prediction': prediction,
            'confidence': confidence,
            'reasoning': '; '.join(reasoning) if reasoning else 'Default banker advantage',
            'strategy': strategy,
            'shoe_penetration': self.shoe.penetration(),
            'cards_remaining': self.shoe.cards_remaining()
        }
    
    def get_session_stats(self) -> Dict:
        """Get current session statistics"""
        accuracy = 0
        if self.session_stats['hands_played'] > 0:
            accuracy = (self.session_stats['correct_predictions'] / self.session_stats['hands_played']) * 100
        
        return {
            'hands_played': self.session_stats['hands_played'],
            'accuracy': accuracy,
            'banker_wins': self.session_stats['banker_wins'],
            'player_wins': self.session_stats['player_wins'],
            'ties': self.session_stats['ties'],
            'shoe_penetration': self.shoe.penetration()
        }
    
    def record_prediction_result(self, prediction: str, actual: str):
        """Record whether prediction was correct"""
        if prediction == actual:
            self.session_stats['correct_predictions'] += 1

def main():
    """Main application interface"""
    print("🎰 Baccarat Predictor v1.0")
    print("=" * 50)
    
    predictor = BaccaratPredictor()
    
    while True:
        print("\n📊 Commands:")
        print("1. Get Prediction (p)")
        print("2. Deal Hand (d)")
        print("3. New Shoe (n)")
        print("4. Session Stats (s)")
        print("5. Auto Play 3 Hands (a)")
        print("6. Quit (q)")
        
        choice = input("\nEnter choice: ").lower().strip()
        
        if choice in ['q', 'quit']:
            break
        elif choice in ['p', 'prediction']:
            prediction = predictor.get_prediction()
            print(f"\n🎯 PREDICTION: {prediction['prediction']}")
            print(f"📈 Confidence: {prediction['confidence']}%")
            print(f"💡 Reasoning: {prediction['reasoning']}")
            print(f"🎮 Strategy: {prediction['strategy']}")
            print(f"🃏 Shoe: {prediction['shoe_penetration']:.1f}% used")
            
        elif choice in ['d', 'deal']:
            result = predictor.deal_hand()
            if result:
                print(f"\n🎲 HAND RESULT:")
                print(f"Player: {result.player_hand}")
                print(f"Banker: {result.banker_hand}")
                print(f"🏆 Winner: {result.winner}")
                
                # Ask if they want to record a prediction
                pred_input = input("Did you make a prediction? (y/n): ").lower()
                if pred_input == 'y':
                    pred_choice = input("What was your prediction? (B/P/T): ").upper()
                    pred_map = {'B': 'Banker', 'P': 'Player', 'T': 'Tie'}
                    if pred_choice in pred_map:
                        predictor.record_prediction_result(pred_map[pred_choice], result.winner)
                        print("✅ Prediction recorded!")
            
        elif choice in ['n', 'new']:
            predictor.new_shoe()
            
        elif choice in ['s', 'stats']:
            stats = predictor.get_session_stats()
            print(f"\n📊 SESSION STATISTICS:")
            print(f"Hands Played: {stats['hands_played']}")
            print(f"Prediction Accuracy: {stats['accuracy']:.1f}%")
            print(f"Banker Wins: {stats['banker_wins']}")
            print(f"Player Wins: {stats['player_wins']}")
            print(f"Ties: {stats['ties']}")
            print(f"Shoe Penetration: {stats['shoe_penetration']:.1f}%")
            
        elif choice in ['a', 'auto']:
            print("\n🎮 AUTO PLAY - 3 HANDS")
            for i in range(3):
                prediction = predictor.get_prediction()
                print(f"\nHand {i+1}:")
                print(f"🎯 Prediction: {prediction['prediction']} ({prediction['confidence']}%)")
                
                result = predictor.deal_hand()
                if result:
                    print(f"🎲 Result: {result.winner}")
                    print(f"Player: {result.player_hand.value()} | Banker: {result.banker_hand.value()}")
                    
                    # Auto-record prediction
                    predictor.record_prediction_result(prediction['prediction'], result.winner)
                    
                    correct = "✅" if prediction['prediction'] == result.winner else "❌"
                    print(f"Prediction: {correct}")
                
                if i < 2:
                    input("Press Enter for next hand...")
            
            stats = predictor.get_session_stats()
            print(f"\n📊 Updated Accuracy: {stats['accuracy']:.1f}%")
        
        else:
            print("❌ Invalid choice. Please try again.")
    
    print("\n👋 Thanks for using Baccarat Predictor!")

if __name__ == "__main__":
    main()