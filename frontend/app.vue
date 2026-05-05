<template>
  <NuxtPage />
</template>

<script setup lang="ts">
import { useAuthStore } from "~/stores/auth";
const auth = useAuthStore();
auth.restore();
</script>
