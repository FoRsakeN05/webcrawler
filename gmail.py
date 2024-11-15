from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuración del servicio de Chrome
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)  
driver.get("https://mail.google.com/")

try:
    # Esperar a que el campo de correo esté visible e ingresar correo
    correo = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "identifierId")))

    correo.send_keys("webtrabajos0@gmail.com")
    correo.send_keys(Keys.ENTER)
    
    # Esperar al campo de contraseña
    contra = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "Passwd")))

    contra.send_keys("Webcraler23")
    contra.send_keys(Keys.RETURN)

    # Esperar a que aparezca el botón "Más" y hacer clic
    boton_mas = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'J-Ke') and contains(@class, 'n4')]"))
    )
    boton_mas.click()

    # Esperar a que el botón "Todos" sea clickeable y hacer clic
    boton_todos = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='Todos']"))
    )
    boton_todos.click()

    # Esperar a que el botón "No leídos" sea clickeable y hacer clic
    boton_no_leidos = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//a[text()='No leídos']"))
    )
    boton_no_leidos.click()

    # Esperar a que los correos no leídos estén visibles
    WebDriverWait(driver, 15).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//span[@email]"))
    )

    # Localizar todos los elementos con el atributo 'email' dentro de los correos no leídos
    correos = driver.find_elements(By.XPATH, "//span[@email]")

    # Extraer los correos y almacenarlos
    correos_lista = [correo.get_attribute('email') for correo in correos]
    
    # Imprimir los correos extraídos
    for correo in correos_lista:
        print(correo)

finally:
    driver.quit()
