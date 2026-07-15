// app.js

let rfmData = [];
let customersChart, revenueChart, rfmChart;

document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  loadCSV();
});

// ======================== NAVIGATION ========================

function setupNavigation() {
  const buttons = document.querySelectorAll(".nav-btn");
  const pages = document.querySelectorAll(".page");

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const target = btn.getAttribute("data-page");

      buttons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");

      pages.forEach((p) => p.classList.remove("active"));
      document.getElementById(`page-${target}`).classList.add("active");
    });
  });
}

// ======================== LOAD CSV ========================

function loadCSV() {
  Papa.parse("rfm_cluster_result.csv", {
    download: true,
    header: true,
    dynamicTyping: true,
    skipEmptyLines: true,
    complete: (results) => {
      // Filter baris kosong / invalid CustomerID
      rfmData = results.data.filter((row) => row.CustomerID !== undefined && row.CustomerID !== null && row.CustomerID !== "");
      console.log("RFM rows loaded:", rfmData.length);

      initDashboard();
    },
    error: (err) => {
      console.error("Error loading CSV:", err);
      alert("Gagal load rfm_cluster_result.csv. Pastikan file ada di folder yang sama dengan index.html.");
    }
  });
}

// ======================== INIT DASHBOARD ========================

function initDashboard() {
  fillKPIs();
  fillSegmentFilter();
  buildDatasetTable();
  buildClusterAggregatesAndCharts("ALL");
  buildClusterSummaryTable();
  buildInsightCards();

  // Event untuk filter segment
  const segFilter = document.getElementById("segmentFilter");
  segFilter.addEventListener("change", (e) => {
    buildClusterAggregatesAndCharts(e.target.value);
  });
}

// ======================== KPI ========================

function fillKPIs() {
  const customerSet = new Set(rfmData.map((d) => d.CustomerID));
  const totalCustomers = customerSet.size;

  const totalRevenue = rfmData.reduce((sum, d) => sum + Number(d.Monetary || 0), 0);
  const avgMonetary = totalRevenue / totalCustomers;

  const clusterSet = new Set(rfmData.map((d) => d.cluster ?? d.Cluster));
  const nClusters = clusterSet.size;

  document.getElementById("kpi-customers").textContent = totalCustomers.toLocaleString();
  document.getElementById("kpi-revenue").textContent = totalRevenue.toLocaleString();
  document.getElementById("kpi-avg-monetary").textContent = Math.round(avgMonetary).toLocaleString();
  document.getElementById("kpi-clusters").textContent = nClusters;
}

// ======================== SEGMENT FILTER ========================

function fillSegmentFilter() {
  const segFilter = document.getElementById("segmentFilter");
  const segments = Array.from(new Set(rfmData.map((d) => d.Segment))).sort();

  segments.forEach((seg) => {
    const opt = document.createElement("option");
    opt.value = seg;
    opt.textContent = seg;
    segFilter.appendChild(opt);
  });
}

// ======================== DATASET TABLE ========================

function buildDatasetTable() {
  const headerRow = document.getElementById("datasetHeaderRow");
  const body = document.getElementById("datasetBody");

  if (rfmData.length === 0) return;

  // buat header dari key di row pertama
  const columns = Object.keys(rfmData[0]);
  columns.forEach((col) => {
    const th = document.createElement("th");
    th.textContent = col;
    headerRow.appendChild(th);
  });

  // isi 50 baris pertama
  const sampleRows = rfmData.slice(0, 50);
  sampleRows.forEach((row) => {
    const tr = document.createElement("tr");
    columns.forEach((col) => {
      const td = document.createElement("td");
      td.textContent = row[col];
      tr.appendChild(td);
    });
    body.appendChild(tr);
  });
}

// ======================== AGGREGATE PER CLUSTER ========================

