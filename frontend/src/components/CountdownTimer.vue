<script setup lang="ts">
import { ref, onMounted } from 'vue';

const targetTime = ref<number | null>(null);
const timeLeft = ref(0);
const API_URL = 'http://localhost/countdown/';  // Django API URL

const fetchTargetTime = async () => {
    const res = await fetch(`${API_URL}get/`);
    const data = await res.json();
    targetTime.value = data.target_time;
    updateTimeLeft();
};

const updateTimeLeft = () => {
    if (targetTime.value) {
        const now = Math.floor(Date.now() / 1000);
        timeLeft.value = Math.max(targetTime.value - now, 0);
    }
};

// Fetch data when component mounts
onMounted(async () => {
    await fetchTargetTime();
    setInterval(updateTimeLeft, 1000);
});

// Restart countdown (sets new timestamp)
const restartCountdown = async (seconds: number) => {
    const newTargetTime = Math.floor(Date.now() / 1000) + seconds;
    await fetch(`${API_URL}set/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target_time: newTargetTime }),
    });
    targetTime.value = newTargetTime;
    updateTimeLeft();
};
</script>

<template>
    <div class="timer">
        <span>{{ String(Math.floor(timeLeft / 60)).padStart(2, '0') }}:{{ String(timeLeft % 60).padStart(2, '0') }}</span>
    </div>
    <button @click="restartCountdown(60)">Restart (60s)</button>
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
</style>
