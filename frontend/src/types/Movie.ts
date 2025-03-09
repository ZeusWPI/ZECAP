import { endpoints } from "../config/endpoints";

export interface MovieJSON {
    id: string;
    original_language: string;
    original_title: string;
    overview: string;
    popularity: number;
    poster_path: string;
    release_date: string;
    title: string;
    vote_average: number;
    vote_count: number;
}

export class Movie {
    constructor(
        public id: string = '',
        public original_language: string = '',
        public original_title: string = '',
        public overview: string = '',
        public popularity: number = 0,
        public poster_path: string = '',
        public release_date: Date = new Date(),
        public title: string = '',
        public vote_average: number = 0,
        public vote_count: number = 0,
    ) {}

    /**
     * Convert a movie object to a movie instance.
     *
     * @param movie
     */
    static fromJSON(movie: MovieJSON): Movie {
        return new Movie(
            movie.id,
            movie.original_language,
            movie.original_title,
            movie.overview,
            movie.popularity,
            endpoints.movies.poster + movie.poster_path,
            new Date(movie.release_date),
            movie.title,
            movie.vote_average,
            movie.vote_count,
        );
    }
}
