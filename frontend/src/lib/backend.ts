const API_BASE = "http://127.0.0.1:8000";

const isBrowser = typeof window !== "undefined";

class BackendAPI {
    private token: string | null = isBrowser
        ? localStorage.getItem("access_token")
        : null;

    getToken() {
        return this.token;
    }

    setToken(token: string | null) {
        this.token = token;

        if (!isBrowser) return;

        if (token) {
            localStorage.setItem("access_token", token);
        } else {
            localStorage.removeItem("access_token");
        }
    }

    private getRefreshToken() {
        if (!isBrowser) return null;
        return localStorage.getItem("refresh_token");
    }

    private setRefreshToken(token: string | null) {
        if (!isBrowser) return;

        if (token) {
            localStorage.setItem("refresh_token", token);
        } else {
            localStorage.removeItem("refresh_token");
        }
    }

    private async request(endpoint: string, options: RequestInit = {}) {
        const headers = new Headers(options.headers);

        headers.set("Content-Type", "application/json");

        if (this.token) {
            headers.set("Authorization", `Bearer ${this.token}`);
        }

        const response = await fetch(`${API_BASE}${endpoint}`, {
            ...options,
            headers,
        });

        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(data.detail || data.message || "Request failed");
        }

        return data;
    }

    async login(email: string, password: string) {
        const response = await this.request("/api/auth/login", {
            method: "POST",
            body: JSON.stringify({
                email,
                password,
            }),
        });

        const auth = response.data;

        this.setToken(auth.access_token);
        this.setRefreshToken(auth.refresh_token);

        return auth;
    }

    async register(email: string, password: string) {
        return await this.request("/api/auth/register", {
            method: "POST",
            body: JSON.stringify({
                email,
                password,
            }),
        });
    }

    async me() {
        return await this.request("/api/auth/me");
    }

    async logout() {
        try {
            await this.request("/api/auth/logout", {
                method: "POST",
            });
        } catch {
            // Ignore logout errors
        }

        this.setToken(null);
        this.setRefreshToken(null);
    }

    async refresh() {
        const refreshToken = this.getRefreshToken();

        if (!refreshToken) {
            throw new Error("No refresh token found");
        }

        const response = await this.request("/api/auth/refresh", {
            method: "POST",
            body: JSON.stringify({
                refresh_token: refreshToken,
            }),
        });

        const auth = response.data;

        this.setToken(auth.access_token);
        this.setRefreshToken(auth.refresh_token);

        return auth;
    }
}

export const backend = new BackendAPI();