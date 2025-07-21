#!/usr/bin/env python3
"""
LinkedIn Profile Scraper
=========================

This script scrapes LinkedIn profiles based on search phrases and extracts:
- Name
- Designation/Title
- Company Name
- Email (when available)

Requirements:
1. LinkedIn account credentials in credentials.txt
2. Search phrases in search_phrases.txt
3. Chrome browser installed
4. Internet connection

Usage:
    python app.py

Output:
    Creates an Excel file with scraped data
"""

import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import random
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('linkedin_scraper.log'),
        logging.StreamHandler()
    ]
)

class LinkedInScraper:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.scraped_data = []
        
    def setup_driver(self):
        """Setup Chrome driver with appropriate options"""
        try:
            chrome_options = Options()
            
            # Add options for better compatibility and avoiding detection
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Optional: Run in headless mode (uncomment next line for headless)
            # chrome_options.add_argument('--headless')
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Execute script to remove webdriver property
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.wait = WebDriverWait(self.driver, 10)
            logging.info("Chrome driver setup successful")
            
        except Exception as e:
            logging.error(f"Error setting up Chrome driver: {str(e)}")
            raise
    
    def load_credentials(self):
        """Load LinkedIn credentials from credentials.txt"""
        try:
            with open('credentials.txt', 'r') as file:
                lines = file.readlines()
                credentials = {}
                for line in lines:
                    if '=' in line:
                        key, value = line.strip().split('=', 1)
                        credentials[key] = value
                
                if 'username' not in credentials or 'password' not in credentials:
                    raise ValueError("Username or password not found in credentials.txt")
                
                logging.info("Credentials loaded successfully")
                return credentials['username'], credentials['password']
                
        except FileNotFoundError:
            logging.error("credentials.txt file not found")
            raise
        except Exception as e:
            logging.error(f"Error loading credentials: {str(e)}")
            raise
    
    def load_search_phrases(self):
        """Load search phrases from search_phrases.txt"""
        try:
            with open('search_phrases.txt', 'r') as file:
                phrases = [line.strip() for line in file.readlines() if line.strip()]
                logging.info(f"Loaded {len(phrases)} search phrases")
                return phrases
                
        except FileNotFoundError:
            logging.error("search_phrases.txt file not found")
            raise
        except Exception as e:
            logging.error(f"Error loading search phrases: {str(e)}")
            raise
    
    def login_to_linkedin(self, username, password):
        """Login to LinkedIn"""
        try:
            logging.info("Navigating to LinkedIn login page")
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for and fill username
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.clear()
            username_field.send_keys(username)
            
            # Fill password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys(password)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for login to complete
            time.sleep(3)
            
            # Check if login was successful
            if "feed" in self.driver.current_url or "linkedin.com/in/" in self.driver.current_url:
                logging.info("Login successful")
                return True
            else:
                logging.error("Login failed - please check credentials")
                return False
                
        except Exception as e:
            logging.error(f"Error during login: {str(e)}")
            return False
    
    def search_profiles(self, search_phrase):
        """Search for profiles based on search phrase"""
        try:
            logging.info(f"Searching for: {search_phrase}")
            
            # Navigate to LinkedIn search
            search_url = f"https://www.linkedin.com/search/results/people/?keywords={search_phrase.replace(' ', '%20')}"
            self.driver.get(search_url)
            
            # Wait for results to load
            time.sleep(3)
            
            # Scroll to load more results
            self.scroll_page()
            
            # Get profile links
            profile_links = self.extract_profile_links()
            logging.info(f"Found {len(profile_links)} profiles for '{search_phrase}'")
            
            return profile_links
            
        except Exception as e:
            logging.error(f"Error searching profiles for '{search_phrase}': {str(e)}")
            return []
    
    def scroll_page(self, scrolls=3):
        """Scroll the page to load more results"""
        try:
            for i in range(scrolls):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
        except Exception as e:
            logging.error(f"Error scrolling page: {str(e)}")
    
    def extract_profile_links(self):
        """Extract profile links from search results"""
        try:
            profile_links = []
            
            # Find all profile links in search results
            link_elements = self.driver.find_elements(
                By.XPATH, 
                "//a[contains(@href, '/in/') and contains(@class, 'app-aware-link')]"
            )
            
            for element in link_elements:
                href = element.get_attribute('href')
                if href and '/in/' in href and href not in profile_links:
                    profile_links.append(href)
            
            # Remove duplicates and limit results
            profile_links = list(set(profile_links))[:20]  # Limit to 20 profiles per search
            
            return profile_links
            
        except Exception as e:
            logging.error(f"Error extracting profile links: {str(e)}")
            return []
    
    def scrape_profile(self, profile_url):
        """Scrape individual profile for information"""
        try:
            logging.info(f"Scraping profile: {profile_url}")
            
            self.driver.get(profile_url)
            time.sleep(random.uniform(2, 4))  # Random delay to avoid detection
            
            # Wait for page to load
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "main")))
            
            # Extract profile information
            profile_data = {
                'name': self.extract_name(),
                'designation': self.extract_designation(),
                'company': self.extract_company(),
                'email': self.extract_email(),
                'profile_url': profile_url
            }
            
            logging.info(f"Scraped: {profile_data['name']} - {profile_data['designation']}")
            return profile_data
            
        except Exception as e:
            logging.error(f"Error scraping profile {profile_url}: {str(e)}")
            return None
    
    def extract_name(self):
        """Extract name from profile"""
        try:
            name_selectors = [
                "h1.text-heading-xlarge",
                "h1.break-words",
                ".pv-text-details__left-panel h1",
                ".ph5 h1"
            ]
            
            for selector in name_selectors:
                try:
                    name_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    return name_element.text.strip()
                except:
                    continue
                    
            return "N/A"
            
        except Exception as e:
            logging.error(f"Error extracting name: {str(e)}")
            return "N/A"
    
    def extract_designation(self):
        """Extract designation/title from profile"""
        try:
            designation_selectors = [
                ".text-body-medium.break-words",
                ".pv-text-details__left-panel .text-body-medium",
                ".ph5 .text-body-medium"
            ]
            
            for selector in designation_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        text = element.text.strip()
                        if text and not any(word in text.lower() for word in ['connections', 'followers', 'mutual']):
                            return text
                except:
                    continue
                    
            return "N/A"
            
        except Exception as e:
            logging.error(f"Error extracting designation: {str(e)}")
            return "N/A"
    
    def extract_company(self):
        """Extract company from profile"""
        try:
            # Look for experience section
            experience_selectors = [
                ".pv-entity__secondary-title",
                ".pv-experience-section .pv-entity__summary-info h3",
                "section[data-section='experience'] .pv-entity__secondary-title"
            ]
            
            for selector in experience_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        return elements[0].text.strip()
                except:
                    continue
            
            # Alternative: look for company in about section
            try:
                about_elements = self.driver.find_elements(By.XPATH, "//span[contains(@class, 'visually-hidden')]")
                for element in about_elements:
                    text = element.text.strip()
                    if 'company' in text.lower() or 'organization' in text.lower():
                        return text
            except:
                pass
                
            return "N/A"
            
        except Exception as e:
            logging.error(f"Error extracting company: {str(e)}")
            return "N/A"
    
    def extract_email(self):
        """Extract email from profile (if available)"""
        try:
            # Look for contact info
            contact_selectors = [
                "a[href*='mailto:']",
                ".pv-contact-info__contact-link",
                "section[data-section='contactinfo'] a"
            ]
            
            for selector in contact_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        href = element.get_attribute('href')
                        if href and 'mailto:' in href:
                            email = href.replace('mailto:', '')
                            if '@' in email:
                                return email
                except:
                    continue
            
            # Look for email patterns in page source
            page_source = self.driver.page_source
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, page_source)
            
            if emails:
                return emails[0]
                
            return "N/A"
            
        except Exception as e:
            logging.error(f"Error extracting email: {str(e)}")
            return "N/A"
    
    def save_to_excel(self, filename=None):
        """Save scraped data to Excel file"""
        try:
            if not self.scraped_data:
                logging.warning("No data to save")
                return
            
            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"linkedin_scraped_data_{timestamp}.xlsx"
            
            df = pd.DataFrame(self.scraped_data)
            df.to_excel(filename, index=False)
            
            logging.info(f"Data saved to {filename}")
            print(f"Scraped data saved to: {filename}")
            
        except Exception as e:
            logging.error(f"Error saving to Excel: {str(e)}")
            raise
    
    def run_scraper(self):
        """Main function to run the scraper"""
        try:
            logging.info("Starting LinkedIn Scraper")
            
            # Setup driver
            self.setup_driver()
            
            # Load credentials and search phrases
            username, password = self.load_credentials()
            search_phrases = self.load_search_phrases()
            
            # Login to LinkedIn
            if not self.login_to_linkedin(username, password):
                raise Exception("Login failed")
            
            # Process each search phrase
            for phrase in search_phrases:
                profile_links = self.search_profiles(phrase)
                
                # Scrape each profile
                for profile_url in profile_links:
                    profile_data = self.scrape_profile(profile_url)
                    if profile_data:
                        profile_data['search_phrase'] = phrase
                        self.scraped_data.append(profile_data)
                    
                    # Add delay between profiles
                    time.sleep(random.uniform(3, 6))
                
                # Add delay between search phrases
                time.sleep(random.uniform(5, 10))
            
            # Save results to Excel
            self.save_to_excel()
            
            logging.info(f"Scraping completed. Total profiles scraped: {len(self.scraped_data)}")
            
        except Exception as e:
            logging.error(f"Error in main scraper function: {str(e)}")
            raise
        finally:
            if self.driver:
                self.driver.quit()
                logging.info("Driver closed")

def main():
    """Main entry point"""
    try:
        scraper = LinkedInScraper()
        scraper.run_scraper()
        print("Scraping completed successfully!")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        logging.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()