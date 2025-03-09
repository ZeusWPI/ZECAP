<script setup lang="ts">
import ProgressSpinner from 'primevue/progressspinner';
import { useTimeout } from '@vueuse/core';

const show = useTimeout(100);
</script>

<template>
    <div class="loader w-full p-3 flex justify-content-center">
        <ProgressSpinner v-if="show" class="custom-spinner" />
    </div>
</template>

<style scoped lang="scss">
.custom-spinner {
    --p-progressspinner-color-one: black; /* Set the color */
    width: 6rem;
    height: 6rem;
}
</style>
