<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-800 to-slate-900 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-white/10 mb-4">
          <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-white">Регистрация</h1>
        <p class="text-slate-400 text-sm mt-1">Создание аккаунта сотрудника</p>
      </div>

      <div class="bg-white rounded-2xl p-8 shadow-2xl">
        <div class="mb-4">
          <label class="label">Полное имя</label>
          <input v-model="form.full_name" type="text" class="input-field" placeholder="Иванов Иван Иванович" />
        </div>
        <div class="mb-4">
          <label class="label">Имя пользователя</label>
          <input v-model="form.username" type="text" class="input-field" placeholder="ivanov" />
        </div>
        <div class="mb-4">
          <label class="label">Email</label>
          <input v-model="form.email" type="email" class="input-field" placeholder="ivanov@company.ru" />
        </div>
        <div class="mb-6">
          <label class="label">Пароль</label>
          <input v-model="form.password" type="password" class="input-field" placeholder="Минимум 6 символов" />
        </div>

        <!-- Роль фиксирована, скрыта от пользователя -->
        <input type="hidden" v-model="form.role" />

        <div class="bg-slate-50 rounded-xl px-4 py-3 text-sm text-slate-500 mb-6">
          Регистрация доступна только для роли <strong>Сотрудник</strong>.
          Аккаунты диспетчеров и водителей создаются администратором.
        </div>

        <p v-if="error" class="text-red-500 text-sm mb-4">{{ error }}</p>

        <button @click="submit" class="btn-primary w-full mb-4" :disabled="loading">
          {{ loading ? "Регистрация..." : "Зарегистрироваться" }}
        </button>

        <p class="text-center text-sm text-slate-500">
          Уже есть аккаунт?
          <NuxtLink to="/login" class="text-blue-600 font-medium hover:underline">Войти</NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: false });
const api = useApi();
const authStore = useAuthStore();

const form = reactive({
  full_name: "",
  username: "",
  email: "",
  password: "",
  role: "employee", // всегда employee при публичной регистрации
});

const loading = ref(false);
const error = ref("");

async function submit() {
  error.value = "";
  if (!form.full_name.trim() || !form.username.trim() || !form.email.trim() || !form.password) {
    error.value = "Заполните все поля";
    return;
  }
  if (form.password.length < 6) {
    error.value = "Пароль должен содержать минимум 6 символов";
    return;
  }
  loading.value = true;
  try {
    await api.post("/auth/register", form);
    // Автоматический вход после регистрации
    const data = await api.post("/auth/login", {
      username: form.username,
      password: form.password,
    });
    authStore.setAuth(data.access_token, {
      id: data.user_id,
      full_name: data.full_name,
      role: data.role,
    });
    navigateTo("/employee");
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}
</script>
