import bcrypt
import pickle
import os

USER_DATA_FILE = 'users.pkl'
BLOG_DATA_FILE = 'blogs.pkl'

# Utility functions
def load_data(filename, default_data):
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)
    return default_data

def save_data(filename, data):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

