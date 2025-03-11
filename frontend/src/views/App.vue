<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Cookies from 'js-cookie';
import axios from 'axios';

const username = ref('');
const isUsernameSet = ref(false);
const sessionName = ref('');
const sessions = ref<string[]>([]); // Explicitly define sessions as an array of strings
const sessionUsers = ref<{ [key: string]: string[] }>({}); // Map of session names to usernames
const selectedSession = ref('');

function getUsername() {
  return Cookies.get('username');
}

onMounted(() => {
  const storedUsername = getUsername();
  if (storedUsername) {
    username.value = storedUsername;
    isUsernameSet.value = true;
  }
  fetchSessions();
});

async function saveUsername() {
  Cookies.set('username', username.value, { expires: 7 });
  isUsernameSet.value = true;
  await saveUsernameToDB(username.value);
}

async function saveUsernameToDB(username: string) {
  try {
    await axios.post('/api/countdown/saveUsername/', { username }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    const response = await axios.get('/api/countdown/getAllUsernames');
    console.log('All usernames:', response.data);
  } catch (error) {
    console.error('Failed to save username to the database:', error);
  }
}

async function createSession() {
  try {
    const response = await axios.post('/api/countdown/createSession/', { session_name: sessionName.value }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    console.log('Session created:', response.data);
    const sessionsResponse = await axios.get('/api/countdown/listSessions');
    console.log('All session names:', sessionsResponse.data);
  } catch (error) {
    console.error('Failed to create session:', error);
  }
}

async function fetchSessions() {
  try {
    const response = await axios.get('/api/countdown/listSessions');
    if (Array.isArray(response.data["sessions"])) {
      sessions.value = response.data["sessions"]; // Ensure it's an array
    } else {
      console.error('Unexpected response format:', response.data);
    }
    if (typeof response.data["sessionUsers"] === 'object') {
      sessionUsers.value = response.data["sessionUsers"]; // Store the map of session names to usernames
    } else {
      console.error('Unexpected response format:', response.data);
    }
  } catch (error) {
    console.error('Failed to fetch sessions:', error);
  }
}

async function joinSession() {
  try {
    const response = await axios.post('/api/countdown/joinSession/', { session_name: selectedSession.value, username: username.value }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    console.log('Joined session:', response.data);
  } catch (error) {
    console.error('Failed to join session:', error);
  }
}

async function leaveSession() {
  try {
    const currentSession = getUserSession();
    if (currentSession) {
      const response = await axios.post('/api/countdown/leaveSession/', { session_name: currentSession, username: username.value }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });
      console.log('Left session:', response.data);
      fetchSessions(); // Refresh sessions after leaving
    }
  } catch (error) {
    console.error('Failed to leave session:', error);
  }
}

function getUserSession() {
  for (const [session, users] of Object.entries(sessionUsers.value)) {
    if (users.includes(username.value)) {
      return session;
    }
  }
  return null;
}
</script>

<template>
  <div>
    <template v-if="!isUsernameSet">
      <input v-model="username" placeholder="Enter your username" />
      <button @click="saveUsername">Save Username</button>
    </template>
    <template v-else>
      <div v-if="getUserSession()">
        <p>You are already in the session: {{ getUserSession() }}</p>
        <button @click="leaveSession">Leave Session</button>
      </div>
      <div v-else>
        <div>
          <input v-model="sessionName" placeholder="Enter session name" />
          <button @click="createSession">Create Session</button>
        </div>
        <div>
          <select v-model="selectedSession">
            <option disabled value="">Select a session</option>
            <option v-for="session in sessions" :key="session" :value="session">
              {{ session }}
            </option>
          </select>
          <button @click="joinSession">Join Session</button>
        </div>
      </div>
      <RouterView />
    </template>
  </div>
</template>

<style lang="scss">
@use '@/main.scss' as *;
</style>