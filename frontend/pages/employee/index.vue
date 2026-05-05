<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-slate-800">Мои заявки</h1>
      <NuxtLink to="/employee/new" class="btn-primary">+ Новая заявка</NuxtLink>
    </div>

    <div v-if="loading" class="card text-center text-slate-400 py-12">Загрузка...</div>
    <div v-else-if="!orders.length" class="card text-center py-12">
      <div class="text-slate-400 mb-4">У вас ещё нет заявок</div>
      <NuxtLink to="/employee/new" class="btn-primary">Подать первую заявку</NuxtLink>
    </div>
    <div v-else class="space-y-4">
      <div v-for="o in orders" :key="o.id" class="card">
        <div class="flex items-start justify-between gap-4">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-3 mb-2">
              <span class="font-mono text-sm text-slate-400">#{{ o.id }}</span>
              <StatusBadge :status="o.status" />
            </div>
            <div class="font-semibold text-slate-800 mb-1">
              {{ o.departure_address }} → {{ o.destination_address }}
            </div>
            <div class="text-sm text-slate-500 mb-1">{{ formatDate(o.desired_datetime) }} · {{ o.purpose }}</div>
            <div v-if="o.driver_name" class="text-sm text-slate-500">
              Водитель: <span class="font-medium text-slate-700">{{ o.driver_name }}</span>
              <span v-if="o.vehicle_info"> · {{ o.vehicle_info }}</span>
            </div>
            <div v-if="o.rejection_reason" class="mt-2 text-sm text-red-500 bg-red-50 rounded-lg px-3 py-2">
              Причина отказа: {{ o.rejection_reason }}
            </div>
          </div>
          <button
            v-if="o.status === 'new'"
            @click="cancelOrder(o.id)"
            class="text-sm text-red-500 hover:text-red-700 font-medium whitespace-nowrap"
          >
            Отменить
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "employee" });
const api = useApi();
const orders = ref<any[]>([]);
const loading = ref(true);

function formatDate(dt: string) {
  return new Date(dt).toLocaleString("ru-RU", {
    day: "2-digit", month: "2-digit", year: "numeric",
    hour: "2-digit", minute: "2-digit",
  });
}

async function load() {
  loading.value = true;
  try {
    orders.value = await api.get("/orders/my");
  } finally {
    loading.value = false;
  }
}

async function cancelOrder(id: number) {
  if (!confirm("Отменить заявку?")) return;
  try {
    await api.delete(`/orders/${id}/cancel`);
    await load();
  } catch (e: any) {
    alert(e.message);
  }
}

onMounted(load);
</script>
