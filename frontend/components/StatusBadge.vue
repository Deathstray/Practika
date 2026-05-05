<template>
  <span :class="['text-xs font-semibold px-2.5 py-1 rounded-full', statusClass]">
    {{ label }}
  </span>
</template>

<script setup lang="ts">
const props = defineProps<{ status: string }>();

const labels: Record<string, string> = {
  new: "Новая",
  accepted: "Принята",
  rejected: "Отклонена",
  in_progress: "Выполняется",
  completed: "Завершена",
  cancelled: "Отменена",
};

const statusClass = computed(() => `status-${props.status}`);
const label = computed(() => labels[props.status] || props.status);
</script>
