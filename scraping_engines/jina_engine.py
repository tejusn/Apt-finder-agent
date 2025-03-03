import json
import logging
import os
import google.generativeai as genai
from google.genai.types import HttpOptions, Part

# Configure logging for this module
logger = logging.getLogger(__name__)

class GeminiAPIError(Exception):
    """Custom exception for Gemini API errors."""
    pass

def scrape_listings(url, config=None):
    """
    Extracts listing data from a website using Google Gemini API.

    Args:
        url (str): The URL of the website to scrape (not directly used in this engine, 
                     but kept for interface consistency).
        config (dict, optional): Configuration parameters, including API key.

    Returns:
        list: A list of dictionaries, where each dictionary represents a listing 
              and contains extracted data. Returns an empty list if extraction fails.
    """
    listings = []
    # Load Google API key from environment variable or config
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        if config and config.get('api_key'):
            api_key = config['api_key']
        else:
            raise ValueError("Gemini API key is required but not found in environment variables or config.")

    genai.configure(api_key=api_key)
    gemini_model = genai.GenerativeModel(model_name="gemini-pro")

    # Consolidated Gemini API prompt for extraction for all listings
    prompt = """Extract the following information from the apartment listing text provided below and return it in JSON format.
Keys in the JSON should be: 'rent', 'square_feet', 'bed_bath', 'available_date', 'address', 'title'.
If the information is not found, use 'N/A' as the value.

Listings text: {}""" # Placeholder for batched listing text


    try:
        # Dummy listing text for now - Replace with actual website scraping and text extraction
        listing_text = """Listing 1:
Luxury Apartment in Downtown
1 Bedroom, 1 Bathroom
Rent: $2500
Available: June 15, 2025
Square Feet: 700 sq ft
Address: 123 Main Street, Anytown

Listing 2:
Spacious Studio Apartment
Rent: $1800
Available: NOW
Square Feet: 450 sq ft
Address: 456 Oak Avenue, Anytown"""

        response = gemini_model.generate_content(prompt.format(listing_text))
        listings_json = response.text.strip() 
        try:
            listings_data = json.loads(listings_json) # Parse JSON response for all listings
            listings = listings_data if isinstance(listings_data, list) else [] # Ensure response is a list
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing JSON response from Gemini API: {e}. Raw response: {listings_json}")
            raise GeminiAPIError(f"JSON Parse Error: {e}") from e
    except Exception as e:
        logger.error(f"Error extracting listing data using Gemini API: {e}")
        raise GeminiAPIError(f"API Request Error: {e}") from e

    return listings

if __name__ == '__main__':
    # Example usage (for testing the engine module directly)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    test_url = "https://namdar.appfolio.com/listings/"  # Replace with a test URL if needed
    
    # You would normally load config from config.json, but for testing, we can create a dummy config
    test_config = {
        "api_key": os.environ.get("GOOGLE_API_KEY") # Or replace with your API key directly for testing
    } 

    try:
        listings = scrape_listings(test_url, test_config)
        logging.info(f"Gemini Engine Test - Extracted {len(listings)} listings:")
        for listing in listings:
            logging.info(listing)
    except GeminiAPIError as e:
        logging.error(f"Gemini API Error during test: {e}")
    except ValueError as e:
        logging.error(f"Configuration Error during test: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during Gemini Engine test: {e}")