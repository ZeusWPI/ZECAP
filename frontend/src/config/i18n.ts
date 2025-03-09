import AppNL from '@/assets/lang/nl.json';
import AppEN from '@/assets/lang/en.json';
import { createI18n } from 'vue-i18n';
import { useLocalStorage } from '@vueuse/core';

// Store the locale in the local storage of the browser
const localeStorage = useLocalStorage('locale', 'nl');

export const i18n = createI18n({
    locale: localeStorage.value,
    fallbackLocale: 'en',
    legacy: false,
    messages: {
        en: {
            ...AppEN,
        },
        nl: {
            ...AppNL,
        },
    },
});
