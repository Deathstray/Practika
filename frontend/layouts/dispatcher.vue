<template>
  <div class="min-h-screen bg-slate-50">

    <!-- Фиксированный навбар сверху -->
    <header class="fixed top-0 left-0 right-0 z-40 bg-white border-b border-slate-200 shadow-sm">
      <div class="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between gap-6">

        <!-- Логотип -->
        <div class="flex items-center gap-2 flex-shrink-0">
          <div class="w-7 h-7 rounded-lg bg-blue-600 flex items-center justify-center text-white">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/>
            </svg>
          </div>
          <span class="font-bold text-slate-800 text-sm hidden sm:block">Диспетчеризация транспорта</span>
        </div>

        <!-- Навигация -->
        <nav class="flex items-center gap-1 flex-1 overflow-x-auto">
          <NuxtLink to="/dispatcher" class="nav-link" :class="{ active: $route.path === '/dispatcher' }">
            Дашборд
          </NuxtLink>
          <NuxtLink to="/dispatcher/orders" class="nav-link"
            :class="{ active: $route.path.startsWith('/dispatcher/orders') }">
            Заявки
          </NuxtLink>
          <NuxtLink to="/dispatcher/history" class="nav-link"
            :class="{ active: $route.path.startsWith('/dispatcher/history') }">
            История
          </NuxtLink>
          <NuxtLink to="/dispatcher/stats" class="nav-link"
            :class="{ active: $route.path.startsWith('/dispatcher/stats') }">
            Статистика
          </NuxtLink>
          <NuxtLink to="/dispatcher/drivers" class="nav-link"
            :class="{ active: $route.path.startsWith('/dispatcher/drivers') }">
            Водители
          </NuxtLink>
          <NuxtLink to="/dispatcher/vehicles" class="nav-link"
            :class="{ active: $route.path.startsWith('/dispatcher/vehicles') }">
            Автомобили
          </NuxtLink>
          <NuxtLink to="/dispatcher/addresses" class="nav-link"
            :class="{ active: $route.path.startsWith('/dispatcher/addresses') }">
            Адреса
          </NuxtLink>
        </nav>

        <!-- Пользователь -->
        <div class="flex items-center gap-3 flex-shrink-0">
          <span class="text-xs font-medium text-blue-600 bg-blue-50 rounded-full px-2.5 py-1 hidden md:block">
            Диспетчер
          </span>
          <span class="text-sm text-slate-600 hidden md:block">{{ authStore.user?.full_name }}</span>
          <button @click="logout" title="Выйти"
            class="text-slate-400 hover:text-red-500 transition-colors p-1.5 rounded-lg hover:bg-red-50">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </button>
        </div>
      </div>
    </header>

    <!-- Контент со смещением под навбар -->
    <main class="pt-14">
      <div class="max-w-7xl mx-auto px-6 py-6">
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
const authStore = useAuthStore();
function logout() {
  authStore.logout();
  navigateTo("/login");
}
</script>

<style scoped>
.nav-link {
  @apply flex-shrink-0 px-3 py-1.5 rounded-lg text-sm font-medium text-slate-600
         transition-colors hover:bg-slate-100 hover:text-slate-900 whitespace-nowrap;
}
.nav-link.active {
  @apply bg-blue-50 text-blue-700;
}
</style>
