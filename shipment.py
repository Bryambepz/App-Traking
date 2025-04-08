# from selenium import webdriver
# from selenium.webdriver.common.by import By
# import time

# options = webdriver.ChromeOptions()
# options.add_experimental_option("detach", True)
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument('--disable-extensions')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-infobars')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--disable-browser-side-navigation')
# options.add_argument('--disable-gpu')

# driver = webdriver.Chrome(options=options)

# # idTraking = '281833456029'
# idTraking = '281833789154' SF6311102743611
# driver.get(f"https://parcelsapp.com/es/tracking/{idTraking}")

# # title = driver.title

# while driver.execute_script("return document.readyState") != "complete":
#     print("¡página CARGANDO!!!")
#     time.sleep(1)  # Pausa de 1 segundo antes de volver a comprobar

# print("¡La página ha terminado de cargarse!")

# time.sleep(15)
# driver.refresh()
# # driver.implicitly_wait(0.5)

# # text_box = driver.find_element(by=By.NAME, value="my-text")
# # submit_button = driver.find_element(by=By.CSS_SELECTOR, value="button")

# # text_box.send_keys("Selenium")
# # submit_button.click()

# # message = driver.find_element(by=By.ID, value="message")
# # text = message.text

# # driver.quit()


# ////////////////////////////////////////////////////////////



# class shipment:
#     def __init__(self, trackingId):
#         self.trackingId
# Tracking number

# states	[...]
# origin	string
# Origin country name localized to requested language

# destination	string
# Destination country name localized to requested language

# originCode	string
# Origin country 2-letter code

# destinationCode	string
# Destination country 2-letter code

# status	string
# Parcel status

# Enum:
# Array [ 5 ]
# detectedCarrier	Carrier{...}
# detected	[...]
# services	[...]
# attributes	[...]
# externalTracking	[...]