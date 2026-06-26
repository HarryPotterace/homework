function parseDashboardSeries(node) {
  const raw = node.dataset.dashboardSeries;
  if (!raw) {
    return [];
  }

  try {
    const parsed = JSON.parse(raw);
    return Object.entries(parsed).map(([label, value]) => ({
      label,
      value: Number(value) || 0,
    }));
  } catch (error) {
    console.warn("Failed to parse dashboard series", error);
    return [];
  }
}

function renderDashboardChart(node) {
  const series = parseDashboardSeries(node);
  const maxValue = series.reduce((max, item) => Math.max(max, item.value), 0);

  if (!series.length) {
    node.innerHTML = '<div class="admin-empty">暂无统计数据</div>';
    return;
  }

  node.innerHTML = series
    .map((item) => {
      const width = maxValue > 0 ? (item.value / maxValue) * 100 : 0;
      return `
        <div class="dashboard-chart-bar">
          <div class="dashboard-chart-meta">
            <strong>${item.label}</strong>
            <span>${item.value}</span>
          </div>
          <div class="dashboard-chart-track">
            <div class="dashboard-chart-fill" style="width: ${width}%"></div>
          </div>
        </div>
      `;
    })
    .join("");
}

document.addEventListener("DOMContentLoaded", () => {
  const page = document.querySelector('[data-page="admin-dashboard"]');
  if (!page) {
    return;
  }

  document.querySelectorAll("[data-dashboard-series]").forEach(renderDashboardChart);
});
