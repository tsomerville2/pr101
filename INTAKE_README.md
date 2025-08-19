# Business Support Email Intake System

A comprehensive email intake system for business support coordinators that allows anyone to submit support requests through multiple interfaces.

## Features

- **Web Interface**: User-friendly web form for submitting support requests
- **Command Line Interface**: CLI for both interactive and automated request submission
- **Email Notifications**: Automatic email notifications to coordinators and confirmation emails to requestors
- **Request Tracking**: JSON-based logging with unique request IDs
- **Priority Management**: Support for Low, Medium, High, and Critical priority levels
- **Department Categorization**: Organize requests by department (IT, HR, Finance, etc.)
- **Statistics Dashboard**: View request statistics and recent activity

## Quick Start

### Web Interface

1. Start the web server:
   ```bash
   python intake_web.py
   ```

2. Open your browser to `http://localhost:5000`

3. Fill out the support request form

### Command Line Interface

1. Interactive submission:
   ```bash
   python intake_cli.py --submit
   ```

2. API-style submission:
   ```bash
   python intake_cli.py --submit --name "John Doe" --email "john@company.com" \
     --subject "Password Reset" --description "Need help resetting my password"
   ```

3. View recent requests:
   ```bash
   python intake_cli.py --list --limit 10
   ```

4. View statistics:
   ```bash
   python intake_cli.py --stats
   ```

## Installation

### Requirements

- Python 3.6+
- Flask (for web interface): `pip install flask`

### Basic Setup

1. Clone or download the intake system files:
   - `email_intake.py` - Core intake system
   - `intake_web.py` - Web interface
   - `intake_cli.py` - Command line interface

2. Configure email settings via environment variables:
   ```bash
   export SMTP_SERVER="your-smtp-server.com"
   export SMTP_PORT="587"
   export SMTP_USERNAME="your-email@company.com"
   export SMTP_PASSWORD="your-password"
   ```

3. Set coordinator email:
   ```bash
   # Default coordinator email for all requests
   python intake_cli.py --coordinator-email "support-team@company.com"
   ```

## Configuration

### Environment Variables

- `SMTP_SERVER`: SMTP server hostname (default: localhost)
- `SMTP_PORT`: SMTP server port (default: 587)
- `SMTP_USERNAME`: SMTP username for authentication
- `SMTP_PASSWORD`: SMTP password for authentication
- `SECRET_KEY`: Flask secret key for web interface

### Email Configuration

The system supports various email configurations:

1. **Local SMTP server** (default)
2. **External SMTP** (Gmail, Outlook, etc.)
3. **Corporate email servers**

## Usage Examples

### Web Interface Features

- **Responsive Design**: Works on desktop and mobile devices
- **Form Validation**: Required field validation and email format checking
- **Priority Selection**: Visual priority indicators with descriptions
- **Department Selection**: Dropdown with common department options
- **Confirmation Page**: Shows request ID and submission details

### CLI Features

- **Interactive Mode**: Step-by-step request submission
- **Batch Mode**: Programmatic submission with command-line arguments
- **Request History**: View and filter recent requests
- **Statistics**: Detailed breakdowns by priority and department

### API Endpoints

The web interface also provides REST API endpoints:

- `POST /api/submit`: Submit a request via JSON
- `GET /api/stats`: Get statistics in JSON format

Example API usage:
```bash
curl -X POST http://localhost:5000/api/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@company.com",
    "subject": "Software License Request",
    "description": "Need access to design software",
    "priority": "Medium",
    "department": "Marketing"
  }'
```

## Request Workflow

1. **Submission**: User submits request via web form or CLI
2. **Validation**: System validates required fields
3. **ID Generation**: Unique request ID assigned (format: REQ_YYYYMMDD_HHMMSS)
4. **Logging**: Request saved to JSON log file
5. **Email Notification**: Coordinator receives email with request details
6. **Confirmation**: Requestor receives confirmation email with request ID
7. **Tracking**: Request can be referenced by ID for follow-up

## Request Data Structure

Each request contains:
- `request_id`: Unique identifier
- `name`: Requestor's full name
- `email`: Requestor's email address
- `department`: Business department
- `priority`: Low, Medium, High, or Critical
- `subject`: Brief description
- `description`: Detailed request information
- `timestamp`: Submission date and time (ISO format)

## Security Considerations

- Form validation prevents basic injection attacks
- Email addresses are validated for format
- Request descriptions are logged as-is (sanitize if displaying in web UI)
- SMTP credentials should be secured via environment variables
- Consider implementing rate limiting for production use

## Customization

### Adding New Departments
Edit the department dropdown in `intake_web.py` and CLI choices in `intake_cli.py`.

### Modifying Priority Levels
Update the priority options in both web and CLI interfaces.

### Custom Email Templates
Modify the `format_email_body()` method in `email_intake.py`.

### Styling
Update the CSS in the HTML templates within `intake_web.py`.

## Troubleshooting

### Email Not Sending
1. Check SMTP configuration
2. Verify network connectivity to SMTP server
3. Confirm authentication credentials
4. Check firewall/proxy settings

### Web Interface Issues
1. Ensure Flask is installed: `pip install flask`
2. Check port 5000 is available
3. Verify file permissions for log files

### CLI Problems
1. Check Python version (3.6+ required)
2. Verify file paths and permissions
3. Ensure proper command syntax

## Production Deployment

For production use, consider:

1. **Web Server**: Use a proper WSGI server (Gunicorn, uWSGI) instead of Flask's dev server
2. **Database**: Replace JSON file logging with a proper database
3. **Security**: Implement HTTPS, authentication, and rate limiting
4. **Monitoring**: Add logging and monitoring for email delivery
5. **Backup**: Regular backup of request data
6. **Load Balancing**: If handling high volume requests

## Support

For issues with the intake system:
1. Check this README for common solutions
2. Review the error messages in console output
3. Verify email and network configuration
4. Test with simple requests first

The system is designed to be lightweight and easy to deploy while providing essential intake functionality for business support teams.