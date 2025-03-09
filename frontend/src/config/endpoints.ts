export const endpoints = {
    movies: {
        retrieveByName: 'https://api.themoviedb.org/3/search/movie?query=${name}&include_adult=false&language={language}&page=1',
        retrieveById: 'https://api.themoviedb.org/3/movie/{id}?language={language}',
        poster: 'https://image.tmdb.org/t/p/w500',
    }
};