import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="SalesHub | Sales Intelligence", page_icon="📊", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:Inter,sans-serif}
.stApp{background:#f5f7fb}
[data-testid="stSidebar"]{background:#101827}
[data-testid="stSidebar"] *{color:#e8edf7!important}
.block-container{max-width:1500px;padding-top:2rem}
.hero{background:linear-gradient(115deg,#111b2e,#202c52,#3f3488);border-radius:24px;padding:34px 38px;color:white;margin-bottom:28px;box-shadow:0 18px 45px rgba(29,42,76,.18);animation:up .5s ease}
.hero .eyebrow{color:#b8a9ff;font-size:13px;font-weight:800;letter-spacing:1.7px}
.hero h1{margin:8px 0;font-size:clamp(32px,4vw,52px);font-weight:800}
.hero p{color:#d9e0f0;line-height:1.7;max-width:900px}
.status{display:inline-block;background:rgba(40,220,150,.13);border:1px solid rgba(40,220,150,.35);color:#65efb1;border-radius:999px;padding:8px 13px;font-size:13px;font-weight:700}
.section{font-size:25px;font-weight:800;color:#111827;margin-top:18px}
.sub{color:#697386;margin-bottom:18px}
.kpi{background:white;border:1px solid #e7eaf0;border-radius:18px;padding:20px 22px;min-height:125px;box-shadow:0 8px 24px rgba(17,24,39,.05);transition:.2s}
.kpi:hover{transform:translateY(-3px);box-shadow:0 14px 30px rgba(17,24,39,.09)}
.kpi-label{color:#697386;font-size:13px;font-weight:700;text-transform:uppercase;letter-spacing:.6px}
.kpi-value{color:#111827;font-size:30px;font-weight:800;margin-top:8px}
.kpi-note{color:#778196;font-size:12px;margin-top:6px}
.insight,.product-card{background:white;border:1px solid #e7eaf0;border-radius:18px;padding:18px 20px;box-shadow:0 8px 24px rgba(17,24,39,.04);height:100%}
.insight-title{font-weight:800;color:#182033;margin-bottom:6px}
.insight-text,.product-meta{color:#687387;font-size:13px;line-height:1.55}
.product-name{font-weight:800;color:#182033}
.product-revenue{font-size:22px;font-weight:800;color:#4f46e5;margin-top:8px}
.footer{margin-top:40px;padding:24px 0 5px;border-top:1px solid #e1e5ec;color:#7a8495;font-size:12px;text-align:center}
@keyframes up{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
</style>
""", unsafe_allow_html=True)

DATA = Path(__file__).with_name("sales_data.csv")

@st.cache_data
def load_data():
    d = pd.read_csv(DATA, parse_dates=["Date"]).drop_duplicates().dropna().copy()
    d["Revenue"] = d["TotalSale"].astype(float)
    d["Month"] = d["Date"].dt.to_period("M").astype(str)
    d["MonthLabel"] = d["Date"].dt.strftime("%b %Y")
    return d

df = load_data()

with st.sidebar:
    st.markdown("## 📊 SalesHub")
    st.caption("Business analytics workspace")
    st.markdown("### Filters")
    regions = sorted(df.Region.unique())
    products = sorted(df.Product.unique())
    sr = st.multiselect("Regions", regions, default=regions)
    sp = st.multiselect("Products", products, default=products)
    dr = st.date_input("Date range", (df.Date.min().date(), df.Date.max().date()),
                       min_value=df.Date.min().date(), max_value=df.Date.max().date())
    st.divider()
    st.markdown("### Dataset")
    st.caption(f"{len(df):,} total transactions")
    st.caption(f"{df.Date.min():%d %b %Y} → {df.Date.max():%d %b %Y}")
    st.caption(f"{df.Product.nunique()} products • {df.Region.nunique()} regions")

f = df[df.Region.isin(sr) & df.Product.isin(sp)].copy()
if len(dr) == 2:
    f = f[(f.Date >= pd.Timestamp(dr[0])) & (f.Date <= pd.Timestamp(dr[1]))]
if f.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

revenue = f.Revenue.sum()
orders = len(f)
units = f.Quantity.sum()
aov = revenue / orders
avg_price = f.UnitPrice.mean()
prod = f.groupby("Product").Revenue.sum().sort_values(ascending=False)
reg = f.groupby("Region").Revenue.sum().sort_values(ascending=False)

st.markdown(f"""
<div class="hero">
<div class="eyebrow">SALES INTELLIGENCE • LIVE FILTERED VIEW</div>
<h1>Turn transactions into decisions.</h1>
<p>A realistic business dashboard for tracking revenue, orders, products and regional performance.
Use the controls on the left to explore the dataset like an analyst.</p>
<span class="status">● Data loaded successfully &nbsp;|&nbsp; {orders:,} matching transactions</span>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section">Executive snapshot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">The numbers that matter most for the selected period.</div>', unsafe_allow_html=True)

cards = [("Revenue", f"₹{revenue:,.0f}", "Selected period"),
         ("Orders", f"{orders:,}", "Transactions"),
         ("Units sold", f"{units:,}", "Quantity across orders"),
         ("Avg. order value", f"₹{aov:,.0f}", "Revenue ÷ orders"),
         ("Avg. unit price", f"₹{avg_price:,.0f}", "Selected period average")]
cols = st.columns(5)
for c,(a,b,d) in zip(cols,cards):
    c.markdown(f'<div class="kpi"><div class="kpi-label">{a}</div><div class="kpi-value">{b}</div><div class="kpi-note">{d}</div></div>', unsafe_allow_html=True)

t1,t2,t3,t4 = st.tabs(["Overview","Products","Regions","Transactions"])

with t1:
    st.markdown('<div class="section">Revenue performance</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub">Daily revenue with a 7-day rolling trend.</div>', unsafe_allow_html=True)
    daily=f.groupby("Date",as_index=False).Revenue.sum().sort_values("Date")
    daily["7-day average"]=daily.Revenue.rolling(7,min_periods=1).mean()
    fig=go.Figure()
    fig.add_trace(go.Scatter(x=daily.Date,y=daily.Revenue,mode="lines+markers",name="Daily revenue",line=dict(width=2.5)))
    fig.add_trace(go.Scatter(x=daily.Date,y=daily["7-day average"],mode="lines",name="7-day average",line=dict(width=2,dash="dash")))
    fig.update_layout(height=390,margin=dict(l=10,r=10,t=15,b=10),plot_bgcolor="white",paper_bgcolor="white",hovermode="x unified")
    fig.update_yaxes(tickprefix="₹",gridcolor="#edf0f5")
    fig.update_xaxes(showgrid=False)
    st.plotly_chart(fig,use_container_width=True)

    a,b=st.columns(2)
    with a:
        st.markdown('<div class="section">Monthly revenue</div>',unsafe_allow_html=True)
        m=f.groupby(["Month","MonthLabel"],as_index=False).Revenue.sum().sort_values("Month")
        fm=px.bar(m,x="MonthLabel",y="Revenue",text_auto=".2s")
        fm.update_layout(height=350,margin=dict(l=10,r=10,t=15,b=10),plot_bgcolor="white",paper_bgcolor="white")
        fm.update_yaxes(tickprefix="₹",gridcolor="#edf0f5")
        fm.update_xaxes(showgrid=False)
        st.plotly_chart(fm,use_container_width=True)
    with b:
        st.markdown('<div class="section">Sales by region</div>',unsafe_allow_html=True)
        rr=reg.reset_index()
        fr=px.pie(rr,names="Region",values="Revenue",hole=.62)
        fr.update_layout(height=350,margin=dict(l=10,r=10,t=15,b=10),paper_bgcolor="white")
        st.plotly_chart(fr,use_container_width=True)

    st.markdown('<div class="section">Quick insights</div>',unsafe_allow_html=True)
    i1,i2,i3=st.columns(3)
    peak=daily.loc[daily.Revenue.idxmax()]
    insights=[
        ("🏆 Best product",f"{prod.index[0]} generated ₹{prod.iloc[0]:,.0f}."),
        ("📍 Leading region",f"{reg.index[0]} leads with ₹{reg.iloc[0]:,.0f} revenue."),
        ("📈 Peak sales day",f"{peak.Date:%d %b %Y} recorded ₹{peak.Revenue:,.0f}.")]
    for c,(title,text) in zip([i1,i2,i3],insights):
        c.markdown(f'<div class="insight"><div class="insight-title">{title}</div><div class="insight-text">{text}</div></div>',unsafe_allow_html=True)

with t2:
    ps=f.groupby("Product").agg(Revenue=("Revenue","sum"),Units=("Quantity","sum"),Orders=("OrderID","count")).reset_index().sort_values("Revenue",ascending=False)
    st.markdown('<div class="section">Product performance</div>',unsafe_allow_html=True)
    st.markdown('<div class="sub">Compare revenue contribution, units sold and order volume.</div>',unsafe_allow_html=True)
    fp=px.bar(ps.sort_values("Revenue"),x="Revenue",y="Product",orientation="h",text_auto=".2s")
    fp.update_layout(height=430,margin=dict(l=10,r=10,t=15,b=10),plot_bgcolor="white",paper_bgcolor="white")
    fp.update_xaxes(tickprefix="₹",gridcolor="#edf0f5")
    fp.update_yaxes(showgrid=False)
    st.plotly_chart(fp,use_container_width=True)
    st.markdown('<div class="section">Top products</div>',unsafe_allow_html=True)
    top=ps.head(4); cc=st.columns(4)
    for c,(_,r) in zip(cc,top.iterrows()):
        share=r.Revenue/revenue*100
        c.markdown(f'<div class="product-card"><div style="font-size:28px">📦</div><div class="product-name">{r.Product}</div><div class="product-revenue">₹{r.Revenue:,.0f}</div><div class="product-meta">{int(r.Units):,} units • {int(r.Orders):,} orders<br>{share:.1f}% of filtered revenue</div></div>',unsafe_allow_html=True)

with t3:
    rs=f.groupby("Region").agg(Revenue=("Revenue","sum"),Units=("Quantity","sum"),Orders=("OrderID","count")).reset_index()
    rs["AOV"]=rs.Revenue/rs.Orders
    st.markdown('<div class="section">Regional performance</div>',unsafe_allow_html=True)
    st.markdown('<div class="sub">See where revenue is strongest and where order value is highest.</div>',unsafe_allow_html=True)
    a,b=st.columns(2)
    with a:
        x=px.bar(rs,x="Region",y="Revenue",text_auto=".2s")
        x.update_layout(height=360,margin=dict(l=10,r=10,t=15,b=10),plot_bgcolor="white",paper_bgcolor="white")
        x.update_yaxes(tickprefix="₹",gridcolor="#edf0f5")
        st.plotly_chart(x,use_container_width=True)
    with b:
        x=px.bar(rs.sort_values("AOV"),x="AOV",y="Region",orientation="h",text_auto=".2s")
        x.update_layout(height=360,margin=dict(l=10,r=10,t=15,b=10),plot_bgcolor="white",paper_bgcolor="white")
        x.update_xaxes(tickprefix="₹",gridcolor="#edf0f5")
        st.plotly_chart(x,use_container_width=True)
    st.dataframe(rs.style.format({"Revenue":"₹{:,.0f}","AOV":"₹{:,.0f}","Units":"{:,.0f}","Orders":"{:,.0f}"}),use_container_width=True,hide_index=True)

with t4:
    st.markdown('<div class="section">Transaction explorer</div>',unsafe_allow_html=True)
    st.markdown('<div class="sub">Search, inspect and export the filtered dataset.</div>',unsafe_allow_html=True)
    q=st.text_input("Search product / region / order ID",placeholder="e.g. Keyboard, North, 1024")
    tx=f.copy()
    if q.strip():
        s=q.strip().lower()
        tx=tx[tx.Product.str.lower().str.contains(s,na=False)|tx.Region.str.lower().str.contains(s,na=False)|tx.OrderID.astype(str).str.contains(s,na=False)]
    show=tx.sort_values("Date",ascending=False)[["OrderID","Date","Product","Region","Quantity","UnitPrice","Revenue"]]
    st.dataframe(show,use_container_width=True,hide_index=True)
    st.download_button("⬇️ Download filtered CSV",show.to_csv(index=False).encode(), "saleshub_filtered_transactions.csv","text/csv")

st.markdown('<div class="footer"><b>SalesHub — Sales Intelligence Dashboard</b><br>Internship Project • Python Developer Intern • Codec Technologies<br>Built with Python, Pandas, Plotly & Streamlit • © 2026 Pulkit Singh</div>',unsafe_allow_html=True)
