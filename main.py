import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from tempfile import mkdtemp

def lambda_handler(event, context):
    # Set the path to the Chrome and ChromeDriver
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-tools")
    chrome_options.add_argument("--no-zygote")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument(f"--user-data-dir={mkdtemp()}")
    chrome_options.add_argument(f"--data-path={mkdtemp()}")
    chrome_options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    chrome_options.add_argument("--remote-debugging-pipe")
    chrome_options.add_argument("--verbose")
    chrome_options.add_argument("--log-path=/tmp")
    chrome_options.binary_location = "/opt/chrome/chrome-linux64/chrome"

    service = Service(
        executable_path="/opt/chrome-driver/chromedriver-linux64/chromedriver",
        service_log_path="/tmp/chromedriver.log"
    )

    driver = webdriver.Chrome(
        service=service,
        options=chrome_options
    )

    # Get the page for scraping
    driver.get("https://troposfera.es/datos/dev-albacete/#/dashboard")

    # Wait for page to load
    time.sleep(2)

    scrapped_data = []

    # Loop through the stations 
    for i in range(16):
        j = 0
        while True:
            try:
                j += 1
                # Find the button for PM10
                button = driver.find_element(By.XPATH, f'/html/body/airadvanced-root/airadvanced-header-menu-layout/div/main/div/airadvanced-dashboard-container/div/div[2]/div[1]/airadvanced-tarjetas-estaciones-red/div/div[2]/airadvanced-card-estacion[{i}]/div/div/div[2]/div/form/div/airadvanced-button-group/div/label[{j}]')
                if button.text == 'PM10':
                    # Get the station name
                    station_name = driver.find_element(By.XPATH, f'/html/body/airadvanced-root/airadvanced-header-menu-layout/div/main/div/airadvanced-dashboard-container/div/div[2]/div[1]/airadvanced-tarjetas-estaciones-red/div/div[2]/airadvanced-card-estacion[{i}]/div/div/div[1]/div/div[1]/div[2]/h5')
                    # Click the button
                    button.click()
                    # Get the PM10 value
                    pm10_value = driver.find_element(By.XPATH, f'/html/body/airadvanced-root/airadvanced-header-menu-layout/div/main/div/airadvanced-dashboard-container/div/div[2]/div[1]/airadvanced-tarjetas-estaciones-red/div/div[2]/airadvanced-card-estacion[{i}]/div/div/div[2]/div/form/div/div/airadvanced-contaminante-widget/div/div[1]/div[3]/div/h4')
                    # Append the scraped data to a list
                    scrapped_data.append({
                        'station': station_name.text,
                        'pm10': pm10_value.text
                    })
                    break
            except:
                # End of the button options
                break

     # Close the WebDriver
    driver.quit()

    return {
            'statusCode': 200,
            'body': scrapped_data
        }            
