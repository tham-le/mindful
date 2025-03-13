#!/usr/bin/env python3
"""
Test script to check if we can run a Flask server
"""
try:
    from flask import Flask, jsonify
    
    app = Flask(__name__)
    
    @app.route('/api/test', methods=['GET'])
    def test():
        return jsonify({'message': 'Flask server is running!'})
    
    if __name__ == '__main__':
        print("Starting Flask server on port 5001...")
        app.run(debug=True, host='0.0.0.0', port=5001)
except ImportError as e:
    print(f"Error importing Flask: {e}")
    print("Please install Flask with: pip install flask")

try:
    import sys
    print(f"Python path: {sys.path}")
except Exception as e:
    print(f"Error: {e}") 