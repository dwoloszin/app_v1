import pickle

# Path to your .pkl file
file_path = 'data_store.pkl'

# Open the file and load the data
with open(file_path, 'rb') as file:
    data_store = pickle.load(file)

# Now, data_store contains the data stored in the .pkl file
if __name__ == "__main__":
    print(data_store)
