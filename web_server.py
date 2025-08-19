#!/usr/bin/env python3
"""
Web server for the Lawn Calculator UI
Serves the static HTML/CSS/JS files and provides API endpoints
"""

import os
import json
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import socketserver
from lawn_care_calculator import LawnCareCalculator, Region, LawnCareActivity


class LawnCalculatorHandler(SimpleHTTPRequestHandler):
    """Custom handler for the lawn calculator web interface"""
    
    def __init__(self, *args, **kwargs):
        # Initialize the lawn care calculator
        self.calculator = LawnCareCalculator()
        super().__init__(*args, directory='static', **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            # Serve the main page
            self.path = '/index.html'
        elif parsed_path.path == '/api/schedule':
            # API endpoint for schedule data
            self.handle_schedule_api(parsed_path.query)
            return
        elif parsed_path.path == '/api/timing':
            # API endpoint for timing window data
            self.handle_timing_api(parsed_path.query)
            return
        
        # Serve static files
        super().do_GET()
    
    def handle_schedule_api(self, query_string):
        """Handle schedule API requests"""
        try:
            params = parse_qs(query_string)
            region_str = params.get('region', ['central'])[0]
            month = int(params.get('month', [datetime.now().month])[0])
            
            # Set calculator region
            region = Region(region_str)
            self.calculator = LawnCareCalculator(region)
            
            # Get activities for the specified month
            activities = self.calculator.get_all_activities_for_month(month)
            activity_list = []
            
            for activity in activities:
                window = self.calculator.get_timing_window(activity)
                activity_list.append({
                    'name': activity.value.replace('_', ' ').title(),
                    'temp_min': window.optimal_temp_min,
                    'temp_max': window.optimal_temp_max,
                    'description': window.description
                })
            
            response_data = {
                'region': region_str,
                'month': month,
                'activities': activity_list
            }
            
            self.send_json_response(response_data)
            
        except Exception as e:
            self.send_error_response(str(e))
    
    def handle_timing_api(self, query_string):
        """Handle timing window API requests"""
        try:
            params = parse_qs(query_string)
            activity_str = params.get('activity', ['seeding'])[0]
            region_str = params.get('region', ['central'])[0]
            
            # Set calculator region
            region = Region(region_str)
            self.calculator = LawnCareCalculator(region)
            
            # Get timing window for activity
            activity = LawnCareActivity(activity_str)
            window_info = self.calculator.get_next_optimal_window(activity)
            
            self.send_json_response(window_info)
            
        except Exception as e:
            self.send_error_response(str(e))
    
    def send_json_response(self, data):
        """Send a JSON response"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        json_data = json.dumps(data, indent=2)
        self.wfile.write(json_data.encode('utf-8'))
    
    def send_error_response(self, error_message):
        """Send an error response"""
        self.send_response(400)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        error_data = {'error': error_message}
        json_data = json.dumps(error_data)
        self.wfile.write(json_data.encode('utf-8'))
    
    def log_message(self, format, *args):
        """Override to provide cleaner logging"""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {format % args}")


def run_server(port=8000):
    """Run the web server"""
    
    # Check if static directory exists
    static_dir = os.path.join(os.getcwd(), 'static')
    if not os.path.exists(static_dir):
        print(f"Error: Static directory '{static_dir}' not found!")
        print("Make sure you run this from the project root directory.")
        return
    
    # Create and start server
    with socketserver.TCPServer(("", port), LawnCalculatorHandler) as httpd:
        print(f"Lawn Calculator Web Server")
        print(f"Serving at http://localhost:{port}")
        print(f"Static files from: {static_dir}")
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped by user")
            httpd.shutdown()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Lawn Calculator Web Server')
    parser.add_argument('--port', '-p', type=int, default=8000,
                       help='Port to serve on (default: 8000)')
    
    args = parser.parse_args()
    run_server(args.port)