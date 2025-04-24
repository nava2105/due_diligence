import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import json
from selenium.common.exceptions import TimeoutException
from docx import Document
from docx.shared import Inches, Pt
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# Add this new function to handle header image
def add_header_image(document, image_path):
    # Set A4 page size (A4 = 210mm × 297mm)
    section = document.sections[0]
    section.page_width = Pt(595.276)  # 210mm in points
    section.page_height = Pt(841.890)  # 297mm in points

    # Set header with no margins
    section.header_distance = Inches(0)
    section.left_margin = Inches(1)  # Regular margin for main content
    section.right_margin = Inches(1)  # Regular margin for main content
    section.top_margin = Inches(1)  # Regular margin for main content
    section.bottom_margin = Inches(1)  # Regular margin for main content

    # Add image to header
    header = section.header
    header_para = header.paragraphs[0]
    header_para.paragraph_format.left_indent = Inches(-1)  # Negative indent to counter page margin
    run = header_para.add_run()
    picture = run.add_picture(image_path, width=Inches(8.27))  # 210mm = 8.27 inches (full A4 width)
    
    # Get the parent element of the picture
    pic = picture._inline.graphic.graphicData.pic
    pic_pr = pic.spPr

    # Create new elements for behind text layout
    a = OxmlElement('a:effectLst')
    pic_pr.append(a)

    # Set the z-order of the picture to be behind text
    pic_pr.append(OxmlElement('a:relativeHeight'))
    pic_pr.append(OxmlElement('a:behindDoc'))

    return document

urls = [
    'https://srienlinea.sri.gob.ec/sri-en-linea/SriRucWeb/ConsultaRuc/Consultas/consultaRuc',
    'https://srienlinea.sri.gob.ec/sri-en-linea/SriDeclaracionesWeb/EstadoTributario/Consultas/consultaEstadoTributario',
    'https://srienlinea.sri.gob.ec/sri-en-linea/SriPagosWeb/ConsultaDeudasFirmesImpugnadas/Consultas/consultaDeudasFirmesImpugnadas'
]
docs_data = [
    "Consulta de RUC/ Empresas fantasmas del SRI",
    "Estado Tributario",
    "Deudas firmes e impugnadas"
]
# Servicio de Rentas Internas
# Consulta de RUC/ Empresas fantasmas del SRI
# Estado Tributario
# Deudas firmes e impugnadas

output_dir = 'screenshots'
os.makedirs(output_dir, exist_ok=True)

# Create Word document
document = Document()
# Replace the regular image addition with header image
add_header_image(document, 'assets/img.png')
document.add_heading('Formato para documentar las Debidas Diligencias Proveedores', level=0)
document.add_heading('Resumen ejecutivo', level=2)
table = document.add_table(1, 2)
table.cell(0, 0).text = 'Fuente:'
table.cell(0, 1).text = 'Servicio de Rentas Internas:'

options = Options()
# options.add_argument('--headless')
# options.add_argument('--disable-gpu')
# options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')


def validate_ruc(ruc):
    validation_url = f"https://srienlinea.sri.gob.ec/sri-catastro-sujeto-servicio-internet/rest/ConsolidadoContribuyente/existePorNumeroRuc?numeroRuc={ruc}"
    response = requests.get(validation_url)
    return response.json()

def get_ruc_data(ruc):
    data_url = f"https://srienlinea.sri.gob.ec/sri-catastro-sujeto-servicio-internet/rest/ConsolidadoContribuyente/obtenerPorNumerosRuc?&ruc={ruc}"
    response = requests.get(data_url)
    return response.json()

def scrape():

    for i, url in enumerate(urls):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        ruc = "0190340325001"
        try:
            # First validate RUC
            is_valid = validate_ruc(ruc)
            if not is_valid:
                print(f"❌ RUC {ruc} no es válido\n")
                continue

            # Get RUC detailed data
            ruc_data = get_ruc_data(ruc)

            # Save JSON data
            json_path = os.path.join(output_dir, f'ruc_data_{ruc}.json')
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(ruc_data, f, ensure_ascii=False, indent=2)
            print(f"✅ Datos JSON guardados en: {json_path}")

            # Continue with screenshot capture
            response = requests.get(url)
            print(f"[{response.status_code}] {url}")
            if response.status_code == 200:
                driver.get(url)
                print("Loading page...")

                # Input RUC number
                try:
                    ruc_input = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "busquedaRucId"))
                    )
                    print("Input field found")
                    ruc_input.clear()
                    ruc_input.send_keys(ruc)
                except Exception as e:
                    print(f"Error finding input field: {str(e)}")
                    raise
                # Click consult button
                try:
                    button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ui-button-text-only') and .//span[contains(text(), 'Consultar')]]"))
                    )
                    print("Button found")
                    button.click()
                    print("Button clicked")
                except Exception as e:
                    print(f"Error with button interaction: {str(e)}")
                    raise

                # Handle CAPTCHA if it appears
                try:
                    # Wait for either CAPTCHA or content to appear
                    captcha_present = False
                    try:
                        captcha = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "g-recaptcha"))
                        )
                        print("CAPTCHA detected!")
                        captcha_present = True
                    except TimeoutException:
                        print("No CAPTCHA found, proceeding...")

                    if captcha_present:
                        # Wait for manual CAPTCHA resolution
                        print("Please solve the CAPTCHA manually...")
                        # Wait for the content to appear after CAPTCHA resolution
                        WebDriverWait(driver, 30).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "ui-panel-content"))
                        )
                    else:
                        # If no CAPTCHA, just wait for content
                        WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "ui-panel-content"))
                        )

                    print("Content loaded")
                    time.sleep(3)
                except Exception as e:
                    raise

                try:
                    ruc_input = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "ui_clickable"))
                    )
                    print("Input field found")
                    ruc_input.clear()
                    ruc_input.send_keys(ruc)
                except Exception as e:
                    raise
                try:
                    ruc_input = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "ui_clickable"))
                    )
                    print("Input field found")
                    ruc_input.clear()
                    ruc_input.send_keys(ruc)
                except Exception as e:
                    raise

                screenshot_path = os.path.join(output_dir, f'capture_{i + 1}.png')
                driver.save_screenshot(screenshot_path)
                
                # Add screenshot to Word document
                document.add_heading(f'Evidence {i + 1}', level=1)
                document.add_paragraph(f'URL: {url}')
                document.add_picture(screenshot_path, width=Inches(6))
                document.add_paragraph('')  # Add some space
                
                print(f"✅ Captura guardada en: {screenshot_path}\n")
            else:
                print("⚠️  No se tomará captura por respuesta distinta de 200.\n")
        except Exception as e:
            screenshot_path = os.path.join(output_dir, f'capture_{i + 1}.png')
            driver.save_screenshot(screenshot_path)

        finally:


            table = document.add_table(2, 2)
            table.cell(0, 0).text = 'Busqueda:'
            table.cell(0, 1).text = docs_data[i]
            document.add_picture(screenshot_path, width=Inches(6))
            
        driver.quit()
    
    # Save Word document
    document.save(os.path.join(output_dir, 'evidence_report.docx'))
    print("✅ Evidence report saved as 'evidence_report.docx'")

if __name__ == '__main__':
    scrape()
