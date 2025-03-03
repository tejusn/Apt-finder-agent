**Product Requirements Document (PRD)**

**Product Name:** Agentic Apartment Finder (MVP)

**1. Introduction/Overview**

The Agentic Apartment Finder is a personal agent designed to automate the time-consuming process of checking apartment website availabilities.  It addresses the user's daily frustration of manually visiting multiple websites to find suitable apartment listings. This MVP focuses on delivering a daily report of new apartment listings that meet specific criteria, saving the user significant time and effort in their apartment search.

**2. Goals (MVP)**

- **Automate Daily Apartment Checks:** Eliminate the need for the user to manually check apartment websites multiple times a day.
- **Deliver Daily Listing Reports:** Provide the user with a daily summary of newly available apartment listings that match their core requirements.
- **Save User Time and Effort:** Significantly reduce the time and effort spent on manual apartment hunting.
- **Provide a Functional Core Agent:** Create a working, albeit basic, agent that can be expanded upon in future iterations.

**3. Target User**

- **Primary User:** The individual who initiated this project (you).
- **User Characteristics:**
    - Currently engaged in an active apartment search.
    - Regularly checks multiple apartment websites for new listings.
    - Values efficiency and wants to automate repetitive tasks.
    - Seeks a 1-bedroom, 1-bathroom apartment with a move-in date around May 10th and a maximum rent of $3200.
    - Comfortable with basic configuration using a JSON file.

**4. Features (MVP Features)**

- **Website Scraping:** The agent will automatically visit and scrape data from a configurable list of apartment websites on a regular schedule.
- **Data Extraction:** The agent will intelligently extract key information from apartment listings, including price, move-in date, and square footage.
- **Listing Alerts (New Listings):** The agent will send email alerts for newly discovered apartment listings that match the user's specified criteria (budget, date range).
- **Configurable Website List:** The user can configure the list of apartment websites to be scraped via a JSON configuration file.
- **Error Handling:** Basic error handling mechanisms will be implemented, including retry attempts, error logging, and email notifications for persistent errors.

**5. Detailed Requirements**

**5.1. Functional Requirements:**

- **Website Scraping:**
    - **Frequency:** Scrape configured websites twice daily, at 6:00 AM and 6:00 PM.
    - **Website Sources:** Scrape websites listed in the `websites` array of the JSON configuration file.
    - **Page Focus:** Prioritize scraping "Floorplans" and "Availability" pages on target websites.
- **Data Extraction:**
    - **Information to Extract:** Extract the following information from each apartment listing:
        - Price (Rent per month)
        - Move-in Date (Availability Date)
        - Square Footage
        - Apartment/Complex Name (if readily available)
        - Listing URL
    - **Extraction Logic (Initial):** Utilize a combination of:
        - **Keyword Spotting:** Search for keywords like "Price," "Rent," "Sq Ft," "Move-in Date," "Available," etc.
        - **Formatting Recognition:** Identify prices (currency symbols), dates (date formats), and square footage (numeric values near "sq ft").
        - **Proximity:** Assume relevant information is located near identified keywords.
    - **Adaptability:** Agent should attempt to adapt to different website layouts without requiring per-website customization (to the extent feasible in MVP).
- **Listing Alerts (New Listings):**
    - **Trigger:** Send an alert when a *new* apartment listing is found that meets the user's criteria.
    - **Criteria:**
        - Apartment Type: 1 bedroom, 1 bathroom (implied from website selection and search focus).
        - Move-in Date: Available within +/- 20 days of May 10th.
        - Maximum Rent: Price is less than or equal to $3200 per month (global threshold).
    - **Alert Frequency:** Send alerts twice daily, aggregated for each run (6 AM and 6 PM).
    - **Alert Method:** Send email notifications to the user's Gmail account.
    - **Alert Content:** Each alert email will contain:
        - Apartment/Complex Name
        - Price
        - Move-in Date
        - Square Footage
        - Listing URL
- **Configuration:**
    - **Configuration File Format:** JSON.
    - **Configuration File Content:**
        - `max_rent_threshold`: Global maximum monthly rent ($3200 initially).
        - `websites`: An array of website URLs to scrape. Example:
            
            **JSON**
            
            `{
              "max_rent_threshold": 3200,
              "price_drop_percentage": 10,
              "websites": [
                "https://www.riversedgepi.com/floorplans/",
                "https://namdar.appfolio.com/listings/",
                "https://www.18park.com/floorplans/1-bed-1-bath?Beds=1"
              ]
            }`
            

**5.2. Non-Functional Requirements:**

- **Usability:** Configuration should be straightforward via editing a JSON file. Alert emails should be clear and informative.
- **Reliability:** Agent should be reasonably robust and handle temporary website errors gracefully (via retry mechanism).
- **Error Handling:** Implement basic error handling as described below.

**5.3. Error Handling Requirements:**

- **Retry Mechanism:** Implement a retry mechanism for website scraping failures (e.g., attempt to re-scrape 2-3 times).
- **Error Notifications:** Send email notifications to the user for persistent scraping errors or critical agent errors.
- **Logging:** Log agent activity and errors to a file for debugging and monitoring purposes.

**5.4. Testing Requirements:**

- **Testing Strategy (MVP):**
    - **Phased Approach:** Focus initial testing on one website from the configuration list to ensure accurate data extraction and alert generation.
    - **Manual Verification:** Manually compare data extracted by the agent with the information displayed on the target websites to validate accuracy.

**6. Out of Scope (Phase 2 Features - Future Enhancements)**

The following features are explicitly excluded from the MVP but are considered for future development in Phase 2 and beyond:

- **Price Drop Alerts:** Alerts for apartment listings that have decreased in price.
- **Price Trend Tracking:** Tracking and reporting on historical price trends for apartment listings.
- **Per-Website Threshold Configuration:** Ability to set different price thresholds or other criteria for individual websites.
- **Interactive User Interface:** A graphical user interface (UI) or command-line interface (CLI) for configuration and agent management.
- **More Advanced AI for Extraction:** Employing more sophisticated Natural Language Processing (NLP) or Machine Learning (ML) techniques for more robust and accurate information extraction from diverse website layouts.
- **Tour Scheduling Integration:** Features to facilitate scheduling apartment tours directly from alerts.
- **Calendar Integration:** Integration with user's calendar to manage viewing appointments or deadlines.
- **Apartments.com, Zillow, Google API Integration:** Direct integration with these platforms (initially focus on individual apartment websites).

---

**End of Product Requirements Document (PRD) - MVP Agentic Apartment Finder**

---