
# Database Change Detector

This Python tool helps you see changes in a database table. It exports the contents of a table to CSV twice (before/after) and shows the differences (added, removed, and changed rows).

## Usage

1. Create a `.env` file with your database credentials (see `.env-example`).
2. Adjust the SQL query (`sql_query`) and comparison key (`compare_key`) in `run.py`.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the script:
   ```bash
   python run.py
   ```
5. Follow the instructions in the terminal.

The CSV files will be saved as `file_01.csv` and `file_02.csv` and compared automatically.

**Notes:**
- Only supports PostgreSQL.
- Never commit your `.env` file to the repository!