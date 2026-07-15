import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Customer Segmentation Dashboard (RFM + K-Means)",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CSS: TEMA BIRU-PUTIH, RAPI, KONTEN DITURUNKAN
# ============================================================
CUSTOM_CSS = """
<style>
:root {
  --bg: #e3f2fd;
  --card-bg: #ffffff;
  --accent: #1976d2;
  --accent-dark: #0d47a1;
  --text-main: #102027;
  --text-muted: #607d8b;
}

/* background utama app */
.stApp {
  background-color: var(--bg) !important;
  color: var(--text-main) !important;
}

/* header Streamlit */
header[data-testid="stHeader"] {
  background-color: var(--bg) !important;
}

/* sidebar: biru gradient */
[data-testid="stSidebar"] {
  background: linear-gradient(135deg, #bbdefb, #64b5f6) !important;
  color: var(--accent-dark) !important;
}
[data-testid="stSidebar"] * {
  color: var(--accent-dark) !important;
}

/* konten utama: turunkan semua isi supaya ga ketutupan header */
.block-container {
  padding-top: 4rem;  /* <<< ini yang bikin ga ketutupan lagi */
}

/* KPI custom cards */
.kpi-card {
  background: var(--card-bg);
  border-radius: 16px;
  padding: 14px 18px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
  border: 1px solid #bbdefb;
}
.kpi-title {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  margin-bottom: 2px;
}
.kpi-value {
  font-size: 1.9rem;
  font-weight: 700;
  color: var(--accent-dark);
}
.kpi-sub {
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-top: 4px;
}

/* judul section */
.section-title-basic {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--accent-dark);
  margin-bottom: 0.15rem;
}
.section-subtitle-basic {
  font-size: 0.9rem;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

/* insight cards */
.insight-card {
  background: var(--card-bg);
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
  padding: 14px 16px;
  border-left: 4px solid rgba(25, 118, 210, 0.6);
  margin-bottom: 0.9rem;
}
.insight-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--accent-dark);
}
.insight-tag {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 4px;
}
.insight-text {
  font-size: 0.9rem;
  color: var(--text-main);
}

/* label widget (Focus Segment, dll) */
label[data-testid="stWidgetLabel"] {
  color: var(--accent-dark) !important;
  font-weight: 500 !important;
  font-size: 0.95rem !important;
}

/* selectbox (Focus Segment) */
div[data-baseweb="select"] > div {
  background-color: #ffffff !important;
  border-radius: 999px !important;
  border: 1px solid #bbdefb !important;
}
div[data-baseweb="select"] span {
  color: var(--text-main) !important;  /* teks ALL jadi gelap dan kebaca */
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Plotly: tema putih + palet biru
px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = ["#1976d2", "#64b5f6", "#0d47a1"]

def kpi_card(title: str, value: str, sub: str) -> str:
    return f"""
    <div class="kpi-card">
      <div class="kpi-title">{title}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-sub">{sub}</div>
    </div>
    """

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_data(path: str):
    df = pd.read_csv(path)
    df = df[df["CustomerID"].notna()]

    if "cluster" in df.columns:
        df["cluster"] = df["cluster"].astype(int)
    elif "Cluster" in df.columns:
        df["cluster"] = df["Cluster"].astype(int)

    for col in ["Recency", "Frequency", "Monetary"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

try:
    df = load_data("rfm_cluster_result.csv")
except Exception as e:
    st.error(f"Gagal membaca rfm_cluster_result.csv: {e}")
    st.stop()

# ============================================================
# SIDEBAR NAV
# ============================================================
st.sidebar.title("Customer Segmentation Dashboard")
st.sidebar.caption("RFM Analysis + K-Means Clustering")

page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Dataset", "Clustering", "Segments & Insights"],
    index=0
)

# ============================================================
# HELPER: AGGREGATE BY CLUSTER
# ============================================================
def aggregate_by_cluster(df_, filter_segment="ALL"):
    d = df_.copy()
    if filter_segment != "ALL" and "Segment" in d.columns:
        d = d[d["Segment"] == filter_segment]

    if d.empty:
        return pd.DataFrame()

    if "Segment" not in d.columns:
        d["Segment"] = "Segment_" + d["cluster"].astype(str)

    agg = (
        d.groupby(["cluster", "Segment"], as_index=False)
        .agg(
            numCustomers=("CustomerID", "nunique"),
            totalRevenue=("Monetary", "sum"),
            recencyMean=("Recency", "mean"),
            freqMean=("Frequency", "mean"),
            monMean=("Monetary", "mean"),
        )
        .sort_values("cluster")
    )
    return agg

# ============================================================
# OVERVIEW PAGE
# ============================================================
if page == "Overview":
    st.markdown('<div class="section-title-basic">Overview</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle-basic">'
        'Ringkasan metrik utama dari hasil analisis RFM dan K-Means clustering.'
        '</div>',
        unsafe_allow_html=True,
    )

    # KPI cards
    col1, col2, col3, col4 = st.columns(4)

    total_customers = df["CustomerID"].nunique()
    total_revenue = df["Monetary"].sum()
    avg_monetary = total_revenue / total_customers if total_customers > 0 else 0
    n_clusters = df["cluster"].nunique()

    with col1:
        st.markdown(
            kpi_card("Total Customers",
                     f"{total_customers:,.0f}",
                     "Unique customers in dataset"),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            kpi_card("Total Revenue",
                     f"{total_revenue:,.0f}",
                     "Sum of Monetary across customers"),
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            kpi_card("Avg Monetary / Customer",
                     f"{avg_monetary:,.0f}",
                     "Average spending per customer"),
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            kpi_card("Number of Clusters",
                     str(int(n_clusters)),
                     "K-Means segments"),
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # Segment filter
    segs = ["ALL"]
    if "Segment" in df.columns:
        segs += sorted(df["Segment"].dropna().unique().tolist())
    focus_segment = st.selectbox("Focus Segment", segs)

    agg = aggregate_by_cluster(df, filter_segment=focus_segment)
    if agg.empty:
        st.warning("Tidak ada data untuk segment tersebut.")
    else:
        c1, c2 = st.columns(2)

        with c1:
            st.markdown(
                '<div class="section-title-basic">Distribution of Customers</div>'
                '<div class="section-subtitle-basic">'
                'Jumlah pelanggan per segment/cluster.'
                '</div>',
                unsafe_allow_html=True,
            )
            fig_cust = px.bar(
                agg,
                x="Segment",
                y="numCustomers",
                labels={"Segment": "Segment", "numCustomers": "Number of Customers"},
            )
            fig_cust.update_layout(
                height=420,
                xaxis_title="",
                yaxis_title="Customers",
                font=dict(size=14, color="#102027"),
                paper_bgcolor="white",
                plot_bgcolor="white",
            )
            st.plotly_chart(fig_cust, use_container_width=True, theme=None)

        with c2:
            st.markdown(
                '<div class="section-title-basic">Distribution of Revenue</div>'
                '<div class="section-subtitle-basic">'
                'Kontribusi revenue per segment/cluster.'
                '</div>',
                unsafe_allow_html=True,
            )
            fig_rev = px.bar(
                agg,
                x="Segment",
                y="totalRevenue",
                labels={"Segment": "Segment", "totalRevenue": "Total Revenue"},
            )
            fig_rev.update_layout(
                height=420,
                xaxis_title="",
                yaxis_title="Revenue",
                font=dict(size=14, color="#102027"),
                paper_bgcolor="white",
                plot_bgcolor="white",
            )
            st.plotly_chart(fig_rev, use_container_width=True, theme=None)

# ============================================================
# DATASET PAGE
# ============================================================
elif page == "Dataset":
    st.markdown(
        '<div class="section-title-basic">Dataset RFM + Cluster</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle-basic">'
        'Pratinjau data hasil pengolahan RFM dan clustering (50 baris pertama).'
        '</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(df.head(50), use_container_width=True, height=500)

# ============================================================
# CLUSTERING PAGE
# ============================================================
elif page == "Clustering":
    st.markdown(
        '<div class="section-title-basic">RFM Profile per Cluster</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle-basic">'
        'Rata-rata Recency (hari), Frequency (jumlah transaksi), dan Monetary (nilai belanja) per cluster.'
        '</div>',
        unsafe_allow_html=True,
    )

    agg_all = aggregate_by_cluster(df, filter_segment="ALL")
    if agg_all.empty:
        st.warning("Data agregasi cluster kosong.")
    else:
        # ===================== CHART: 3 FASET PER METRIK =====================
        # pakai nilai asli, bukan normalized 0–1
        rfm_melt = agg_all.melt(
            id_vars=["cluster", "Segment"],
            value_vars=["recencyMean", "freqMean", "monMean"],
            var_name="Metric",
            value_name="Value",
        )

        rfm_melt["Metric"] = rfm_melt["Metric"].map(
            {
                "recencyMean": "Recency (days)",
                "freqMean": "Frequency",
                "monMean": "Monetary",
            }
        )

        fig_rfm = px.bar(
            rfm_melt,
            x="Segment",
            y="Value",
            facet_col="Metric",          # 3 panel: Recency, Frequency, Monetary
            color="Metric",
            facet_col_spacing=0.06,
        )
        # tiap metrik punya skala Y sendiri, jadi batang kecil juga kelihatan
        fig_rfm.update_yaxes(matches=None)
        fig_rfm.update_layout(
            height=450,
            xaxis_title="",
            yaxis_title="Value",
            font=dict(size=14, color="#102027"),
            legend=dict(
                orientation="h",
                y=-1.15,
                x=0.5,
                xanchor="center",
                yanchor="bottom",
                title_text=""
            ),
            margin=dict(t=90, b=60),
            paper_bgcolor="white",
            plot_bgcolor="white",
        )
        st.plotly_chart(fig_rfm, use_container_width=True, theme=None)

        # ===================== TABEL RINGKASAN (tetap sama) =====================
        st.markdown("---")
        st.markdown(
            '<div class="section-title-basic">Ringkasan Statistik per Cluster</div>',
            unsafe_allow_html=True,
        )

        summary_df = agg_all.copy()
        summary_df["totalRevenue"] = summary_df["totalRevenue"].round(0)
        summary_df["recencyMean"] = summary_df["recencyMean"].round(1)
        summary_df["freqMean"] = summary_df["freqMean"].round(2)
        summary_df["monMean"] = summary_df["monMean"].round(1)

        summary_df = summary_df.rename(
            columns={
                "cluster": "Cluster",
                "Segment": "Segment",
                "numCustomers": "# Customers",
                "totalRevenue": "Total Revenue",
                "recencyMean": "Avg Recency",
                "freqMean": "Avg Frequency",
                "monMean": "Avg Monetary",
            }
        )

        st.dataframe(summary_df, use_container_width=True, height=400)

# ============================================================
# SEGMENTS & INSIGHTS PAGE
# ============================================================
elif page == "Segments & Insights":
    st.markdown(
        '<div class="section-title-basic">Business Insights per Segment</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="section-subtitle-basic">'
        'Interpretasi hasil segmentasi dan rekomendasi strategi pemasaran untuk tiap segmen.'
        '</div>',
        unsafe_allow_html=True,
    )

    if "Segment" not in df.columns:
        st.warning("Kolom 'Segment' tidak ditemukan di dataset.")
    else:
        seg_group = (
            df.groupby("Segment", as_index=False)
            .agg(
                customers=("CustomerID", "nunique"),
                revenue=("Monetary", "sum"),
            )
        )

        total_c = seg_group["customers"].sum()
        total_r = seg_group["revenue"].sum()

        template_texts = {
            "High-Value / VIP Customers": {
                "title": "High-Value / VIP Customers",
                "text": (
                    "Pelanggan dengan kontribusi pendapatan terbesar. Frekuensi pembelian tinggi dan nilai transaksi besar. "
                    "Fokus utama: retensi. Terapkan program VIP/loyalty eksklusif, layanan prioritas, early access produk, "
                    "dan penawaran yang sangat personal untuk mencegah churn."
                ),
            },
            "Loyal Mid-Value Customers": {
                "title": "Loyal Mid-Value Customers",
                "text": (
                    "Pelanggan aktif dengan recency terbaik dan frekuensi tinggi, namun nilai belanja masih menengah. "
                    "Dorong naik kelas jadi VIP lewat cross-sell, upsell, bundling paket, serta program poin loyalitas "
                    "dan rekomendasi produk yang relevan."
                ),
            },
            "Occasional Low-Value Customers": {
                "title": "Occasional Low-Value Customers",
                "text": (
                    "Pelanggan yang berbelanja sesekali dengan nilai transaksi rendah. Masih cukup recent sehingga masih punya potensi tumbuh. "
                    "Fokus pada kampanye peningkatan frekuensi: promo paket hemat, storytelling produk, dan reminder ringan."
                ),
            },
            "Lost / Dormant Low-Value": {
                "title": "Lost / Dormant Low-Value",
                "text": (
                    "Pelanggan yang sudah lama tidak bertransaksi dengan nilai belanja rendah. Cocok untuk kampanye reaktivasi biaya rendah "
                    "seperti diskon sekali pakai atau email win-back. Kalau respons rendah, jangan terlalu banyak alokasi budget ke sini."
                ),
            },
        }

        col_left, col_right = st.columns(2)

        for i, row in seg_group.iterrows():
            seg_name = row["Segment"]
            share_c = (row["customers"] / total_c * 100) if total_c > 0 else 0
            share_r = (row["revenue"] / total_r * 100) if total_r > 0 else 0

            info = template_texts.get(
                seg_name,
                {
                    "title": seg_name,
                    "text": "Segment ini belum memiliki deskripsi khusus. Tambahkan insight manual sesuai kebutuhan bisnis.",
                },
            )

            card_html = f"""
            <div class="insight-card">
              <div class="insight-title">{info['title']}</div>
              <div class="insight-tag">
                ~{share_c:.1f}% customers · ~{share_r:.1f}% revenue
              </div>
              <div class="insight-text">{info['text']}</div>
            </div>
            """

            if i % 2 == 0:
                col_left.markdown(card_html, unsafe_allow_html=True)
            else:
                col_right.markdown(card_html, unsafe_allow_html=True)
