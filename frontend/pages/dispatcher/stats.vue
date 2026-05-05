<template>
  <div>
    <h1 class="text-2xl font-bold text-slate-800 mb-6">Статистика</h1>

    <div class="card mb-6">
      <div class="flex gap-4 items-end flex-wrap">
        <div>
          <label class="label">Период с</label>
          <input v-model="dateFrom" type="date" class="input-field" />
        </div>
        <div>
          <label class="label">Период по</label>
          <input v-model="dateTo" type="date" class="input-field" />
        </div>
        <button class="btn-primary" @click="loadStats">Применить</button>
      </div>
    </div>

    <div v-if="loading" class="card text-center text-slate-400 py-12">Загрузка...</div>
    <div v-else-if="stats">
      <!-- Summary -->
      <div class="grid grid-cols-2 gap-6 mb-6">
        <div class="card text-center">
          <div class="text-4xl font-bold text-brand-500 mb-1">{{ stats.total_orders }}</div>
          <div class="text-sm text-slate-400">Всего заявок</div>
        </div>
        <div class="card text-center">
          <div class="text-4xl font-bold text-emerald-500 mb-1">{{ stats.completed_orders }}</div>
          <div class="text-sm text-slate-400">Завершено поездок</div>
        </div>
      </div>

      <!-- Charts -->
      <div class="grid grid-cols-2 gap-6 mb-6">
        <div class="card">
          <h3 class="font-semibold text-slate-700 mb-4">Заявки по дням</h3>
          <div ref="lineChartEl" class="h-52"></div>
        </div>
        <div class="card">
          <h3 class="font-semibold text-slate-700 mb-4">Топ направлений</h3>
          <div ref="pieChartEl" class="h-52"></div>
        </div>
      </div>

      <div class="card">
        <h3 class="font-semibold text-slate-700 mb-4">Загруженность водителей</h3>
        <div ref="barChartEl" class="h-64"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import * as echarts from "echarts";

definePageMeta({ layout: "dispatcher" });
const api = useApi();

const stats = ref<any>(null);
const loading = ref(false);
const lineChartEl = ref<HTMLElement | null>(null);
const pieChartEl = ref<HTMLElement | null>(null);
const barChartEl = ref<HTMLElement | null>(null);

const now = new Date();
const dateFrom = ref(new Date(now.getFullYear(), now.getMonth(), 1).toISOString().slice(0, 10));
const dateTo = ref(now.toISOString().slice(0, 10));

async function loadStats() {
  loading.value = true;
  try {
    const p = new URLSearchParams({
      date_from: new Date(dateFrom.value).toISOString(),
      date_to: new Date(dateTo.value + "T23:59:59").toISOString(),
    });
    stats.value = await api.get(`/stats/?${p}`);
    await nextTick();
    renderCharts();
  } finally {
    loading.value = false;
  }
}

function renderCharts() {
  if (!stats.value) return;

  // Line chart
  if (lineChartEl.value) {
    const chart = echarts.init(lineChartEl.value);
    chart.setOption({
      tooltip: { trigger: "axis" },
      xAxis: { type: "category", data: stats.value.daily_counts.map((d: any) => d.date), axisLabel: { fontSize: 10 } },
      yAxis: { type: "value", minInterval: 1 },
      series: [{ type: "line", data: stats.value.daily_counts.map((d: any) => d.count), smooth: true, areaStyle: { opacity: 0.15 }, color: "#1a4aff" }],
      grid: { left: 30, right: 10, top: 10, bottom: 40 },
    });
  }

  // Pie chart
  if (pieChartEl.value) {
    const chart = echarts.init(pieChartEl.value);
    chart.setOption({
      tooltip: { trigger: "item" },
      series: [{
        type: "pie", radius: ["40%", "70%"],
        data: stats.value.top_routes.map((r: any) => ({ name: r.route, value: r.count })),
        label: { fontSize: 10, formatter: "{b|{b}}\n{c} поездок", rich: { b: { fontWeight: "bold" } } },
      }],
    });
  }

  // Bar chart
  if (barChartEl.value) {
    const chart = echarts.init(barChartEl.value);
    chart.setOption({
      tooltip: { trigger: "axis" },
      xAxis: { type: "value", minInterval: 1 },
      yAxis: { type: "category", data: stats.value.driver_loads.map((d: any) => d.driver_name), axisLabel: { fontSize: 11 } },
      series: [{ type: "bar", data: stats.value.driver_loads.map((d: any) => d.completed), color: "#10b981" }],
      grid: { left: 140, right: 20, top: 10, bottom: 30 },
    });
  }
}

onMounted(loadStats);
</script>
