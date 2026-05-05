<template>
  <div class="min-h-screen bg-gradient-to-br from-brand-900 via-brand-800 to-slate-950 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-white">Регистрация</h1>
        <p class="text-brand-200 text-sm mt-1">Создайте аккаунт</p>
      </div>
      <div class="bg-white rounded-2xl p-8 shadow-2xl">
        <form @submit.prevent="handleRegister">
          <div class="mb-4">
            <label class="label">ФИО</label>
            <input v-model="form.full_name" type="text" class="input-field" placeholder="Иванов Иван Иванович" required />
          </div>
          <div class="mb-4">
            <label class="label">Имя пользователя</label>
            <input v-model="form.username" type="text" class="input-field" placeholder="ivanov" required />
          </div>
          <div class="mb-4">
            <label class="label">Email</label>
            <input v-model="form.email" type="email" class="input-field" placeholder="ivanov@company.ru" required />
          </div>
          <div class="mb-4">
            <label class="label">Пароль</label>
            <input v-model="form.password" type="password" class="input-field" required />
          </div>
          <div class="mb-6">
            <label class="label">Роль</label>
            <select v-model="form.role" class="input-field">
              <option value="employee">Сотрудник</option>
              <option value="dispatcher">Диспетчер</option>
              <option value="driver">Водитель</option>
            </select>
          </div>
          <p v-if="error" class="text-red-500 text-sm mb-4">{{ error }}</p>
          <button type="submit" class="btn-primary w-full" :disabled="loading">
            {{ loading ? "Регистрация..." : "Зарегистрироваться" }}
          </button>
        </form>
        <p class="text-center text-sm text-slate-500 mt-5">
          Уже есть аккаунт?
          <NuxtLink to="/login" class="text-brand-500 font-semibold hover:underline">Войти</NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false });
const config = useRuntimeConfig();
const form = reactive({ username: "", email: "", password: "", full_name: "", role: "employee" });
const loading = ref(false);
const error = ref("");

async function handleRegister() {
  loading.value = true;
  error.value = "";
  try {
    const res = await fetch(`${config.public.apiBase}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    if (!res.ok) {
      const e = await res.json();
      throw new Error(e.detail || "Ошибка регистрации");
    }
    navigateTo("/login");
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}
</script>
