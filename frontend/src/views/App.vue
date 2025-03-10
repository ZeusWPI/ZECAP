<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Cookies from 'js-cookie';

const username = ref('');
const isUsernameSet = ref(false);

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

function saveUsername() {
  Cookies.set('username', username.value, { expires: 7 });
  isUsernameSet.value = true;
}
</script>

<template>
  <div>
    <template v-if="!isUsernameSet">
      <input v-model="username" placeholder="Enter your username" />
      <button @click="saveUsername">Save Username</button>
    </template>
    <template v-else>
      <RouterView />
    </template>
  </div>
</template>

<style lang="scss">
@use '@/main.scss' as *;
</style>