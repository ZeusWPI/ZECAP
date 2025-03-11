<script setup lang="ts">
import { ref, onMounted, watch  } from 'vue';
import { basicSetup } from "codemirror";
import { python } from "@codemirror/lang-python";
import { oneDark } from "@codemirror/theme-one-dark";
import { Codemirror } from "vue-codemirror";
import Cookies from 'js-cookie';
import axios from 'axios';

const targetTime = ref<number | null>(null);
const timeLeft = ref(0);
const pythonCode = ref(""); // Stores the Python code
const API_URL = 'api/countdown/';  // Django API URL
const timeOptions = ref([30, 60, 90, 120]); // Time options in seconds
const selectedTime = ref(timeOptions.value[1]); // Default to 60 seconds
const sessionUsers = ref<{ [key: string]: string[] }>({}); // Map of session names to usernames


const username = ref('');

function getUsername() {
  return Cookies.get('username');
}

onMounted(() => {
  const storedUsername = getUsername();
  if (storedUsername) {
    username.value = storedUsername;
  }
  setInterval(fetchTargetTime, 1000);
  setInterval(fetchSessions, 1000);
  setInterval(updateTimeLeft, 1000);
});

async function fetchSessions() {
  try {
    const response = await axios.get('/api/countdown/listSessions');
    if (typeof response.data["sessionUsers"] === 'object') {
      sessionUsers.value = response.data["sessionUsers"]; // Store the map of session names to usernames
    } else {
      console.error('Unexpected response format:', response.data);
    }
  } catch (error) {
    console.error('Failed to fetch sessions:', error);
  }
}

const fetchTargetTime = async () => {
    try {
        console.log(`Fetching from: ${API_URL}get/`); // Log the URL

        const res = await fetch(`${API_URL}get/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_name: getUserSession() }) // Include session_name in the body
        });

        if (!res.ok) {
            const errorText = await res.text(); // Read response in case of errors
            throw new Error(`HTTP ${res.status}: ${errorText}`);
        }

        const data = await res.json();
        // console.log('Received data:', data); // Log the response data

        targetTime.value = data.target_time;
        updateTimeLeft();
    } catch (error: any) {
        console.error('Failed to fetch target time:', error);
        alert(`Error fetching target time: ${error.message}`); // Display error in UI
    }
};


const updateTimeLeft = () => {
    if (targetTime.value) {
        const now = Math.floor(Date.now() / 1000);
        timeLeft.value = Math.max(targetTime.value - now, 0);
    }
};

// Restart countdown (sets new timestamp)
const restartCountdown = async (seconds: number) => {
    await fetch(`${API_URL}startSession/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({session_name: getUserSession()}),
    });
    const newTargetTime = Math.floor(Date.now() / 1000) + seconds;
    await fetch(`${API_URL}set/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_time: newTargetTime, session_name: getUserSession()}),
    });
    targetTime.value = newTargetTime;
    updateTimeLeft();
};

// Watch `timeLeft`, when it reaches 0, print and clear the input field
watch(timeLeft, (newValue, oldValue) => {
    if (oldValue > 0 && newValue === 0) {
        console.log("Python Code Input at Timer End:", pythonCode.value);
        
        // Send the Python code to the server
        axios.post(`${API_URL}submitAnswer/`, {
            session_name: getUserSession(),
            user_name: username.value,
            code: pythonCode.value
        })
        .then(response => {
            console.log('Code submitted successfully:', response.data);
        })
        .catch(error => {
            if (error.response) {
                // Server responded with a status other than 200 range
                console.error('Failed to submit code:', error.response.data);
                console.error('Status:', error.response.status);
                console.error('Headers:', error.response.headers);
            } else if (error.request) {
                // Request was made but no response received
                console.error('No response received:', error.request);
            } else {
                // Something else happened while setting up the request
                console.error('Error setting up request:', error.message);
            }
        });

        pythonCode.value = ""; // Clear input field
    }
});

// Function to format the time in MM:SS format
const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = time % 60;
    return `${String(minutes).padStart(2, '0')}m:${String(seconds).padStart(2, '0')}s`;
};


function checkUserSessionStatus() {
  for (const [session, users] of Object.entries(sessionUsers.value)) {
    if (users.includes(username.value)) {
      return users[0] === username.value;
    }
  }
  return 0;
}

function getUserSession() {
  for (const [session, users] of Object.entries(sessionUsers.value)) {
    if (users.includes(username.value)) {
      return session;
    }
  }
  return 0;
}
</script>

<template>
    <div>
        <p>Welcome, {{ username }}!</p>
        <div class="timer">
            <span>{{ String(Math.floor(timeLeft / 60)).padStart(2, '0') }}:{{ String(timeLeft % 60).padStart(2, '0') }}</span>
        </div>

        <!-- Conditionally show the time selection and restart button -->
        <div v-if="checkUserSessionStatus()">
            <select id="time-select" v-model="selectedTime">
                <option v-for="time in timeOptions" :key="time" :value="time">
                    {{ formatTime(time) }}
                </option>
            </select>
            <div v-if="timeLeft === 0">
                <button @click="restartCountdown(selectedTime)">Start Round ({{ formatTime(selectedTime) }})</button>
            </div>
        </div>

        <!-- Python Code Input -->
        <Codemirror
            v-model="pythonCode"
            :extensions="[basicSetup, python()]"
            :disabled="timeLeft === 0"
            :theme="oneDark"
            class="code-editor"
        />
    </div>
</template>

<style scoped>
.timer {
    font-size: 3rem;
    font-family: 'Courier New', Courier, monospace;
    color: red;
    text-shadow: 0 0 10px red, 0 0 20px rgba(255, 0, 0, 0.8);
    background: black;
    padding: 10px 20px;
    border-radius: 10px;
    display: inline-block;
    border: 2px solid red;
    margin-bottom: 20px; /* Add spacing below the timer */
}

button {
    padding: 10px;
    font-size: 1.2rem;
    background-color: red;
    color: white;
    border: none;
    cursor: pointer;
}

.code-editor {
    width: 100%;
    height: 200px;
    border-radius: 5px;
}


</style>
