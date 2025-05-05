# due_diligence: Automatize the due diligence process from open sources for consultation
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-white?style=for-the-badge&logo=scrapy)


## Table of Contents
1. [Abstract](#abstract)
2. [Theoretical Framework](#theoretical-framework)
3. [Methodology](#methodology)
4. [Deployment](#deployment)
5. [Technical Implementation](#technical-implementation)
6. [Installation](#installation)
7. [Usage](#usage)
8. [License](#license)

## Abstract
due_diligence is a web scraping tool designed to take screenshots of the information sources using selenium webdriver. It exports the screenshots as evidences in a word file following the format given in CELEC EP. The information sources are:
- **Servicio de Rentas Internas**
  - [Consulta de RUC/ Empresas fantasmas del SRI](https://srienlinea.sri.gob.ec/sri-en-linea/SriRucWeb/ConsultaRuc/Consultas/consultaRuc)
  - [Estado Tributario](https://srienlinea.sri.gob.ec/sri-en-linea/SriDeclaracionesWeb/EstadoTributario/Consultas/consultaEstadoTributario)
  - [Deudas firmes e impugnadas](https://srienlinea.sri.gob.ec/sri-en-linea/SriPagosWeb/ConsultaDeudasFirmesImpugnadas/Consultas/consultaDeudasFirmesImpugnadas)
- **Aduana del Ecuador**
  - [Liquidaciones vencidas](https://www.aduana.gob.ec/consulta-de-certificado-cumplimiento/)
- **Fiscalía**
  - [Procesos Fiscales](https://www.fiscalia.gob.ec/consulta-de-noticias-del-delito/)
- **Consejo de la Judicatura**
  - [Procesos Judiciales](https://procesosjudiciales.funcionjudicial.gob.ec/busqueda-filtros)
- **Servicio Nacional de Contratación Pública (SERCOP)**
  - [Búsqueda de no ser contratista incumplido o adjudicatario fallido con el Estado](https://www.compraspublicas.gob.ec/ProcesoContratacion/compras/EP/EmpReporteIncumplidos.cpe)
- **Contraloría General del Estado**
  - [Informes Aprobados](https://www.contraloria.gob.ec/Consultas/InformesAprobados)
- More to come ...

## Theoretical Framework
- **Due Diligence**: Due diligence is a pre-transaction investigative process aimed at assessing risks and opportunities by thoroughly examining a company or asset to verify expectations and uncover potential issues.
- **Web Scraping**: The process of extracting data from websites using automated scripts.
- **Word Report**: Using python-docx to create Word files with the screenshots of the consulted sites.

## Methodology
The due_diligence follows a structured approach:
1. **User  Input**: Users provide a RUC.
2. **Word Export**: The captured screenshots is exported to Word files, with appropriate format.

## Deployment
due_diligence is built using Flask, allowing it to run as a web application. The application processes user requests and returns the extracted data in Word format.

## Technical Implementation
due_diligence is developed in Python 3.9, utilizing:
- **Flask** for the web interface.
- **Requests** for making HTTP requests to the SRI website.
- **Selenium** for simulating the user interaction with the websites and capture the screenshots.
- **Python-docx** for exporting the report to Word files.

## Installation
### Prerequisites
- **Python 3.9**: Ensure that Python is installed and configured in your system.

or
- **Docker**: Ensure to have Docker installed and running in the system.

### Installation
#### Via Github
- **Clone the repository**
  ```bash
  git clone https://github.com/nava2105/due_diligence.git
  cd due_diligence
  ```
- **Required Libraries**: Install the necessary libraries using pip:
  ```bash
  pip install -r requirements.txt
  ```
- **Run the application**
  ```bash
  python app.py
  ```
- **Access the application:** Open your web browser and navigate to http://localhost:5000
#### Via Dockerhub
- **Clone the docker image**
  ```bash
  docker pull na4va4/due_diligence
  ```
- **Run the image in a container**
  ```bash
  docker run -p 5000:5000 na4va4/due_diligence
  ```
- **Access the application:** Open your web browser and navigate to http://localhost:5000

## Usage
Once the application is up and running, you can interact with the system by:
### Generating the due diligence report: 
- Input the RUC.
- Submitting the form to generate and download the corresponding Word file.

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.