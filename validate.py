#!/usr/bin/env python3
"""
LinkedIn Scraper Validation Script
==================================

This script validates that all requirements are met before running the scraper.
"""

import sys
import os

def check_file_exists(filename, description):
    """Check if a file exists"""
    if os.path.exists(filename):
        print(f"✅ {description}: {filename}")
        return True
    else:
        print(f"❌ {description}: {filename} - NOT FOUND")
        return False

def check_credentials():
    """Check if credentials are properly configured"""
    try:
        with open('credentials.txt', 'r') as file:
            content = file.read()
            if 'your_linkedin_email@example.com' in content:
                print("❌ Credentials: Please update credentials.txt with your actual LinkedIn credentials")
                return False
            elif 'username=' in content and 'password=' in content:
                print("✅ Credentials: credentials.txt appears to be configured")
                return True
            else:
                print("❌ Credentials: credentials.txt format is incorrect")
                return False
    except FileNotFoundError:
        print("❌ Credentials: credentials.txt not found")
        return False

def check_search_phrases():
    """Check if search phrases are configured"""
    try:
        with open('search_phrases.txt', 'r') as file:
            phrases = [line.strip() for line in file.readlines() if line.strip()]
            if phrases:
                print(f"✅ Search phrases: {len(phrases)} phrases found")
                return True
            else:
                print("❌ Search phrases: search_phrases.txt is empty")
                return False
    except FileNotFoundError:
        print("❌ Search phrases: search_phrases.txt not found")
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        ('selenium', 'selenium'),
        ('beautifulsoup4', 'bs4'),
        ('pandas', 'pandas'),
        ('openpyxl', 'openpyxl'),
        ('webdriver-manager', 'webdriver_manager')
    ]
    
    missing_packages = []
    for package_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✅ Package: {package_name}")
        except ImportError:
            print(f"❌ Package: {package_name} - NOT INSTALLED")
            missing_packages.append(package_name)
    
    return len(missing_packages) == 0

def main():
    """Main validation function"""
    print("LinkedIn Scraper Validation")
    print("=" * 30)
    print()
    
    all_good = True
    
    # Check files
    files_to_check = [
        ('app.py', 'Main application'),
        ('requirements.txt', 'Requirements file'),
        ('setup.sh', 'Setup script'),
        ('build_exe.sh', 'Build script')
    ]
    
    for filename, description in files_to_check:
        if not check_file_exists(filename, description):
            all_good = False
    
    print()
    
    # Check credentials
    if not check_credentials():
        all_good = False
    
    print()
    
    # Check search phrases
    if not check_search_phrases():
        all_good = False
    
    print()
    
    # Check dependencies
    print("Checking Python packages...")
    if not check_dependencies():
        all_good = False
        print("\nTo install missing packages, run:")
        print("pip install -r requirements.txt")
    
    print()
    print("=" * 30)
    
    if all_good:
        print("✅ All checks passed! The scraper is ready to run.")
        print("\nTo start scraping, run:")
        print("python app.py")
    else:
        print("❌ Some issues found. Please fix them before running the scraper.")
        print("\nFor setup help, check the README.md file")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
