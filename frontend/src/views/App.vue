<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Cookies from 'js-cookie';
import axios from 'axios';

const username = ref('');
const isUsernameSet = ref(false);
const sessionName = ref('');

function getUsername() {
  return Cookies.get('username');
}

onMounted(() => {
  const storedUsername = getUsername();
  if (storedUsername) {
    username.value = storedUsername;
    isUsernameSet.value = true;
  }
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
</script>

<template>
  <div>
    <template v-if="!isUsernameSet">
      <input v-model="username" placeholder="Enter your username" />
      <button @click="saveUsername">Save Username</button>
    </template>
    <template v-else>
      <input v-model="sessionName" placeholder="Enter session name" />
      <button @click="createSession">Create Session</button>
      <RouterView />
    </template>
  </div>
</template>

<style lang="scss">
@use '@/main.scss' as *;
</style>