"""
BDD Environment configuration for Lawn Care Timing Calculator
"""
import sys
import os

# Add the parent directory to the Python path to import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def before_all(context):
    """Set up test environment before running all scenarios"""
    context.calculator = None
    context.last_result = None
    context.last_error = None

def before_scenario(context, scenario):
    """Set up before each scenario"""
    context.activity = None
    context.region = None  
    context.month = None
    context.temperature = None
    context.timing_window = None
    context.is_optimal = None
    context.next_window = None

def after_scenario(context, scenario):
    """Clean up after each scenario"""
    pass