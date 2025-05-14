import sys, os

# 1) Make our vendored lib/ directory importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

# 2) Add the app root so "import app" works
sys.path.insert(0, os.path.dirname(__file__))

from app import app as application