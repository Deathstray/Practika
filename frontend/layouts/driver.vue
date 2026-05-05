<template>
  <div class="flex min-h-screen bg-slate-50">
    <aside class="w-64 bg-white border-r border-slate-100 flex flex-col fixed h-full z-10">
      <div class="p-6 border-b border-slate-100">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 bg-amber-500 rounded-xl flex items-center justify-center">
            <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
            </svg>
          </div>
          <div>
            <div class="font-bold text-slate-800 text-sm">Транспорт</div>
            <div class="text-xs text-slate-400">Водитель</div>
          </div>
        </div>
      </div>
      <nav class="flex-1 p-4 space-y-1">
        <NuxtLink to="/driver" exact class="sidebar-link" active-class="active">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
          Мои поездки
        </NuxtLink>
      </nav>
      <div class="p-4 border-t border-slate-100">
        <div class="text-sm text-slate-600 font-semibold mb-1">{{ auth.fullName }}</div>
        <button @click="logout" class="text-sm text-red-500 hover:text-red-600 font-medium">Выйти</button>
      </div>
    </aside>
    <main class="flex-1 ml-64 p-8">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "~/stores/auth";
const auth = useAuthStore();
function logout() { auth.logout(); navigateTo("/login"); }
</script>
