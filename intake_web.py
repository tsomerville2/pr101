#!/usr/bin/env python3
"""
Web interface for the Business Support Email Intake System

This module provides a simple web interface using Flask for submitting support requests.
"""

try:
    from flask import Flask, render_template_string, request, redirect, url_for, flash, jsonify
except ImportError:
    print("Flask not installed. Install with: pip install flask")
    exit(1)

from email_intake import EmailIntakeSystem
import os


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize intake system
intake_system = EmailIntakeSystem()


# HTML Templates
INTAKE_FORM_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Business Support Request</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background-color: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
        input, select, textarea { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; }
        textarea { height: 120px; resize: vertical; }
        .btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        .btn:hover { background: #0056b3; }
        .alert { padding: 15px; margin-bottom: 20px; border-radius: 4px; }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .alert-error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .required { color: red; }
        .help-text { font-size: 12px; color: #666; margin-top: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Business Support Request</h1>
        <p>Please fill out this form to submit a support request to our business support coordinators. All fields marked with <span class="required">*</span> are required.</p>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST" action="{{ url_for('submit_request') }}">
            <div class="form-group">
                <label for="name">Full Name <span class="required">*</span></label>
                <input type="text" id="name" name="name" required value="{{ request.form.get('name', '') }}">
            </div>
            
            <div class="form-group">
                <label for="email">Email Address <span class="required">*</span></label>
                <input type="email" id="email" name="email" required value="{{ request.form.get('email', '') }}">
                <div class="help-text">We'll send a confirmation and any updates to this email address.</div>
            </div>
            
            <div class="form-group">
                <label for="department">Department</label>
                <select id="department" name="department">
                    <option value="General" {% if request.form.get('department') == 'General' %}selected{% endif %}>General</option>
                    <option value="IT" {% if request.form.get('department') == 'IT' %}selected{% endif %}>IT</option>
                    <option value="HR" {% if request.form.get('department') == 'HR' %}selected{% endif %}>Human Resources</option>
                    <option value="Finance" {% if request.form.get('department') == 'Finance' %}selected{% endif %}>Finance</option>
                    <option value="Operations" {% if request.form.get('department') == 'Operations' %}selected{% endif %}>Operations</option>
                    <option value="Marketing" {% if request.form.get('department') == 'Marketing' %}selected{% endif %}>Marketing</option>
                    <option value="Other" {% if request.form.get('department') == 'Other' %}selected{% endif %}>Other</option>
                </select>
            </div>
            
            <div class="form-group">
                <label for="priority">Priority Level</label>
                <select id="priority" name="priority">
                    <option value="Low" {% if request.form.get('priority') == 'Low' %}selected{% endif %}>Low - General inquiry or non-urgent request</option>
                    <option value="Medium" {% if request.form.get('priority') == 'Medium' or not request.form.get('priority') %}selected{% endif %}>Medium - Standard business request</option>
                    <option value="High" {% if request.form.get('priority') == 'High' %}selected{% endif %}>High - Urgent business need</option>
                    <option value="Critical" {% if request.form.get('priority') == 'Critical' %}selected{% endif %}>Critical - Business stopping issue</option>
                </select>
                <div class="help-text">Please select the appropriate priority level for your request.</div>
            </div>
            
            <div class="form-group">
                <label for="subject">Subject <span class="required">*</span></label>
                <input type="text" id="subject" name="subject" required value="{{ request.form.get('subject', '') }}" placeholder="Brief description of your request">
            </div>
            
            <div class="form-group">
                <label for="description">Detailed Description <span class="required">*</span></label>
                <textarea id="description" name="description" required placeholder="Please provide a detailed description of your request, including any relevant background information, specific requirements, or steps you've already tried.">{{ request.form.get('description', '') }}</textarea>
            </div>
            
            <button type="submit" class="btn">Submit Support Request</button>
        </form>
        
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #666;">
            <p><strong>What happens next?</strong></p>
            <ul>
                <li>You'll receive an email confirmation with your request ID</li>
                <li>A business support coordinator will review your request</li>
                <li>Response times: Critical (1-2 hours), High (4 hours), Medium (24-48 hours), Low (3-5 business days)</li>
                <li>You'll be contacted directly via email with updates or questions</li>
            </ul>
        </div>
    </div>
</body>
</html>
"""

SUCCESS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Request Submitted Successfully</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; background-color: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }
        h1 { color: #28a745; margin-bottom: 20px; }
        .request-id { font-size: 24px; font-weight: bold; color: #007bff; margin: 20px 0; }
        .details { text-align: left; background: #f8f9fa; padding: 20px; border-radius: 4px; margin: 20px 0; }
        .btn { display: inline-block; background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; margin: 10px; }
        .btn:hover { background: #0056b3; }
        .icon { font-size: 48px; color: #28a745; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="icon">✅</div>
        <h1>Request Submitted Successfully!</h1>
        
        <p>Your support request has been submitted and forwarded to our business support coordinators.</p>
        
        <div class="request-id">Request ID: {{ request_id }}</div>
        
        <div class="details">
            <h3>Request Details:</h3>
            <p><strong>Subject:</strong> {{ subject }}</p>
            <p><strong>Priority:</strong> {{ priority }}</p>
            <p><strong>Department:</strong> {{ department }}</p>
            <p><strong>Submitted:</strong> {{ timestamp }}</p>
        </div>
        
        <p>A confirmation email has been sent to <strong>{{ email }}</strong>.</p>
        
        <p>Our business support coordinators will review your request and respond according to the priority level selected.</p>
        
        <a href="{{ url_for('index') }}" class="btn">Submit Another Request</a>
        <a href="{{ url_for('view_stats') }}" class="btn">View Request Statistics</a>
    </div>
</body>
</html>
"""

STATS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Support Request Statistics</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; background-color: #f5f5f5; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        h1 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }
        .stat-card { background: #f8f9fa; padding: 20px; border-radius: 4px; border-left: 4px solid #007bff; }
        .stat-number { font-size: 24px; font-weight: bold; color: #007bff; }
        .btn { display: inline-block; background: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; margin: 10px 0; }
        .btn:hover { background: #0056b3; }
        .request-item { border-bottom: 1px solid #eee; padding: 15px 0; }
        .request-item:last-child { border-bottom: none; }
        .priority-high { color: #dc3545; font-weight: bold; }
        .priority-medium { color: #ffc107; font-weight: bold; }
        .priority-low { color: #28a745; font-weight: bold; }
        .priority-critical { color: #dc3545; font-weight: bold; background: #f8d7da; padding: 2px 6px; border-radius: 3px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Support Request Statistics</h1>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{{ stats.total }}</div>
                <div>Total Requests</div>
            </div>
            
            {% for priority, count in stats.by_priority.items() %}
            <div class="stat-card">
                <div class="stat-number">{{ count }}</div>
                <div>{{ priority }} Priority</div>
            </div>
            {% endfor %}
        </div>
        
        <h2>Recent Requests</h2>
        <div>
            {% for request in recent_requests %}
            <div class="request-item">
                <div><strong>{{ request.request_id }}</strong></div>
                <div>{{ request.name }} ({{ request.department }})</div>
                <div>{{ request.subject }}</div>
                <div class="priority-{{ request.priority.lower() }}">{{ request.priority }} Priority</div>
                <div style="font-size: 12px; color: #666;">{{ request.timestamp }}</div>
            </div>
            {% endfor %}
        </div>
        
        <a href="{{ url_for('index') }}" class="btn">Submit New Request</a>
    </div>
</body>
</html>
"""


@app.route('/')
def index():
    """Display the intake form."""
    return render_template_string(INTAKE_FORM_TEMPLATE)


@app.route('/submit', methods=['POST'])
def submit_request():
    """Process the submitted support request."""
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        department = request.form.get('department', 'General')
        priority = request.form.get('priority', 'Medium')
        subject = request.form.get('subject', '').strip()
        description = request.form.get('description', '').strip()
        
        # Submit the request
        result = intake_system.submit_request(
            name=name,
            email=email,
            department=department,
            priority=priority,
            subject=subject,
            description=description
        )
        
        if result['success']:
            return render_template_string(SUCCESS_TEMPLATE,
                request_id=result['request_id'],
                subject=subject,
                priority=priority,
                department=department,
                email=email,
                timestamp=result['timestamp']
            )
        else:
            flash(result['error'], 'error')
            return render_template_string(INTAKE_FORM_TEMPLATE)
            
    except Exception as e:
        flash(f'An error occurred while processing your request: {str(e)}', 'error')
        return render_template_string(INTAKE_FORM_TEMPLATE)


@app.route('/stats')
def view_stats():
    """Display support request statistics."""
    stats = intake_system.get_request_stats()
    recent_requests = intake_system.get_request_history(10)
    
    return render_template_string(STATS_TEMPLATE,
        stats=stats,
        recent_requests=recent_requests
    )


@app.route('/api/submit', methods=['POST'])
def api_submit_request():
    """API endpoint for submitting requests programmatically."""
    try:
        data = request.get_json()
        
        result = intake_system.submit_request(
            name=data.get('name', ''),
            email=data.get('email', ''),
            department=data.get('department', 'General'),
            priority=data.get('priority', 'Medium'),
            subject=data.get('subject', ''),
            description=data.get('description', '')
        )
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/stats')
def api_get_stats():
    """API endpoint for getting support statistics."""
    stats = intake_system.get_request_stats()
    return jsonify(stats)


if __name__ == '__main__':
    print("Starting Business Support Email Intake Web Interface...")
    print("Access the form at: http://localhost:5000")
    print("View statistics at: http://localhost:5000/stats")
    print("API endpoints:")
    print("  POST /api/submit - Submit request via API")
    print("  GET /api/stats - Get statistics via API")
    print("")
    
    app.run(debug=True, host='0.0.0.0', port=5000)