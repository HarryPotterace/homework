const scheduleStatus = document.getElementById("schedule-status");

if (scheduleStatus) {
  const apiUrl = scheduleStatus.dataset.scheduleApi;
  if (apiUrl) {
    fetch(apiUrl)
      .then((response) => response.json())
      .then((items) => {
        const availableCount = items.filter((item) => item.is_available).length;
        scheduleStatus.textContent = `已异步加载 ${items.length} 个预约时段，其中 ${availableCount} 个可预约。`;
      })
      .catch(() => {
        scheduleStatus.textContent = "预约时段状态刷新失败，请稍后重试。";
      });
  }
}
