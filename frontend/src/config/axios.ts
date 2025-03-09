import axios from 'axios';

export const movieClient = axios.create({
    headers: {
        accept: 'application/json',
        Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3ODY2MDRhMjE4MjZiMTM3ZjJlNTFlZWViNTY3YmFlMiIsIm5iZiI6MTc0MTIwNjg2Mi4xNzYsInN1YiI6IjY3YzhiNTRlMGM2NWVlOWFiYWU3MjAwNiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.-VDJdzIH2BIjToAfPYO53aw1klGVOQUJ3sB78EcwQoY'
      }
});
