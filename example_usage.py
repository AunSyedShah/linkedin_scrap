#!/usr/bin/env python3
"""
LinkedIn Scraper Usage Example
==============================

This script demonstrates how to use the LinkedIn scraper programmatically.
"""

from app import LinkedInScraper
import logging

def example_usage():
    """Example of how to use the LinkedInScraper class"""
    
    # Configure logging for this example
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Create scraper instance
    scraper = LinkedInScraper()
    
    try:
        # Example: Custom search phrases (instead of reading from file)
        custom_phrases = ["python developer", "machine learning engineer"]
        
        # Setup driver
        scraper.setup_driver()
        
        # Load credentials from file
        username, password = scraper.load_credentials()
        
        # Login
        if scraper.login_to_linkedin(username, password):
            print("Login successful!")
            
            # Search for profiles with custom phrases
            for phrase in custom_phrases:
                print(f"Searching for: {phrase}")
                profile_links = scraper.search_profiles(phrase)
                
                # Scrape first 5 profiles only (for demo)
                for i, profile_url in enumerate(profile_links[:5]):
                    print(f"Scraping profile {i+1}/{min(5, len(profile_links))}")
                    profile_data = scraper.scrape_profile(profile_url)
                    
                    if profile_data:
                        profile_data['search_phrase'] = phrase
                        scraper.scraped_data.append(profile_data)
                        print(f"✅ Scraped: {profile_data['name']}")
                    else:
                        print("❌ Failed to scrape profile")
            
            # Save results
            if scraper.scraped_data:
                scraper.save_to_excel("example_scraped_data.xlsx")
                print(f"Saved {len(scraper.scraped_data)} profiles to example_scraped_data.xlsx")
            else:
                print("No data was scraped")
        
        else:
            print("Login failed!")
    
    except Exception as e:
        print(f"Error: {str(e)}")
    
    finally:
        # Always close the driver
        if scraper.driver:
            scraper.driver.quit()

if __name__ == "__main__":
    print("LinkedIn Scraper Example Usage")
    print("=" * 35)
    print()
    print("This example will:")
    print("1. Login to LinkedIn using credentials from credentials.txt")
    print("2. Search for 'python developer' and 'machine learning engineer'")
    print("3. Scrape the first 5 profiles from each search")
    print("4. Save results to example_scraped_data.xlsx")
    print()
    
    choice = input("Do you want to run this example? (y/n): ").lower().strip()
    
    if choice == 'y' or choice == 'yes':
        example_usage()
    else:
        print("Example cancelled.")
