import json
import logging
import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText
import google.generativeai as genai
from flask import jsonify

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config():
    """Loads configuration from config.json."""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            logging.info("Configuration loaded successfully.")

            # Ensure filters section exists in config
            if 'filters' not in config:
                config['filters'] = {}

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
        'Cookie': '.AspNetCore.Antiforgery.-rXc1S2HjzU=CfDJ8CtwjdPBESBMu9DVKc5_ZZ0nq2iPHLw2-VS6GAbmWzbhIkjJ8sLVqisiLudi9Wic1D-e5cx7TFN_67-QIEntMdhxXhCfEbmNw0ABK_OATlGSTDpRgZljif0MLzEYgNQLWJAy1E15_uwRcC76LhDs6qA; _cfuvid=MHI7jQp8.qJ4FOraGbadxjLFOnpevL5dhsKwdlJBjYg-1740537138507-0.0.1.1-604800000; yTrackUser=7JV529LUTIJJ5KTB4YUMT40537138575; PropLeadSource_1473965=portal; sReferrerURL=https%3A%2F%2Fwww.riversedgepi.com%2Ffloorplans; sCurrentURL=https%3A%2F%2Fwww.riversedgepi.com%2Ffloorplans%2Fa9%3Fmidate%3D05%2F10%2F2025; __utmzzses=1; _yTrackUser=MzI5OTA0Mzk2NiM0MDAzNDIyNDQ%253d-phXh3FjAj80%253d; rpTrackingExternalUserId=371559a4-c582-4735-af5d-16197cde34e0; sessionTrafficSource=utmcsr=(direct)|utmcmd=(none)|utmccn=(not set)|utmknock=(not set)|pathname=/floorplans/a9; _gid=GA1.2.1611080335.1740953636; __cf_bm=qshJW22wbssGx8OStcjtiqbRv1KXsQ3ZoPPyD.CqfVw-1741035282-1.0.1.1-_qFgPJEY1eUNPIDzGSPLDPiq3laUsYpjB7cZoysY3OjtAdL2g_4DkSuhzLGj4B0eaTlS9Nk.im.frq8vOBMWlkZyXDUXUTKbqS3PxBWnYfw; yTrackVisit=CVSJS3U5NYZEEFYWGJVI281035282321; _yTrackVisit=NTQ3MTA3NzM0NiMzNTAzNjk0ODc%253d-GaHMIiAZd74%253d; cf_clearance=CQ3VnRHp_595rGaK1N_kOQzdFgEI9Awp5DBLdzx6qN8-1741035282-1.2.1.1-4EhBpNSSSjdMwePSFnWCZF77MEJgE1jQpriCViXWOJnrKj3JAHzY65UolPBPuwcdO3GtXMDieUve_HJEI9bgQ3ei3D8LUpCsFVOnkqQd6Bq.OiQAPEoqTQbOswENZmYcnJzki8bKuDg6I9u4eKlpQd.gQ9ZeRT9yt._Ky8Zevk12wVNtvNM4fCkwUV9IDb_G59jTcLFG1WnyFE7zqrZqDm_WUYYWsqh82Ny_zWWY01gzt1eT_B9mOw5RWnZlqiATRbJKBOgApITnuw905itokwyA5tvozonxLD02xdJMnBpVa.VYi7P4Aahc_9orygc02oe6zWoFMTKM.3r2aSV.lhyEyTI3roVyAybLl2hwU7msdBbkW_A6HRBihW6XP7LevqAvkcJojz4ZCJU8Ei4PyNVZEaRw9GNWPmPkMq3XLb4; trackThisPage=1741035691097; _dc_gtm_UA-56407927-4=1; _dc_gtm_UA-99654580-21=1; _ga=GA1.1.1888777578.1740537139; _ga_DLQBM166D8=GS1.1.1741035283.11.1.1741035692.0.0.0; rpTrackingFirstPartyUserObj=%7B%22id%22%3A%22c23a63f8-6d3e-4e47-b3e2-ab060c2bd86c%22%2C%22hit%22%3A49%7D; _ga_QVB9X5Z5XV=GS1.2.1741035283.10.1.1741035692.60.0.0; _gali=btnFrontDesk',
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

def scrape_using_jina_ai(url):
    """Scrapes a website using the Jina AI API."""
    headers = {
    'Authorization': 'Bearer ' + os.environ.get("JINA_API_KEY"),
    'X-Retain-Images': 'none',
    'X-Return-Format': 'markdown'
    }

    response = requests.get('https://r.jina.ai/' + url, headers=headers)
    return response.text

