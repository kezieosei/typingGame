// const admin = require('firebase-admin');
// const fs = require('fs');

// // Read the configuration file
// const config = JSON.parse(fs.readFileSync('config.json'));

// const filePath = config.firebaseServiceAccountKeyPath;

// // Check if the file exists
// if (!fs.existsSync(filePath)) {
//   console.error('The specified service account key JSON file does not exist.');
//   process.exit(1);
// }

// // Load the Firebase service account key JSON file
// const serviceAccount = require(filePath);

// // Initialize the Firebase admin SDK
// admin.initializeApp({
//   credential: admin.credential.cert(serviceAccount),
//   databaseURL: config.databaseURL
// });

// // Get a reference to the Realtime Database root node
// const db = admin.database();

// // Function to send data to the database
// function sendDataToDatabase(data) {
//   // Generate a new key for the data
//   const newKey = db.ref().push().key;

//   // Create the data object
//   const newData = {
//     [newKey]: data
//   };

//   // Save the data to the database
//   return db.ref().update(newData);
// }

// // Usage: node app.js "Data to send"
// const dataToSend = process.argv[2];

// if (!dataToSend) {
//   console.error('No data provided. Please provide the data to send as a command-line argument.');
// } else {
//   sendDataToDatabase(dataToSend)
//     .then(() => {
//       console.log('Data sent successfully to the database.');
//       process.exit(0);
//     })
//     .catch(error => {
//       console.error('Error sending data to the database:', error);
//       process.exit(1);
//     });
// }



// // Create a simple database structure
// const messagesRef = db.ref('messages');

// // Method 1: Set Data
// messagesRef.set({
//   message1: {
//     content: "Hello, World!",
//     sender: "user123"
//   },
//   message2: {
//     content: "Hi there!",
//     sender: "user456"
//   }
// });

// // Method 2: Update Data
// const message1Ref = messagesRef.child('message1');
// message1Ref.update({
//   content: "Updated message content!"
// });

// // Method 3: Push Data with Auto-generated Keys
// const usersRef = db.ref('users');
// const newUserRef = usersRef.push();
// newUserRef.set({
//   name: "John Doe",
//   email: "john@example.com"
// });
