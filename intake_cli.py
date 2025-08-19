#!/usr/bin/env python3
"""
Command-line interface for the Business Support Email Intake System
"""

import argparse
import sys
import json
from email_intake import EmailIntakeSystem


def main():
    """Main CLI entry point for the intake system."""
    parser = argparse.ArgumentParser(
        description="Business Support Email Intake System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python intake_cli.py --submit
  python intake_cli.py --list --limit 10
  python intake_cli.py --stats
  python intake_cli.py --web
  
  # API submission example:
  python intake_cli.py --submit --name "John Doe" --email "john@company.com" \\
    --subject "Help needed" --description "I need assistance with..."
        """
    )
    
    parser.add_argument('--submit', '-s',
                       action='store_true',
                       help='Submit a new support request (interactive mode)')
    
    parser.add_argument('--list', '-l',
                       action='store_true',
                       help='List recent support requests')
    
    parser.add_argument('--stats', '--statistics',
                       action='store_true',
                       help='Show support request statistics')
    
    parser.add_argument('--web', '-w',
                       action='store_true',
                       help='Start web interface server')
    
    parser.add_argument('--limit',
                       type=int,
                       default=10,
                       help='Limit number of requests to show (default: 10)')
    
    # API submission parameters
    parser.add_argument('--name',
                       help='Requestor name (for API submission)')
    
    parser.add_argument('--email',
                       help='Requestor email (for API submission)')
    
    parser.add_argument('--department',
                       choices=['General', 'IT', 'HR', 'Finance', 'Operations', 'Marketing', 'Other'],
                       default='General',
                       help='Department (default: General)')
    
    parser.add_argument('--priority',
                       choices=['Low', 'Medium', 'High', 'Critical'],
                       default='Medium',
                       help='Priority level (default: Medium)')
    
    parser.add_argument('--subject',
                       help='Request subject (for API submission)')
    
    parser.add_argument('--description',
                       help='Request description (for API submission)')
    
    parser.add_argument('--coordinator-email',
                       default='support@company.com',
                       help='Business support coordinator email (default: support@company.com)')
    
    args = parser.parse_args()
    
    # Initialize intake system
    intake = EmailIntakeSystem(coordinator_email=args.coordinator_email)
    
    print("Business Support Email Intake System")
    print("=" * 45)
    
    # Handle different command modes
    if args.web:
        start_web_interface()
    
    elif args.submit:
        if args.name and args.email and args.subject and args.description:
            # API mode submission
            submit_request_api(intake, args)
        else:
            # Interactive mode submission
            submit_request_interactive(intake)
    
    elif args.list:
        list_recent_requests(intake, args.limit)
    
    elif args.stats:
        show_statistics(intake)
    
    else:
        # Default: show overview
        show_overview(intake)


def start_web_interface():
    """Start the web interface server."""
    print("\nStarting web interface...")
    print("Access the form at: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    
    try:
        from intake_web import app
        app.run(debug=False, host='0.0.0.0', port=5000)
    except ImportError:
        print("Error: Flask not installed. Install with: pip install flask")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nServer stopped.")


def submit_request_interactive(intake):
    """Submit a request in interactive mode."""
    print("\nSubmit New Support Request")
    print("-" * 30)
    
    try:
        name = input("Full Name: ").strip()
        email = input("Email Address: ").strip()
        
        print("\nDepartment Options: General, IT, HR, Finance, Operations, Marketing, Other")
        department = input("Department (default: General): ").strip() or "General"
        
        print("\nPriority Options: Low, Medium, High, Critical")
        priority = input("Priority (default: Medium): ").strip() or "Medium"
        
        subject = input("Subject: ").strip()
        
        print("Description (enter multiple lines, end with empty line):")
        description_lines = []
        while True:
            line = input()
            if not line:
                break
            description_lines.append(line)
        description = "\n".join(description_lines)
        
        # Submit the request
        result = intake.submit_request(
            name=name,
            email=email,
            department=department,
            priority=priority,
            subject=subject,
            description=description
        )
        
        if result['success']:
            print(f"\n✅ Request submitted successfully!")
            print(f"Request ID: {result['request_id']}")
            print(f"Timestamp: {result['timestamp']}")
            print(f"Email notification sent: {'Yes' if result['email_sent'] else 'No'}")
            print(f"Confirmation email sent: {'Yes' if result['confirmation_sent'] else 'No'}")
        else:
            print(f"\n❌ Error: {result['error']}")
            
    except KeyboardInterrupt:
        print("\n\nRequest submission cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def submit_request_api(intake, args):
    """Submit a request using API parameters."""
    result = intake.submit_request(
        name=args.name,
        email=args.email,
        department=args.department,
        priority=args.priority,
        subject=args.subject,
        description=args.description
    )
    
    if result['success']:
        print(f"\n✅ Request submitted successfully!")
        print(f"Request ID: {result['request_id']}")
        print(f"Timestamp: {result['timestamp']}")
        print(f"Email notification sent: {'Yes' if result['email_sent'] else 'No'}")
        print(f"Confirmation email sent: {'Yes' if result['confirmation_sent'] else 'No'}")
    else:
        print(f"\n❌ Error: {result['error']}")
        sys.exit(1)


def list_recent_requests(intake, limit):
    """List recent support requests."""
    print(f"\nRecent Support Requests (Last {limit})")
    print("-" * 50)
    
    requests = intake.get_request_history(limit)
    
    if not requests:
        print("No support requests found.")
        return
    
    for i, request in enumerate(reversed(requests), 1):
        priority_marker = {
            'Critical': '🔴',
            'High': '🟠', 
            'Medium': '🟡',
            'Low': '🟢'
        }.get(request['priority'], '⚪')
        
        print(f"{i}. {priority_marker} {request['request_id']}")
        print(f"   From: {request['name']} ({request['email']})")
        print(f"   Subject: {request['subject']}")
        print(f"   Priority: {request['priority']} | Department: {request['department']}")
        print(f"   Submitted: {request['timestamp']}")
        print(f"   Description: {request['description'][:100]}{'...' if len(request['description']) > 100 else ''}")
        print()


def show_statistics(intake):
    """Show support request statistics."""
    print("\nSupport Request Statistics")
    print("-" * 35)
    
    stats = intake.get_request_stats()
    
    print(f"Total Requests: {stats['total']}")
    
    if stats['by_priority']:
        print(f"\nBy Priority:")
        for priority, count in sorted(stats['by_priority'].items(), 
                                    key=lambda x: ['Critical', 'High', 'Medium', 'Low'].index(x[0]) if x[0] in ['Critical', 'High', 'Medium', 'Low'] else 999):
            percentage = (count / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"  {priority}: {count} ({percentage:.1f}%)")
    
    if stats['by_department']:
        print(f"\nBy Department:")
        for department, count in sorted(stats['by_department'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"  {department}: {count} ({percentage:.1f}%)")


def show_overview(intake):
    """Show a general overview of the intake system."""
    print("\nBusiness Support Email Intake System Overview")
    print("-" * 50)
    
    stats = intake.get_request_stats()
    
    print(f"Total requests logged: {stats['total']}")
    print(f"Coordinator email: {intake.coordinator_email}")
    print(f"Request log file: {intake.requests_log}")
    
    # Show recent activity
    recent = intake.get_request_history(3)
    if recent:
        print(f"\nRecent Activity:")
        for request in reversed(recent):
            print(f"  • {request['request_id']} - {request['subject'][:50]}{'...' if len(request['subject']) > 50 else ''}")
    
    print(f"\nAvailable Commands:")
    print(f"  --submit        Submit a new support request")
    print(f"  --list          Show recent requests")
    print(f"  --stats         Show detailed statistics")
    print(f"  --web           Start web interface")
    print(f"  --help          Show all available options")
    
    if stats['total'] == 0:
        print(f"\n💡 No requests have been submitted yet. Use --submit to create your first request.")


if __name__ == '__main__':
    main()