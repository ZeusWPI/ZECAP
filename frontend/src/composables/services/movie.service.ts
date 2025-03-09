import { computed, ref, type Ref } from 'vue';
import { Movie } from '@/types/Movie';
import { endpoints } from '@/config/endpoints.ts';
import { get, getList } from './helpers.ts';
import { useI18n } from 'vue-i18n';

interface MovieState {
    movie: Ref<Movie | null>;
    movies: Ref<Movie[] | null>;
    getMovieByName: (name: string) => Promise<void>;
    getMoviesByName: (names: string[]) => Promise<void>;
    getMovieById: (id: string) => Promise<void>;
}

export function useMovie(): MovieState {
    /* State */
    const movie = ref<Movie | null>(null);
    const movies = ref<Movie[] | null>([]);

    /* Get current language */
    const { locale } = useI18n();

    async function getMovieByName(name: string): Promise<void> {
        const endpoint = endpoints.movies.retrieveByName.replace('{name}', name).replace('{language}', locale.value);
        await get<Movie>(endpoint, movie, Movie.fromJSON);
    }

    async function getMovieById(id: string): Promise<void> {
        const endpoint = endpoints.movies.retrieveById.replace('{id}', id).replace('{language}', locale.value);
        await get<Movie>(endpoint, movie, Movie.fromJSON);
    }

    async function getMoviesByName(names: string[]): Promise<void> {
       const listEndpoints = names.map((name: string) => {
              return endpoints.movies.retrieveByName.replace('{name}', name).replace('{language}', locale.value);
        });
        await getList<Movie>(listEndpoints, movies, Movie.fromJSON);
    }

    return {
        movie,
        movies,
        getMovieByName,
        getMoviesByName,
        getMovieById,
    };
}