import { defineStore } from "pinia";

interface AuthUser {
  id: number;
  full_name: string;
  role: string;
}

const TOKEN_KEY = "transport_token";
const USER_KEY = "transport_user";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: null as string | null,
    user: null as AuthUser | null,
  }),

  getters: {
    isLoggedIn: (s) => !!s.token,
    role: (s) => s.user?.role ?? null,
  },

  actions: {
    setAuth(token: string, user: AuthUser) {
      this.token = token;
      this.user = user;
      if (import.meta.client) {
        localStorage.setItem(TOKEN_KEY, token);
        localStorage.setItem(USER_KEY, JSON.stringify(user));
      }
    },

    // Восстанавливаем сессию из localStorage при перезагрузке страницы
    restore() {
      if (!import.meta.client) return;
      if (this.token) return; // уже восстановлено
      const token = localStorage.getItem(TOKEN_KEY);
      const raw = localStorage.getItem(USER_KEY);
      if (token && raw) {
        try {
          this.token = token;
          this.user = JSON.parse(raw);
        } catch {
          this.logout();
        }
      }
    },

    logout() {
      this.token = null;
      this.user = null;
      if (import.meta.client) {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
      }
    },
  },
});
