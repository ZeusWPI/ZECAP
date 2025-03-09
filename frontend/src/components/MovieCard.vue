Using this code, there is whitespace below my card that is still clickable. how to fix that the full card is the image?
<script setup lang="ts">
import { RouterLink } from 'vue-router';
import { Movie } from '@/types/Movie';

/* Component props */
defineProps<{
    movie: Movie;
}>();

</script>

<template>
    <RouterLink :to="{ name: 'movieDetail', params: { movieId: movie.id } }">
        <div class="movie-card p-1">
            <img :src="movie.poster_path" :alt="movie.original_title" class="movie-image" />
        </div>
    </RouterLink>
</template>

<style lang="scss">
.movie-card {
    width: 100%;
    height: 100%;
    overflow: hidden;
}

.movie-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block; /* Ensure the image behaves as a block element */
    border-radius: 12px; /* Match the border-radius of the card */
}
</style>