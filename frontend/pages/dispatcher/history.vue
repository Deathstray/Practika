<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-slate-800">История поездок</h1>
      <button class="btn-primary flex items-center gap-2" @click="exportExcel">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
        Экспорт Excel
      </button>
    </div>

    <div class="card mb-6">
      <div class="flex gap-4 flex-wrap">
        <div>
          <label class="label">Статус</label>
          <select v-model="filters.status" class="input-field w-48" @change="load">
            <option value="">Все</option>
            <option value="completed">Завершена</option>
            <option value="cancelled">Отменена</option>
            <option value="rejected">Отклонена</option>
          </select>
        </div>
        <div>
          <label class="label">Дата от</label>
          <input v-model="filters.date_from" type="datetime-local" class="input-field" @change="load" />
        </div>
        <div>
          <label class="label">Дата до</label>
          <input v-model="filters.date_to" type="datetime-local" class="input-field" @change="load" />
        </div>
        <div>
          <label class="label">Водитель</label>
          <select v-model="filters.driver_id" class="input-field w-48" @change="load">
            <option value="">Все водители</option>
            <option v-for="d in drivers" :key="d.id" :value="d.id">{{ d.full_name }}</option>
          </select>
        </div>
        <div class="flex items-end">
          <button class="btn-secondary" @click="resetFilters">Сбросить</button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="card text-center text-slate-400 py-12">Загрузка...</div>
    <div v-else-if="!orders.length" class="card text-center text-slate-400 py-12">Заявки не найдены</div>
    <div v-else class="card overflow-x-auto">
      <table>
        <thead>
          <tr><th>№</th><th>Сотрудник</th><th>Водитель</th><th>Автомобиль</th><th>Откуда</th><th>Куда</th><th>Дата</th><th>Выезд</th><th>Возврат</th><th>Статус</th></tr>
        </thead>
        <tbody>
          <tr v-for="o in orders" :key="o.id">
            <td class="font-mono text-xs">#{{ o.id }}</td>
            <td>{{ o.employee_name }}</td>
            <td>{{ o.driver_name || "—" }}</td>
            <td class="text-xs">{{ o.vehicle_info || "—" }}</td>
            <td class="max-w-xs"><div class="truncate text-xs" :title="o.departure_address">{{ o.departure_address }}</div></td>
            <td class="max-w-xs"><div class="truncate text-xs" :title="o.destination_address">{{ o.destination_address }}</div></td>
            <td class="whitespace-nowrap text-xs">{{ fmt(o.desired_datetime) }}</td>
            <td class="whitespace-nowrap text-xs">{{ o.actual_departure ? fmt(o.actual_departure) : "—" }}</td>
            <td class="whitespace-nowrap text-xs">{{ o.actual_return ? fmt(o.actual_return) : "—" }}</td>
            <td><StatusBadge :status="o.status" /></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dispatcher" });
const api = useApi();
const orders = ref<any[]>([]);
const drivers = ref<any[]>([]);
const loading = ref(true);
const filters = reactive({ status: "", date_from: "", date_to: "", driver_id: "" });

function fmt(dt: string) {
  return new Date(dt).toLocaleString("ru-RU", { day: "2-digit", month: "2-digit", year: "2-digit", hour: "2-digit", minute: "2-digit" });
}

function buildParams() {
  const p = new URLSearchParams();
  if (filters.status) p.set("status", filters.status);
  if (filters.date_from) p.set("date_from", new Date(filters.date_from).toISOString());
  if (filters.date_to) p.set("date_to", new Date(filters.date_to).toISOString());
  if (filters.driver_id) p.set("driver_id", String(filters.driver_id));
  p.set("limit", "200");
  return p.toString();
}

async function load() {
  loading.value = true;
  try { orders.value = await api.get(`/orders/?${buildParams()}`); }
  finally { loading.value = false; }
}

async function exportExcel() {
  await api.download(`/orders/export/excel?${buildParams()}`);
}

function resetFilters() {
  Object.assign(filters, { status: "", date_from: "", date_to: "", driver_id: "" });
  load();
}

onMounted(async () => {
  drivers.value = await api.get("/drivers/");
  await load();
});
</script>
