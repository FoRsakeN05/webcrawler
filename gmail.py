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
driver.get("https://mail.google.com/")

try:
    correo = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "identifierId")))

    correo.send_keys("webtrabajos0@gmail.com")
    correo.send_keys(Keys.ENTER)
    
    contra = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "Passwd")))

    contra.send_keys("Webcraler23")
    contra.send_keys(Keys.RETURN)
    
    boton_mas = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'J-Ke') and contains(@class, 'n4')]"))
    )
    boton_mas.click()

    boton_todos = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Todos']"))
    )
    boton_todos.click()

    boton_no_leidos = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='No leídos']"))
    )
    boton_no_leidos.click()

    WebDriverWait(driver, 15).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//span[@email]"))
    )

    correos = driver.find_elements(By.XPATH, "//span[@email]")

    correos_lista = [correo.get_attribute('email') for correo in correos]
    
    for correo in correos_lista:
        print(correo)

finally:
    driver.quit()
