<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-slate-800">Справочник адресов</h1>
      <button class="btn-primary" @click="openCreate">+ Добавить адрес</button>
    </div>

    <div class="card overflow-x-auto">
      <div v-if="loading" class="text-center text-slate-400 py-8">Загрузка...</div>
      <table v-else>
        <thead><tr><th>Адрес</th><th>Метка</th><th>Использований</th><th>Статус</th><th>Действия</th></tr></thead>
        <tbody>
          <tr v-for="a in addresses" :key="a.id">
            <td class="font-medium">{{ a.address }}</td>
            <td class="text-slate-500">{{ a.label || "—" }}</td>
            <td>{{ a.usage_count }}</td>
            <td>
              <span :class="['text-xs font-semibold px-2 py-1 rounded-full', a.is_active ? 'bg-emerald-50 text-emerald-600' : 'bg-slate-100 text-slate-400']">
                {{ a.is_active ? "Активен" : "Скрыт" }}
              </span>
            </td>
            <td>
              <button class="text-brand-500 hover:text-brand-700 font-medium text-sm mr-3" @click="openEdit(a)">Изменить</button>
              <button v-if="a.is_active" class="text-red-400 hover:text-red-600 font-medium text-sm" @click="deactivate(a)">Скрыть</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="modal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50" @click.self="modal = null">
      <div class="bg-white rounded-2xl w-full max-w-md shadow-2xl p-6">
        <h2 class="text-lg font-bold text-slate-800 mb-5">{{ modal.id ? "Редактировать адрес" : "Новый адрес" }}</h2>
        <div class="space-y-4">
          <div>
            <label class="label">Адрес *</label>
            <input v-model="modal.address" class="input-field" placeholder="ул. Ленина, 1, Москва" />
          </div>
          <div>
            <label class="label">Метка (необязательно)</label>
            <input v-model="modal.label" class="input-field" placeholder="Главный офис" />
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
const addresses = ref<any[]>([]);
const loading = ref(true);
const modal = ref<any>(null);
const error = ref("");

async function load() {
  loading.value = true;
  try { addresses.value = await api.get("/addresses/"); }
  finally { loading.value = false; }
}

function openCreate() { modal.value = { address: "", label: "" }; error.value = ""; }
function openEdit(a: any) { modal.value = { ...a }; error.value = ""; }

async function save() {
  error.value = "";
  try {
    if (modal.value.id) {
      await api.patch(`/addresses/${modal.value.id}`, { address: modal.value.address, label: modal.value.label });
    } else {
      await api.post("/addresses/", { address: modal.value.address, label: modal.value.label });
    }
    modal.value = null;
    await load();
  } catch (e: any) { error.value = e.message; }
}

async function deactivate(a: any) {
  await api.delete(`/addresses/${a.id}`);
  await load();
}

onMounted(load);
</script>
