const datos = JSON.parse(document.getElementById("datos-graficos").textContent);
const COLOR_ANIO = { 2024: "#3a97c9", 2025: "#3655b3" };
const CATEGORICOS = ["#3655b3", "#0e9a83", "#c27a14"];

Chart.defaults.font.family = "Inter, system-ui, sans-serif";
Chart.defaults.color = "#546273";
Chart.defaults.maintainAspectRatio = false;
Chart.defaults.plugins.legend.labels.usePointStyle = true;
Chart.defaults.plugins.tooltip.backgroundColor = "#141a2e";

const dolares = (v) => "US$ " + v.toLocaleString("en-US", { maximumFractionDigits: 0 });
const porciento = (v) => v.toFixed(2) + " %";
const rejilla = { color: "rgba(20,26,46,0.07)" };

function porAnio(id, etiquetas, serie, formato, horizontal = false) {
  const eje = { grid: rejilla, ticks: { callback: (v) => (formato === dolares ? (v / 1e6).toLocaleString("en-US") + " M" : v + " %") } };
  const categorias = { grid: { display: false } };
  new Chart(document.getElementById(id), {
    type: "bar",
    data: {
      labels: etiquetas,
      datasets: [2024, 2025].map((a) => ({ label: String(a), data: serie[a], backgroundColor: COLOR_ANIO[a], borderRadius: 4, maxBarThickness: 22 })),
    },
    options: {
      indexAxis: horizontal ? "y" : "x",
      scales: horizontal ? { x: eje, y: categorias } : { y: eje, x: categorias },
      plugins: { tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${formato(c.raw)}` } } },
    },
  });
}

function estructura(id, partes) {
  new Chart(document.getElementById(id), {
    type: "bar",
    data: {
      labels: ["2024", "2025"],
      datasets: partes.map((p, i) => ({ label: p.nombre, data: p.valores, backgroundColor: CATEGORICOS[i], borderColor: "#f4f7f9", borderWidth: { top: 2 }, maxBarThickness: 76 })),
    },
    options: {
      scales: { x: { stacked: true, grid: { display: false } }, y: { stacked: true, max: 100, grid: rejilla, ticks: { callback: (v) => v + " %" } } },
      plugins: { legend: { position: "bottom" }, tooltip: { callbacks: { label: (c) => `${c.dataset.label}: ${porciento(c.raw)}` } } },
    },
  });
}

porAnio("g-resultados", datos.resultados.etiquetas, datos.resultados, dolares, true);
porAnio("g-margenes", datos.margenes.etiquetas, datos.margenes, porciento, true);
estructura("g-activos", datos.activos);
estructura("g-financiamiento", datos.financiamiento);