function aggregateByCluster(filterSegment = "ALL") {
  const clusterMap = {};

  rfmData.forEach((row) => {
    const cluster = Number(row.cluster ?? row.Cluster);
    const segment = row.Segment || `Segment_${cluster}`;

    if (filterSegment !== "ALL" && segment !== filterSegment) return;

    if (!clusterMap[cluster]) {
      clusterMap[cluster] = {
        cluster,
        segment,
        numCustomers: 0,
        totalRevenue: 0,
        recencySum: 0,
        freqSum: 0,
        monSum: 0
      };
    }

    const m = Number(row.Monetary || 0);
    const r = Number(row.Recency || 0);
    const f = Number(row.Frequency || 0);

    clusterMap[cluster].numCustomers += 1;
    clusterMap[cluster].totalRevenue += m;
    clusterMap[cluster].recencySum += r;
    clusterMap[cluster].freqSum += f;
    clusterMap[cluster].monSum += m;
  });

  const clusters = Object.values(clusterMap).sort((a, b) => a.cluster - b.cluster);

  clusters.forEach((c) => {
    c.recencyMean = c.numCustomers > 0 ? c.recencySum / c.numCustomers : 0;
    c.freqMean = c.numCustomers > 0 ? c.freqSum / c.numCustomers : 0;
    c.monMean = c.numCustomers > 0 ? c.monSum / c.numCustomers : 0;
  });

  return clusters;
}

// ======================== CHARTS ========================

function buildClusterAggregatesAndCharts(filterSegment = "ALL") {
  const clusterAgg = aggregateByCluster(filterSegment);
  if (!clusterAgg.length) return;

  const labels = clusterAgg.map((d) => d.segment);
  const customers = clusterAgg.map((d) => d.numCustomers);
  const revenue = clusterAgg.map((d) => d.totalRevenue);

  const rec = clusterAgg.map((d) => d.recencyMean);
  const freq = clusterAgg.map((d) => d.freqMean);
  const mon = clusterAgg.map((d) => d.monMean);

  const ctxCust = document.getElementById("customersChart").getContext("2d");
  const ctxRev = document.getElementById("revenueChart").getContext("2d");
  const ctxRfm = document.getElementById("rfmChart").getContext("2d");

  if (customersChart) customersChart.destroy();
  if (revenueChart) revenueChart.destroy();
  if (rfmChart) rfmChart.destroy();

  customersChart = new Chart(ctxCust, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Number of Customers",
          data: customers,
          borderRadius: 10,
          backgroundColor: "rgba(25, 118, 210, 0.85)"
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } }
    }
  });

  revenueChart = new Chart(ctxRev, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Total Revenue",
          data: revenue,
          borderRadius: 10,
          backgroundColor: "rgba(100, 181, 246, 0.95)"
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } }
    }
  });

  rfmChart = new Chart(ctxRfm, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Recency (days)",
          data: rec,
          backgroundColor: "rgba(144, 202, 249, 0.95)", // Biru Muda
          yAxisID: 'rec_mon_axis' // Sumbu Y Bersama Kiri
        },
        {
          label: "Frequency",
          data: freq,
          backgroundColor: "rgba(255, 99, 132, 0.9)", // Warna Kontras (Merah)
          yAxisID: 'freq_axis' // Sumbu Y Khusus Kanan
        },
        {
          label: "Monetary",
          data: mon,
          backgroundColor: "rgba(21, 101, 192, 0.9)", // Biru Tua
          yAxisID: 'rec_mon_axis' // Sumbu Y Bersama Kiri
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        // Sumbu Kiri: Untuk Recency dan Monetary (skala lebih besar)
        rec_mon_axis: {
          type: 'linear',
          position: 'left',
          beginAtZero: true,
          title: { display: true, text: 'Recency (Days) / Monetary (Value)' },
          // Pastikan Monetary (value) dan Recency (days) menggunakan skala ini
        },
        // Sumbu Kanan: Untuk Frequency (skala kecil)
        freq_axis: {
          type: 'linear',
          position: 'right',
          beginAtZero: true,
          grid: { drawOnChartArea: false }, // Penting: Menyembunyikan grid dari sumbu kanan agar grafik tidak terlalu ramai
          title: { display: true, text: 'Frequency (Count)' }
        }
      }
    }
  });
}

