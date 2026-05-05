import { useAuthStore } from "~/stores/auth";

export function useApi() {
  const config = useRuntimeConfig();
  const auth = useAuthStore();

  async function request<T = any>(path: string, options: RequestInit = {}): Promise<T> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    };
    if (auth.token) {
      headers["Authorization"] = `Bearer ${auth.token}`;
    }

    const res = await fetch(`${config.public.apiBase}${path}`, {
      ...options,
      headers,
    });

    if (res.status === 401) {
      auth.logout();
      navigateTo("/login");
      throw new Error("Не авторизован");
    }

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Ошибка сервера" }));
      throw new Error(err.detail || "Ошибка сервера");
    }

    const ct = res.headers.get("content-type") || "";
    if (ct.includes("application/json")) return res.json();
    return res as any;
  }

  return {
    get: <T>(path: string) => request<T>(path, { method: "GET" }),
    post: <T>(path: string, body?: any) =>
      request<T>(path, { method: "POST", body: body ? JSON.stringify(body) : undefined }),
    patch: <T>(path: string, body?: any) =>
      request<T>(path, { method: "PATCH", body: body ? JSON.stringify(body) : undefined }),
    delete: <T>(path: string) => request<T>(path, { method: "DELETE" }),
    download: async (path: string) => {
      const res = await fetch(`${config.public.apiBase}${path}`, {
        headers: { Authorization: `Bearer ${auth.token}` },
      });
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "history.xlsx";
      a.click();
    },
  };
}
