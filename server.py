"""
C.R.O.P.S. — Root Entrypoint Launcher
Delegates execution directly to backend/server.py
"""

import sys
import os

# Add backend directory to module search path
BACKEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from server import run_server

if __name__ == "__main__":
    run_server(port=5000)
