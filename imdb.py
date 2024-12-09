import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import streamlit as st
import csv


# Function to setup WebDriver
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
    time.sleep(3)  # Wait for the page to load

    # Scraping the data using XPaths
    try:
        tab_open =  driver.find_element(By.XPATH, '//*[@id="list-view-option-detailed"]')
        tab_open.click()

        titles = driver.find_elements(By.XPATH,
                                      '//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li/div[2]/div/div/div[1]/a/h3')
        years = driver.find_elements(By.XPATH,
                                     '//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li/div[2]/div/div/div[2]/span[1]')
        ratings = driver.find_elements(By.XPATH,
                                       '//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li/div[2]/div/div/span/div/span/span[1]')
        directors = driver.find_elements(By.XPATH, '//*[@id="nm0001104"]')  # Director name

        descriptions = driver.find_elements(By.XPATH,
                                            '//*[@id="__next"]/main/div/div[3]/section/div/div[2]/div/ul/li[1]/div/div/div/div[2]/div/div/text()')  # Description

        titles_text = [title.text for title in titles]
        years_text = [year.text for year in years]
        ratings_text = [rating.text for rating in ratings]
        directors_text = [director.text for director in directors]
        descriptions_text = [description.text.strip() for description in descriptions]


        # If no data is scraped, show an error message
        if not titles_text:
            st.error("No data scraped. Please try again.")
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
        st.error(f"Error scraping data: {e}")
        driver.quit()
        return pd.DataFrame()


# Streamlit UI
st.title("Web Scraper")
st.markdown("Enter the URL of the website ")

# Input box to enter the URL
url_input = st.text_input("Enter Website URL", "https://www.imdb.com/chart/top/")

if st.button('Scrape Data'):
    if url_input:
        # Scrape the data and display the DataFrame
        df = scrape_movie_details(url_input)

        if not df.empty:  # If the dataframe is not empty
            st.write("### Scraped Data", df.head())  # Display the head of the DataFrame

            # Provide an option to download the CSV file
            with open('scraped_data.csv', 'rb') as f:
                st.download_button(
                    label="Download CSV",
                    data=f,
                    file_name='scraped_data.csv',
                    mime='text/csv'
                )
        else:
            st.warning("No data found. Please check the URL or try again.")
    else:
        st.warning("Please enter a valid URL.")
