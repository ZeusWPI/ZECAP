const API_URL = 'http://localhost:8000/api/countdown/'; // Django API-URL


const fetchTargetTime = async () => {
    try {
        const res = await fetch(`${API_URL}get/`);
        if (!res.ok) {
            const errorText = await res.text(); // Get error details from response
            throw new Error(`HTTP ${res.status}: ${errorText}`);
        }
        const data = await res.json();
        targetTime.value = data.target_time;
        updateTimeLeft();
    } catch (error) {
        console.error('Failed to fetch target time:', error.message);
        alert(`Error: ${error.message}`); // Show error in UI
    }
};

