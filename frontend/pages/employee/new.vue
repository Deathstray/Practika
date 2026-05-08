<template>
  <div class="max-w-2xl">
    <div class="flex items-center gap-4 mb-6">
      <NuxtLink to="/employee" class="text-slate-400 hover:text-slate-600">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
      </NuxtLink>
      <h1 class="text-2xl font-bold text-slate-800">Новая заявка на транспорт</h1>
    </div>

    <div class="card">
      <form @submit.prevent="submit">
        <!-- Departure -->
        <div class="mb-5">
          <label class="label">Откуда <span class="text-red-400">*</span></label>
          <div class="relative">
            <input
                v-model="form.departure_address"
                type="text"
                class="input-field"
                placeholder="Начните вводить адрес..."
                required
                autocomplete="off"
                @input="searchAddresses('departure')"
                @blur="() => setTimeout(() => departureSuggestions = [], 200)"
            />
            <ul v-if="departureSuggestions.length" class="absolute z-10 left-0 right-0 bg-white border border-slate-200 rounded-xl mt-1 shadow-lg overflow-hidden">
              <li
                  v-for="a in departureSuggestions" :key="a.id"
                  @mousedown.prevent="selectAddress('departure', a.address)"
                  class="px-4 py-2.5 text-sm cursor-pointer hover:bg-slate-50 border-b border-slate-100 last:border-0"
              >
                <span class="font-medium text-slate-700">{{ a.address }}</span>
                <span v-if="a.label" class="text-slate-400 ml-2">{{ a.label }}</span>
              </li>
            </ul>
          </div>
        </div>

        <!-- Destination -->
        <div class="mb-5">
          <label class="label">Куда <span class="text-red-400">*</span></label>
          <div class="relative">
            <input
                v-model="form.destination_address"
                type="text"
                class="input-field"
                placeholder="Начните вводить адрес..."
                required
                autocomplete="off"
                @input="searchAddresses('destination')"
                @blur="() => setTimeout(() => destinationSuggestions = [], 200)"
            />
            <ul v-if="destinationSuggestions.length" class="absolute z-10 left-0 right-0 bg-white border border-slate-200 rounded-xl mt-1 shadow-lg overflow-hidden">
              <li
                  v-for="a in destinationSuggestions" :key="a.id"
                  @mousedown.prevent="selectAddress('destination', a.address)"
                  class="px-4 py-2.5 text-sm cursor-pointer hover:bg-slate-50 border-b border-slate-100 last:border-0"
              >
                <span class="font-medium text-slate-700">{{ a.address }}</span>
                <span v-if="a.label" class="text-slate-400 ml-2">{{ a.label }}</span>
              </li>
            </ul>
          </div>
        </div>

        <!-- DateTime & Duration -->
        <div class="grid grid-cols-2 gap-4 mb-5">
          <div>
            <label class="label">Дата и время <span class="text-red-400">*</span></label>
            <input
                v-model="form.desired_datetime"
                type="datetime-local"
                class="input-field"
                :min="minDateTime"
                required
            />
            <p v-if="dateError" class="text-red-500 text-xs mt-1">{{ dateError }}</p>
          </div>
          <div>
            <label class="label">Продолжительность (мин)</label>
            <input
                v-model.number="form.expected_duration_minutes"
                type="number"
                min="15"
                max="480"
                class="input-field"
            />
          </div>
        </div>

        <!-- Purpose -->
        <div class="mb-5">
          <label class="label">Цель поездки <span class="text-red-400">*</span></label>
          <input v-model="form.purpose" type="text" class="input-field" placeholder="Деловая встреча, командировка..." required />
        </div>

        <!-- Notes -->
        <div class="mb-6">
          <label class="label">Особые отметки</label>
          <textarea v-model="form.notes" class="input-field" rows="3" placeholder="Багаж, особые требования..."></textarea>
        </div>

        <p v-if="error" class="text-red-500 text-sm mb-4">{{ error }}</p>
        <div class="flex gap-3">
          <button type="submit" class="btn-primary" :disabled="loading || !!dateError">
            {{ loading ? "Отправка..." : "Отправить заявку" }}
          </button>
          <NuxtLink to="/employee" class="btn-secondary">Отмена</NuxtLink>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: "employee" });
const api = useApi();

const form = reactive({
  departure_address: "",
  destination_address: "",
  desired_datetime: "",
  expected_duration_minutes: 60,
  purpose: "",
  notes: "",
});

const loading = ref(false);
const error = ref("");
const departureSuggestions = ref<any[]>([]);
const destinationSuggestions = ref<any[]>([]);

// Минимально допустимая дата/время — прямо сейчас (обновляется каждую минуту)
const minDateTime = ref(getCurrentMinDateTime());

function getCurrentMinDateTime() {
  const now = new Date();
  now.setSeconds(0, 0);
  return now.toISOString().slice(0, 16);
}

// Обновляем minDateTime каждую минуту чтобы не устаревало
let minInterval: ReturnType<typeof setInterval>;
onMounted(() => {
  minInterval = setInterval(() => {
    minDateTime.value = getCurrentMinDateTime();
  }, 60_000);
});
onUnmounted(() => clearInterval(minInterval));

// Валидация даты
const dateError = computed(() => {
  if (!form.desired_datetime) return "";
  const selected = new Date(form.desired_datetime);
  const now = new Date();
  if (selected < now) return "Нельзя выбрать прошедшую дату и время";
  return "";
});

let debounceTimer: ReturnType<typeof setTimeout>;

async function searchAddresses(field: "departure" | "destination") {
  clearTimeout(debounceTimer);
  const query = field === "departure" ? form.departure_address : form.destination_address;
  if (query.length < 2) {
    if (field === "departure") departureSuggestions.value = [];
    else destinationSuggestions.value = [];
    return;
  }
  debounceTimer = setTimeout(async () => {
    try {
      const results = await api.get(`/addresses/?q=${encodeURIComponent(query)}`);
      if (field === "departure") departureSuggestions.value = results;
      else destinationSuggestions.value = results;
    } catch {}
  }, 300);
}

function selectAddress(field: "departure" | "destination", address: string) {
  if (field === "departure") {
    form.departure_address = address;
    departureSuggestions.value = [];
  } else {
    form.destination_address = address;
    destinationSuggestions.value = [];
  }
}

async function submit() {
  if (dateError.value) return;
  loading.value = true;
  error.value = "";
  try {
    await api.post("/orders/", {
      ...form,
      desired_datetime: new Date(form.desired_datetime).toISOString(),
    });
    navigateTo("/employee");
  } catch (e: any) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}
</script>