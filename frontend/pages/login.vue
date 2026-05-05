<template>
  <div class="min-h-screen bg-gradient-to-br from-brand-900 via-brand-800 to-slate-950 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-white/10 rounded-2xl mb-4">
          <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-white">Диспетчеризация транспорта</h1>
        <p class="text-brand-200 text-sm mt-1">Войдите в систему</p>
      </div>

      <!-- Form -->
      <div class="bg-white rounded-2xl p-8 shadow-2xl">
        <form @submit.prevent="handleLogin">
          <div class="mb-5">
            <label class="label">Имя пользователя</label>
            <input v-model="form.username" type="text" class="input-field" placeholder="username" required />
          </div>
          <div class="mb-6">
            <label class="label">Пароль</label>
            <input v-model="form.password" type="password" class="input-field" placeholder="••••••••" required />
          </div>
          <p v-if="error" class="text-red-500 text-sm mb-4">{{ error }}</p>
          <button type="submit" class="btn-primary w-full" :disabled="loading">
            {{ loading ? "Вход..." : "Войти" }}
          </button>
        </form>
        <p class="text-center text-sm text-slate-500 mt-5">
          Нет аккаунта?
          <NuxtLink to="/register" class="text-brand-500 font-semibold hover:underline">Зарегистрироваться</NuxtLink>
        </p>

        <!-- Demo hints -->
        <div class="mt-6 pt-5 border-t border-slate-100">
          <p class="text-xs text-slate-400 mb-2 font-semibold uppercase tracking-wide">Демо-аккаунты (пароль: admin123)</p>
          <div class="grid grid-cols-3 gap-2 text-xs">
            <button @click="fillDemo('dispatcher')" class="bg-slate-50 hover:bg-slate-100 rounded-lg p-2 text-center transition-colors">
              <div class="font-semibold text-slate-700">dispatcher</div>
              <div class="text-slate-400">Диспетчер</div>
            </button>
            <button @click="fillDemo('employee1')" class="bg-slate-50 hover:bg-slate-100 rounded-lg p-2 text-center transition-colors">
              <div class="font-semibold text-slate-700">employee1</div>
              <div class="text-slate-400">Сотрудник</div>
            </button>
            <button @click="fillDemo('driver1')" class="bg-slate-50 hover:bg-slate-100 rounded-lg p-2 text-center transition-colors">
              <div class="font-semibold text-slate-700">driver1</div>
              <div class="text-slate-400">Водитель</div>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "~/stores/auth";

definePageMeta({ layout: false });

const auth = useAuthStore();
const config = useRuntimeConfig();

const form = reactive({ username: "", password: "" });
const loading = ref(false);
const error = ref("");

function fillDemo(username: string) {
  form.username = username;
  form.password = "admin123";
}

async function handleLogin() {
  loading.value = true;
  error.value = "";
  try {
    const res = await fetch(`${config.public.apiBase}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    if (!res.ok) {
      const e = await res.json();
      throw new Error(e.detail || "Ошибка входа");
    }
    const data = await res.json();
    auth.setAuth(data);
    navigateTo(`/${data.role}`);
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}
</script>
