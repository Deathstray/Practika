<template>
  <div class="min-h-screen flex bg-slate-50">

    <!-- Sidebar -->
    <aside class="w-64 bg-white border-r border-slate-200 flex flex-col min-h-screen fixed left-0 top-0 z-30">
      <!-- Logo -->
      <div class="px-6 py-5 border-b border-slate-200">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-xl bg-emerald-600 flex items-center justify-center text-white">
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
        <span class="inline-flex items-center gap-1.5 text-xs font-medium text-emerald-700 bg-emerald-50 rounded-full px-2.5 py-1">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
          Сотрудник
        </span>
      </div>

      <!-- Nav -->
      <nav class="flex-1 px-3 py-4 space-y-1">
        <NuxtLink to="/employee" class="nav-link" :class="{ active: $route.path === '/employee' }">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
          </svg>
          Мои заявки
        </NuxtLink>
        <NuxtLink to="/employee/new" class="nav-link" :class="{ active: $route.path === '/employee/new' }">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M12 4v16m8-8H4"/>
          </svg>
          Новая заявка
        </NuxtLink>
      </nav>

      <!-- User / logout -->
      <div class="px-3 py-4 border-t border-slate-200">
        <div class="flex items-center gap-3 px-3 py-2 rounded-xl">
          <div class="w-8 h-8 rounded-full bg-emerald-100 flex items-center justify-center text-emerald-600 font-bold text-sm flex-shrink-0">
            {{ authStore.user?.full_name?.[0] ?? 'С' }}
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
  @apply bg-emerald-50 text-emerald-700;
}
</style>
