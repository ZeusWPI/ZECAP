<script setup lang="ts">
import { ref, onMounted, watch  } from 'vue';
import { basicSetup } from "codemirror";
import { python } from "@codemirror/lang-python";
import { oneDark } from "@codemirror/theme-one-dark";
import { Codemirror } from "vue-codemirror";

const targetTime = ref<number | null>(null);
const timeLeft = ref(0);
const pythonCode = ref(""); // Stores the Python code
const API_URL = 'api/countdown/';  // Django API URL

const fetchTargetTime = async () => {
    try {
        console.log(`Fetching from: ${API_URL}get/`); // Log the URL

        const res = await fetch(`${API_URL}get/`);

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

// Watch `timeLeft`, when it reaches 0, print and clear the input field
watch(timeLeft, (newValue, oldValue) => {
    if (oldValue > 0 && newValue === 0) {
        console.log("Python Code Input at Timer End:", pythonCode.value);
        pythonCode.value = ""; // Clear input field
    }
});
</script>

<template>
    <div class="timer">
        <span>{{ String(Math.floor(timeLeft / 60)).padStart(2, '0') }}:{{ String(timeLeft % 60).padStart(2, '0') }}</span>
    </div>
    <button @click="restartCountdown(60)">Restart (60s)</button>

    <!-- Python Code Input -->
    <Codemirror
        v-model="pythonCode"
        :extensions="[basicSetup, python()]"
        :disabled="timeLeft === 0"
        :theme="oneDark"
        class="code-editor"
    />
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
