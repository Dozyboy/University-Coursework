# run_tests.py - Trinh chay tat ca cac unit tests
import unittest
import sys
import os

# Them thu muc src/ vao path de cac test module co the import dung module
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

if __name__ == "__main__":
    print("Dang chay tat ca cac kiem thu tu dong...")
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="test_*.py")
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if not result.wasSuccessful():
        sys.exit(1)
    sys.exit(0)
