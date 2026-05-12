<template>
  <div class="min-h-screen flex bg-slate-50">

    <!-- Sidebar -->
    <aside class="w-64 bg-white border-r border-slate-200 flex flex-col min-h-screen fixed left-0 top-0 z-30">
      <!-- Logo -->
      <div class="px-6 py-5 border-b border-slate-200">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-blue-600 flex items-center justify-center text-white">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M8 7h12m0 0l-4-4m4 4l-4 4m0 6H4m0 0l4 4m-4-4l4-4"/>
            </svg>
          </div>
          <div>
            <div class="font-bold text-slate-800 text-sm leading-tight">Диспетчеризация</div>
            <div class="text-xs text-slate-400">транспорта</div>
          </div>
        </div>
      </div>

      <!-- Role badge -->
      <div class="px-6 py-3 border-b border-slate-100">
        <span class="inline-flex items-center gap-1.5 text-xs font-medium text-blue-700 bg-blue-50 rounded-full px-2.5 py-1">
          <span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span>
          Диспетчер
        </span>
      </div>

      <!-- Nav -->
      <nav class="flex-1 px-3 py-4 space-y-1">
        <NuxtLink to="/dispatcher" class="nav-link" :class="{ active: $route.path === '/dispatcher' }">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"/>
          </svg>
          Дашборд
        </NuxtLink>
        <NuxtLink to="/dispatcher/orders" class="nav-link" :class="{ active: $route.path.startsWith('/dispatcher/orders') }">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          Заявки
        </NuxtLink>
        <NuxtLink to="/dispatcher/history" class="nav-link" :class="{ active: $route.path.startsWith('/dispatcher/history') }">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          История поездок
        </NuxtLink>
        <NuxtLink to="/dispatcher/stats" class="nav-link" :class="{ active: $route.path.startsWith('/dispatcher/stats') }">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
          </svg>
          Статистика
        </NuxtLink>

        <div class="pt-3 pb-1">
          <p class="px-3 text-xs font-semibold text-slate-400 uppercase tracking-wider">Справочники</p>
        </div>
        <NuxtLink to="/dispatcher/drivers" class="nav-link" :class="{ active: $route.path.startsWith('/dispatcher/drivers') }">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          </svg>
          Водители
        </NuxtLink>
        <NuxtLink to="/dispatcher/vehicles" class="nav-link" :class="{ active: $route.path.startsWith('/dispatcher/vehicles') }">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M8 7h12m0 0l-4-4m4 4l-4 4M4 17h12m0 0l-4-4m4 4l-4 4"/>
          </svg>
          Автомобили
        </NuxtLink>
        <NuxtLink to="/dispatcher/addresses" class="nav-link" :class="{ active: $route.path.startsWith('/dispatcher/addresses') }">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
          </svg>
          Адреса
        </NuxtLink>
      </nav>

      <!-- User / logout -->
      <div class="px-3 py-4 border-t border-slate-200">
        <div class="flex items-center gap-3 px-3 py-2 rounded-xl">
          <div class="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold text-sm flex-shrink-0">
            {{ authStore.user?.full_name?.[0] ?? 'Д' }}
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-sm font-medium text-slate-700 truncate">{{ authStore.user?.full_name }}</div>
          </div>
          <button @click="logout" title="Выйти" class="text-slate-400 hover:text-red-500 transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"/>
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- Main content -->
    <main class="flex-1 ml-64 p-8">
      <slot />
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
  @apply flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm text-slate-600 font-medium transition-colors hover:bg-slate-100 hover:text-slate-900;
}
.nav-link.active {
  @apply bg-blue-50 text-blue-700;
}
</style>
