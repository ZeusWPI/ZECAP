<script setup lang="ts">
import { ref } from 'vue';
import { onMounted } from 'vue';
import  Carousel from 'primevue/carousel';
import { useMovie } from '@/composables/services/movie.service.ts';
import { defineProps } from 'vue';
import Loading from '@/components/Loading.vue';
import MovieCard from './MovieCard.vue';

/* Props */
const props = defineProps<{
    movieNames: string[];
}>();

const { movies, getMoviesByName } = useMovie();

/* State of component */
const loading = ref(true);

/* Fetch posters when the component mounts */
onMounted(async () => {
    loading.value = true;
    await getMoviesByName(props.movieNames);
    loading.value = false;
    console.log(movies.value);
});

/* Responsive options of the carousel */
const responsiveOptions = ref([
  { breakpoint: '1024px', numVisible: 3, numScroll: 3 },
  { breakpoint: '768px', numVisible: 2, numScroll: 2 },
  { breakpoint: '560px', numVisible: 1, numScroll: 1 }
]);
</script>

<template>
  <div>
    <template v-if="!loading">
        <Carousel :value="movies" :numVisible="7" :numScroll="7" :responsiveOptions="responsiveOptions" :show-indicators="false">
            <template #item="slotProps">
                <MovieCard :movie="slotProps.data" />
            </template>
        </Carousel>
    </template>
    <template v-else>
        <Loading />
    </template>
  </div>
</template>

<style scoped>

</style>
