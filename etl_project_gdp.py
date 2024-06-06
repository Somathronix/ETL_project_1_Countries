import requests
from bs4 import BeautifulSoup
import json
import sqlite3
from datetime import datetime

# Function to log messages to the log file
def log(message):
    with open("etl_project_log.txt", "a") as log_file:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp}: {message}\n"
        log_file.write(log_entry)

# URL of the webpage with GDP data
url = "https://web.archive.org/web/20230902185326/https://en.wikipedia.org/wiki/List_of_countries_by_GDP_%28nominal%29"

# Get the HTML content of the webpage
response = requests.get(url)
html_content = response.text

# Create BeautifulSoup object to parse HTML
soup = BeautifulSoup(html_content, "html.parser")

# Find the table containing GDP data
table = soup.find("table", {"class": "wikitable sortable static-row-numbers plainrowheaders srn-white-background"})
if table:
    # Create a list to store country data
    countries = []

    # Extract data from the table
    for row in table.find_all("tr")[1:]:
        columns = row.find_all("td")
        # Check if there are enough columns in the current row
        if len(columns) >= 3:
            country_name = columns[0].text.strip()  # Country name
            gdp_estimate = columns[2].text.strip()  # GDP of the country (IMF Estimate)
        
            # Skip the row for "World"
            if country_name != "World":
                countries.append({"Country": country_name, "GDP_IMF_Estimate": gdp_estimate})

    # Create a JSON file with the data
    with open("Countries_GDP_IMF_Estimates.json", "w") as json_file:
        json.dump(countries, json_file, indent=4)

    log("Data successfully extracted and saved to 'Countries_GDP_IMF_Estimates.json'.")

    # Save the data to the database
    try:
        conn = sqlite3.connect("World_Economies.db")
        cursor = conn.cursor()

        # Create the table
        cursor.execute('''CREATE TABLE IF NOT EXISTS WorldEconomies
                          (Country TEXT, GDP_USD_billion REAL)''')

        # Insert data into the table
        for country in countries:
            try:
                gdp = float(country["GDP_IMF_Estimate"].replace(",", ""))
                if gdp > 100:  # Filter by GDP > $100 billion USD
                    cursor.execute("INSERT INTO WorldEconomies VALUES (?, ?)", (country["Country"], gdp))
            except ValueError:
                pass

        conn.commit()
        conn.close()

        log("Database 'World_Economies.db' successfully created and populated.")

        # Read data from the database
        conn = sqlite3.connect("World_Economies.db")
        cursor = conn.cursor()

        # Execute query for countries with GDP > $100 billion USD
        cursor.execute("SELECT * FROM WorldEconomies WHERE GDP_USD_billion > 100")
        results = cursor.fetchall()
        print("Countries with economies exceeding $100 billion USD:")
        for row in results:
            print(row)

        conn.close()

    except sqlite3.Error as e:
        log(f"Error working with the database: {e}")

else:
    log("Table with data not found.")
