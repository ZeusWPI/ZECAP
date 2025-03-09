import { type Ref } from 'vue';
import { movieClient } from '@/config/axios';

/**
 * Get an item.
 *
 * @param endpoint
 * @param ref
 * @param fromJson
 */
export async function get<T>(
    endpoint: string,
    ref: Ref<T | null>,
    fromJson: (data: any) => T,
): Promise<void> {
    try {
        const response = await movieClient.get(endpoint);

        if (response.data !== '' && response.data !== null) {
            ref.value = fromJson(response.data);
        }
    } catch (error: any) {
        // TODO: Implement error handling
        console.error(error); // Log the error for debugging
    }
}

/**
 * Get a list of items.
 *
 * @param endpoints
 * @param ref
 * @param fromJson
 */
export async function getList<T>(
    endpoints: string[],
    ref: Ref<T[] | null>,
    fromJson: (data: any) => T,
): Promise<void> {
    try {
        const promises = endpoints.map(async (endpoint: string) => {
            const response = await movieClient.get(endpoint);

            if (response.data.results.length > 0) {
                ref.value?.push(fromJson(response.data.results[0]));
            }
        });

        await Promise.all(promises);
    } catch (error: any) {
        console.error(error); // Log the error for debugging
    }
}
