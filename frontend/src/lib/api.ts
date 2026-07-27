import axios from "axios";

const API_BASE_URL =
    import.meta.env.VITE_API_URL ??
    "http://127.0.0.1:8000";

const api = axios.create({
    baseURL: API_BASE_URL,
    // 5 minutes — uploads, agent runs, and other long endpoints
    // (anything that isn't using the SSE stream) need headroom.
    timeout: 300000,
    headers: {
        "Content-Type": "application/json",
    },
});

// ========================================
// Attach JWT from localStorage
// ========================================

api.interceptors.request.use((config) => {
    if (typeof window !== "undefined") {
        const token = localStorage.getItem("access_token");

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
    }

    return config;
});

// ========================================
// Handle Unauthorized
// ========================================

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            if (typeof window !== "undefined") {
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");

                window.location.href = "/login";
            }
        }

        return Promise.reject(error);
    }
);

export default api;