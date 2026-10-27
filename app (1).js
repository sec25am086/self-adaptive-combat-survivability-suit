const $ = (id) => document.getElementById(id);

async function post(url) {
  const r = await fetch(url, { method: "POST" });
  return r.json();
}

function setStatus(s) {
  const el = $("collector-status");
  el.textContent = s;
  el.className = s.toLowerCase();
}

$("btn-start").onclick = async () => setStatus((await post("/api/collector/start")).status);
$("btn-stop").onclick = async () => setStatus((await post("/api/collector/stop")).status);

async function refreshSensors() {
  const d = await (await fetch("/api/sensors")).json();
  $("s-temp").textContent = d.temperature_c;
  $("s-hum").textContent = d.humidity_pct;
  $("s-pm").textContent = d.pm2_5;
  $("s-gas").textContent = d.gas_ppm;
  $("s-light").textContent = d.light_lux;
}
$("btn-refresh").onclick = refreshSensors;

function drawMatrix(pattern) {
  const m = $("matrix");
  m.innerHTML = "";
  pattern.flat().forEach(([r, g, b]) => {
    const px = document.createElement("div");
    px.style.background = `rgb(${r},${g},${b})`;
    m.appendChild(px);
  });
}

$("btn-detect").onclick = async () => {
  const file = $("image-input").files[0];
  if (!file) { $("detect-result").textContent = "Please choose an image first."; return; }
  const fd = new FormData();
  fd.append("image", file);
  const res = await fetch("/api/detect", { method: "POST", body: fd });
  const d = await res.json();
  if (d.error) { $("detect-result").textContent = d.error; return; }
  $("detect-result").textContent =
    `Terrain: ${d.terrain} | Confidence: ${(d.confidence * 100).toFixed(1)}% | Avg RGB: ${d.average_rgb.join(", ")}`;
  drawMatrix(d.pattern);
};

$("btn-data").onclick = async () => {
  const rows = await (await fetch("/api/data")).json();
  const t = $("data-table");
  const cols = Object.keys(rows[0]);
  t.innerHTML = "<tr>" + cols.map((c) => `<th>${c}</th>`).join("") + "</tr>" +
    rows.map((r) => "<tr>" + cols.map((c) => `<td>${r[c]}</td>`).join("") + "</tr>").join("");
};

fetch("/api/collector/status").then((r) => r.json()).then((d) => setStatus(d.status));
