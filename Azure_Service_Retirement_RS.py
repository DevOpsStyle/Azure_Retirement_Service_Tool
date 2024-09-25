############################################
# Tommaso Sacco - Cloud Solution Architect #
#                   V0.2                   #
############################################
import feedparser
import spacy
from jinja2 import Template
from datetime import datetime
import re
import logging

# Configurazione del logger
logging.basicConfig(filename='Azure_Service_Retirements.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Carica il modello SpaCy per il riconoscimento di entità (NER)
logging.info('Caricamento Spacy lib')
nlp = spacy.load("en_core_web_sm")

# Funzione per estrarre date usando SpaCy
def extract_dates_spacy(text):
    logging.info('Ricerca date con Spacy')
    doc = nlp(text)
    dates = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
    return dates if dates else ["No date found"]

# Funzione per rimuovere suffissi come "th", "nd", "rd"
def clean_date_text(text):
    return re.sub(r'(\d{1,2})(st|nd|rd|th)', r'\1', text)

# Funzione per estrarre date con regex specifiche per formati non standard
def extract_dates_regex(text):
    logging.info('Applicazione Regex per ricerca Retirement Date')

    # Pulisce il testo dai suffissi
    text = clean_date_text(text)

    # Regex per formati di date con suffissi e virgole
    regex_patterns = [
        r'\b\d{1,2}(st|nd|rd|th)?\s(?:January|February|March|April|May|June|July|August|September|October|November|December),?\s\d{4}\b',  # 31st August, 2024
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2}(st|nd|rd|th)?,?\s\d{4}\b',  # 31st August 2024
        r'\b\d{1,2}[-/](?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-zA-Z]*[-/]\d{4}\b',  # 30-Sep-2026
        r'\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b',  # 26/09/2025
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}\b'  # March 2025
    ]

    for regex in regex_patterns:
        match = re.search(regex, text)
        if match:
            print(f"Data trovata: {match.group(0)} nel testo: {text}")  # Stampa la data catturata
            return match.group(0)

    print(f"Nessuna data trovata nel testo: {text}")  # Stampa se nessuna data è trovata
    return "No date found"

# Funzione per estrarre la data di retirement dal titolo o dalla descrizione
def extract_retirement_date(title, description):
    # Prova prima con la regex nel titolo
    retirement_dates_title = extract_dates_regex(title)

    # Se non ci sono date valide nel titolo, prova nella descrizione
    if retirement_dates_title == "No date found":
        retirement_dates_description = extract_dates_regex(description)

        # Ritorna la data trovata nella descrizione o nel titolo
        return retirement_dates_description if retirement_dates_description != "No date found" else retirement_dates_title

    return retirement_dates_title

# Funzione per ottenere i dati dal feed RSS e generare la tabella
def get_retirement_data():
    logging.info('Apertura del link RSS per ottenere i dati')
    url = "https://aztty.azurewebsites.net/rss/updates?category=retirements"
    feed = feedparser.parse(url)

    retirements = []
    for entry in feed.entries:
        title = entry.title
        description = entry.description
        pub_date_str = entry.published.replace(" Z", "")  # Rimuovi il carattere 'Z'
        pub_date = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S')
        formatted_date = pub_date.strftime('%d %B %Y')  # Formattiamo la data

        # Estrazione della data di retirement dal titolo o descrizione
        retirement_date = extract_retirement_date(title, description)

        retirements.append({
            "title": title,
            "link": entry.link,
            "description": description,
            "pub_date": formatted_date,
            "retirement_date": retirement_date  # Aggiungi la data di retirement
        })

    logging.info('Dati RSS raccolti con successo')
    return retirements

