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
def display_record(identifier):
     for record in database:
        if record['score'] == identifier:
            print(record)
            break
def print_leaderboard():
     sorted_data = sorted(database, key=lambda x: x["score"], reverse=True)

    # Get the names and scores of the top 5 scores
     top_5_names_scores = [(item["name"], item["score"]) for item in sorted_data[:5]]
     print("---------------------LEADERBOARD--------------------")
    # Display the names and scores of the top 5 scores
     for name, score in top_5_names_scores:
        print(f"{name}: {score}")

    
def game():
   
        
    # Game setup 
    name = input('Enter name \n>>')
    words = ['apple', 'banana', 'orange', 'grape', 'mango']  # List of words for the game
    score = 0  # Player's score
    start_time = time.time()  # Start time for tracking the duration of the game
    total_time = 1 # Total duration of the game in seconds

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
        if (time.time() - start_time) < 0:
            print("Game Over")
            break
       
    #pls let me push my changes github
    #print("Game over!")
   # print("Final score:", score)
    
    create_record({'name': name, 'score': score })
   #update_record
x = read_records()
print_leaderboard()
   # for entry in x:
       # print(entry)
        # y = json.loads(str(entry))
        # print(y['name'])
   # print(read_records())
    

# print(read_records())
# print_leaderboard()
  

game()

