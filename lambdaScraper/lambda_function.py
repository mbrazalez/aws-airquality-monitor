import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def lambda_handler(event, context):
    # Webdriver setup
    options = Options()
    options.headless = True
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(options=options, service=Service(ChromeDriverManager().install()))

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

    print('Web scraping finished')  
    print(scrapped_data)
            
