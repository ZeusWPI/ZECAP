const API_URL = 'http://127.0.0.1:8000/countdown/';  // Django API URL

const fetchTargetTime = async () => {
    try {
        const res = await fetch(`${API_URL}get/`);
        if (!res.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await res.json();
        targetTime.value = data.target_time;
        updateTimeLeft();
    } catch (error) {
        console.error('Failed to fetch target time:', error);
    }
};