// ======================== CLUSTER SUMMARY TABLE ========================

function buildClusterSummaryTable() {
  const tbody = document.getElementById("clusterSummaryBody");
  tbody.innerHTML = "";

  const aggAll = aggregateByCluster("ALL");
  aggAll.forEach((c) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${c.cluster}</td>
      <td>${c.segment}</td>
      <td>${c.numCustomers.toLocaleString()}</td>
      <td>${Math.round(c.totalRevenue).toLocaleString()}</td>
      <td>${c.recencyMean.toFixed(1)}</td>
      <td>${c.freqMean.toFixed(2)}</td>
      <td>${c.monMean.toFixed(1)}</td>
    `;
    tbody.appendChild(tr);
  });
}

// ======================== INSIGHT CARDS ========================

function buildInsightCards() {
  const container = document.getElementById("insightGrid");
  container.innerHTML = "";

  // agregasi per Segment
  const segMap = {};
  rfmData.forEach((row) => {
    const seg = row.Segment || "Unknown";
    if (!segMap[seg]) {
      segMap[seg] = { seg, customers: 0, revenue: 0 };
    }
    segMap[seg].customers += 1;
    segMap[seg].revenue += Number(row.Monetary || 0);
  });

  const segArr = Object.values(segMap);
  const totalCust = segArr.reduce((s, x) => s + x.customers, 0);
  const totalRev = segArr.reduce((s, x) => s + x.revenue, 0);

  const templateTexts = {
    "High-Value / VIP Customers": {
      title: "High-Value / VIP Customers",
      text:
        "Pelanggan dengan kontribusi pendapatan terbesar. Frekuensi pembelian tinggi dan nilai transaksi besar. " +
        "Fokus utama: retensi. Terapkan program VIP/loyalty eksklusif, layanan prioritas, early access produk, dan penawaran sangat personal untuk mencegah churn."
    },
    "Loyal Mid-Value Customers": {
      title: "Loyal Mid-Value Customers",
      text:
        "Pelanggan aktif dengan recency terbaik dan frekuensi tinggi, namun nilai belanja masih menengah. " +
        "Strategi: dorong naik kelas menjadi VIP melalui cross-sell, upsell, bundling paket, serta program poin loyalitas dan rekomendasi produk yang relevan."
    },
    "Occasional Low-Value Customers": {
      title: "Occasional Low-Value Customers",
      text:
        "Pelanggan yang berbelanja sesekali dengan nilai transaksi rendah. Masih cukup recent sehingga punya potensi ditingkatkan. " +
        "Fokus pada kampanye peningkatan frekuensi: promo paket hemat, storytelling produk, dan reminder ringan."
    },
    "Lost / Dormant Low-Value": {
      title: "Lost / Dormant Low-Value",
      text:
        "Pelanggan yang sudah lama tidak bertransaksi dengan nilai belanja rendah. Cocok untuk kampanye reaktivasi berbiaya rendah seperti diskon sekali pakai atau email win-back. " +
        "Jika respons rendah, jangan mengalokasikan terlalu banyak anggaran di segmen ini."
    }
  };

  segArr.forEach((s) => {
    const shareCust = (s.customers / totalCust) * 100;
    const shareRev = (s.revenue / totalRev) * 100;

    const info = templateTexts[s.seg] || {
      title: s.seg,
      text: "Segment ini belum memiliki deskripsi khusus. Tambahkan insight manual sesuai kebutuhan bisnis."
    };

    const div = document.createElement("div");
    div.className = "insight-card";
    div.innerHTML = `
      <div class="insight-title">${info.title}</div>
      <div class="insight-tag">
        ~${shareCust.toFixed(1)}% customers · ~${shareRev.toFixed(1)}% revenue
      </div>
      <div class="insight-text">${info.text}</div>
    `;
    container.appendChild(div);
  });
}

