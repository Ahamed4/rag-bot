from app_code.utils import json_to_markdown as create_md
from app_code.chroma_db_ingest import main as ingest_data
from app_code.initialize_llm import main as initialize_llm
from paths import SOURCE_DATA_DIR
import os

def main():
    print("Welcome to the Interactive LLM Terminal!")
    print("Let us first ingest some data.")
    
    query = input("Do you want to convert a JSON file to markdown files? (y/n) [default: y]: ").strip().lower()
    if query not in ('y', 'yes', ''):
        print("\033[1;31mPlease ensure that you have required markdown files in the data directory as a data source.\033[0m")
        print("Skipping JSON to markdown conversion.")
        return
    # Query 1: JSON file name
    query1 = input("Enter the json file name to convert to markdown (or press Enter to use default): ").strip()
    if query1:
        json_path = os.path.join(SOURCE_DATA_DIR, query1)
    else:
        json_path = None  # Let function use its default

    # Query 2: Number of entries
    query2 = input("Enter number of json entries to process (or press Enter to use default): ").strip()
    if query2:
        try:
            num_entries = int(query2)
            if num_entries <= 0:
                print("Number must be positive. Using default.")
                num_entries = None
        except ValueError:
            print("Invalid number. Using default.")
            num_entries = None
    else:
        num_entries = None  # Let function use its default

    # Call function with appropriate arguments
    if json_path and num_entries:
        create_md(json_path=json_path, num_entries_to_process=num_entries)
    elif json_path:
        create_md(json_path=json_path)
    elif num_entries:
        create_md(num_entries_to_process=num_entries)
    else:
        create_md()  # Use all defaults

if __name__ == "__main__":
    main()
    ingest_data()
    print("\nData ingestion completed.")
    print("-" * 100)
    # print("\nNow, let's set up the LLM.")
    # initialize_llm()