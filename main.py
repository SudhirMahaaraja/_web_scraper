import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Function to set up WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.headless = False
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver_service = Service(r"C:\Windows\chromedriver.exe")
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    return driver

# Function to scrape movie details
def scrape_movie_details(url):
    driver = setup_driver()
    driver.get(url)
    time.sleep(2)  # Wait for the page to load

    # Scraping the data using class names
    try:
        tab_open = driver.find_element(By.CLASS_NAME, 'ipc-icon-button ipc-icon-button--base ipc-icon-button--onAccent2')  # Title class
        tab_open.click()

        time.sleep(1)  # Give time for the detailed view to load

        # Scraping titles, years, ratings, directors, and descriptions using class names
        titles = driver.find_elements(By.CLASS_NAME, 'ipc-title__text')  # Title class
        years = driver.find_elements(By.CLASS_NAME, 'sc-300a8231-7')  # Year class
        ratings = driver.find_elements(By.CLASS_NAME, 'ipc-rating-star--rating')  # Ratings class
        directors = driver.find_elements(By.CLASS_NAME, 'ipc-link ipc-link--base')  # Director class
        descriptions = driver.find_elements(By.CLASS_NAME, 'ipc-html-content-inner-div')  # Description class

        titles_text = [title.text for title in titles]
        years_text = [year.text for year in years]
        ratings_text = [rating.text for rating in ratings]
        directors_text = [director.text for director in directors]
        descriptions_text = [description.text.strip() for description in descriptions]

        # If no data is scraped, show an error message
        if not titles_text:
            print("No data scraped. Please try again.")
            driver.quit()
            return pd.DataFrame()

        # Create a DataFrame
        data = {
            'Title': titles_text,
            'Year': years_text,
            'Rating': ratings_text,
            'Director': directors_text,
            'Description': descriptions_text
        }

        # Create DataFrame and save to CSV
        df = pd.DataFrame(data)
        df.to_csv("scraped_data.csv", index=False)
        driver.quit()
        return df

    except Exception as e:
        print(f"Error scraping data: {e}")
        driver.quit()
        return pd.DataFrame()

# Main Program
url_input = "https://www.imdb.com/chart/top/"

if url_input:
    # Scrape the data and display the DataFrame
    df = scrape_movie_details(url_input)

    if not df.empty:  # If the dataframe is not empty
        print("### Scraped Data")
        print(df.head())  # Display the head of the DataFrame

        # Provide an option to download the CSV file
        with open('scraped_data.csv', 'rb') as f:
            # Simulate the download
            print("Download the CSV file at the provided path.")
    else:
        print("No data found. Please check the URL or try again.")
else:
    print("Please enter a valid URL.")
