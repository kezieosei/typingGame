import random
import time
import json

  # File path to store the database
database_file = "leaderboard.json"

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

def game():
   
        
    # Game setup 
    name = input('Enter name \n>>')
    words = ['apple', 'banana', 'orange', 'grape', 'mango']  # List of words for the game
    score = 0  # Player's score
    start_time = time.time()  # Start time for tracking the duration of the game
    total_time = 10  # Total duration of the game in seconds

    # Game loop
    while time.time() - start_time < total_time:
        target_word = random.choice(words)  # Select a random word from the list
        print("Type the word:", target_word)
        user_input = input()

        if user_input.strip().lower() == target_word:
            score += 1
            print("Correct!")
        else:
            print("Incorrect!")

        print("Score:", score)
        print("Time remaining:", total_time - (time.time() - start_time), "seconds")

    print("Game over!")
    print("Final score:", score)
    # create_record({'name': name, 'score': score } )
    x = read_records()
    for entry in x:
        print(entry)
        # y = json.loads(str(entry))
        # print(y['name'])
    print(read_records())
    

print(read_records())
  

# game()
# 0add leaderboard
