# Azure Retirement Service Tool

[![Python](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/)  

## 🚀 Introduction

**Azure Retirement Service Tool** is a Python-based tool designed to simplify the access to information about Azure services approaching retirement. This tool fetches data from the official Azure Update Blog RSS feed and generates a formatted HTML page that includes:

- 📝 **Update Title**
- 📖 **Service Description**
- 📅 **Publication Date**
- 🚨 **Retirement Date**

The project is not intended to replace existing tools provided by Azure, which remain the official sources of information. Instead, our goal is to provide users with a simplified way to search and view the relevant data.

## 🎯 Project Goal

With Azure offering a wide range of services, keeping track of service retirement dates can be challenging. This tool aims to:

1. Fetch real-time update information directly from the Azure RSS feed.
2. Display service details in a well-organized HTML page.
3. Allow users to perform targeted searches on the collected information, saving time and effort.

## ✨ Key Features

- **Dynamic Updates:** The application updates the information every time it is run, reading data from the official Azure RSS feed.
- **Formatted HTML Output:** All information is displayed in a clean, well-structured HTML page.
- **Simplified Search:** Users can quickly search for specific services or retirement dates, improving visibility and management of critical deadlines.

## 🛠️ Requirements

- Python 3.x
- Required Python libraries:
  - `feedparser` – To read the RSS feed from the Azure blog.
  - `spacy` – Used for natural language processing to enhance the understanding of extracted data.
  - `jinja2` – For generating dynamic HTML templates.
  - `datetime` – To handle publication and retirement dates.
  - `re` – Used for regular expressions in string manipulation.
  - `logging` – For log management and activity monitoring.

## 🖥️ Installation

1. Clone the repository to your local environment:
    ```bash
    git clone https://github.com/yourusername/Azure_Retirement_Service_Tool.git
    ```
   
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the tool:
    ```bash
    python azure_retirement_service_tool.py
    ```

## 🌟 Usage Example

After running the tool, an HTML page will be generated that includes all the relevant details about retiring Azure services. You can search within the page to quickly filter the services that interest you.

### HTML Output

The generated page will include:

- **Update Title** (e.g., *Azure Storage retiring on XYZ Date*)
- **Service Description**
- **Publication Date** and **Retirement Date**

## 📢 Important Note

This tool does not replace official Azure tools. The displayed information is fetched directly from the Azure Update Blog and should be verified using Azure’s official sources before making critical decisions.

## 📜 Contributors

| Contributor       | LinkedIn Profile                                |
|-------------------|-------------------------------------------------|
| Tommaso Sacco - Cloud Solution Architect | [LinkedIn Profile](https://www.linkedin.com/in/tommasosaccoit/) |

## 🤝 Contributions

Contributions are welcome! If you'd like to improve this project, feel free to open a pull request or create an issue.
