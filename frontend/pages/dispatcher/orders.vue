<template>
  <div>
    <h1 class="text-2xl font-bold text-slate-800 mb-6">Заявки</h1>

    <!-- Filters -->
    <div class="card mb-6">
      <div class="flex gap-4 flex-wrap">
        <div>
          <label class="label">Статус</label>
          <select v-model="filters.status" class="input-field w-48" @change="loadOrders">
            <option value="">Все статусы</option>
            <option value="new">Новая</option>
            <option value="accepted">Принята</option>
            <option value="rejected">Отклонена</option>
            <option value="in_progress">Выполняется</option>
            <option value="completed">Завершена</option>
            <option value="cancelled">Отменена</option>
          </select>
        </div>
        <div>
          <label class="label">Дата от</label>
          <input v-model="filters.date_from" type="datetime-local" class="input-field" @change="loadOrders" />
        </div>
        <div>
          <label class="label">Дата до</label>
          <input v-model="filters.date_to" type="datetime-local" class="input-field" @change="loadOrders" />
        </div>
        <div class="flex items-end">
          <button class="btn-secondary" @click="resetFilters">Сбросить</button>
        </div>
      </div>
    </div>

    <!-- Orders -->
    <div v-if="loading" class="card text-center text-slate-400 py-12">Загрузка...</div>
    <div v-else-if="!orders.length" class="card text-center text-slate-400 py-12">Заявки не найдены</div>
    <div v-else class="card overflow-x-auto">
      <table>
        <thead>
          <tr><th>№</th><th>Сотрудник</th><th>Откуда</th><th>Куда</th><th>Дата/время</th><th>Статус</th><th>Действия</th></tr>
        </thead>
        <tbody>
          <tr v-for="o in orders" :key="o.id">
            <td class="font-mono text-xs">#{{ o.id }}</td>
            <td>{{ o.employee_name }}</td>
            <td class="max-w-xs">
              <div class="truncate" :title="o.departure_address">{{ o.departure_address }}</div>
            </td>
            <td class="max-w-xs">
              <div class="truncate" :title="o.destination_address">{{ o.destination_address }}</div>
            </td>
            <td class="whitespace-nowrap text-xs">{{ formatDate(o.desired_datetime) }}</td>
            <td><StatusBadge :status="o.status" /></td>
            <td>
              <button class="text-brand-500 hover:text-brand-700 font-medium text-sm" @click="openOrder(o)">
                Открыть
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Order detail modal -->
    <div v-if="selected" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50 p-4" @click.self="selected = null">
      <div class="bg-white rounded-2xl w-full max-w-xl shadow-2xl max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-slate-100 flex items-center justify-between">
          <h2 class="text-lg font-bold text-slate-800">Заявка #{{ selected.id }}</h2>
          <button @click="selected = null" class="text-slate-400 hover:text-slate-600">✕</button>
        </div>
        <div class="p-6 space-y-4">
          <div class="grid grid-cols-2 gap-4 text-sm">
            <div><span class="text-slate-400">Сотрудник:</span> <span class="font-medium">{{ selected.employee_name }}</span></div>
            <div><span class="text-slate-400">Статус:</span> <StatusBadge :status="selected.status" /></div>
            <div class="col-span-2"><span class="text-slate-400">Откуда:</span> <span class="font-medium">{{ selected.departure_address }}</span></div>
            <div class="col-span-2"><span class="text-slate-400">Куда:</span> <span class="font-medium">{{ selected.destination_address }}</span></div>
            <div><span class="text-slate-400">Дата/время:</span> <span class="font-medium">{{ formatDate(selected.desired_datetime) }}</span></div>
            <div><span class="text-slate-400">Длительность:</span> <span class="font-medium">{{ selected.expected_duration_minutes }} мин</span></div>
            <div class="col-span-2"><span class="text-slate-400">Цель:</span> <span class="font-medium">{{ selected.purpose }}</span></div>
            <div v-if="selected.notes" class="col-span-2"><span class="text-slate-400">Примечания:</span> <span class="font-medium">{{ selected.notes }}</span></div>
            <div v-if="selected.rejection_reason" class="col-span-2 bg-red-50 rounded-xl p-3">
              <span class="text-red-500 font-semibold">Причина отклонения:</span> {{ selected.rejection_reason }}
            </div>
            <div v-if="selected.driver_name"><span class="text-slate-400">Водитель:</span> <span class="font-medium">{{ selected.driver_name }}</span></div>
            <div v-if="selected.vehicle_info"><span class="text-slate-400">Автомобиль:</span> <span class="font-medium">{{ selected.vehicle_info }}</span></div>
          </div>

          <!-- Actions -->
          <div v-if="selected.status === 'new'" class="flex gap-3 pt-2">
            <button class="btn-primary flex-1" @click="acceptOrder">Принять</button>
            <button class="btn-danger flex-1" @click="showReject = true">Отклонить</button>
          </div>

          <div v-if="selected.status === 'accepted'" class="space-y-3 pt-2">
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="label">Водитель</label>
                <select v-model="assign.driver_id" class="input-field">
                  <option value="">Выберите водителя</option>
                  <option v-for="d in drivers" :key="d.id" :value="d.id">{{ d.full_name }}</option>
                </select>
              </div>
              <div>
                <label class="label">Автомобиль</label>
                <select v-model="assign.vehicle_id" class="input-field">
                  <option value="">Выберите автомобиль</option>
                  <option v-for="v in vehicles" :key="v.id" :value="v.id">{{ v.make }} {{ v.model }} ({{ v.license_plate }})</option>
                </select>
              </div>
            </div>
            <div>
              <label class="label">Ожидаемая длительность (мин)</label>
              <input v-model.number="assign.expected_duration_minutes" type="number" min="15" class="input-field" />
            </div>
            <p v-if="assignError" class="text-red-500 text-sm">{{ assignError }}</p>
            <button class="btn-primary w-full" @click="assignOrder" :disabled="!assign.driver_id || !assign.vehicle_id">
              Назначить
            </button>
          </div>

          <!-- Reject dialog -->
          <div v-if="showReject" class="border-t pt-4">
            <label class="label">Причина отклонения *</label>
            <textarea v-model="rejectReason" class="input-field mb-3" rows="3" placeholder="Укажите причину..."></textarea>
            <button class="btn-danger w-full" @click="rejectOrder" :disabled="!rejectReason.trim()">Подтвердить отклонение</button>
          </div>

          <!-- History -->
          <div v-if="selected.status_history?.length" class="border-t pt-4">
            <h3 class="font-semibold text-slate-700 mb-3 text-sm">История статусов</h3>
            <div class="space-y-2">
              <div v-for="h in selected.status_history" :key="h.id" class="flex gap-3 text-sm">
                <div class="text-xs text-slate-400 whitespace-nowrap mt-0.5">{{ formatDate(h.changed_at) }}</div>
                <div>
                  <StatusBadge :status="h.new_status" />
                  <span v-if="h.comment" class="ml-2 text-slate-500">{{ h.comment }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dispatcher" });
const api = useApi();
const orders = ref<any[]>([]);
const loading = ref(true);
const selected = ref<any>(null);
const showReject = ref(false);
const rejectReason = ref("");
const assignError = ref("");
const drivers = ref<any[]>([]);
const vehicles = ref<any[]>([]);
const assign = reactive({ driver_id: "", vehicle_id: "", expected_duration_minutes: 60 });
const filters = reactive({ status: "", date_from: "", date_to: "" });

function formatDate(dt: string) {
  return new Date(dt).toLocaleString("ru-RU", { day: "2-digit", month: "2-digit", year: "2-digit", hour: "2-digit", minute: "2-digit" });
}

async function loadOrders() {
  loading.value = true;
  const params = new URLSearchParams();
  if (filters.status) params.set("status", filters.status);
  if (filters.date_from) params.set("date_from", new Date(filters.date_from).toISOString());
  if (filters.date_to) params.set("date_to", new Date(filters.date_to).toISOString());
  try { orders.value = await api.get(`/orders/?${params}`); }
  finally { loading.value = false; }
}

async function openOrder(o: any) {
  selected.value = o;
  showReject.value = false;
  rejectReason.value = "";
  assignError.value = "";
  assign.driver_id = "";
  assign.vehicle_id = "";
  assign.expected_duration_minutes = o.expected_duration_minutes;
  if (o.status === "accepted") {
    [drivers.value, vehicles.value] = await Promise.all([
      api.get("/drivers/?status=active"),
      api.get("/vehicles/?status=active"),
    ]);
  }
}

async function acceptOrder() {
  await api.post(`/orders/${selected.value.id}/accept`);
  await loadOrders();
  selected.value = null;
}

async function rejectOrder() {
  await api.post(`/orders/${selected.value.id}/reject`, { rejection_reason: rejectReason.value });
  await loadOrders();
  selected.value = null;
}

async function assignOrder() {
  assignError.value = "";
  try {
    await api.post(`/orders/${selected.value.id}/assign`, {
      driver_id: Number(assign.driver_id),
      vehicle_id: Number(assign.vehicle_id),
      expected_duration_minutes: assign.expected_duration_minutes,
    });
    await loadOrders();
    selected.value = null;
  } catch (e: any) {
    assignError.value = e.message;
  }
}

function resetFilters() {
  filters.status = "";
  filters.date_from = "";
  filters.date_to = "";
  loadOrders();
}

onMounted(loadOrders);
</script>
