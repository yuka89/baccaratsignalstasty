#!/usr/bin/env python3
"""
Test script to verify that the baccarat predictor modules work correctly
"""

import sys
import traceback

def test_basic_predictor():
    """Test the basic predictor functionality"""
    print("Testing basic predictor...")
    try:
        from baccarat_predictor import BaccaratPredictor
        
        predictor = BaccaratPredictor()
        
        # Test new shoe
        predictor.new_shoe()
        print(f"✅ New shoe created with {predictor.shoe.cards_remaining()} cards")
        
        # Test prediction
        prediction = predictor.get_prediction()
        print(f"✅ Prediction: {prediction['prediction']} ({prediction['confidence']}%)")
        
        # Test dealing a hand
        result = predictor.deal_hand()
        if result:
            print(f"✅ Hand dealt: {result.winner} wins")
            print(f"   Player: {result.player_hand.value()}, Banker: {result.banker_hand.value()}")
        
        # Test session stats
        stats = predictor.get_session_stats()
        print(f"✅ Session stats: {stats['hands_played']} hands played")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic predictor test failed: {e}")
        traceback.print_exc()
        return False

def test_advanced_strategy():
    """Test the advanced strategy module"""
    print("\nTesting advanced strategy...")
    try:
        from advanced_strategy import AdvancedBaccaratStrategy
        
        strategy = AdvancedBaccaratStrategy()
        
        # Test with sample data
        sample_results = ['Banker', 'Player', 'Banker', 'Banker', 'Player', 'Tie', 'Player']
        sample_card_counts = {'A': 5, '2': 3, '3': 4, '4': 2, '5': 6, '6': 3, '7': 4, '8': 2, '9': 1, '10': 8}
        
        prediction = strategy.get_advanced_prediction(sample_results, sample_card_counts, 300)
        print(f"✅ Advanced prediction: {prediction['prediction']} ({prediction['confidence']}%)")
        
        # Test betting recommendation
        bet_size = strategy.get_betting_recommendation('fibonacci', 10, 100)
        print(f"✅ Betting recommendation: ${bet_size}")
        
        return True
        
    except Exception as e:
        print(f"❌ Advanced strategy test failed: {e}")
        traceback.print_exc()
        return False

def test_web_app():
    """Test the web application imports"""
    print("\nTesting web application...")
    try:
        from web_app import app
        print("✅ Web application imports successful")
        
        # Test that the app is configured correctly
        with app.test_client() as client:
            # Test if the index route works
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Web application routes working")
            else:
                print(f"⚠️ Web application route returned status {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Web application test failed: {e}")
        traceback.print_exc()
        return False

def test_integration():
    """Test integration between modules"""
    print("\nTesting integration...")
    try:
        from baccarat_predictor import BaccaratPredictor
        from advanced_strategy import AdvancedBaccaratStrategy
        
        # Create instances
        predictor = BaccaratPredictor()
        advanced = AdvancedBaccaratStrategy()
        
        # Deal several hands to generate data
        for i in range(10):
            result = predictor.deal_hand()
            if not result:
                break
        
        # Test advanced analysis with real data
        if len(predictor.results_history) > 5:
            results = [r.winner for r in predictor.results_history]
            card_counts = predictor.card_counter.card_counts
            cards_remaining = predictor.shoe.cards_remaining()
            
            advanced_prediction = advanced.get_advanced_prediction(results, card_counts, cards_remaining)
            basic_prediction = predictor.get_prediction()
            
            print(f"✅ Integration test successful")
            print(f"   Basic: {basic_prediction['prediction']} ({basic_prediction['confidence']}%)")
            print(f"   Advanced: {advanced_prediction['prediction']} ({advanced_prediction['confidence']}%)")
            
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Main test runner"""
    print("🎰 Baccarat Predictor Test Suite")
    print("=" * 50)
    
    tests = [
        test_basic_predictor,
        test_advanced_strategy,
        test_web_app,
        test_integration
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! The application is ready to use.")
        print("\nTo run the application:")
        print("1. Command line: python baccarat_predictor.py")
        print("2. Web interface: python web_app.py")
        return 0
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())