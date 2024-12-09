import time
import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Selenium setup
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

def scrape_10times(url):
    try:
        # Set up Selenium WebDriver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Open the website
        driver.get(url)
        time.sleep(5)  # Wait for the page to load

        # Scrape event titles
        events = driver.find_elements(By.CSS_SELECTOR, "bg-white p-2 border rounded-3 box-shadow link cursor-pointer")
        event_titles = [event.text for event in events]

        # Scrape event locations
        locations = driver.find_elements(By.CSS_SELECTOR, ".venue-name")
        event_locations = [location.text for location in locations]

        # Scrape event dates
        dates = driver.find_elements(By.CSS_SELECTOR, ".date")
        event_dates = [date.text for date in dates]

        # Close the WebDriver
        driver.quit()

        # Combine data into a DataFrame
        data = {"Event Title": event_titles, "Location": event_locations, "Date": event_dates}
        df = pd.DataFrame(data)

        # Return the DataFrame and an empty error message
        return df, None
    except Exception as e:
        # Return an empty DataFrame and the error message
        return pd.DataFrame(), str(e)


# Streamlit UI
st.title("10times.com Event Scraper")

# Input field for URL
url = st.text_input("Enter the URL to scrape:", "https://10times.com/")

if st.button("Scrape Data"):
    if url:
        st.info("Scraping data from the website. Please wait...")
        scraped_data, error = scrape_10times(url)

        if not scraped_data.empty:
            st.success("Scraping completed successfully!")
            st.dataframe(scraped_data)

            # Convert DataFrame to CSV for download
            csv_data = scraped_data.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name="10times_events.csv",
                mime="text/csv",
            )
        else:
            st.error(f"Scraping failed: {error}")
    else:
        st.error("Please enter a valid URL.")
