import pickle
from pathlib import Path

# Define the file path where the data will be stored
DATA_STORE_FILE = Path("data_store.pkl")

def save_data_store(data_store):
    """
    Save the data_store dictionary to a file.
    """
    try:
        with open(DATA_STORE_FILE, 'wb') as f:
            pickle.dump(data_store, f)
        print("Data store successfully saved.")
    except Exception as e:
        print(f"Error saving data store: {e}")

def load_data_store():
    """
    Load the data_store dictionary from a file.
    Returns an empty dictionary if the file does not exist.
    """
    if DATA_STORE_FILE.exists():
        try:
            with open(DATA_STORE_FILE, 'rb') as f:
                data_store = pickle.load(f)
            print("Data store successfully loaded.")
            return data_store
        except Exception as e:
            print(f"Error loading data store: {e}")
            return {}
    else:
        print("Data store file not found, initializing empty data store.")
        return {}

# Optional: Automatically load data store when this module is imported
data_store = load_data_store()
