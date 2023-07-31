import os
import random
import sys
import time
import json
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



# Read the configuration file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Get the file path to the service account key
file_path = config["firebaseServiceAccountKeyPath"]

# Check if the file exists
if not os.path.exists(file_path):
    print('The specified service account key JSON file does not exist.')
    exit(1)

# Initialize the Firebase app with the service account key
cred = credentials.Certificate(file_path)
firebase_admin.initialize_app(cred, {
    'databaseURL': config["databaseURL"]
})

# Reference to the root of your Firebase Realtime Database
root = db.reference()

# Get a reference to the "leaderboard" node
leaderboard_ref = root.child('leaderboard')

database_file = 'C:/Users/dwwil/OneDrive/Documents/VSCode/Tutor/typingGame/test.json'
# Load the database from the file if it exists, or initialize an empty database
try:
    with open(database_file, "r") as file:
        database = json.load(file)
except FileNotFoundError:
    database = []

def save_database():
    # Save the database to the file
    with open(database_file, "w") as file:
        json.dump(database, file)
        
def create_record(record):
    database.append(record)
    save_database()

def read_records(field=None, value=None):
    if field and value:
        return [record for record in database if record.get(field) == value]
    else:
        return database

def update_record(record_id, updates):
    for record in database:
        if record['id'] == record_id:
            record.update(updates)
            save_database()
            break

def delete_record(record_id):
    for record in database:
        if record['id'] == record_id:
            database.remove(record)
            save_database()
            break
def display_record(identifier):
     for record in database:
        if record['score'] == identifier:
            print(record)
            break
def print_leaderboard():  # deprecated - used locally for testing
     sorted_data = sorted(database, key=lambda x: x["score"], reverse=True)

    # Get the names and scores of the top 5 scores
     top_5_names_scores = [(item["name"], item["score"]) for item in sorted_data[:5]]
     print("---------------------LEADERBOARD--------------------")
    # Display the names and scores of the top 5 scores
     for name, score in top_5_names_scores:
        print(f"{name}: {score}")

def add_leaderboard_entry(name, score):
    leaderboard_ref = root.child('board')
    new_entry_ref = leaderboard_ref.push()
    new_entry_ref.set({
        'name': name,
        'score': score
    })
    
def display_leaderboard():
    print("\n---------------------LEADERBOARD--------------------")
    leaderboard_ref = root.child('board')
    leaderboard = leaderboard_ref.order_by_child('score').limit_to_last(10).get()
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]['score'], reverse=True)
    
    # print("Leaderboard:")
    for idx, (key, value) in enumerate(sorted_leaderboard, start=1):
        print(f"{idx}. {value['name']}: {value['score']}")

    
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')  
      
# Set up the terminal refresh interval
REFRESH_INTERVAL = 0.0001  # Adjust this value as needed


# Define the API URL
WORDS_API_URL = 'https://random-word-api.vercel.app/api?words=100'

def get_random_words():
    try:
        response = requests.get(WORDS_API_URL)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        # Parse the response as JSON
        data = response.json()
        return data  # Return the list of random words

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching random words: {e}")
        return []  # Return an empty list in case of an error



def game():
   
        
    # Game setup 
    name = input('Enter name \n>>')
    words = get_random_words()  # List of words for the game
    score = 0  # Player's score
    incorrect = 0
    start_time = time.time()  # Start time for tracking the duration of the game
    total_time = 30 # Total duration of the game in seconds
    messages = [] # List of messages

    # Game loop
    while time.time() - start_time < total_time:
        clear_screen()

        if messages:
            sys.stdout.write("\n".join(messages) + "\n")
            sys.stdout.flush()

        target_word = random.choice(words)  # Select a random word from the list
        sys.stdout.write("Type the word: " + target_word + "\n")
        sys.stdout.flush()

        user_input = input()

        if user_input.strip().lower() == target_word:
            score += 1
            sys.stdout.write("Correct!\n")
            sys.stdout.flush()
        else:
            incorrect += 1
            sys.stdout.write("Incorrect!\n")
            sys.stdout.flush()

        messages = [
            f'Score: {score}',
            f'Time remaining: {total_time - (time.time() - start_time):.2f} seconds'
        ]
        time.sleep(REFRESH_INTERVAL)
        if incorrect == 0:
            sys.stdout.write("\nGame Over\n                P E R F E C T   G A M E\n")
            sys.stdout.flush()
        else:
            sys.stdout.write("\nGame Over")
            sys.stdout.flush()
        
       

    create_record({'name': name, 'score': score })
    add_leaderboard_entry(name, score)
    display_leaderboard()
    again = input("Play Again? (y/n): \n>>")
    if again == 'y':
        game()
    else:
        print("Thank you for playing!")
        time.sleep(.7)
        print("<3")
    
game()
display_leaderboard()


