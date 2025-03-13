import sys
print(f"Python path: {sys.path}")

try:
    from flask import Flask
    print("Flask imported successfully!")
    
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return "Hello, World!"
    
    if __name__ == '__main__':
        print("Starting Flask app...")
        app.run(debug=True, host='0.0.0.0', port=5000)
except ImportError as e:
    print(f"Error importing Flask: {e}")
    sys.exit(1) 