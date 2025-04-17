# Agentic Apartment Finder

This project contains an agentic apartment finder that scrapes websites, extracts listing information, and sends email alerts.

## Project Structure

*   **`agent_checkpoint.py`:** This is the original Python script designed for local execution.
*   **`main.py`:** This is the refactored version of the script, designed for deployment as a Google Cloud Function.
*   **`config.json`:** Configuration file containing website URLs, scraping engine selection, and filter criteria.
*   **`requirements.txt`:** Lists the Python dependencies for the project.
*   **`.env`:** (Not for deployment) This file is used for local development to store environment variables like API keys.
*   **`scraping_engines/`:** (Potentially contains different scraping engine implementations)

## `agent_checkpoint.py` (Local Execution)

### Setup (Local)

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Configure Environment Variables:**
    *   Create a `.env` file in the project root.
    *   Add your Google API key and Jina AI API key:

        ```
        GOOGLE_API_KEY=your_google_api_key
        JINA_API_KEY=your_jina_api_key
        ```
3.  **Configure `config.json`:**
    *   Edit the `config.json` file to specify the websites to scrape, the scraping engine (`BeautifulSoup` or `JinaAi`), and any desired filters (e.g., minimum square footage, number of bedrooms/bathrooms, move-in date).  Example:

    ```json
    {
      "websites": [
        {
          "name": "Example Property",
          "url": "https://www.example.com/apartments"
        }
      ],
      "scraping_engine": "BeautifulSoup",
      "filters": {
        "min_sqft": 500,
        "bedrooms": 1,
        "bathrooms": 1,
        "desired_move_in_date": "2024-03-15",
        "move_in_date_range_days": 30
      }
    }
    ```

### Running Locally

Execute the script:

```bash
python agent_checkpoint.py
```

The script will scrape the configured websites, extract listing information, and send an email alert.

## `main.py` (Google Cloud Function)

This file contains the code for deploying the apartment finder as a Google Cloud Function.

### Deployment (Google Cloud Functions)

1.  **Create a Google Cloud Project:** If you don't already have one, create a Google Cloud project.
2.  **Enable APIs:** Enable the necessary APIs (e.g., Cloud Functions API, Cloud Build API).
3.  **Install the `gcloud` CLI:** If you haven't already, install and configure the Google Cloud SDK (`gcloud` CLI).
4.  **Deploy the Function:**
    *   Navigate to the project directory in your terminal.
    *   Deploy using the `gcloud` command:

    ```bash
     gcloud functions deploy apartment-finder \
        --region YOUR_REGION \
        --runtime python39 \
        --trigger-http \
        --entry-point run_apartment_finder \
        --memory 256MB \
        --timeout 60 \
        --set-env-vars GOOGLE_API_KEY=your_google_api_key,JINA_API_KEY=your_jina_api_key
    ```

    *   Replace `YOUR_REGION` with the desired region (e.g., `us-central1`).
    *   Adjust `--memory` and `--timeout` as needed.
    *   Make sure to set the `GOOGLE_API_KEY` and `JINA_API_KEY` environment variables.
    * You can also deploy through the Google Cloud Console by creating a new function, selecting HTTP trigger, setting the runtime to Python 3.9 (or later), setting the entry point to `run_apartment_finder`, and uploading the `main.py`, `config.json`, and `requirements.txt` files. Remember to set the environment variables in the Cloud Function configuration.

5. **Test the Function:** Once deployed, you can test the function by sending an HTTP request to its trigger URL (which you can find in the Cloud Functions console).

### Notes

*   The `main.py` file is designed to be self-contained and does not rely on the `.env` file for deployment.
*   Consider using Cloud Tasks for more robust, asynchronous email sending in a production environment.
*   The provided code uses basic error handling. For a production system, you would want to implement more comprehensive error handling and logging.