<script setup lang="ts">
import { onUnmounted, ref } from 'vue';
import CountdownTimer from '@/components/CountdownTimer.vue';

onUnmounted(() => {
    console.log('Home component unmounted');
});

</script>

<template>
    <div>
        <CountdownTimer/>
    </div>
</template>

<style scoped>

</style>
