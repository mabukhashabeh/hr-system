#!/usr/bin/env python3
"""
Test runner script for the HR system backend.
Provides easy commands to run different types of tests.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"\n✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {description} failed with exit code {e.returncode}")
        return False

def run_unit_tests():
    """Run unit tests only."""
    cmd = [
        "python", "-m", "pytest", 
        "candidate/tests.py::CandidateModelTest",
        "candidate/tests.py::StatusHistoryModelTest", 
        "candidate/tests.py::CandidateSerializerTest",
        "candidate/tests.py::PermissionTest",
        "-v", "--tb=short"
    ]
    return run_command(cmd, "Unit Tests")

def run_integration_tests():
    """Run integration tests only."""
    cmd = [
        "python", "-m", "pytest",
        "candidate/tests.py::CandidateAPITest",
        "candidate/tests.py::StatusHistoryAPITest", 
        "-v", "--tb=short"
    ]
    return run_command(cmd, "Integration Tests")

def run_performance_tests():
    """Run performance tests only."""
    cmd = [
        "python", "-m", "pytest",
        "candidate/tests.py::PerformanceTest",
        "-v", "--tb=short"
    ]
    return run_command(cmd, "Performance Tests")

def run_edge_case_tests():
    """Run edge case tests only."""
    cmd = [
        "python", "-m", "pytest",
        "candidate/tests.py::EdgeCaseTest",
        "-v", "--tb=short"
    ]
    return run_command(cmd, "Edge Case Tests")

def run_all_tests():
    """Run all tests with coverage."""
    cmd = [
        "python", "-m", "pytest",
        "--cov=candidate",
        "--cov=core", 
        "--cov-report=html",
        "--cov-report=term-missing",
        "--cov-fail-under=80",
        "-v"
    ]
    return run_command(cmd, "All Tests with Coverage")

def run_tests_with_parallel():
    """Run tests in parallel for faster execution."""
    cmd = [
        "python", "-m", "pytest",
        "-n", "auto",  # Use all available CPU cores
        "--cov=candidate",
        "--cov=core",
        "--cov-report=term-missing",
        "-v"
    ]
    return run_command(cmd, "Parallel Tests")

def run_linting():
    """Run code linting."""
    cmd = ["flake8", "candidate", "core", "--max-line-length=88"]
    return run_command(cmd, "Code Linting")

def run_formatting():
    """Run code formatting."""
    cmd = ["black", "candidate", "core", "--check"]
    return run_command(cmd, "Code Formatting Check")

def run_import_sorting():
    """Run import sorting check."""
    cmd = ["isort", "candidate", "core", "--check-only"]
    return run_command(cmd, "Import Sorting Check")

def run_security_checks():
    """Run security checks."""
    cmd = ["bandit", "-r", "candidate", "-f", "json", "-o", "bandit-report.json"]
    return run_command(cmd, "Security Checks")

def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(description="HR System Backend Test Runner")
    parser.add_argument(
        "test_type",
        choices=[
            "unit", "integration", "performance", "edge", 
            "all", "parallel", "lint", "format", "imports", "security"
        ],
        help="Type of tests to run"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Set environment variable for test settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.test_settings")
    
    # Map test types to functions
    test_functions = {
        "unit": run_unit_tests,
        "integration": run_integration_tests,
        "performance": run_performance_tests,
        "edge": run_edge_case_tests,
        "all": run_all_tests,
        "parallel": run_tests_with_parallel,
        "lint": run_linting,
        "format": run_formatting,
        "imports": run_import_sorting,
        "security": run_security_checks,
    }
    
    # Run the selected test function
    success = test_functions[args.test_type]()
    
    if success:
        print("\n🎉 All tests passed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 