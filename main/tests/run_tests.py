#!/usr/bin/env python3
"""
Script to run tests and generate reports for Allure, Sonar, Checkstyle, and Jacoco
"""
import subprocess
import sys
import os
from pathlib import Path

def run_tests_and_generate_reports():
    """Run tests and generate various reports"""
    
    # Change to backend directory
    os.chdir(os.path.join(os.path.dirname(__file__)))
    
    print("Running tests and generating reports...")
    
    # Run pytest with coverage
    print("Running pytest with coverage...")
    subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/", 
        "-v", 
        "--cov=.", 
        "--cov-report=html:reports/coverage_html", 
        "--cov-report=xml:reports/coverage.xml",  # Jacoco-compatible format
        "--cov-report=term-missing",
        "--junitxml=reports/junit.xml"
    ])
    
    # Create reports directory if it doesn't exist
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Generate additional reports
    print("Generating additional reports...")
    
    # Run flake8 for checkstyle report
    try:
        subprocess.run([
            sys.executable, "-m", "flake8", 
            ".", 
            "--format=xml", 
            "--output-file=reports/checkstyle.xml"
        ])
    except Exception as e:
        print(f"Could not generate checkstyle report: {e}")
    
    # Create a summary results file
    results = {
        "test_results": "reports/junit.xml",
        "coverage_results": "reports/coverage.xml",
        "checkstyle_results": "reports/checkstyle.xml",
        "allure_results": "reports/allure-results/",
        "timestamp": __import__('time').time()
    }
    
    # Write results to JSON
    import json
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("Tests completed and reports generated in the 'reports' directory.")
    print("Results summary saved to 'results.json'.")


if __name__ == "__main__":
    run_tests_and_generate_reports()