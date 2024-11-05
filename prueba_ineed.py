from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time 

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)  
driver.get("https://mx.indeed.com/")



try:
    titulo = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "text-input-what")))          
    titulo.send_keys("lunes a viernes")
    lugar = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "text-input-where")))
    lugar.send_keys("Guadalajara, Jal")
    lugar.send_keys(Keys.RETURN)

    time.sleep(10)
    trabajos = driver.find_elements(By.CLASS_NAME, "resultContent")

   
    for trabajo in trabajos:
        
        job_title = trabajo.find_element(By.CLASS_NAME, "jobTitle").text
       
        company_name = trabajo.find_element(By.CLASS_NAME, "company_location").text
        print(f"Trabajo: {job_title}")
        print(f"Empresa: {company_name}")
        print("-" * 40)

    time.sleep(15)
finally:
    driver.quit()  
