import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuración inicial
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://mail.google.com/")

emails_data = []  # Lista para almacenar información de correos

try:
    # Inicio de sesión
    correo = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "identifierId")))
    correo.send_keys("webtrabajos0@gmail.com")
    correo.send_keys(Keys.ENTER)

    contra = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.NAME, "Passwd")))
    contra.send_keys("Webcraler23")
    contra.send_keys(Keys.RETURN)

    # Esperar a que cargue la bandeja de entrada
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//table[@role='grid']")))

    # Buscar correos en la bandeja de entrada
    correos = driver.find_elements(By.XPATH, "//table[@role='grid']//tr[@class='zA zE']")  # Selecciona solo correos no leídos
    
    print("=== Detalles de correos no leídos ===")
    for correo in correos:
        try:
            # Haz clic en el correo para abrirlo
            correo.click()

            # Espera a que el cuerpo del mensaje se cargue
            contenido_mensaje = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='listitem']//div[@dir='ltr']"))
            ).text

            # Extrae información adicional
            asunto = driver.find_element(By.XPATH, "//h2[@class='hP']").text  # Asunto del correo
            remitente = driver.find_element(By.XPATH, "//span[@class='gD']").text  # Remitente
            
            print(f"De: {remitente}")
            print(f"Asunto: {asunto}")
            print(f"Contenido:\n{contenido_mensaje}")
            print("-" * 40)

            # Guardar la información en la lista
            emails_data.append({
                "remitente": remitente,
                "asunto": asunto,
                "contenido": contenido_mensaje
            })

            # Regresar a la bandeja de entrada
            driver.back()

            # Esperar a que se recargue la lista de correos
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//table[@role='grid']")))

        except Exception as e:
            print(f"Error al procesar un correo: {e}")
            driver.back()  # Regresar en caso de error
            continue

    # Guardar los datos en un archivo JSON
    with open("emails_data.json", "w") as f:
        json.dump(emails_data, f, indent=4)

finally:
    driver.quit()  # Cerrar el navegador al finalizar