#!/usr/bin/env python3
"""
Startup script for the JIRA MCP.
This ensures the correct path setup when running from Claude Desktop.
"""
import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main function
from src.main import main

if __name__ == "__main__":
    main()