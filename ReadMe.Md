# MyNotionWork 🚀

A Python-based automation tool to upload structured data (e.g., from Excel or CSV files) into [Notion](https://www.notion.so/) databases. This project streamlines the process of enriching and pushing datasets—like movies, tasks, or project items—into Notion workspaces using Notion's API.

---

## 📁 Project Structure
```
.
├── ReadMe.Md
├── config
│   ├── basic_config.yaml
│   └── just_testing.py
├── data
│   ├── Showtime.xlsx
│   └── test_showtime.xlsx
├── nuploaders
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-311.pyc
│   │   ├── config_loader.cpython-311.pyc
│   │   ├── file_reader.cpython-311.pyc
│   │   ├── imdb_url_fetcher.cpython-311.pyc
│   │   ├── main.cpython-311.pyc
│   │   └── notion_client.cpython-311.pyc
│   ├── config_loader.py
│   ├── file_reader.py
│   ├── imdb_url_fetcher.py
│   ├── main.py
│   └── notion_client.py
├── random
├── requirements.txt
└── tests
```

---

## ⚙️ Features

- 🔄 Converts input data (e.g. movies list) into Notion-compatible format  
- 🔐 Uses Notion API with secure token handling via config  
- 🧠 Supports basic enrichment logic (e.g., fetching IMDb links)  
- 📤 Automatically uploads data to specified Notion database  
- ✅ Ready for CI/CD integration  

---

## 🛠️ Setup Instructions

1. **Clone the Repository**

```
git clone https://github.com/SrikarManthatti/mynotionwork.git
cd mynotionwork
```

2. **Install Dependencies**

```pip install -r requirements.txt```

3. **Add Configuration**
Update the /config/basic_config.yaml with your own parent id pages

4. **Data**
Place your data inside /data folder, and update basic_config.yaml file 

5. **Run Uploader**
```python nuploaders/main.py```
or
```python3 -m nuploaders.main "creup"```
5.1. *Input Arguments*
 - Create: Only created Database in Notion
 - Update: Only updates rows in a Database
 - Creup - Creates and updates database

# Futures Enhancements:
- Caching layer before hitting OMDB or IMDB everytime
- Integrate Create and Update (when only Create is run, store the database id somewhere so it can be used)
- Accept the data files from API request?
- Also accept data columns configuration from user, instead of manually hardcoding in script
