"""
Advanced Baccarat Strategy Module
Implements sophisticated strategies and betting systems for baccarat prediction
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import deque
# import numpy as np  # Optional - for advanced calculations

@dataclass
class BettingStrategy:
    """Represents a betting strategy configuration"""
    name: str
    base_unit: float
    max_bet: float
    progression_type: str  # 'flat', 'martingale', 'fibonacci', 'labouchere'
    risk_level: str  # 'conservative', 'moderate', 'aggressive'

class AdvancedPatternAnalyzer:
    """Advanced pattern recognition and analysis"""
    
    def __init__(self):
        self.pattern_library = {
            'dragon_tail': {'pattern': 'BBBBBBB', 'counter_bet': 'Player', 'confidence': 75},
            'big_road_chop': {'pattern': 'BPBPBP', 'counter_bet': 'Banker', 'confidence': 65},
            'natural_bias': {'pattern': 'streak_break', 'analysis': 'statistical'},
            'shoe_composition': {'analysis': 'card_counting'},
            'derived_roads': {'analysis': 'advanced_charting'}
        }
        
        self.road_maps = {
            'big_road': [],
            'big_eye_road': [],
            'small_road': [],
            'cockroach_road': []
        }
        
        self.trend_analysis = {
            'banker_dominance': 0,
            'player_dominance': 0,
            'chop_frequency': 0,
            'streak_tendency': 0
        }
    
    def analyze_derived_roads(self, results: List[str]) -> Dict:
        """Analyze derived road patterns for advanced prediction"""
        if len(results) < 10:
            return {'status': 'insufficient_data'}
        
        # Build Big Road
        big_road = self._build_big_road(results)
        
        # Build derived roads
        big_eye_road = self._build_derived_road(big_road, 'big_eye')
        small_road = self._build_derived_road(big_road, 'small')
        cockroach_road = self._build_derived_road(big_road, 'cockroach')
        
        # Analyze patterns
        pattern_analysis = self._analyze_road_patterns(big_eye_road, small_road, cockroach_road)
        
        return {
            'big_road': big_road,
            'derived_roads': {
                'big_eye': big_eye_road,
                'small': small_road,
                'cockroach': cockroach_road
            },
            'pattern_analysis': pattern_analysis,
            'prediction_confidence': self._calculate_road_confidence(pattern_analysis)
        }
    
    def _build_big_road(self, results: List[str]) -> List[List[str]]:
        """Build the Big Road chart"""
        big_road = []
        current_column = []
        current_winner = None
        
        for result in results:
            if result == 'Tie':
                continue
                
            if result == current_winner:
                current_column.append(result)
            else:
                if current_column:
                    big_road.append(current_column)
                current_column = [result]
                current_winner = result
        
        if current_column:
            big_road.append(current_column)
        
        return big_road
    
    def _build_derived_road(self, big_road: List[List[str]], road_type: str) -> List[str]:
        """Build derived roads (Big Eye, Small, Cockroach)"""
        if len(big_road) < 3:
            return []
        
        derived_road = []
        comparison_distance = {'big_eye': 1, 'small': 2, 'cockroach': 3}
        distance = comparison_distance[road_type]
        
        for i in range(distance + 1, len(big_road)):
            current_col = big_road[i]
            compare_col = big_road[i - distance] if i - distance >= 0 else []
            
            if len(current_col) == len(compare_col):
                derived_road.append('R')  # Red - predictable
            else:
                derived_road.append('B')  # Blue - not predictable
        
        return derived_road
    
    def _analyze_road_patterns(self, big_eye: List[str], small: List[str], cockroach: List[str]) -> Dict:
        """Analyze patterns in derived roads"""
        analysis = {
            'predictability_score': 0,
            'pattern_strength': 0,
            'road_consensus': 'neutral'
        }
        
        if not big_eye:
            return analysis
        
        # Calculate predictability
        red_count = sum(1 for road in [big_eye, small, cockroach] for r in road if r == 'R')
        total_count = sum(len(road) for road in [big_eye, small, cockroach])
        
        if total_count > 0:
            predictability = red_count / total_count
            analysis['predictability_score'] = predictability * 100
            
            # Determine consensus
            if predictability > 0.6:
                analysis['road_consensus'] = 'predictable'
                analysis['pattern_strength'] = min(85, predictability * 100)
            elif predictability < 0.4:
                analysis['road_consensus'] = 'chaotic'
                analysis['pattern_strength'] = min(70, (1 - predictability) * 100)
        
        return analysis
    
    def _calculate_road_confidence(self, pattern_analysis: Dict) -> int:
        """Calculate confidence based on road analysis"""
        base_confidence = 50
        
        if pattern_analysis['road_consensus'] == 'predictable':
            confidence = base_confidence + (pattern_analysis['pattern_strength'] * 0.3)
        elif pattern_analysis['road_consensus'] == 'chaotic':
            confidence = base_confidence + (pattern_analysis['pattern_strength'] * 0.2)
        else:
            confidence = base_confidence
        
        return min(int(confidence), 85)

class CardCompositionAnalyzer:
    """Advanced card composition analysis"""
    
    def __init__(self):
        self.card_effects = {
            'A': {'player_favor': 0.5, 'banker_favor': -0.5},
            '2': {'player_favor': 0.4, 'banker_favor': -0.4},
            '3': {'player_favor': 0.3, 'banker_favor': -0.3},
            '4': {'player_favor': 0.8, 'banker_favor': -0.8},
            '5': {'player_favor': -0.7, 'banker_favor': 0.7},
            '6': {'player_favor': -0.6, 'banker_favor': 0.6},
            '7': {'player_favor': -0.3, 'banker_favor': 0.3},
            '8': {'player_favor': -0.1, 'banker_favor': 0.1},
            '9': {'player_favor': -0.1, 'banker_favor': 0.1},
            '10': {'player_favor': 0.1, 'banker_favor': -0.1}
        }
    
    def calculate_true_count(self, card_counts: Dict, cards_remaining: int) -> Dict:
        """Calculate true count for remaining cards"""
        if cards_remaining == 0:
            return {'true_count': 0, 'advantage': 'neutral'}
        
        total_effect = 0
        for card_value, count in card_counts.items():
            if card_value in self.card_effects:
                # Calculate effect of removed cards
                effect = self.card_effects[card_value]['player_favor'] * count
                total_effect += effect
        
        # Calculate true count (effect per remaining deck)
        decks_remaining = cards_remaining / 52
        true_count = total_effect / max(decks_remaining, 0.5)
        
        return {
            'true_count': round(true_count, 2),
            'advantage': 'player' if true_count > 0.5 else 'banker' if true_count < -0.5 else 'neutral',
            'strength': min(abs(true_count) * 10, 100)
        }

class BettingSystemManager:
    """Manages various betting systems and progressions"""
    
    def __init__(self):
        self.systems = {
            'flat': self._flat_betting,
            'martingale': self._martingale_system,
            'fibonacci': self._fibonacci_system,
            'labouchere': self._labouchere_system,
            'paroli': self._paroli_system
        }
        
        self.session_state = {
            'current_sequence': [],
            'wins': 0,
            'losses': 0,
            'current_bet': 0,
            'fibonacci_index': 0
        }
    
    def get_next_bet(self, system_name: str, base_unit: float, max_bet: float, 
                    last_result: Optional[str] = None) -> float:
        """Get the next bet amount based on the system"""
        if system_name not in self.systems:
            return base_unit
        
        return self.systems[system_name](base_unit, max_bet, last_result)
    
    def _flat_betting(self, base_unit: float, max_bet: float, last_result: Optional[str]) -> float:
        """Flat betting system - always bet the same amount"""
        return base_unit
    
    def _martingale_system(self, base_unit: float, max_bet: float, last_result: Optional[str]) -> float:
        """Martingale system - double after loss"""
        if last_result == 'loss':
            next_bet = (self.session_state['current_bet'] or base_unit) * 2
        else:
            next_bet = base_unit
        
        self.session_state['current_bet'] = min(next_bet, max_bet)
        return self.session_state['current_bet']
    
    def _fibonacci_system(self, base_unit: float, max_bet: float, last_result: Optional[str]) -> float:
        """Fibonacci betting system"""
        fib_sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        
        if last_result == 'loss':
            self.session_state['fibonacci_index'] = min(
                self.session_state['fibonacci_index'] + 1, 
                len(fib_sequence) - 1
            )
        elif last_result == 'win' and self.session_state['fibonacci_index'] > 0:
            self.session_state['fibonacci_index'] = max(
                self.session_state['fibonacci_index'] - 2, 
                0
            )
        
        next_bet = base_unit * fib_sequence[self.session_state['fibonacci_index']]
        return min(next_bet, max_bet)
    
    def _labouchere_system(self, base_unit: float, max_bet: float, last_result: Optional[str]) -> float:
        """Labouchere system (cancellation system)"""
        if not self.session_state['current_sequence']:
            self.session_state['current_sequence'] = [1, 2, 3, 4]
        
        sequence = self.session_state['current_sequence']
        
        if not sequence:
            self.session_state['current_sequence'] = [1, 2, 3, 4]
            sequence = self.session_state['current_sequence']
        
        next_bet = base_unit * (sequence[0] + sequence[-1])
        
        if last_result == 'win':
            if len(sequence) > 1:
                sequence.pop(0)
                sequence.pop(-1)
        elif last_result == 'loss':
            sequence.append(int(next_bet / base_unit))
        
        return min(next_bet, max_bet)
    
    def _paroli_system(self, base_unit: float, max_bet: float, last_result: Optional[str]) -> float:
        """Paroli system (reverse martingale)"""
        if last_result == 'win':
            next_bet = (self.session_state['current_bet'] or base_unit) * 2
            self.session_state['wins'] += 1
        else:
            next_bet = base_unit
            self.session_state['wins'] = 0
        
        # Reset after 3 consecutive wins
        if self.session_state['wins'] >= 3:
            next_bet = base_unit
            self.session_state['wins'] = 0
        
        self.session_state['current_bet'] = min(next_bet, max_bet)
        return self.session_state['current_bet']

class AdvancedBaccaratStrategy:
    """Main advanced strategy controller"""
    
    def __init__(self):
        self.pattern_analyzer = AdvancedPatternAnalyzer()
        self.card_analyzer = CardCompositionAnalyzer()
        self.betting_manager = BettingSystemManager()
        
        self.strategy_weights = {
            'pattern_analysis': 0.3,
            'card_composition': 0.25,
            'derived_roads': 0.25,
            'trend_analysis': 0.2
        }
    
    def get_advanced_prediction(self, results_history: List[str], 
                              card_counts: Dict, cards_remaining: int) -> Dict:
        """Generate advanced prediction using multiple analysis methods"""
        
        # 1. Pattern Analysis
        pattern_analysis = self.pattern_analyzer.analyze_derived_roads(results_history)
        
        # 2. Card Composition Analysis
        composition_analysis = self.card_analyzer.calculate_true_count(card_counts, cards_remaining)
        
        # 3. Combine analyses
        prediction = self._combine_analyses(pattern_analysis, composition_analysis)
        
        # 4. Risk Assessment
        risk_assessment = self._assess_risk(prediction, len(results_history))
        
        return {
            'prediction': prediction['bet_recommendation'],
            'confidence': prediction['confidence'],
            'reasoning': prediction['reasoning'],
            'risk_level': risk_assessment['risk_level'],
            'recommended_bet_size': risk_assessment['bet_size'],
            'pattern_strength': pattern_analysis.get('prediction_confidence', 50),
            'card_advantage': composition_analysis.get('strength', 0),
            'advanced_strategy': True
        }
    
    def _combine_analyses(self, pattern_analysis: Dict, composition_analysis: Dict) -> Dict:
        """Combine different analysis methods for final prediction"""
        
        # Start with neutral prediction
        banker_score = 50
        player_score = 50
        reasoning = []
        
        # Apply pattern analysis
        if pattern_analysis.get('status') != 'insufficient_data':
            pattern_conf = pattern_analysis.get('prediction_confidence', 50)
            if pattern_conf > 60:
                # Favor the pattern prediction
                consensus = pattern_analysis.get('pattern_analysis', {}).get('road_consensus', 'neutral')
                if consensus == 'predictable':
                    banker_score += 15
                    reasoning.append("Derived roads show predictable pattern")
                elif consensus == 'chaotic':
                    player_score += 10
                    reasoning.append("Chaotic pattern detected")
        
        # Apply card composition
        if composition_analysis['advantage'] == 'player':
            player_score += composition_analysis['strength'] * 0.3
            reasoning.append(f"Card composition favors player ({composition_analysis['true_count']})")
        elif composition_analysis['advantage'] == 'banker':
            banker_score += composition_analysis['strength'] * 0.3
            reasoning.append(f"Card composition favors banker ({composition_analysis['true_count']})")
        
        # Determine final prediction
        if banker_score > player_score:
            prediction = 'Banker'
            confidence = min(banker_score, 85)
        else:
            prediction = 'Player'
            confidence = min(player_score, 85)
        
        return {
            'bet_recommendation': prediction,
            'confidence': int(confidence),
            'reasoning': '; '.join(reasoning) if reasoning else 'Balanced analysis'
        }
    
    def _assess_risk(self, prediction: Dict, hands_played: int) -> Dict:
        """Assess risk level and recommend bet sizing"""
        
        confidence = prediction['confidence']
        
        if confidence >= 75:
            risk_level = 'low'
            bet_multiplier = 1.5
        elif confidence >= 65:
            risk_level = 'moderate'
            bet_multiplier = 1.2
        elif confidence >= 55:
            risk_level = 'high'
            bet_multiplier = 1.0
        else:
            risk_level = 'very_high'
            bet_multiplier = 0.5
        
        # Adjust for session length
        if hands_played < 10:
            bet_multiplier *= 0.8  # More conservative early in session
        
        return {
            'risk_level': risk_level,
            'bet_size': bet_multiplier,
            'confidence_threshold': confidence
        }
    
    def get_betting_recommendation(self, strategy_name: str, base_unit: float, 
                                 max_bet: float, last_result: Optional[str] = None) -> float:
        """Get betting recommendation based on selected system"""
        return self.betting_manager.get_next_bet(strategy_name, base_unit, max_bet, last_result)
    
    def reset_session(self):
        """Reset all session-specific data"""
        self.betting_manager.session_state = {
            'current_sequence': [],
            'wins': 0,
            'losses': 0,
            'current_bet': 0,
            'fibonacci_index': 0
        }
        
        self.pattern_analyzer.road_maps = {
            'big_road': [],
            'big_eye_road': [],
            'small_road': [],
            'cockroach_road': []
        }