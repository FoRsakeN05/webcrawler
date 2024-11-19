import json
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cargar datos del archivo JSON
with open("emails_data.json", "r") as f:
    emails_data = json.load(f)

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://mx.indeed.com/")

try:
    for email in emails_data:
        # Usar el asunto del correo como título de búsqueda
        search_query = email["asunto"]
        print(f"Buscando trabajos relacionados con el asunto: {search_query}\n")
        
        # Esperar que los campos de búsqueda estén disponibles
        titulo = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "text-input-what")))
        titulo.clear()
        titulo.send_keys(search_query)

        lugar = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "text-input-where")))
        lugar.clear()
        lugar.send_keys("Guadalajara, Jal")
        lugar.send_keys(Keys.RETURN)

        # Esperar que los resultados se carguen
        time.sleep(random.uniform(8, 12))  # Pausa aleatoria de 8 a 12 segundos

        # Obtener trabajos que coincidan
        trabajos = driver.find_elements(By.CLASS_NAME, "resultContent")
        print(f"Resultados para: {search_query}\n{'-' * 40}")
        
        if trabajos:
            for trabajo in trabajos:
                try:
                    # Extraer título del trabajo
                    job_title = trabajo.find_element(By.CLASS_NAME, "jobTitle").text

                    # Filtrar por coincidencia exacta del título con el asunto del correo
                    if search_query.lower() in job_title.lower():
                        company_name = trabajo.find_element(By.CLASS_NAME, "company_location").text
                        print(f"Trabajo: {job_title}")
                        print(f"Empresa: {company_name}")
                        print("-" * 40)
                except Exception as e:
                    print(f"Error al procesar un trabajo: {e}")
        else:
            print("No se encontraron trabajos para esta búsqueda.\n")
        
        # Regresar a la página principal para realizar otra búsqueda
        driver.get("https://mx.indeed.com/")

        # Pausa entre búsquedas para evitar ser bloqueado
        time.sleep(random.uniform(20, 30))  # Pausa aleatoria de 20 a 30 segundos

    print("Búsquedas completadas.")

finally:
    driver.quit()