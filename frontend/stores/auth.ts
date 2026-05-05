import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: null as string | null,
    role: null as string | null,
    userId: null as number | null,
    fullName: null as string | null,
  }),
  getters: {
    isLoggedIn: (s) => !!s.token,
    isEmployee: (s) => s.role === "employee",
    isDispatcher: (s) => s.role === "dispatcher",
    isDriver: (s) => s.role === "driver",
  },
  actions: {
    setAuth(data: { access_token: string; role: string; user_id: number; full_name: string }) {
      this.token = data.access_token;
      this.role = data.role;
      this.userId = data.user_id;
      this.fullName = data.full_name;
      if (process.client) {
        localStorage.setItem("auth", JSON.stringify({ token: this.token, role: this.role, userId: this.userId, fullName: this.fullName }));
      }
    },
    logout() {
      this.token = null;
      this.role = null;
      this.userId = null;
      this.fullName = null;
      if (process.client) localStorage.removeItem("auth");
    },
    restore() {
      if (process.client) {
        const raw = localStorage.getItem("auth");
        if (raw) {
          const d = JSON.parse(raw);
          this.token = d.token;
          this.role = d.role;
          this.userId = d.userId;
          this.fullName = d.fullName;
        }
      }
    },
  },
});
