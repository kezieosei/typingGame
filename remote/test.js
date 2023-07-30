const admin = require('firebase-admin');
const fs = require('fs');

// Read the configuration file
const config = JSON.parse(fs.readFileSync('config.json'));

const filePath = config.firebaseServiceAccountKeyPath;

// Check if the file exists
if (!fs.existsSync(filePath)) {
  console.error('The specified service account key JSON file does not exist.');
  process.exit(1);
}

// Load the Firebase service account key JSON file
const serviceAccount = require(filePath);

// Initialize the Firebase admin SDK
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: config.databaseURL
});

// Get a reference to the Realtime Database root node
const db = admin.database();


const leaderboardRef = db.ref('leaderboard');

// Function to add a user's score to the leaderboard
function addUserToLeaderboard(username, score) {
  // Create a new unique key for the user
  const newUserRef = leaderboardRef.push();
  
  // Set the data for the new user entry
  newUserRef.set({
    username: username,
    score: score
  });
}

// Function to get the leaderboard data (Top N scores)
// Function to get the leaderboard data as an object (username as key, score as value)
// Function to get the leaderboard data in descending order (highest score at the top)
function getLeaderboard(topN) {
  // Query the leaderboard node to get the top N scores
  leaderboardRef.orderByChild('score').limitToLast(topN).once('value')
  .then((snapshot) => {
    // The snapshot contains the leaderboard data for the top N scores
    const leaderboardData = {};
    
    snapshot.forEach((childSnapshot) => {
      const key = childSnapshot.key;
      const { username, score } = childSnapshot.val();
      leaderboardData[username] = score;
    });
    
    // Sort the leaderboard data in descending order by score
    const sortedLeaderboard = Object.fromEntries(
      Object.entries(leaderboardData).sort((a, b) => b[1] - a[1])
      );
      
      // Process the sorted leaderboard data as needed
      console.log(sortedLeaderboard);
    })
    .catch((error) => {
      console.error('Error getting leaderboard data:', error);
    });
  }
  
  // Function to fetch random words from the API
  const readline = require('readline');
  const fetch = require('node-fetch');
  
  let words = [];
  let timer;
  let startTime;
  let remainingSeconds = 60;
  let correctCount = 0;
  let incorrectCount = 0;
  
  // creating a function to get random words  TODO: specify the word length
  async function fetchRandomWords() {
    const apiUrl = 'https://random-word-api.vercel.app/api?words=10';
  
    try {
      const response = await fetch(apiUrl);
  
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
  
      const data = await response.json();
  
      return data;
    } catch (error) {
      console.error('Error fetching data:', error);
      return []; // Return an empty array in case of an error
    }
  }
  // Main function - 
  async function startGame() {
    correctCount = 0;
    incorrectCount = 0;
  
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
  
    rl.question("Enter your name: ", async (name) => {
      name = name.trim();
  
      if (name === "") {
        console.log("Please enter your name.");
        rl.close();
        return;
      }
  
      console.log("Welcome to the Word Typing Game!");
      console.log(`Hello, ${name}!`);
      console.log("You have 60 seconds to type a word each time.");
  
      // Fetch random words from the API
      words = await fetchRandomWords();
  
      // Start the timer
      startTime = Date.now();
      startTimer();
  
      // Prompt the user to type a word
      getRandomWord(rl, name);
    });
  }
  
  function startTimer() {
    timer = setInterval(() => {
      const currentTime = Date.now();
      const elapsedSeconds = Math.floor((currentTime - startTime) / 1000);
      remainingSeconds = 60 - elapsedSeconds;
  
      if (remainingSeconds <= 0) {
        clearInterval(timer);
        console.log("Time's up!");
        showScore();
        process.exit(0);
      }
    }, 1000);
  }
  
  async function getRandomWord(rl, name) {
    const randomIndex = Math.floor(Math.random() * words.length);
    const word = words[randomIndex];
  
    rl.question(`Time remaining: ${remainingSeconds} seconds\nType: ${word}\n`, async (userInput) => {
      if (userInput.trim().toLowerCase() === word) {
        console.log("Correct!");
        correctCount++;
      } else {
        console.log("Wrong!");
        incorrectCount++;
      }
  
      words.splice(randomIndex, 1);
  
      if (words.length === 0) {
        clearInterval(timer);
        showScore(name);
        process.exit(0);
      }
  
      getRandomWord(rl, name);
    });
  }
  // Display score and add to Realtime Firebase Database
  function showScore(name) {
    const score = correctCount;
    console.log(`Game over, ${name}!`);
    console.log(`Your score is: ${score}`);
    addUserToLeaderboard(name, score);
  }
  
  startGame();
  


  
  
  
  
  
  
  
  // Example usage:
  // Add user scores to the leaderboard
  // addUserToLeaderboard('User1', 100);
  // addUserToLeaderboard('User2', 150);
  // addUserToLeaderboard('User3', 80);
  
  // // Get the top 5 scores from the leaderboard
  // getLeaderboard(5);
  
  
  
  