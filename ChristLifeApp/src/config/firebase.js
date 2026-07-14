import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';
import { getStorage } from 'firebase/storage';

// Your real Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDgM_kBoVl0dwJkhCkD5v16uSgAyiYe3Io",
  authDomain: "christlifecrusaders-72a4f.firebaseapp.com",
  projectId: "christlifecrusaders-72a4f",
  storageBucket: "christlifecrusaders-72a4f.firebasestorage.app",
  messagingSenderId: "498059172870",
  appId: "1:498059172870:web:0b11d3dd5b888bd71b7787",
  measurementId: "G-Q6PW9Z44KE"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Export the services our app needs
export const auth = getAuth(app);
export const db = getFirestore(app);
export const storage = getStorage(app);