# Funzione per generare la pagina HTML
def create_html_page(retirements):
    logging.info('Generazione della pagina HTML')
    template_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Azure Service Retirements</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f9;
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            .search-container {
                display: flex;
                justify-content: center;
                margin-bottom: 20px;
            }
            .search-bar {
                padding: 10px;
                width: 300px;
                box-sizing: border-box;
                border-radius: 5px;
                border: 1px solid #ddd;
                transition: width 0.4s ease-in-out;
            }
            .search-bar:focus {
                width: 500px;
            }
            .search-btn, .export-btn {
                padding: 10px;
                margin-left: 10px;
                background-color: #0078d4;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            .search-btn:hover, .export-btn:hover {
                background-color: #005ba1;
            }
            .table-container {
                width: 100%;
                overflow-x: auto; /* Permette lo scorrimento orizzontale */
            }
            table {
                width: 100%;
                border-collapse: collapse;
                background-color: white;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                table-layout: auto;
                min-width: 600px; /* Imposta una larghezza minima per evitare l'impaginazione errata */
            }
            th, td {
                padding: 10px;
                border: 1px solid #ddd;
                text-align: left;
                cursor: pointer;
            }
            th {
                background-color: #f2f2f2;
                color: #333;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            tr:nth-child(odd) {
                background-color: #ffffff;
            }
            tfoot {
                margin-top: 20px;
            }
        </style>
        <script>
            function searchService() {
                let input = document.getElementById('searchInput').value.toLowerCase();
                let rows = document.getElementById('retirementTable').getElementsByTagName('tr');
                for (let i = 1; i < rows.length; i++) {
                    let title = rows[i].getElementsByTagName('td')[0].innerText.toLowerCase();
                    if (title.includes(input)) {
                        rows[i].style.display = '';
                    } else {
                        rows[i].style.display = 'none';
                    }
                }
            }

            function filterByColumn(columnIndex) {
                let filterText = prompt("Inserisci il testo da cercare:").toLowerCase();
                let rows = document.getElementById('retirementTable').getElementsByTagName('tr');

                for (let i = 1; i < rows.length; i++) {
                    let cellText = rows[i].getElementsByTagName('td')[columnIndex].innerText.toLowerCase();
                    if (cellText.includes(filterText)) {
                        rows[i].style.display = '';
                    } else {
                        rows[i].style.display = 'none';
                    }
                }
            }

            function exportToCSV() {
                let rows = document.querySelectorAll('#retirementTable tr:not([style*="display: none"])');
                let csv = [];
                rows.forEach(row => {
                    let cols = row.querySelectorAll('td, th');
                    let csvRow = [];
                    cols.forEach(col => {
                        csvRow.push('"' + col.innerText.replace(/"/g, '""') + '"');
                    });
                    csv.push(csvRow.join(','));
                });

                let csvContent = csv.join("\\n");
                let blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
                let link = document.createElement('a');
                let url = URL.createObjectURL(blob);
                link.setAttribute('href', url);
                link.setAttribute('download', 'Azure_Service_Retirements.csv');
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
        </script>
    </head>
    <body>
        <h1>Azure Service Retirements</h1>
        <div class="search-container">
            <input type="text" id="searchInput" class="search-bar" placeholder="Search for services..">
            <button class="search-btn" onclick="searchService()">Search</button>
            <button class="export-btn" onclick="exportToCSV()">Export to CSV</button>
        </div>
        <div class="table-container">
            <table id="retirementTable">
                <thead>
                    <tr>
                        <th onclick="filterByColumn(0)">Service</th>
                        <th onclick="filterByColumn(1)">Description</th>
                        <th onclick="filterByColumn(2)">Publication Date</th>
                        <th onclick="filterByColumn(3)">Target Retirement Date</th> <!-- Nuova colonna -->
                    </tr>
                </thead>
                <tbody>
                    {% for retirement in retirements %}
                    <tr>
                        <td><a href="{{ retirement.link }}" target="_blank">{{ retirement.title }}</a></td>
                        <td>{{ retirement.description }}</td>
                        <td>{{ retirement.pub_date }}</td>
                        <td>{{ retirement.retirement_date }}</td> <!-- Data di retirement -->
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        <tfoot style="text-align: left; margin-top: 40px;">
            <div style="text-align: left; width: 100%; display: flex; justify-content: flex-start;">
                <img src="https://upload.wikimedia.org/wikipedia/commons/9/96/Microsoft_logo_%282012%29.svg" alt="Microsoft Logo" width="100">
            </div>
        </tfoot>
    </body>
    </html>
    """

    template = Template(template_html)
    html_content = template.render(retirements=retirements)

    with open('azure_service_retirements.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    logging.info('Pagina HTML generata e salvata con successo')

# Esecuzione dello script
if __name__ == "__main__":
    logging.info('Esecuzione dello script iniziata')
    retirements = get_retirement_data()
    create_html_page(retirements)
    logging.info('Esecuzione dello script completata con successo')
