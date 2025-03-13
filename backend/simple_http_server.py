import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs

# Define the port
PORT = 5000

# Global variables
preferred_currency = "EUR"
personality_mode = "balanced"

class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        self._set_headers()
        
    def do_GET(self):
        global preferred_currency
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == "/":
            self._set_headers("text/html")
            self.wfile.write(b"MindfulWealth API is running!")
            return
            
        if path == "/api/currency":
            self._set_headers()
            response = {"currency": preferred_currency}
            self.wfile.write(json.dumps(response).encode())
            return
            
        if path == "/api/transactions":
            self._set_headers()
            mock_transactions = [
                {
                    'id': 1,
                    'amount': 100.0,
                    'category': 'Food',
                    'date': '2023-03-01T12:00:00',
                    'description': 'Grocery shopping'
                },
                {
                    'id': 2,
                    'amount': 50.0,
                    'category': 'Entertainment',
                    'date': '2023-03-02T18:30:00',
                    'description': 'Movie tickets'
                }
            ]
            self.wfile.write(json.dumps(mock_transactions).encode())
            return
            
        if path == "/api/budget":
            self._set_headers()
            mock_budget = {
                'total': 1000.0,
                'spent': 500.0,
                'categories': [
                    {
                        'name': 'Food',
                        'planned': 300.0,
                        'actual': 250.0
                    },
                    {
                        'name': 'Entertainment',
                        'planned': 200.0,
                        'actual': 150.0
                    },
                    {
                        'name': 'Transportation',
                        'planned': 150.0,
                        'actual': 100.0
                    }
                ]
            }
            self.wfile.write(json.dumps(mock_budget).encode())
            return
            
        if path == "/api/saved-impulses":
            self._set_headers()
            mock_impulses = [
                {
                    'id': 1,
                    'item': 'Designer shoes',
                    'amount': 200.0,
                    'category': 'Clothing',
                    'date': '2023-03-01T12:00:00',
                    'potential_value': 216.0
                },
                {
                    'id': 2,
                    'item': 'Smart watch',
                    'amount': 300.0,
                    'category': 'Electronics',
                    'date': '2023-03-02T18:30:00',
                    'potential_value': 324.0
                }
            ]
            self.wfile.write(json.dumps(mock_impulses).encode())
            return
            
        if path == "/api/dashboard":
            self._set_headers()
            mock_dashboard = {
                'total_spent': 500.0,
                'total_budget': 1000.0,
                'total_saved': 500.0,
                'potential_growth': 540.0,
                'categories': [
                    {
                        'name': 'Food',
                        'spent': 250.0,
                        'budget': 300.0
                    },
                    {
                        'name': 'Entertainment',
                        'spent': 150.0,
                        'budget': 200.0
                    },
                    {
                        'name': 'Transportation',
                        'spent': 100.0,
                        'budget': 150.0
                    }
                ],
                'recent_transactions': [
                    {
                        'id': 1,
                        'amount': 100.0,
                        'category': 'Food',
                        'date': '2023-03-01T12:00:00',
                        'description': 'Grocery shopping'
                    },
                    {
                        'id': 2,
                        'amount': 50.0,
                        'category': 'Entertainment',
                        'date': '2023-03-02T18:30:00',
                        'description': 'Movie tickets'
                    }
                ],
                'saved_impulses': [
                    {
                        'id': 1,
                        'item': 'Designer shoes',
                        'amount': 200.0,
                        'category': 'Clothing',
                        'date': '2023-03-01T12:00:00',
                        'potential_value': 216.0
                    },
                    {
                        'id': 2,
                        'item': 'Smart watch',
                        'amount': 300.0,
                        'category': 'Electronics',
                        'date': '2023-03-02T18:30:00',
                        'potential_value': 324.0
                    }
                ]
            }
            self.wfile.write(json.dumps(mock_dashboard).encode())
            return
            
        # Default response for unknown paths
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"error": "Not found"}
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        global preferred_currency, personality_mode
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            response = {"error": "Invalid JSON"}
            self.wfile.write(json.dumps(response).encode())
            return
            
        if path == "/api/currency":
            currency = data.get('currency', 'EUR')
            
            # Validate currency
            valid_currencies = ['USD', 'EUR', 'GBP', 'JPY']
            if currency not in valid_currencies:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'success': False, 'error': 'Invalid currency'}
                self.wfile.write(json.dumps(response).encode())
                return
                
            preferred_currency = currency
            self._set_headers()
            response = {'success': True, 'currency': preferred_currency}
            self.wfile.write(json.dumps(response).encode())
            return
            
        if path == "/api/personality":
            mode = data.get('mode', 'balanced')
            
            # Validate mode
            valid_modes = ['conservative', 'balanced', 'aggressive']
            if mode not in valid_modes:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {'success': False, 'error': 'Invalid personality mode'}
                self.wfile.write(json.dumps(response).encode())
                return
                
            personality_mode = mode
            self._set_headers()
            response = {'success': True, 'mode': personality_mode}
            self.wfile.write(json.dumps(response).encode())
            return
            
        if path == "/api/chat":
            message = data.get('message', '')
            
            # Simple mock response
            response_text = f"You said: {message}. This is a test response from the backend."
            
            self._set_headers()
            response = {
                'response': response_text,
                'financial_data': None
            }
            self.wfile.write(json.dumps(response).encode())
            return
            
        # Default response for unknown paths
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {"error": "Not found"}
        self.wfile.write(json.dumps(response).encode())

def run_server():
    handler = SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")
            httpd.server_close()

if __name__ == "__main__":
    run_server() 