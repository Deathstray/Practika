<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="text-slate-400">Перенаправление...</div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from "~/stores/auth";

const auth = useAuthStore();
// Восстанавливаем сессию из localStorage до редиректа
auth.restore();

onMounted(() => {
  if (!auth.isLoggedIn) {
    navigateTo("/login");
  } else {
    navigateTo(`/${auth.role}`);
  }
});
</script>
