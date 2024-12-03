import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from csv_diff import load_csv, compare
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.panel import Panel
import warnings


# SQL query and comparison key

#sql_query = "SELECT * from gfr.gfrgebaeude where gfrgebaeudeid = 13971"
sql_query = "SELECT * from gfr.gfrgebaeude"
compare_key = "gfrgebaeudeid"

# Suppress the specific pandas warning
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable")

# Initialize rich console
console = Console()

# Load environment variables from .env file
load_dotenv()

# Fetch database connection details from environment variables
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

# Validate environment variables
if not DB_NAME or not DB_USER or not DB_PASSWORD or not DB_HOST:
    console.print("[red]Environment variables for database credentials are missing![/red]")
    exit(1)

# File names with timestamps
file1 = "file_01.csv"
file2 = "file_02.csv"



# Database connection string
conn_str = f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST}"

def clear_screen():
    # Clear the screen based on the operating system
    if os.name == "nt":  # For Windows
        os.system("cls")
    else:  # For macOS and Linux
        os.system("clear")
        
def export_table_to_csv(query, output_file):
    try:
        # Connect to the database
        conn = psycopg2.connect(conn_str)
        console.print("[green]Connected to the database.[/green]")

        # Execute the query and fetch data
        df = pd.read_sql_query(query, conn)

        # Export to CSV
        df.to_csv(output_file, index=False)
        console.print(f"[cyan]Data exported to:[/cyan] {output_file}")

        # Close the connection
        conn.close()

    except Exception as e:
        console.print(f"[red]Error exporting data:[/red] {e}")
        console.print("[red]Please check the database connection and query.[/red]")

def compare_csv_files(file1, file2, key_column):
    # Load the CSV files
    file1_data = load_csv(open(file1), key_column)
    file2_data = load_csv(open(file2), key_column)

    # Compare the CSV files
    diff = compare(file1_data, file2_data)

    # Display added rows
    if diff["added"]:
        console.print("\n[green]Added Rows:[/green]")
        table = Table(show_header=True, header_style="bold green")
        table.add_column(key_column)
        for key, row in enumerate(diff["added"], start=1):
            table.add_row(str(key), str(row))
        console.print(table)
    else:
        console.print("\n[green]No rows were added.[/green]")

    # Display removed rows
    if diff["removed"]:
        console.print("\n[red]Removed Rows:[/red]")
        table = Table(show_header=True, header_style="bold red")
        table.add_column(key_column)
        for key, row in enumerate(diff["removed"], start=1):
            table.add_row(str(key), str(row))
        console.print(table)
    else:
        console.print("\n[green]No rows were removed.[/green]")

    # Display changed rows
    if diff["changed"]:
        console.print("\n[cyan]Changed Rows:[/cyan]")
        for change in diff["changed"]:
            key = change["key"]
            console.print(f"  [yellow]Row with key '{key}' has changes:[/yellow]")
            for column, column_diff in change["changes"].items():
                if isinstance(column_diff, list):
                    console.print(f"    [cyan]Column '{column}': Multiple changes -> {column_diff}[/cyan]")
                elif isinstance(column_diff, dict):
                    console.print(f"    [cyan]Column '{column}': {column_diff['old_value']} -> {column_diff['new_value']}[/cyan]")
    else:
        console.print("\n[green]No rows were changed.[/green]")

if __name__ == "__main__":
    
    clear_screen()
    
    # Display fancy header
    header = Panel.fit(
        Text("CSV Comparison Tool", justify="center", style="bold white on blue"),
        border_style="cyan",
    )
    console.print(header)
    
    console.print(f"Running query: [cyan]{sql_query}[/cyan]")   
    
    export_table_to_csv(sql_query, file1)
    
    console.print("[yellow]Now make your changes in the database table...[/yellow]")
    console.print("[magenta]Press Enter once you have made the changes to continue...[/magenta]", end="")
    input()

    
    export_table_to_csv(sql_query, file2)
    
    console.print(f"Comparing files on key: [green]{compare_key}[/green]")
    compare_csv_files(file1, file2, compare_key)
