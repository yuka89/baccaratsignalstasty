"""
Baccarat Predictor Web Application
Flask-based web interface for the baccarat predictor
"""

from flask import Flask, render_template, request, jsonify, session
import json
import os
from datetime import datetime
from baccarat_predictor import BaccaratPredictor
from advanced_strategy import AdvancedBaccaratStrategy

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Global predictors
predictors = {}

def get_predictor(session_id):
    """Get or create a predictor for the session"""
    if session_id not in predictors:
        predictors[session_id] = {
            'basic': BaccaratPredictor(),
            'advanced': AdvancedBaccaratStrategy()
        }
    return predictors[session_id]

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/new_shoe', methods=['POST'])
def new_shoe():
    """Start a new shoe"""
    session_id = session.get('session_id', 'default')
    predictor = get_predictor(session_id)
    
    predictor['basic'].new_shoe()
    predictor['advanced'].reset_session()
    
    return jsonify({
        'status': 'success',
        'message': 'New shoe started',
        'cards_remaining': predictor['basic'].shoe.cards_remaining()
    })

@app.route('/api/get_prediction', methods=['GET'])
def get_prediction():
    """Get prediction for next hand"""
    session_id = session.get('session_id', 'default')
    predictor = get_predictor(session_id)
    
    # Get basic prediction
    basic_prediction = predictor['basic'].get_prediction()
    
    # Get advanced prediction if we have enough data
    advanced_prediction = None
    if len(predictor['basic'].results_history) >= 5:
        results_history = [r.winner for r in predictor['basic'].results_history]
        card_counts = predictor['basic'].card_counter.card_counts
        cards_remaining = predictor['basic'].shoe.cards_remaining()
        
        advanced_prediction = predictor['advanced'].get_advanced_prediction(
            results_history, card_counts, cards_remaining
        )
    
    return jsonify({
        'basic_prediction': basic_prediction,
        'advanced_prediction': advanced_prediction,
        'session_stats': predictor['basic'].get_session_stats()
    })

@app.route('/api/deal_hand', methods=['POST'])
def deal_hand():
    """Deal a hand and return the result"""
    session_id = session.get('session_id', 'default')
    predictor = get_predictor(session_id)
    
    result = predictor['basic'].deal_hand()
    if result:
        return jsonify({
            'status': 'success',
            'result': {
                'player_cards': [str(card) for card in result.player_hand.cards],
                'banker_cards': [str(card) for card in result.banker_hand.cards],
                'player_value': result.player_hand.value(),
                'banker_value': result.banker_hand.value(),
                'winner': result.winner,
                'timestamp': result.timestamp.isoformat()
            },
            'session_stats': predictor['basic'].get_session_stats()
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Not enough cards remaining'
        })

@app.route('/api/record_prediction', methods=['POST'])
def record_prediction():
    """Record a prediction result"""
    session_id = session.get('session_id', 'default')
    predictor = get_predictor(session_id)
    
    data = request.json
    prediction = data.get('prediction')
    actual = data.get('actual')
    
    predictor['basic'].record_prediction_result(prediction, actual)
    
    return jsonify({
        'status': 'success',
        'session_stats': predictor['basic'].get_session_stats()
    })

@app.route('/api/auto_play', methods=['POST'])
def auto_play():
    """Auto play multiple hands"""
    session_id = session.get('session_id', 'default')
    predictor = get_predictor(session_id)
    
    data = request.json
    num_hands = data.get('num_hands', 3)
    
    results = []
    for i in range(min(num_hands, 10)):  # Limit to 10 hands
        # Get prediction
        prediction = predictor['basic'].get_prediction()
        
        # Deal hand
        result = predictor['basic'].deal_hand()
        if result:
            # Record prediction
            predictor['basic'].record_prediction_result(prediction['prediction'], result.winner)
            
            results.append({
                'hand_number': i + 1,
                'prediction': prediction,
                'result': {
                    'player_value': result.player_hand.value(),
                    'banker_value': result.banker_hand.value(),
                    'winner': result.winner
                },
                'correct': prediction['prediction'] == result.winner
            })
        else:
            break
    
    return jsonify({
        'status': 'success',
        'results': results,
        'session_stats': predictor['basic'].get_session_stats()
    })

@app.route('/api/get_stats', methods=['GET'])
def get_stats():
    """Get session statistics"""
    session_id = session.get('session_id', 'default')
    predictor = get_predictor(session_id)
    
    stats = predictor['basic'].get_session_stats()
    
    # Add recent results
    recent_results = []
    for result in predictor['basic'].results_history[-10:]:
        recent_results.append({
            'winner': result.winner,
            'player_value': result.player_hand.value(),
            'banker_value': result.banker_hand.value(),
            'timestamp': result.timestamp.isoformat()
        })
    
    return jsonify({
        'stats': stats,
        'recent_results': recent_results,
        'cards_remaining': predictor['basic'].shoe.cards_remaining()
    })

@app.route('/api/betting_recommendation', methods=['POST'])
def betting_recommendation():
    """Get betting recommendation based on strategy"""
    session_id = session.get('session_id', 'default')
    predictor = get_predictor(session_id)
    
    data = request.json
    strategy = data.get('strategy', 'flat')
    base_unit = data.get('base_unit', 10)
    max_bet = data.get('max_bet', 100)
    last_result = data.get('last_result', None)
    
    bet_amount = predictor['advanced'].get_betting_recommendation(
        strategy, base_unit, max_bet, last_result
    )
    
    return jsonify({
        'recommended_bet': bet_amount,
        'strategy': strategy,
        'base_unit': base_unit
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)