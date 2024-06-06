# ETL_project_1_Countries

This Python script extracts GDP (Gross Domestic Product) data from a Wikipedia webpage, transforms it into a usable format, and loads it into both a JSON file and a SQLite database. Here's what the script does:

1. **Data Extraction:**
   - The script fetches HTML content from a Wikipedia page containing a table of GDP data.
   - It parses the HTML content using BeautifulSoup to extract the necessary information.

2. **Data Transformation:**
   - After extracting the data, the script processes it to remove unnecessary elements and format it correctly.
   - It filters out the row for the "World" economy and converts GDP values from strings to floating-point numbers.

3. **Data Loading:**
   - The transformed data is stored in a JSON file named "Countries_GDP_IMF_Estimates.json" for further analysis.
   - The script creates a SQLite database named "World_Economies.db" and populates it with the extracted GDP data.
   - Within the database, a table named "WorldEconomies" is created to store country names and their respective GDP values.

4. **Logging:**
   - The script logs each step of the process, including successful data extraction, database creation, and any encountered errors, to a log file named "etl_project_log.txt".

5. **Data Querying:**
   - Finally, the script executes a query on the database to retrieve countries with GDP values exceeding $100 billion USD and prints the results.

This script demonstrates a basic ETL (Extract, Transform, Load) process for handling web data and storing it in both JSON and database formats.
