<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-slate-800">Автомобили</h1>
      <button class="btn-primary" @click="openCreate">+ Добавить автомобиль</button>
    </div>

    <div class="card overflow-x-auto">
      <div v-if="loading" class="text-center text-slate-400 py-8">Загрузка...</div>
      <table v-else>
        <thead><tr><th>Марка</th><th>Модель</th><th>Гос. номер</th><th>Тип</th><th>Вместимость</th><th>Статус</th><th>Действия</th></tr></thead>
        <tbody>
          <tr v-for="v in vehicles" :key="v.id">
            <td class="font-medium">{{ v.make }}</td>
            <td>{{ v.model }}</td>
            <td class="font-mono text-xs">{{ v.license_plate }}</td>
            <td>{{ v.vehicle_type }}</td>
            <td>{{ v.capacity ?? "—" }}</td>
            <td>
              <span :class="['text-xs font-semibold px-2 py-1 rounded-full', v.status === 'active' ? 'bg-emerald-50 text-emerald-600' : 'bg-slate-100 text-slate-400']">
                {{ v.status === "active" ? "Активен" : "Неактивен" }}
              </span>
            </td>
            <td>
              <button class="text-brand-500 hover:text-brand-700 font-medium text-sm mr-3" @click="openEdit(v)">Изменить</button>
              <button v-if="v.status === 'active'" class="text-red-400 hover:text-red-600 font-medium text-sm" @click="deactivate(v)">Деактивировать</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="modal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50" @click.self="modal = null">
      <div class="bg-white rounded-2xl w-full max-w-md shadow-2xl p-6">
        <h2 class="text-lg font-bold text-slate-800 mb-5">{{ modal.id ? "Редактировать автомобиль" : "Новый автомобиль" }}</h2>
        <div class="space-y-4">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="label">Марка *</label>
              <input v-model="modal.make" class="input-field" />
            </div>
            <div>
              <label class="label">Модель *</label>
              <input v-model="modal.model" class="input-field" />
            </div>
          </div>
          <div>
            <label class="label">Гос. номер *</label>
            <input v-model="modal.license_plate" class="input-field" />
          </div>
          <div>
            <label class="label">Тип ТС *</label>
            <select v-model="modal.vehicle_type" class="input-field">
              <option value="sedan">Седан</option>
              <option value="suv">Внедорожник</option>
              <option value="minibus">Микроавтобус</option>
              <option value="bus">Автобус</option>
              <option value="truck">Грузовик</option>
            </select>
          </div>
          <div>
            <label class="label">Вместимость</label>
            <input v-model.number="modal.capacity" type="number" class="input-field" />
          </div>
          <div v-if="modal.id">
            <label class="label">Статус</label>
            <select v-model="modal.status" class="input-field">
              <option value="active">Активен</option>
              <option value="inactive">Неактивен</option>
            </select>
          </div>
        </div>
        <p v-if="error" class="text-red-500 text-sm mt-3">{{ error }}</p>
        <div class="flex gap-3 mt-6">
          <button class="btn-primary flex-1" @click="save">Сохранить</button>
          <button class="btn-secondary flex-1" @click="modal = null">Отмена</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dispatcher" });
const api = useApi();
const vehicles = ref<any[]>([]);
const loading = ref(true);
const modal = ref<any>(null);
const error = ref("");

async function load() {
  loading.value = true;
  try { vehicles.value = await api.get("/vehicles/"); }
  finally { loading.value = false; }
}

function openCreate() { modal.value = { make: "", model: "", license_plate: "", vehicle_type: "sedan", capacity: null }; error.value = ""; }
function openEdit(v: any) { modal.value = { ...v }; error.value = ""; }

async function save() {
  error.value = "";
  try {
    if (modal.value.id) {
      await api.patch(`/vehicles/${modal.value.id}`, { make: modal.value.make, model: modal.value.model, license_plate: modal.value.license_plate, vehicle_type: modal.value.vehicle_type, capacity: modal.value.capacity, status: modal.value.status });
    } else {
      await api.post("/vehicles/", { make: modal.value.make, model: modal.value.model, license_plate: modal.value.license_plate, vehicle_type: modal.value.vehicle_type, capacity: modal.value.capacity });
    }
    modal.value = null;
    await load();
  } catch (e: any) { error.value = e.message; }
}

async function deactivate(v: any) {
  if (!confirm(`Деактивировать автомобиль ${v.make} ${v.model}?`)) return;
  await api.delete(`/vehicles/${v.id}`);
  await load();
}

onMounted(load);
</script>
