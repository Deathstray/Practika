<template>
  <div>
    <h1 class="text-2xl font-bold text-slate-800 mb-6">Дашборд</h1>

    <!-- Stats cards -->
    <div class="grid grid-cols-3 gap-6 mb-8">
      <div class="card flex items-center gap-4">
        <div class="w-14 h-14 bg-amber-50 rounded-2xl flex items-center justify-center flex-shrink-0">
          <svg class="w-7 h-7 text-amber-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
        </div>
        <div>
          <div class="text-3xl font-bold text-slate-800">{{ stats?.active_trips ?? "—" }}</div>
          <div class="text-sm text-slate-400 font-medium">Активные поездки</div>
        </div>
      </div>
      <div class="card flex items-center gap-4">
        <div class="w-14 h-14 bg-emerald-50 rounded-2xl flex items-center justify-center flex-shrink-0">
          <svg class="w-7 h-7 text-emerald-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/></svg>
        </div>
        <div>
          <div class="text-3xl font-bold text-slate-800">{{ stats?.free_drivers ?? "—" }}</div>
          <div class="text-sm text-slate-400 font-medium">Свободные водители</div>
        </div>
      </div>
      <div class="card flex items-center gap-4">
        <div class="w-14 h-14 bg-brand-50 rounded-2xl flex items-center justify-center flex-shrink-0">
          <svg class="w-7 h-7 text-brand-500" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/></svg>
        </div>
        <div>
          <div class="text-3xl font-bold text-slate-800">{{ stats?.new_orders ?? "—" }}</div>
          <div class="text-sm text-slate-400 font-medium">Новых заявок</div>
        </div>
      </div>
    </div>

    <!-- Active orders table -->
    <div class="card">
      <h2 class="text-lg font-bold text-slate-800 mb-4">Активные поездки</h2>
      <div v-if="loading" class="text-slate-400 text-sm py-8 text-center">Загрузка...</div>
      <div v-else-if="!stats?.active_orders?.length" class="text-slate-400 text-sm py-8 text-center">Нет активных поездок</div>
      <table v-else>
        <thead>
          <tr>
            <th>№</th><th>Сотрудник</th><th>Водитель</th><th>Автомобиль</th><th>Откуда</th><th>Куда</th><th>Время</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="o in stats.active_orders" :key="o.id">
            <td class="font-mono">#{{ o.id }}</td>
            <td>{{ o.employee_name }}</td>
            <td>{{ o.driver_name || "—" }}</td>
            <td>{{ o.vehicle_info || "—" }}</td>
            <td class="max-w-xs truncate">{{ o.departure_address }}</td>
            <td class="max-w-xs truncate">{{ o.destination_address }}</td>
            <td class="whitespace-nowrap">{{ formatDate(o.desired_datetime) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dispatcher" });
const api = useApi();
const stats = ref<any>(null);
const loading = ref(true);

function formatDate(dt: string) {
  return new Date(dt).toLocaleString("ru-RU", { day: "2-digit", month: "2-digit", hour: "2-digit", minute: "2-digit" });
}

onMounted(async () => {
  try { stats.value = await api.get("/stats/dashboard"); }
  finally { loading.value = false; }
});
</script>
