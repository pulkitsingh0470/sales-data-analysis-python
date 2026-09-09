import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Sales Intelligence | Analytics Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Theme / styling
# -----------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.block-container { max-width: 1500px; padding-top: 1.2rem; padding-bottom: 3rem; }

/* Background */
[data-testid="stAppViewContainer"] { background: #f6f7fb; }
[data-testid="stHeader"] { background: rgba(246,247,251,.85); }
[data-testid="stSidebar"] { background: #111827; }
[data-testid="stSidebar"] * { color: #e5e7eb !important; }
[data-testid="stSidebar"] .stMarkdown p { color: #9ca3af !important; }

/* Sidebar brand */
.brand { padding: 8px 2px 22px 2px; }
.brand-row { display:flex; align-items:center; gap:10px; }
.brand-icon { width:40px; height:40px; border-radius:12px; background:linear-gradient(135deg,#6366f1,#8b5cf6); display:flex; align-items:center; justify-content:center; font-size:21px; }
.brand-name { font-family:'Space Grotesk'; font-size:1.15rem; font-weight:700; color:white; }
.brand-sub { color:#9ca3af; font-size:.78rem; margin-top:2px; }

/* Hero */
.hero { background:linear-gradient(135deg,#111827 0%,#1e293b 55%,#312e81 100%); border-radius:24px; padding:30px 34px; color:white; position:relative; overflow:hidden; margin-bottom:22px; box-shadow:0 16px 40px rgba(15,23,42,.12); }
.hero:after { content:''; position:absolute; width:260px; height:260px; border-radius:50%; right:-70px; top:-100px; background:rgba(255,255,255,.08); }
.hero-kicker { color:#c4b5fd; text-transform:uppercase; letter-spacing:.12em; font-size:.74rem; font-weight:700; }
.hero-title { font-family:'Space Grotesk'; font-size:2.55rem; line-height:1.05; font-weight:700; margin:8px 0 10px; }
.hero-text { max-width:760px; color:#cbd5e1; font-size:.98rem; line-height:1.6; }
.status-pill { display:inline-block; margin-top:18px; padding:7px 11px; border-radius:999px; background:rgba(34,197,94,.14); color:#86efac; border:1px solid rgba(134,239,172,.2); font-size:.78rem; font-weight:600; }

/* KPI cards */
.kpi { background:white; border:1px solid #e5e7eb; border-radius:18px; padding:18px 19px; min-height:126px; box-shadow:0 5px 18px rgba(15,23,42,.04); }
.kpi-label { color:#6b7280; font-size:.8rem; font-weight:600; }
.kpi-value { font-family:'Space Grotesk'; font-size:1.72rem; font-weight:700; color:#111827; margin:7px 0 3px; }
.kpi-note { font-size:.76rem; color:#6b7280; }
.kpi-up { color:#16a34a; font-weight:700; }
.kpi-down { color:#dc2626; font-weight:700; }

/* Sections */
.section-title { font-family:'Space Grotesk'; font-size:1.35rem; font-weight:700; color:#111827; margin:24px 0 4px; }
.section-sub { color:#6b7280; font-size:.86rem; margin-bottom:14px; }
.panel { background:white; border:1px solid #e5e7eb; border-radius:18px; padding:16px 18px 8px; box-shadow:0 5px 18px rgba(15,23,42,.035); }

/* Insight cards */
.insight { background:#fff; border:1px solid #e5e7eb; border-radius:18px; padding:18px; min-height:155px; box-shadow:0 5px 18px rgba(15,23,42,.035); }
.insight-icon { font-size:1.45rem; }
.insight-label { color:#6b7280; font-size:.76rem; text-transform:uppercase; letter-spacing:.08em; margin-top:8px; }
.insight-title { font-family:'Space Grotesk'; font-size:1.05rem; font-weight:700; margin:5px 0; color:#111827; }
.insight-body { color:#6b7280; font-size:.82rem; line-height:1.45; }

/* Footer */
.footer { margin-top:32px; padding-top:18px; border-top:1px solid #e5e7eb; color:#6b7280; font-size:.78rem; }

/* Streamlit tabs */
.stTabs [data-baseweb="tab-list"] { gap:8px; }
.stTabs [data-baseweb="tab"] { border-radius:10px; padding:8px 14px; }

/* Dataframe */
[data-testid="stDataFrame"] { border-radius:14px; overflow:hidden; }
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv", parse_dates=["Date"]).drop_duplicates().dropna().copy()
    for col in ["Quantity", "UnitPrice", "TotalSale"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Day"] = df["Date"].dt.day_name()
    df["Month"] = df["Date"].dt.to_period("M").astype(str)
    df["MonthName"] = df["Date"].dt.strftime("%b %Y")
    return df

# remove accidental decorator helper if parser sees it as a variable

df = load_data()

# -----------------------------
# Sidebar filters
# -----------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
          <div class="brand-row">
            <div class="brand-icon">📊</div>
            <div>
              <div class="brand-name">SalesHub</div>
              <div class="brand-sub">Business analytics workspace</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Filters")
    st.caption("Build a focused view of your sales performance.")

    regions = sorted(df["Region"].unique())
    products = sorted(df["Product"].unique())

    selected_regions = st.multiselect("Regions", regions, default=regions)
    selected_products = st.multiselect("Products", products, default=products)

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()
    date_range = st.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

    st.markdown("---")
    st.markdown("**Dataset**")
    st.caption(f"{len(df):,} transactions • {len(products)} products • {len(regions)} regions")
    st.caption(f"Data window: {min_date:%d %b %Y} → {max_date:%d %b %Y}")

if len(date_range) == 2:
    start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
else:
    start_date, end_date = pd.Timestamp(min_date), pd.Timestamp(max_date)

filtered = df[
    df["Region"].isin(selected_regions)
    & df["Product"].isin(selected_products)
    & df["Date"].between(start_date, end_date)
].copy()

if filtered.empty:
    st.warning("No transactions match the selected filters. Try widening the date range or selecting more products/regions.")
    st.stop()

# -----------------------------
# KPIs + comparison
# -----------------------------
revenue = filtered["TotalSale"].sum()
orders = filtered["OrderID"].nunique()
units = filtered["Quantity"].sum()
aov = revenue / orders if orders else 0
avg_price = filtered["UnitPrice"].mean()

period_days = max((end_date - start_date).days + 1, 1)
prev_end = start_date - pd.Timedelta(days=1)
prev_start = prev_end - pd.Timedelta(days=period_days - 1)
previous = df[
    df["Region"].isin(selected_regions)
    & df["Product"].isin(selected_products)
    & df["Date"].between(prev_start, prev_end)
]
prev_revenue = previous["TotalSale"].sum()
prev_orders = previous["OrderID"].nunique()
prev_units = previous["Quantity"].sum()
prev_aov = prev_revenue / prev_orders if prev_orders else 0

def pct_change(current, previous_value):
    return ((current - previous_value) / previous_value * 100) if previous_value else None

rev_delta = pct_change(revenue, prev_revenue)
order_delta = pct_change(orders, prev_orders)
unit_delta = pct_change(units, prev_units)
aov_delta = pct_change(aov, prev_aov)

# -----------------------------
# Header / hero
# -----------------------------
st.markdown(
    f"""
    <div class="hero">
      <div class="hero-kicker">Sales intelligence • live filtered view</div>
      <div class="hero-title">Turn transactions into decisions.</div>
      <div class="hero-text">A realistic business dashboard for tracking revenue, orders, products and regional performance. Use the controls on the left to explore the dataset like an analyst would.</div>
      <div class="status-pill">● Data loaded successfully &nbsp;|&nbsp; {len(filtered):,} matching transactions</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Executive snapshot</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">The numbers that matter most for the selected period.</div>', unsafe_allow_html=True)

k1, k2, k3, k4, k5 = st.columns(5)

def kpi_html(label, value, note, delta=None):
    delta_html = ""
    if delta is not None:
        cls = "kpi-up" if delta >= 0 else "kpi-down"
        arrow = "↑" if delta >= 0 else "↓"
        delta_html = f'<span class="{cls}">{arrow} {abs(delta):.1f}%</span> vs previous period'
    else:
        delta_html = note
    return f'<div class="kpi"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{delta_html}</div></div>'

with k1: st.markdown(kpi_html("Revenue", f"₹{revenue:,.0f}", "", rev_delta), unsafe_allow_html=True)
with k2: st.markdown(kpi_html("Orders", f"{orders:,}", "", order_delta), unsafe_allow_html=True)
with k3: st.markdown(kpi_html("Units sold", f"{units:,.0f}", "", unit_delta), unsafe_allow_html=True)
with k4: st.markdown(kpi_html("Avg. order value", f"₹{aov:,.0f}", "", aov_delta), unsafe_allow_html=True)
with k5: st.markdown(kpi_html("Avg. unit price", f"₹{avg_price:,.0f}", "Selected period average"), unsafe_allow_html=True)

# -----------------------------
# Main analytics tabs
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Products", "Regions", "Transactions"])

# Shared calculations
daily = filtered.groupby("Date", as_index=False)["TotalSale"].sum().sort_values("Date")
daily["7-Day Average"] = daily["TotalSale"].rolling(7, min_periods=1).mean()

monthly = filtered.groupby("Month", as_index=False).agg(Revenue=("TotalSale", "sum"), Orders=("OrderID", "nunique"), Units=("Quantity", "sum"))
monthly["MonthLabel"] = pd.to_datetime(monthly["Month"]).dt.strftime("%b %Y")
monthly = monthly.sort_values("Month")

product_sales = filtered.groupby("Product", as_index=False).agg(
    Revenue=("TotalSale", "sum"), Units=("Quantity", "sum"), Orders=("OrderID", "nunique")
).sort_values("Revenue", ascending=False)
product_sales["Share"] = product_sales["Revenue"] / revenue * 100

region_sales = filtered.groupby("Region", as_index=False).agg(
    Revenue=("TotalSale", "sum"), Units=("Quantity", "sum"), Orders=("OrderID", "nunique")
).sort_values("Revenue", ascending=False)
region_sales["Share"] = region_sales["Revenue"] / revenue * 100

# -----------------------------
# Overview
# -----------------------------
with tab1:
    st.markdown('<div class="section-title">Revenue performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Daily revenue with a rolling 7-day trend to make spikes and slowdowns easier to spot.</div>', unsafe_allow_html=True)
    with st.container(border=True):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=daily["Date"], y=daily["TotalSale"], mode="lines", name="Daily revenue", line=dict(width=2.5)))
        fig.add_trace(go.Scatter(x=daily["Date"], y=daily["7-Day Average"], mode="lines", name="7-day average", line=dict(width=3, dash="dash")))
        fig.update_layout(height=410, margin=dict(l=15,r=15,t=10,b=15), hovermode="x unified", template="plotly_white", yaxis_title="Revenue (₹)", xaxis_title=None, legend=dict(orientation="h", y=1.08, x=0))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    o1, o2 = st.columns([1.35, 1])
    with o1:
        st.markdown('<div class="section-title">Monthly momentum</div>', unsafe_allow_html=True)
        with st.container(border=True):
            figm = go.Figure()
            figm.add_trace(go.Bar(x=monthly["MonthLabel"], y=monthly["Revenue"], name="Revenue", text=monthly["Revenue"], texttemplate="₹%{text:,.0f}", textposition="outside"))
            figm.update_layout(height=360, margin=dict(l=10,r=10,t=20,b=10), template="plotly_white", yaxis_title="Revenue (₹)", xaxis_title=None, showlegend=False)
            st.plotly_chart(figm, use_container_width=True, config={"displayModeBar": False})
    with o2:
        st.markdown('<div class="section-title">Revenue mix</div>', unsafe_allow_html=True)
        with st.container(border=True):
            figdonut = px.pie(product_sales, names="Product", values="Revenue", hole=.62)
            figdonut.update_layout(height=360, margin=dict(l=5,r=5,t=10,b=10), template="plotly_white", showlegend=True, legend=dict(font=dict(size=10)))
            figdonut.update_traces(textposition="inside", textinfo="percent")
            st.plotly_chart(figdonut, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-title">Business signals</div>', unsafe_allow_html=True)
    top_product = product_sales.iloc[0]
    top_region = region_sales.iloc[0]
    best_date_row = daily.loc[daily["TotalSale"].idxmax()]
    best_day = filtered.groupby("Day")["TotalSale"].sum().idxmax()
    avg_daily = daily["TotalSale"].mean()
    peak_multiple = best_date_row["TotalSale"] / avg_daily if avg_daily else 0

    i1, i2, i3, i4 = st.columns(4)
    cards = [
        ("🏆", "Top product", str(top_product["Product"]), f"₹{top_product['Revenue']:,.0f} revenue • {top_product['Share']:.1f}% of total"),
        ("🌍", "Leading region", str(top_region["Region"]), f"₹{top_region['Revenue']:,.0f} revenue • {top_region['Share']:.1f}% share"),
        ("⚡", "Peak sales day", f"{best_date_row['Date']:%d %b %Y}", f"₹{best_date_row['TotalSale']:,.0f} • {peak_multiple:.1f}× average day"),
        ("📅", "Strongest weekday", str(best_day), "Highest combined revenue across weekdays"),
    ]
    for col, card in zip([i1,i2,i3,i4], cards):
        with col:
            st.markdown(f'<div class="insight"><div class="insight-icon">{card[0]}</div><div class="insight-label">{card[1]}</div><div class="insight-title">{card[2]}</div><div class="insight-body">{card[3]}</div></div>', unsafe_allow_html=True)

# -----------------------------
# Products
# -----------------------------
with tab2:
    st.markdown('<div class="section-title">Product performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">See which products drive revenue and whether volume follows the same pattern.</div>', unsafe_allow_html=True)
    p1, p2 = st.columns([1.35, 1])
    with p1:
        with st.container(border=True):
            figp = px.bar(product_sales.sort_values("Revenue"), x="Revenue", y="Product", orientation="h", text="Revenue", hover_data=["Units","Orders","Share"])
            figp.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
            figp.update_layout(height=460, margin=dict(l=10,r=25,t=10,b=15), template="plotly_white", xaxis_title="Revenue (₹)", yaxis_title=None)
            st.plotly_chart(figp, use_container_width=True, config={"displayModeBar": False})
    with p2:
        with st.container(border=True):
            figu = px.scatter(product_sales, x="Units", y="Revenue", size="Orders", text="Product", hover_data=["Share"])
            figu.update_traces(textposition="top center")
            figu.update_layout(height=460, margin=dict(l=10,r=10,t=10,b=15), template="plotly_white", xaxis_title="Units sold", yaxis_title="Revenue (₹)")
            st.plotly_chart(figu, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-title">Product leaderboard</div>', unsafe_allow_html=True)
    product_table = product_sales.copy()
    product_table["Revenue"] = product_table["Revenue"].map(lambda x: f"₹{x:,.0f}")
    product_table["Share"] = product_table["Share"].map(lambda x: f"{x:.1f}%")
    st.dataframe(product_table[["Product","Revenue","Share","Units","Orders"]], use_container_width=True, hide_index=True)

# -----------------------------
# Regions
# -----------------------------
with tab3:
    st.markdown('<div class="section-title">Regional performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Compare markets by revenue, order count and sales volume.</div>', unsafe_allow_html=True)
    r1, r2 = st.columns([1.2, 1])
    with r1:
        with st.container(border=True):
            figr = px.bar(region_sales.sort_values("Revenue"), x="Region", y="Revenue", text="Revenue", hover_data=["Units","Orders","Share"])
            figr.update_traces(texttemplate="₹%{text:,.0f}", textposition="outside")
            figr.update_layout(height=420, margin=dict(l=10,r=10,t=10,b=15), template="plotly_white", yaxis_title="Revenue (₹)")
            st.plotly_chart(figr, use_container_width=True, config={"displayModeBar": False})
    with r2:
        with st.container(border=True):
            figr2 = px.pie(region_sales, names="Region", values="Revenue", hole=.58)
            figr2.update_layout(height=420, margin=dict(l=5,r=5,t=10,b=10), template="plotly_white")
            figr2.update_traces(textinfo="label+percent")
            st.plotly_chart(figr2, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-title">Product × region matrix</div>', unsafe_allow_html=True)
    with st.container(border=True):
        matrix = filtered.pivot_table(index="Product", columns="Region", values="TotalSale", aggfunc="sum", fill_value=0)
        heat = px.imshow(matrix, text_auto=".0f", aspect="auto", color_continuous_scale="Blues", labels=dict(x="Region", y="Product", color="Revenue"))
        heat.update_layout(height=460, margin=dict(l=10,r=10,t=10,b=10), template="plotly_white")
        st.plotly_chart(heat, use_container_width=True, config={"displayModeBar": False})

# -----------------------------
# Transactions
# -----------------------------
with tab4:
    st.markdown('<div class="section-title">Transaction explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">A clean operational view for checking individual orders behind the headline numbers.</div>', unsafe_allow_html=True)

    search = st.text_input("Search product / region / order ID", placeholder="e.g. Keyboard, North, 120")
    tx = filtered.copy()
    if search.strip():
        s = search.strip().lower()
        tx = tx[
            tx["Product"].str.lower().str.contains(s)
            | tx["Region"].str.lower().str.contains(s)
            | tx["OrderID"].astype(str).str.contains(s)
        ]

    tx = tx.sort_values("Date", ascending=False).copy()
    display_tx = tx.head(100).copy()
    display_tx["Date"] = display_tx["Date"].dt.strftime("%d %b %Y")
    display_tx["UnitPrice"] = display_tx["UnitPrice"].map(lambda x: f"₹{x:,.0f}")
    display_tx["TotalSale"] = display_tx["TotalSale"].map(lambda x: f"₹{x:,.2f}")
    st.caption(f"Showing {len(display_tx):,} of {len(tx):,} matching transactions")
    st.dataframe(display_tx[["OrderID","Date","Product","Region","Quantity","UnitPrice","TotalSale"]], use_container_width=True, hide_index=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    '<div class="footer">SalesHub Analytics • Built with Python, Pandas, Plotly & Streamlit • Internship project dashboard</div>',
    unsafe_allow_html=True,
)
