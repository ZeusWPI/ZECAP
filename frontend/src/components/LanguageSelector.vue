<script setup lang="ts">
import { Select } from 'primevue';
import { useI18n } from 'vue-i18n';
import { onMounted } from 'vue';
import { useLocalStorage } from '@vueuse/core';
import { type PrimeVueLocaleOptions, usePrimeVue } from 'primevue/config';

/* Composables */
const { locale, availableLocales, t, messages } = useI18n();
const { config } = usePrimeVue();
const localeStorage = useLocalStorage('locale', locale.value);

/**
 * Update the locale settings when the locale changes.
 *
 * @param locale
 */
function updateLocale(locale: string): void {
    // Update saved locale
    localeStorage.value = locale;
    // Update PrimeVue locale
    config.locale = messages.value[locale].primevue as PrimeVueLocaleOptions;
}

// /**
//  * Get the flag for the given locale.
//  *
//  * @param locale
//  */
// function getFlag(locale: string): string {
//     if (locale === 'nl') {
//         return nl;
//     }

//     return en;
// }

/* Hooks */
onMounted(() => {
    updateLocale(locale.value);
});
</script>

<template>
    <Select
        id="language"
        v-model="locale"
        class="w-auto"
        :options="availableLocales"
        @change="updateLocale($event.value)"
        variant="outlined"
    >
        <template #option="{ option }">
            <div class="flex align-items-center">
                <!-- <img :alt="t('layout.header.language.' + option)" :src="getFlag(option)" class="h-1rem mr-2" /> -->
                <span>{{ t('language.mapping.' + option) }}</span>
            </div>
        </template>
        <template #value="{ value }">
            <div class="h-full flex justify-content-center align-items-center">
                <div class="uppercase text-sm">{{ value }}</div>
            </div>
        </template>
    </Select>
</template>

<style scoped lang="scss"></style>
