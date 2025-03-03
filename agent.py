import json
import logging
import requests
from bs4 import BeautifulSoup
import re
import datetime
import os
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load Google API key from environment variable
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("GOOGLE_API_KEY environment variable is required. Please set it in .env file.")

# Configure Gemini API globally
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Google Gemini model
gemini_model = genai.GenerativeModel(model_name="gemini-2.0-flash-001")

def load_config():
    """Loads configuration from config.json."""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            logging.info("Configuration loaded successfully.")

            # Ensure filters and engine_config sections exist in config
            if 'filters' not in config:
                config['filters'] = {}
            if 'engine_config' not in config:
                config['engine_config'] = {}

            return config
    except FileNotFoundError:
        logging.error("Configuration file 'config.json' not found.")
        return None
    except json.JSONDecodeError:
        logging.error("Error decoding JSON in 'config.json'.")
        return None

def scrape_website(url):
    """Fetches content from a given URL with enhanced headers."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'DNT': '1',
        'Priority': 'u=0, i',
        'Sec-CH-UA': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'Sec-CH-UA-Mobile': '?0',
        'Sec-CH-UA-Platform': '"macOS"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Service-Worker-Navigation-Preload': 'true',
        'Upgrade-Insecure-Requests': '1',
        'Referer': url  # Set Referer to the website URL itself
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Error scraping {url}: {e}")
        return None

def send_email_alert(all_listings):
    """Sends email alert with listing details, organized by property."""
    if not all_listings:
        logging.info("No new listings matching criteria to send alerts for.")
        return

    # Email configuration - Replace with your actual email settings
    sender_email = "learnittej@gmail.com" # Replace with your email
    sender_password = "eerj oobk dxfs hmgv"  # Replace with your Gmail App Password
    receiver_email = "divtejus@gmail.com" # Replace with recipient email (your email for testing)
    subject = "Daily Apartment Listing Alert - New Listings Found"

    email_body = "Here are the new apartment listings matching your criteria:\n\n"

    for property_data in all_listings:
        property_name = property_data['name']
        listings = property_data['listings']

        email_body += f"Property: {property_name}\n" # Add property name as title
        email_body += f"--------------------\n"

        if not listings:
            email_body += "No listings found for this property.\n\n"
        else:
            for listing in listings:
                email_body += f"  --------------------\n" # Indent listings under property title
                email_body += f"  Title: {listing.get('title', 'N/A')}\n"
                email_body += f"  Address: {listing.get('address', 'N/A')}\n"
                email_body += f"  Rent: {listing.get('rent', 'N/A')}\n"
                email_body += f"  Bed/Bath: {listing.get('bed_bath', 'N/A')}\n"
                email_body += f"  Sq Ft: {listing.get('square_feet', 'N/A')}\n"
                email_body += f"  Available Date: {listing.get('available_date', 'N/A')}\n"
                email_body += f"  URL: {listing.get('url', 'N/A')}\n\n"
            email_body += "\n" # Add extra newline after each property's listings

    email_body += "\n\nHappy apartment hunting!\nYour Agentic Apartment Finder"

    message = MIMEText(email_body, 'plain')
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        logging.info("Email alert sent successfully.")
    except Exception as e:
        logging.error(f"Error sending email alert: {e}")

def main():
    config = load_config()
    if config:
        logging.info("Agent started with configuration: %s", config)

        # Load scraping engine and config from config
        scraping_engine_name = config.get('scraping_engine', 'beautifulsoup') # Default to beautifulsoup
        engine_config = config.get('engine_config', {})

        if scraping_engine_name == 'beautifulsoup':
            from scraping_engines import beautifulsoup_engine
            scraping_engine = beautifulsoup_engine.scrape_listings
            logging.info("Using BeautifulSoup scraping engine.")
        elif scraping_engine_name == 'jina':
            from scraping_engines import jina_engine
            scraping_engine = jina_engine.scrape_listings
            logging.info("Using Jina AI scraping engine.")
        else:
            logging.error(f"Invalid scraping engine specified: {scraping_engine_name}. Defaulting to BeautifulSoup.")
            from scraping_engines import beautifulsoup_engine
            scraping_engine = beautifulsoup_engine.scrape_listings


        for url in config.get('websites', []):
            logging.info(f"Scraping website: {url} using {scraping_engine_name} engine.")
            html_content = scrape_website(url) # keep website fetching with requests for now, move to engine later if needed
            if html_content:
                listings = scraping_engine(html_content, config) # Call engine's scrape_listings
                logging.info(f"Extracted {len(listings)} listings using {scraping_engine_name} engine.")
                for listing in listings:
                    logging.info(listing) # Print extracted listing data for now
                # TODO: Process listings (filtering, alerting)
            import time
            time.sleep(10)  # Increase delay to 10 seconds
    else:
        logging.error("Agent could not start due to configuration errors.")

if __name__ == "__main__":
    main()