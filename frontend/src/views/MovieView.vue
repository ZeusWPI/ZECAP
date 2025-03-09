<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useMovie } from '@/composables/services/movie.service';
import { useI18n } from 'vue-i18n';
import Button from 'primevue/button';
import Tag from 'primevue/tag';
import Loading from '@/components/Loading.vue';
import LanguageSelector from '@/components/LanguageSelector.vue';

/* Reactive movie data */
const { params } = useRoute();
const { movie, getMovieById } = useMovie();
const { t, locale } = useI18n();

/* State of component */
const loading = ref(true);

/* Fetch movie data */
const fetchMovie = async () => {
    loading.value = true;
    await getMovieById(params.movieId as string);
    loading.value = false;
    console.log(movie.value);
};

/* Fetch movie data when the component mounts */
onMounted(fetchMovie);

/* Watch for locale changes and refetch movie data */
watch(locale, fetchMovie);

</script>

<template>
    <div class="movie-detail-container" v-if="!loading && movie">
        <div class="movie-content">
            <!-- Movie Poster -->
            <img :src="movie.poster_path" :alt="movie.title" class="movie-poster" />

            <!-- Movie Details -->
            <div class="movie-info">
                <h1 class="movie-title">{{ movie.title }}</h1>
                
                <div class="movie-meta">
                    <span class="release-date">
                        📅 {{ new Intl.DateTimeFormat(locale, { dateStyle: 'long' }).format(movie.release_date) }}
                    </span>                    
                    <Tag :value="movie.original_language.toUpperCase()" severity="info" />
                </div>

                <div class="rating">
                    <p class="vote-average">⭐ {{ movie.vote_average.toFixed(1) }} / 10</p>
                    <p class="vote-count">({{ movie.vote_count + ' ' + t('views.movieDetail.votes')}} )</p>
                </div>

                <p class="overview">{{ movie.overview }}</p>

                <Button :label="t('views.movieDetail.goBack')" icon="pi pi-arrow-left" class="p-button-secondary" @click="$router.push('/')"/>
            </div>
        </div>
    </div>
    <template v-else>
        <Loading />
    </template >
</template>

<style scoped>
.movie-detail-container {
    max-width: 900px;
    margin: 40px auto;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.movie-content {
    display: flex;
    flex-direction: row;
    gap: 20px;
}

.movie-poster {
    width: 300px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.movie-info {
    flex-grow: 1;
}

.movie-title {
    font-size: 28px;
    font-weight: bold;
}

.movie-meta {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 10px 0;
}

.vote-average {
    font-size: 20px;
    font-weight: bold;
}

.vote-count {
    font-size: 14px;
    color: gray;
}

.overview {
    margin-top: 20px;
    font-size: 16px;
    line-height: 1.5;
}

.rating {
    display: flex;
    align-items: center;
    gap: 8px;
    margin: 10px 0;
}
</style>