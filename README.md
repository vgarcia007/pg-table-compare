# ZFA GUI Change Helper

This tool helps identify changes in the ZFA GUI by comparing columns in the database. It works seamlessly with Docker, allowing you to make modifications on the fly through mounted scripts.

## Features

- Easy setup with Docker Compose.
- Dynamically editable scripts for on-the-fly changes.
- Compare columns in the database to detect GUI changes.

---

## Getting Started

### Prerequisites

1. Docker and Docker Compose installed on your system.
2. A `.env` file with database credentials.

### Setup

1. **Create a `.env` file:**  
   Add your database credentials to the `.env` file. See the example provided below:

   ```
   DB_NAME=application
   DB_USER=##########
   DB_PASSWORD=###########
   DB_HOST=10.2.0.4
   ```


2. **Start the container:**  
   Run the following command to spin up the Docker container:

   ```
   docker compose up -d 
   ```

3. **Log in to the container:**  
   Access the container to perform further setup:

   ```
   docker exec -it db-compare bash
   ```

---

## Installation

Inside the container, install the required Python packages:

```
pip install -r requirements.txt
```

---

## Configuration

Edit the following lines in the `run.py` file to suit your requirements:

```
sql_query = "SELECT * from gfr.gfrgebaeude"  # Replace with your SQL query  
compare_key = "gfrgebaeudeid"                # Replace with your comparison key  
```

---

## Usage

Once the setup and configuration are complete, you are ready to start detecting changes in the ZFA GUI. Simply run the script in the container as needed.
```
python run.py
```