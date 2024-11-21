import imaplib
import email
import json
import time
import random
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Función para acceder a los correos no leídos
def fetch_unread_emails():
    """Accede a los correos no leídos de la bandeja de entrada"""
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login("webtrabajos0@gmail.com", ".i.")  # Contraseña como string

        # Seleccionar la bandeja de entrada
        mail.select("inbox")
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()
        emails = []

        for email_id in email_ids:
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    from_email = msg["From"]
                    subject = msg["Subject"]
                    email_content = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                email_content += part.get_payload(decode=True).decode()
                    else:
                        email_content = msg.get_payload(decode=True).decode()
                    email_content = re.sub(r'\s+', ' ', email_content).strip()  # Limpiar contenido
                    emails.append({"contenido": email_content, "remitente": from_email, "asunto": subject})
        mail.logout()
        return emails
    except Exception as e:
        print(f"Error al acceder a los correos: {e}")
        return []

# Función para extraer el puesto y la ciudad del cuerpo del correo
def extract_job_details(email_content):
    """Extrae el puesto y ciudad del cuerpo del correo"""
    puesto = None
    ciudad = "Guadalajara"  # Ciudad por defecto

    # Buscar el puesto y ciudad con expresiones regulares
    puesto_match = re.search(r'Puesto:\s*(.*)', email_content)
    ciudad_match = re.search(r'Ciudad:\s*(.*)', email_content)

    if puesto_match:
        puesto = puesto_match.group(1).strip()
    if ciudad_match:
        ciudad = ciudad_match.group(1).strip()

    return puesto, ciudad

# Función para enviar el correo con los resultados
def send_email(subject, body, to_email):
    """Envía un correo con los resultados"""
    from_email = "webtrabajos0@gmail.com"
    from_password = "oits qeyf hygn zhoz"  # Contraseña de aplicación

    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Establecer la conexión SMTP
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Iniciar TLS para seguridad
            server.login(from_email, from_password)
            server.sendmail(from_email, to_email, msg.as_string())
            print(f"Correo enviado a {to_email}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Función para guardar los datos en un archivo JSON
def save_email_data(emails):
    """Guarda los datos de los correos no leídos en un archivo JSON"""
    with open("emails_data.json", "w") as f:
        json.dump(emails, f, indent=4)
    print("Datos de correos guardados en 'emails_data.json'.")

# Procesar los correos no leídos
unread_emails = fetch_unread_emails()  # Obtener los correos no leídos
save_email_data(unread_emails)  # Guardar los correos en un archivo JSON

# Cargar los datos de los correos guardados
with open("emails_data.json", "r") as f:
    emails_data = json.load(f)

# Procesar solo el último correo recibido
last_email = emails_data[-1]  # El último correo en la lista

contenido_mensaje = last_email["contenido"]  # Obtener el contenido del correo

# Extraer los detalles del trabajo (puesto y ciudad)
puesto, ciudad = extract_job_details(contenido_mensaje)

if puesto and ciudad:  # Si tenemos el puesto y la ciudad
    print(f"Buscando trabajos de {puesto} en {ciudad}...")

    # Configuración del WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://mx.indeed.com/")

    # Usar el puesto y la ciudad para realizar la búsqueda en Indeed
    # Esperar que los campos de búsqueda estén disponibles
    titulo = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "text-input-what")))

    titulo.clear()
    titulo.send_keys(puesto)

    lugar = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "text-input-where")))
    lugar.clear()
    lugar.send_keys(ciudad)
    lugar.send_keys(Keys.RETURN)

    # Esperar que los resultados se carguen
    time.sleep(random.uniform(8, 12))  # Pausa aleatoria de 8 a 12 segundos

    # Obtener trabajos que coincidan
    trabajos = driver.find_elements(By.CLASS_NAME, "resultContent")
    print(f"Resultados para: {puesto} en {ciudad}\n{'-' * 40}")

    trabajos_encontrados = []

    if trabajos:
        for trabajo in trabajos:
            try:
                # Extraer título del trabajo
                job_title = trabajo.find_element(By.CLASS_NAME, "jobTitle").text

                # Filtrar por coincidencia exacta del título con el puesto del correo
                if puesto.lower() in job_title.lower():
                    company_name = trabajo.find_element(By.CLASS_NAME, "company_location").text
                    trabajos_encontrados.append(f"Trabajo: {job_title}\nEmpresa: {company_name}\n{'-' * 40}")
            except Exception as e:
                print(f"Error al procesar un trabajo: {e}")
    else:
        trabajos_encontrados.append("No se encontraron trabajos para esta búsqueda.\n")

    # Enviar los resultados por correo
    if trabajos_encontrados:
        email_body = "\n".join(trabajos_encontrados)
        send_email(f"Resultados de búsqueda para {puesto} en {ciudad}", email_body, last_email["remitente"])

    print("Búsquedas completadas.")
    driver.quit()

else:
    print("No se pudieron extraer los datos de trabajo correctamente.")