def generate_listing_text(html_content, config):
    """Generates batched listing text from HTML content."""
    batched_listing_text = ""
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        listing_items = soup.find_all('div', class_='listing-item result js-listing-item')

        for index, item in enumerate(listing_items):
            listing_text = item.text.strip()
            batched_listing_text += f"Listing {index + 1}:\n{listing_text}\n\n"
    return batched_listing_text

def extract_listings_with_gemini(batched_listing_text, config):
    """Extracts listing data from batched listing text using Gemini API and filters."""
    listings = []
    if not batched_listing_text:
        return listings

    filters = config.get('filters', {})
    filter_criteria = ""
    if filters:
        filter_criteria += "The listings should match the following criteria:\n"
        if 'min_sqft' in filters:
            filter_criteria += f"- Minimum Square Feet: {filters['min_sqft']}\n"
        if 'bedrooms' in filters:
            filter_criteria += f"- Bedrooms: {filters['bedrooms']}\n"
        if 'bathrooms' in filters:
            filter_criteria += f"- Bathrooms: {filters['bathrooms']}\n"
        if 'move_in_date_range_days' in filters and 'desired_move_in_date' in filters:
            filter_criteria += f"- Move-in Date within {filters['move_in_date_range_days']} days of {filters['desired_move_in_date']}\n"
    else:
        filter_criteria = "No specific criteria provided. Extract all available information."

    # Consolidated Gemini API prompt for extraction for all listings with filters
    prompt = """Extract the following information from each apartment listing text provided below and return it in JSON format. It must include 'Square Feet', 'Rent', 'Bed/Bath', 'Available Date', 'Address', 'Title', 'URL'.
    Rent is the $ amount. 
    URL should be a link to the floor plan or more details about the unit if not present website url for the listing.
Keys in the JSON should be: 'rent', 'square_feet', 'bed_bath', 'available_date', 'address', 'title', 'url'.
    If the information is not found, use 'N/A' as the value.

    Filter criteria: {}

    Listings text: {}""" # Placeholder for batched listing text

    try:
        response = gemini_model.generate_content(prompt.format(filter_criteria, batched_listing_text))
        json_str = response.text.strip().replace('```json\n', '').replace('\n```', '')
        listings_json = json.loads(json_str) # Parse JSON response for all listings
        listings = listings_json if isinstance(listings_json, list) else [] # Ensure response is a list
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing JSON response from Gemini API: {e}. Raw response: {response}")
        listings = [] # Return empty list if JSON parsing fails
    except Exception as e:
        logging.error(f"Error extracting listing data using Gemini API: {e}")
        listings = [] # Return empty list in case of error

    return listings

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

        email_body += f"--------------------\n"
        email_body += f"Property: {property_name}\n" # Add property name as title

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

def run_apartment_finder(request):
    """Runs the apartment finder logic. This is the entry point for the Cloud Function."""
    try:
        # Handle potential JSON input (not used in this basic version)
        request_json = request.get_json(silent=True)

        config = load_config()
        if not config:
            return jsonify({"error": "Failed to load configuration."}), 500

        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        gemini_model = genai.GenerativeModel(model_name="gemini-2.0-flash-001")

        logging.info("Agent started with configuration: %s", config)
        all_listings = []

        for property in config.get('websites', []):
            logging.info(f"Scraping website: {property['url']}")
            if config.get('scraping_engine','') == 'BeautifulSoup':
                html_content = scrape_website(property['url'])
                if html_content:
                    batched_listing_text = generate_listing_text(html_content, config)
                    property_listings = extract_listings_with_gemini(batched_listing_text, config)
                    
            elif config.get('scraping_engine','') == 'JinaAi':
                listing_text = scrape_using_jina_ai(property['url'])
                property_listings = extract_listings_with_gemini(listing_text, config)
            
            logging.info(f"Extracted {len(property_listings)} listings using Gemini API.")
               
            # Append the property name and its listings to all_listings
            
            all_listings.append({
                'name': property['name'],
                'listings': property_listings
            })   
        send_email_alert(all_listings)  # Send email alert. Consider moving to Cloud Tasks for production.
        return jsonify({"message": "Apartment finder ran successfully!", "listings": all_listings}), 200

    except Exception as e:
        logging.exception("An error occurred: %s", e)  # Log the full traceback
        return jsonify({"error": "An internal server error occurred."}), 500