<template>
  <div>
    <h1 class="text-2xl font-bold text-slate-800 mb-6">Мои поездки</h1>

    <div v-if="error" class="card bg-red-50 border border-red-100 text-red-600 mb-6">{{ error }}</div>

    <div v-if="loading" class="card text-center text-slate-400 py-12">Загрузка...</div>
    <div v-else-if="!orders.length" class="card text-center py-12 text-slate-400">
      Назначенных поездок нет
    </div>
    <div v-else class="space-y-4">
      <div v-for="o in orders" :key="o.id" class="card">
        <div class="flex items-start justify-between gap-4">
          <div class="flex-1">
            <div class="flex items-center gap-3 mb-2">
              <span class="font-mono text-sm text-slate-400">#{{ o.id }}</span>
              <StatusBadge :status="o.status" />
            </div>
            <div class="font-semibold text-slate-800 mb-1">
              {{ o.departure_address }} → {{ o.destination_address }}
            </div>
            <div class="text-sm text-slate-500 mb-1">
              {{ formatDate(o.desired_datetime) }} · {{ o.expected_duration_minutes }} мин
            </div>
            <div class="text-sm text-slate-500 mb-1">
              Заказчик: <span class="font-medium text-slate-700">{{ o.employee_name }}</span>
            </div>
            <div class="text-sm text-slate-500 mb-3">Цель: {{ o.purpose }}</div>
            <div v-if="o.vehicle_info" class="text-sm text-slate-500">
              Автомобиль: <span class="font-medium text-slate-700">{{ o.vehicle_info }}</span>
            </div>

            <!-- Departure / Return times -->
            <div class="mt-3 flex gap-4 text-sm">
              <div v-if="o.actual_departure" class="text-emerald-600">
                ✓ Выехал: {{ formatDate(o.actual_departure) }}
              </div>
              <div v-if="o.actual_return" class="text-emerald-600">
                ✓ Вернулся: {{ formatDate(o.actual_return) }}
              </div>
            </div>
          </div>

          <!-- Actions -->
          <div v-if="o.status === 'in_progress'" class="flex flex-col gap-2">
            <button
              v-if="!o.actual_departure"
              @click="markDepart(o.id)"
              class="btn-primary text-sm whitespace-nowrap"
            >
              Отметить выезд
            </button>
            <button
              v-if="o.actual_departure && !o.actual_return"
              @click="markReturn(o.id)"
              class="btn-primary text-sm whitespace-nowrap"
            >
              Отметить возврат
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "driver" });
const api = useApi();
const orders = ref<any[]>([]);
const loading = ref(true);
const error = ref("");

function formatDate(dt: string) {
  return new Date(dt).toLocaleString("ru-RU", {
    day: "2-digit", month: "2-digit",
    hour: "2-digit", minute: "2-digit",
  });
}

async function load() {
  loading.value = true;
  error.value = "";
  try {
    orders.value = await api.get("/orders/driver/assignments");
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

async function markDepart(id: number) {
  try {
    await api.post(`/orders/${id}/depart`);
    await load();
  } catch (e: any) {
    alert(e.message);
  }
}

async function markReturn(id: number) {
  try {
    await api.post(`/orders/${id}/return`);
    await load();
  } catch (e: any) {
    alert(e.message);
  }
}

onMounted(load);
</script>
