import sqlite3
import csv

def export_table_to_csv(db_path, table_name):
    
    csv_path = f"core/start_data/{table_name}.csv"
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Fetch all rows from the table
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        
        # Fetch column names
        column_names = [description[0] for description in cursor.description]
        
        # Write data to CSV
        with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)  # Write header
            writer.writerows(rows)        # Write data rows
            
        print(f"Data from table '{table_name}' has been exported to '{csv_path}'.")
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

# Example usage
if __name__ == "__main__":
    database_path = "db.sqlite3"       # Path to your SQLite database

    # data models
    data_models = [
        {
            "app": "clients",
            "models": [
                "ClientType",
                "ClientSubType",
                "ClientStatus",
                "ClientAMLRiskRating",
                "ClientAccountStatus",
                "Country",
            ]
        },
        {
            "app": "core",
            "models": [
                "Currency",
                "DealStatus",
            ]
        }
    ]

    for data in data_models:
        for model in data["models"]:
            export_table_to_csv(database_path, f"{data['app']}_{model.lower()}")
