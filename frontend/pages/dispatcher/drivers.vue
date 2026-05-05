<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-slate-800">Водители</h1>
      <button class="btn-primary" @click="openCreate">+ Добавить водителя</button>
    </div>

    <div class="card overflow-x-auto">
      <div v-if="loading" class="text-center text-slate-400 py-8">Загрузка...</div>
      <table v-else>
        <thead><tr><th>ФИО</th><th>Табельный №</th><th>Телефон</th><th>Удостоверение</th><th>Статус</th><th>Действия</th></tr></thead>
        <tbody>
          <tr v-for="d in drivers" :key="d.id">
            <td class="font-medium">{{ d.full_name }}</td>
            <td class="font-mono text-xs">{{ d.employee_number }}</td>
            <td>{{ d.phone || "—" }}</td>
            <td>{{ d.license_number || "—" }}</td>
            <td>
              <span :class="['text-xs font-semibold px-2 py-1 rounded-full', d.status === 'active' ? 'bg-emerald-50 text-emerald-600' : 'bg-slate-100 text-slate-400']">
                {{ d.status === "active" ? "Активен" : "Неактивен" }}
              </span>
            </td>
            <td>
              <button class="text-brand-500 hover:text-brand-700 font-medium text-sm mr-3" @click="openEdit(d)">Изменить</button>
              <button v-if="d.status === 'active'" class="text-red-400 hover:text-red-600 font-medium text-sm" @click="deactivate(d)">Деактивировать</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
    <div v-if="modal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50" @click.self="modal = null">
      <div class="bg-white rounded-2xl w-full max-w-md shadow-2xl p-6">
        <h2 class="text-lg font-bold text-slate-800 mb-5">{{ modal.id ? "Редактировать водителя" : "Новый водитель" }}</h2>
        <div class="space-y-4">
          <div>
            <label class="label">ФИО *</label>
            <input v-model="modal.full_name" class="input-field" required />
          </div>
          <div v-if="!modal.id">
            <label class="label">Табельный номер *</label>
            <input v-model="modal.employee_number" class="input-field" required />
          </div>
          <div>
            <label class="label">Телефон</label>
            <input v-model="modal.phone" class="input-field" />
          </div>
          <div>
            <label class="label">Номер удостоверения</label>
            <input v-model="modal.license_number" class="input-field" />
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
          <button class="btn-primary flex-1" @click="saveDriver">Сохранить</button>
          <button class="btn-secondary flex-1" @click="modal = null">Отмена</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "dispatcher" });
const api = useApi();
const drivers = ref<any[]>([]);
const loading = ref(true);
const modal = ref<any>(null);
const error = ref("");

async function load() {
  loading.value = true;
  try { drivers.value = await api.get("/drivers/"); }
  finally { loading.value = false; }
}

function openCreate() { modal.value = { full_name: "", employee_number: "", phone: "", license_number: "" }; error.value = ""; }
function openEdit(d: any) { modal.value = { ...d }; error.value = ""; }

async function saveDriver() {
  error.value = "";
  try {
    if (modal.value.id) {
      await api.patch(`/drivers/${modal.value.id}`, { full_name: modal.value.full_name, phone: modal.value.phone, license_number: modal.value.license_number, status: modal.value.status });
    } else {
      await api.post("/drivers/", { full_name: modal.value.full_name, employee_number: modal.value.employee_number, phone: modal.value.phone, license_number: modal.value.license_number });
    }
    modal.value = null;
    await load();
  } catch (e: any) { error.value = e.message; }
}

async function deactivate(d: any) {
  if (!confirm(`Деактивировать водителя ${d.full_name}?`)) return;
  await api.delete(`/drivers/${d.id}`);
  await load();
}

onMounted(load);
</script>
