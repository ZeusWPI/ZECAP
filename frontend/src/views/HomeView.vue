<script setup lang="ts">
import { onUnmounted, ref } from 'vue';
import MovieCarousel from '@/components/MovieCarousel.vue';
import CountdownTimer from '@/components/CountdownTimer.vue';

onUnmounted(() => {
    console.log('Home component unmounted');
});

/* List with the movies names */
const movieNames = ref([]);

</script>

<template>
    <div>
        <CountdownTimer :seconds="160" />
    </div>
</template>

<style scoped>

</style>
