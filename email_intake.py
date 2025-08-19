#!/usr/bin/env python3
"""
Email Intake System for Business Support Coordinators

This module provides a web-based intake system that allows anyone to submit
support requests via email to business support coordinators.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Dict, Optional
from dataclasses import dataclass
import json


@dataclass
class SupportRequest:
    """Represents a support request submitted through the intake system."""
    name: str
    email: str
    department: str
    priority: str
    subject: str
    description: str
    timestamp: str
    request_id: str


class EmailIntakeSystem:
    """Email intake system for business support coordinators."""
    
    def __init__(self, coordinator_email: str = "support@company.com"):
        self.coordinator_email = coordinator_email
        self.smtp_server = os.getenv('SMTP_SERVER', 'localhost')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.requests_log = "support_requests.json"
    
    def generate_request_id(self) -> str:
        """Generate a unique request ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"REQ_{timestamp}"
    
    def create_support_request(self, name: str, email: str, department: str, 
                             priority: str, subject: str, description: str) -> SupportRequest:
        """Create a new support request."""
        request = SupportRequest(
            name=name,
            email=email,
            department=department,
            priority=priority,
            subject=subject,
            description=description,
            timestamp=datetime.now().isoformat(),
            request_id=self.generate_request_id()
        )
        return request
    
    def log_request(self, request: SupportRequest) -> None:
        """Log the request to a JSON file for tracking."""
        try:
            # Load existing requests
            if os.path.exists(self.requests_log):
                with open(self.requests_log, 'r') as f:
                    requests = json.load(f)
            else:
                requests = []
            
            # Add new request
            request_dict = {
                'request_id': request.request_id,
                'name': request.name,
                'email': request.email,
                'department': request.department,
                'priority': request.priority,
                'subject': request.subject,
                'description': request.description,
                'timestamp': request.timestamp
            }
            requests.append(request_dict)
            
            # Save updated requests
            with open(self.requests_log, 'w') as f:
                json.dump(requests, f, indent=2)
                
        except Exception as e:
            print(f"Error logging request: {e}")
    
    def format_email_body(self, request: SupportRequest) -> str:
        """Format the email body for the support request."""
        return f"""
New Support Request Received

Request ID: {request.request_id}
Submitted: {request.timestamp}

REQUESTOR INFORMATION:
Name: {request.name}
Email: {request.email}
Department: {request.department}

REQUEST DETAILS:
Priority: {request.priority}
Subject: {request.subject}

Description:
{request.description}

---
This request was submitted through the Business Support Intake System.
Please respond directly to {request.email} for any follow-up questions.
        """.strip()
    
    def send_email_notification(self, request: SupportRequest) -> bool:
        """Send email notification to business support coordinators."""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username or request.email
            msg['To'] = self.coordinator_email
            msg['Subject'] = f"[{request.priority.upper()}] Support Request: {request.subject}"
            
            # Attach body
            body = self.format_email_body(request)
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.smtp_username and self.smtp_password:
                    server.starttls()
                    server.login(self.smtp_username, self.smtp_password)
                
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def send_confirmation_email(self, request: SupportRequest) -> bool:
        """Send confirmation email to the requestor."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username or self.coordinator_email
            msg['To'] = request.email
            msg['Subject'] = f"Support Request Received - {request.request_id}"
            
            body = f"""
Thank you for submitting your support request.

Request ID: {request.request_id}
Subject: {request.subject}
Priority: {request.priority}
Submitted: {request.timestamp}

Our business support coordinators will review your request and respond within 24-48 hours for standard priority items, or within 4 hours for high priority items.

For urgent matters, please contact our support team directly at {self.coordinator_email}.

Best regards,
Business Support Team
            """.strip()
            
            msg.attach(MIMEText(body, 'plain'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.smtp_username and self.smtp_password:
                    server.starttls()
                    server.login(self.smtp_username, self.smtp_password)
                
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            print(f"Error sending confirmation email: {e}")
            return False
    
    def submit_request(self, name: str, email: str, department: str = "General", 
                      priority: str = "Medium", subject: str = "", 
                      description: str = "") -> Dict:
        """Submit a new support request."""
        
        # Validate required fields
        if not all([name, email, subject, description]):
            return {
                'success': False,
                'error': 'Name, email, subject, and description are required fields.'
            }
        
        # Create request
        request = self.create_support_request(
            name=name,
            email=email,
            department=department,
            priority=priority,
            subject=subject,
            description=description
        )
        
        # Log request
        self.log_request(request)
        
        # Send notifications
        email_sent = self.send_email_notification(request)
        confirmation_sent = self.send_confirmation_email(request)
        
        return {
            'success': True,
            'request_id': request.request_id,
            'email_sent': email_sent,
            'confirmation_sent': confirmation_sent,
            'timestamp': request.timestamp
        }
    
    def get_request_history(self, limit: int = 50) -> list:
        """Get recent support requests."""
        try:
            if os.path.exists(self.requests_log):
                with open(self.requests_log, 'r') as f:
                    requests = json.load(f)
                    return requests[-limit:]  # Return most recent requests
            return []
        except Exception as e:
            print(f"Error reading request history: {e}")
            return []
    
    def get_request_stats(self) -> Dict:
        """Get statistics about support requests."""
        requests = self.get_request_history(1000)  # Get more for stats
        
        if not requests:
            return {'total': 0, 'by_priority': {}, 'by_department': {}}
        
        stats = {
            'total': len(requests),
            'by_priority': {},
            'by_department': {}
        }
        
        for req in requests:
            priority = req.get('priority', 'Unknown')
            department = req.get('department', 'Unknown')
            
            stats['by_priority'][priority] = stats['by_priority'].get(priority, 0) + 1
            stats['by_department'][department] = stats['by_department'].get(department, 0) + 1
        
        return stats


def main():
    """Demo the email intake system."""
    intake = EmailIntakeSystem()
    
    print("Business Support Email Intake System")
    print("=" * 45)
    
    # Example request submission
    print("\nSubmitting example support request...")
    
    result = intake.submit_request(
        name="John Doe",
        email="john.doe@company.com",
        department="IT",
        priority="High",
        subject="Password Reset Request",
        description="I need help resetting my password for the company portal. I've tried the self-service option but it's not working."
    )
    
    if result['success']:
        print(f"✅ Request submitted successfully!")
        print(f"Request ID: {result['request_id']}")
        print(f"Timestamp: {result['timestamp']}")
        print(f"Email notification sent: {result['email_sent']}")
        print(f"Confirmation email sent: {result['confirmation_sent']}")
    else:
        print(f"❌ Error: {result['error']}")
    
    # Show request history
    print(f"\nRecent Support Requests:")
    print("-" * 30)
    
    history = intake.get_request_history(5)
    for request in history:
        print(f"ID: {request['request_id']}")
        print(f"From: {request['name']} ({request['email']})")
        print(f"Subject: {request['subject']}")
        print(f"Priority: {request['priority']}")
        print(f"Department: {request['department']}")
        print(f"Submitted: {request['timestamp']}")
        print("-" * 30)
    
    # Show stats
    stats = intake.get_request_stats()
    print(f"\nSupport Request Statistics:")
    print(f"Total requests: {stats['total']}")
    print(f"By priority: {stats['by_priority']}")
    print(f"By department: {stats['by_department']}")


if __name__ == "__main__":
    main()