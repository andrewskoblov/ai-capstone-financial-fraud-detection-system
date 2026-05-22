import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyairtable import Api
from datetime import datetime
import io

AIRTABLE_TOKEN = st.secrets["AIRTABLE_TOKEN"]
BASE_ID = "appOBt37iEsQy2Nbd"

st.set_page_config(page_title="SentinelIQ", page_icon="⬡", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Syne:wght@400;500;600;700&display=swap');

*, html, body { box-sizing: border-box; }
[data-testid="stAppViewContainer"], .main, [data-testid="stMain"] {
    background: #f5f3ee !important;
    font-family: 'Syne', sans-serif;
}
[data-testid="stSidebar"] { display: none; }
[data-testid="stHeader"] { display: none; }
[data-testid="stToolbar"] { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }

.topbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 18px 36px;
    background: #1a1a1a;
    border-bottom: 1px solid #2d2d2d;
}
.logo { font-family: 'IBM Plex Mono', monospace; font-size: 1.1rem; color: #e8e4db; letter-spacing: -0.02em; }
.logo span { color: #c8ff57; }
.status-dot { width: 7px; height: 7px; background: #c8ff57; border-radius: 50%; display: inline-block; margin-right: 6px; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
.topbar-right { display: flex; align-items: center; gap: 20px; font-size: 0.75rem; color: #666; font-family: 'IBM Plex Mono', monospace; }

.page-wrapper { padding: 32px 36px; max-width: 1400px; }

.stat-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 1px; background: #d4d0c8; border: 1px solid #d4d0c8; border-radius: 4px; overflow: hidden; margin-bottom: 32px; }
.stat-cell { background: #f5f3ee; padding: 20px 22px; }
.stat-cell-dark { background: #1a1a1a; padding: 20px 22px; }
.stat-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: #999; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px; }
.stat-label-dark { font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; color: #555; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px; }
.stat-val { font-size: 2.2rem; font-weight: 700; color: #1a1a1a; line-height: 1; }
.stat-val-dark { font-size: 2.2rem; font-weight: 700; color: #c8ff57; line-height: 1; }
.stat-sub { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: #999; margin-top: 4px; }
.stat-sub-dark { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: #555; margin-top: 4px; }

.section-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.7rem; color: #999; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #d4d0c8; }

.txn-row {
    padding: 14px 18px;
    background: #faf9f5;
    border: 1px solid #e8e4db;
    border-radius: 3px;
    margin-bottom: 4px;
    border-left: 3px solid #e8e4db;
    cursor: pointer;
}
.txn-row:hover { background: #fff; border-color: #1a1a1a; }
.txn-row.crit { border-left-color: #ff3b30; }
.txn-row.high { border-left-color: #ff9500; }
.txn-row.med  { border-left-color: #007aff; }
.txn-row.low  { border-left-color: #34c759; }

.txn-expand {
    background: #1a1a1a;
    border-radius: 3px;
    padding: 18px 20px;
    margin-bottom: 4px;
    margin-top: -2px;
}

.txn-id { font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; color: #999; }
.txn-merchant { font-size: 0.95rem; font-weight: 600; color: #1a1a1a; margin: 2px 0; }
.txn-amount { font-family: 'IBM Plex Mono', monospace; font-size: 1.05rem; font-weight: 500; color: #1a1a1a; text-align: right; }
.txn-score { font-family: 'IBM Plex Mono', monospace; font-size: 0.78rem; text-align: right; margin-top: 2px; }
.score-crit { color: #ff3b30; } .score-high { color: #ff9500; } .score-med { color: #007aff; } .score-low { color: #34c759; } .score-clean { color: #bbb; }

.pill { display: inline-block; padding: 2px 8px; border-radius: 2px; font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; font-weight: 500; margin-right: 3px; margin-top: 4px; }
.pill-foreign { background: #fff0e6; color: #cc5500; }
.pill-home { background: #e6f0ff; color: #0055cc; }
.pill-flag { background: #f0ede6; color: #666; border: 1px solid #e0ddd6; }

.expl { font-size: 0.78rem; color: #888; margin-top: 6px; line-height: 1.5; font-style: italic; }

.expand-field { margin-bottom: 10px; }
.expand-label { font-family: 'IBM Plex Mono', monospace; font-size: 0.65rem; color: #555; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 3px; }
.expand-value { font-family: 'IBM Plex Mono', monospace; font-size: 0.82rem; color: #e8e4db; }
.expand-expl { font-size: 0.85rem; color: #aaa; line-height: 1.6; font-style: italic; }

.gauge-container { text-align: center; padding: 10px 0; }

.case-row { display: flex; align-items: center; justify-content: space-between; padding: 16px 18px; background: #faf9f5; border: 1px solid #e8e4db; border-radius: 3px; margin-bottom: 4px; }
.case-id { font-family: 'IBM Plex Mono', monospace; font-size: 0.8rem; color: #1a1a1a; font-weight: 500; }
.case-status-open { background: #fff0e6; color: #cc5500; padding: 3px 10px; border-radius: 2px; font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; }
.case-status-investigating { background: #e6f0ff; color: #0055cc; padding: 3px 10px; border-radius: 2px; font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; }
.case-status-resolved { background: #e6f5ec; color: #1a7a3a; padding: 3px 10px; border-radius: 2px; font-family: 'IBM Plex Mono', monospace; font-size: 0.68rem; }

.search-bar { width: 100%; padding: 10px 16px; font-family: 'IBM Plex Mono', monospace; font-size: 0.82rem; background: #faf9f5; border: 1px solid #d4d0c8; border-radius: 3px; color: #1a1a1a; margin-bottom: 16px; }

[data-testid="stButton"] > button {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    background: #1a1a1a !important;
    color: #c8ff57 !important;
    border: none !important;
    border-radius: 2px !important;
    padding: 6px 14px !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
}
[data-testid="stButton"] > button:hover { background: #333 !important; }
[data-testid="stDownloadButton"] > button {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    background: #c8ff57 !important;
    color: #1a1a1a !important;
    border: none !important;
    border-radius: 2px !important;
    padding: 6px 14px !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}

.chart-box { background: #faf9f5; border: 1px solid #e8e4db; border-radius: 3px; padding: 20px; margin-bottom: 20px; }
div[data-baseweb="select"] { background: #faf9f5 !important; border-color: #d4d0c8 !important; border-radius: 2px !important; }
.stTextInput input { font-family: 'IBM Plex Mono', monospace !important; font-size: 0.82rem !important; background: #faf9f5 !important; border-color: #d4d0c8 !important; border-radius: 3px !important; }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=30)
def load_transactions():
    try:
        api = Api(AIRTABLE_TOKEN)
        table = api.table(BASE_ID, "Transactions")
        records = table.all()
        rows = []
        for r in records:
            f = r.get("fields", {})
            rows.append({
                "id": r["id"],
                "transaction_id": f.get("transaction_id", ""),
                "account_id": f.get("account_id", ""),
                "amount": float(f.get("amount", 0)),
                "merchant": f.get("merchant", "Unknown"),
                "location": f.get("location", ""),
                "status": f.get("status", "unprocessed"),
                "risk_score": float(f.get("risk_score", 0)),
                "anomaly_flags": f.get("anomaly_flags", ""),
                "ai_explanation": f.get("ai_explanation", ""),
                "timestamp": f.get("timestamp", ""),
            })
        return pd.DataFrame(rows)
    except Exception as e:
        st.error(f"Airtable error: {e}")
        return pd.DataFrame()

@st.cache_data(ttl=30)
def load_cases():
    try:
        api = Api(AIRTABLE_TOKEN)
        table = api.table(BASE_ID, "Cases")
        records = table.all()
        rows = []
        for r in records:
            f = r.get("fields", {})
            rows.append({
                "id": r["id"],
                "case_id": f.get("case_id", ""),
                "transaction_id": f.get("transaction_id", ""),
                "assigned_to": f.get("assigned_to", "Unassigned"),
                "status": f.get("Status", "open"),
                "risk_score": float(f.get("risk_score", 0)),
                "created_at": f.get("created_at", ""),
            })
        return pd.DataFrame(rows)
    except Exception as e:
        return pd.DataFrame()

def update_case(record_id, status):
    try:
        api = Api(AIRTABLE_TOKEN)
        api.table(BASE_ID, "Cases").update(record_id, {"Status": status})
        st.cache_data.clear()
        return True
    except:
        return False

def risk_cls(score):
    if score >= 0.9: return "crit"
    if score >= 0.7: return "high"
    if score >= 0.4: return "med"
    if score > 0.1:  return "low"
    return "clean"

def score_cls(score):
    return f"score-{risk_cls(score)}"

def loc_pill(loc):
    home = any(c in loc for c in ["New York","Brooklyn","Chicago","Miami","Los Angeles","New Jersey"])
    cls = "pill-home" if home else "pill-foreign"
    return f'<span class="pill {cls}">{loc}</span>'

def flag_pills(flags_str):
    if not flags_str or flags_str.strip() in ["none","","Analysis unavailable"]:
        return ""
    flags = [f.strip() for f in flags_str.replace(",", " ").split() if f.strip() not in ["none","Risk","High","Low","Medium","Unknown"]]
    return "".join(f'<span class="pill pill-flag">{f}</span>' for f in flags[:6])

def make_gauge(avg_risk, flagged, total):
    level = "CRITICAL" if avg_risk >= 0.7 else "ELEVATED" if avg_risk >= 0.4 else "NORMAL"
    color = "#ff3b30" if avg_risk >= 0.7 else "#ff9500" if avg_risk >= 0.4 else "#34c759"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(avg_risk * 100),
        number={"suffix": "%", "font": {"family": "IBM Plex Mono", "size": 28, "color": color}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#d4d0c8",
                     "tickfont": {"family": "IBM Plex Mono", "size": 9, "color": "#999"}},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "#faf9f5",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "#f0f5ec"},
                {"range": [40, 70], "color": "#faf5ec"},
                {"range": [70, 100], "color": "#faf0ee"},
            ],
            "threshold": {"line": {"color": color, "width": 3}, "thickness": 0.75, "value": avg_risk * 100}
        }
    ))
    fig.update_layout(
        plot_bgcolor="#faf9f5", paper_bgcolor="#faf9f5",
        margin=dict(l=20, r=20, t=30, b=10), height=200,
        font=dict(family="IBM Plex Mono"),
        annotations=[{
            "text": f"THREAT LEVEL: {level}",
            "x": 0.5, "y": -0.08, "showarrow": False,
            "font": {"family": "IBM Plex Mono", "size": 10, "color": color},
            "xref": "paper", "yref": "paper"
        }]
    )
    return fig

def to_csv(dataframe):
    return dataframe.to_csv(index=False).encode("utf-8")


# ── Session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "overview"
if "expanded_txn" not in st.session_state:
    st.session_state.expanded_txn = None

# ── Top bar ───────────────────────────────────────────────────────────────────
now = datetime.now().strftime("%H:%M:%S")
st.markdown(f"""
<div class="topbar">
    <div class="logo">⬡ Sentinel<span>IQ</span></div>
    <div class="topbar-right">
        <span><span class="status-dot"></span>LIVE</span>
        <span>{now}</span>
        <span>FRAUD INTELLIGENCE PLATFORM v2.0</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Nav ───────────────────────────────────────────────────────────────────────
nav_cols = st.columns([1,1,1,1,4,1])
pages = [("overview","OVERVIEW"), ("alerts","ALERTS"), ("cases","CASES"), ("analytics","ANALYTICS")]
for i, (key, label) in enumerate(pages):
    with nav_cols[i]:
        if st.button(label, key=f"nav_{key}"):
            st.session_state.page = key
            st.session_state.expanded_txn = None
            st.rerun()
with nav_cols[5]:
    if st.button("↻ REFRESH"):
        st.cache_data.clear()
        st.rerun()

# ── Load data ─────────────────────────────────────────────────────────────────
df = load_transactions()
cases = load_cases()
if df.empty:
    st.error("No data. Run Components 1 and 2 first.")
    st.stop()

df["risk_level"] = df["risk_score"].apply(lambda s: "Critical" if s>=0.9 else "High" if s>=0.7 else "Medium" if s>=0.4 else "Low" if s>0.1 else "Clean")
analyzed = df[df["status"] != "unprocessed"]
total    = len(df)
flagged  = len(df[df["risk_score"] >= 0.7])
review   = len(df[(df["risk_score"] >= 0.4) & (df["risk_score"] < 0.7)])
clean_ct = len(df[df["risk_score"] < 0.1])
exposure = df[df["risk_score"] >= 0.7]["amount"].sum()
avg_risk = df["risk_score"].mean() if not df.empty else 0

st.markdown('<div class="page-wrapper">', unsafe_allow_html=True)


# ── OVERVIEW ──────────────────────────────────────────────────────────────────
if st.session_state.page == "overview":
    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-cell-dark">
            <div class="stat-label-dark">Fraud exposure</div>
            <div class="stat-val-dark">${exposure:,.0f}</div>
            <div class="stat-sub-dark">{flagged} flagged transactions</div>
        </div>
        <div class="stat-cell">
            <div class="stat-label">Total transactions</div>
            <div class="stat-val">{total}</div>
            <div class="stat-sub">all time</div>
        </div>
        <div class="stat-cell">
            <div class="stat-label">Flagged</div>
            <div class="stat-val" style="color:#ff3b30">{flagged}</div>
            <div class="stat-sub">risk ≥ 0.70</div>
        </div>
        <div class="stat-cell">
            <div class="stat-label">Needs review</div>
            <div class="stat-val" style="color:#ff9500">{review}</div>
            <div class="stat-sub">risk 0.40–0.69</div>
        </div>
        <div class="stat-cell">
            <div class="stat-label">Clean</div>
            <div class="stat-val" style="color:#34c759">{clean_ct}</div>
            <div class="stat-sub">risk &lt; 0.10</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown('<div class="section-label">Top flagged transactions — click to expand</div>', unsafe_allow_html=True)
        top = df[df["risk_score"] >= 0.7].sort_values("risk_score", ascending=False).head(6)
        for _, row in top.iterrows():
            rc = risk_cls(row["risk_score"])
            is_expanded = st.session_state.expanded_txn == row["transaction_id"]
            st.markdown(f"""
            <div class="txn-row {rc}">
                <div style="display:flex;justify-content:space-between;align-items:flex-start">
                    <div style="flex:1">
                        <div class="txn-id">{row['transaction_id']} · {row['account_id']}</div>
                        <div class="txn-merchant">{row['merchant']}</div>
                        <div>{loc_pill(row['location'])}{flag_pills(row['anomaly_flags'])}</div>
                    </div>
                    <div style="min-width:90px;padding-left:16px;text-align:right">
                        <div class="txn-amount">${row['amount']:,.2f}</div>
                        <div class="txn-score {score_cls(row['risk_score'])}">{row['risk_score']:.2f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("▾ Expand" if not is_expanded else "▴ Collapse", key=f"exp_ov_{row['transaction_id']}"):
                st.session_state.expanded_txn = None if is_expanded else row["transaction_id"]
                st.rerun()
            if is_expanded:
                st.markdown(f"""
                <div class="txn-expand">
                    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin-bottom:16px">
                        <div class="expand-field"><div class="expand-label">Account</div><div class="expand-value">{row['account_id']}</div></div>
                        <div class="expand-field"><div class="expand-label">Timestamp</div><div class="expand-value">{row['timestamp'][:19] if row['timestamp'] else 'N/A'}</div></div>
                        <div class="expand-field"><div class="expand-label">Status</div><div class="expand-value">{row['status']}</div></div>
                        <div class="expand-field"><div class="expand-label">Amount</div><div class="expand-value">${row['amount']:,.2f}</div></div>
                        <div class="expand-field"><div class="expand-label">Risk score</div><div class="expand-value" style="color:#ff3b30">{row['risk_score']:.2f}</div></div>
                        <div class="expand-field"><div class="expand-label">Location</div><div class="expand-value">{row['location']}</div></div>
                    </div>
                    <div class="expand-field"><div class="expand-label">Anomaly flags</div><div class="expand-value">{row['anomaly_flags'] or 'none'}</div></div>
                    <div class="expand-field" style="margin-top:12px"><div class="expand-label">AI analysis</div><div class="expand-expl">{row['ai_explanation'] or 'No explanation available'}</div></div>
                </div>
                """, unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">System threat level</div>', unsafe_allow_html=True)
        st.plotly_chart(make_gauge(avg_risk, flagged, total), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Risk distribution</div>', unsafe_allow_html=True)
        rc_data = df["risk_level"].value_counts().reindex(["Critical","High","Medium","Low","Clean"], fill_value=0)
        colors = {"Critical":"#ff3b30","High":"#ff9500","Medium":"#007aff","Low":"#34c759","Clean":"#d4d0c8"}
        fig = go.Figure(go.Bar(
            x=rc_data.index.tolist(), y=rc_data.values.tolist(),
            marker_color=[colors[l] for l in rc_data.index],
            marker_line_width=0,
        ))
        fig.update_layout(plot_bgcolor="#faf9f5", paper_bgcolor="#faf9f5",
                          margin=dict(l=0,r=0,t=0,b=0), height=160,
                          font=dict(family="IBM Plex Mono", color="#999", size=10),
                          xaxis=dict(gridcolor="#e8e4db"), yaxis=dict(gridcolor="#e8e4db"),
                          showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if not cases.empty:
            st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            st.markdown('<div class="section-label">Case queue</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:2.5rem;font-weight:700;color:#1a1a1a">{len(cases[cases.status=="open"])}</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#999">{len(cases[cases.status=="investigating"])} investigating · {len(cases[cases.status=="resolved"])} resolved</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)


# ── ALERTS ────────────────────────────────────────────────────────────────────
elif st.session_state.page == "alerts":
    st.markdown('<div class="section-label">Alert feed</div>', unsafe_allow_html=True)

    search = st.text_input("", placeholder="Search by transaction ID, account, merchant, or location...", label_visibility="collapsed")

    f1, f2, f3, f4 = st.columns([2,2,2,2])
    with f1:
        min_risk = st.slider("Min risk score", 0.0, 1.0, 0.0, 0.05)
    with f2:
        merchants = ["All"] + sorted(df["merchant"].unique().tolist())
        merch_sel = st.selectbox("Merchant", merchants)
    with f3:
        statuses = ["All"] + sorted(df["status"].unique().tolist())
        stat_sel = st.selectbox("Status", statuses)
    with f4:
        sort_by = st.selectbox("Sort by", ["Risk (high→low)", "Amount (high→low)", "Transaction ID"])

    filtered = df[df["risk_score"] >= min_risk].copy()
    if merch_sel != "All":
        filtered = filtered[filtered["merchant"] == merch_sel]
    if stat_sel != "All":
        filtered = filtered[filtered["status"] == stat_sel]
    if search.strip():
        q = search.strip().lower()
        filtered = filtered[
            filtered["transaction_id"].str.lower().str.contains(q) |
            filtered["account_id"].str.lower().str.contains(q) |
            filtered["merchant"].str.lower().str.contains(q) |
            filtered["location"].str.lower().str.contains(q)
        ]
    if sort_by == "Risk (high→low)":
        filtered = filtered.sort_values("risk_score", ascending=False)
    elif sort_by == "Amount (high→low)":
        filtered = filtered.sort_values("amount", ascending=False)
    else:
        filtered = filtered.sort_values("transaction_id")

    exp_col, dl_col, _ = st.columns([2, 2, 6])
    with exp_col:
        st.markdown(f'<div style="font-family:IBM Plex Mono,monospace;font-size:0.7rem;color:#999;padding-top:8px">{len(filtered)} records</div>', unsafe_allow_html=True)
    with dl_col:
        csv_data = to_csv(filtered[["transaction_id","account_id","amount","merchant","location","risk_score","anomaly_flags","ai_explanation","status"]])
        st.download_button("⬇ Export CSV", data=csv_data, file_name=f"fraud_alerts_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")

    for _, row in filtered.iterrows():
        rc = risk_cls(row["risk_score"])
        is_expanded = st.session_state.expanded_txn == row["transaction_id"]
        expl = str(row["ai_explanation"])
        expl_short = expl[:180] + "…" if len(expl) > 180 else expl

        st.markdown(f"""
        <div class="txn-row {rc}">
            <div style="display:flex;justify-content:space-between;align-items:flex-start">
                <div style="flex:1">
                    <div class="txn-id">{row['transaction_id']} · {row['account_id']} · {row['timestamp'][:10] if row['timestamp'] else ''}</div>
                    <div class="txn-merchant">{row['merchant']}</div>
                    <div>{loc_pill(row['location'])}{flag_pills(row['anomaly_flags'])}</div>
                    <div class="expl">{expl_short}</div>
                </div>
                <div style="min-width:100px;padding-left:16px;text-align:right">
                    <div class="txn-amount">${row['amount']:,.2f}</div>
                    <div class="txn-score {score_cls(row['risk_score'])}">{row['risk_score']:.2f}</div>
                    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.65rem;color:#ccc;margin-top:4px">{row['status']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("▾ Full details" if not is_expanded else "▴ Close", key=f"exp_al_{row['transaction_id']}"):
            st.session_state.expanded_txn = None if is_expanded else row["transaction_id"]
            st.rerun()

        if is_expanded:
            same_acct = df[df["account_id"] == row["account_id"]].sort_values("risk_score", ascending=False)
            st.markdown(f"""
            <div class="txn-expand">
                <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:16px">
                    <div class="expand-field"><div class="expand-label">Transaction ID</div><div class="expand-value">{row['transaction_id']}</div></div>
                    <div class="expand-field"><div class="expand-label">Account</div><div class="expand-value">{row['account_id']}</div></div>
                    <div class="expand-field"><div class="expand-label">Timestamp</div><div class="expand-value">{row['timestamp'][:19] if row['timestamp'] else 'N/A'}</div></div>
                    <div class="expand-field"><div class="expand-label">Status</div><div class="expand-value">{row['status']}</div></div>
                    <div class="expand-field"><div class="expand-label">Amount</div><div class="expand-value">${row['amount']:,.2f}</div></div>
                    <div class="expand-field"><div class="expand-label">Merchant</div><div class="expand-value">{row['merchant']}</div></div>
                    <div class="expand-field"><div class="expand-label">Location</div><div class="expand-value">{row['location']}</div></div>
                    <div class="expand-field"><div class="expand-label">Risk score</div><div class="expand-value" style="color:#ff3b30">{row['risk_score']:.2f}</div></div>
                </div>
                <div class="expand-field"><div class="expand-label">Anomaly flags</div><div class="expand-value">{row['anomaly_flags'] or 'none'}</div></div>
                <div class="expand-field" style="margin-top:12px"><div class="expand-label">Full AI analysis</div><div class="expand-expl">{row['ai_explanation'] or 'No explanation available'}</div></div>
                <div style="margin-top:16px;padding-top:12px;border-top:1px solid #2d2d2d">
                    <div class="expand-label" style="margin-bottom:8px">Other transactions on this account ({len(same_acct)} total)</div>
                    {''.join(f'<div style="font-family:IBM Plex Mono,monospace;font-size:0.72rem;color:#{'ff3b30' if r.risk_score>=0.7 else 'aaa'};margin-bottom:4px">{r.transaction_id} · {r.merchant} · ${r.amount:,.2f} · {r.risk_score:.2f}</div>' for _, r in same_acct.head(5).iterrows())}
                </div>
            </div>
            """, unsafe_allow_html=True)


# ── CASES ─────────────────────────────────────────────────────────────────────
elif st.session_state.page == "cases":
    st.markdown('<div class="section-label">Investigation queue</div>', unsafe_allow_html=True)

    if cases.empty:
        st.markdown('<div style="color:#bbb;padding:40px 0;font-family:IBM Plex Mono,monospace;font-size:0.8rem">No cases. Run Component 3 to generate cases from high-risk transactions.</div>', unsafe_allow_html=True)
    else:
        c1,c2,c3,c4 = st.columns(4)
        with c1: st.markdown(f'<div class="stat-cell" style="border:1px solid #e8e4db;border-radius:3px"><div class="stat-label">Total</div><div class="stat-val">{len(cases)}</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="stat-cell" style="border:1px solid #e8e4db;border-radius:3px"><div class="stat-label">Open</div><div class="stat-val" style="color:#ff3b30">{len(cases[cases.status=="open"])}</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="stat-cell" style="border:1px solid #e8e4db;border-radius:3px"><div class="stat-label">Investigating</div><div class="stat-val" style="color:#007aff">{len(cases[cases.status=="investigating"])}</div></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="stat-cell" style="border:1px solid #e8e4db;border-radius:3px"><div class="stat-label">Resolved</div><div class="stat-val" style="color:#34c759">{len(cases[cases.status=="resolved"])}</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        sf_col, dl_col, _ = st.columns([2, 2, 6])
        with sf_col:
            status_filter = st.selectbox("Filter by status", ["All","open","investigating","resolved"])
        with dl_col:
            st.markdown("<br>", unsafe_allow_html=True)
            cases_csv = to_csv(cases[["case_id","transaction_id","status","risk_score","assigned_to","created_at"]])
            st.download_button("⬇ Export Cases CSV", data=cases_csv, file_name=f"cases_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")

        display_cases = cases if status_filter == "All" else cases[cases["status"] == status_filter]

        for _, case in display_cases.iterrows():
            txn_match = df[df["transaction_id"] == case["transaction_id"]]
            txn = txn_match.iloc[0] if not txn_match.empty else None
            s = case["status"]
            status_html = f'<span class="case-status-{s}">{s.upper()}</span>'

            st.markdown(f"""
            <div class="case-row">
                <div>
                    <div class="case-id">{case['case_id']}</div>
                    <div style="font-family:'IBM Plex Mono',monospace;font-size:0.7rem;color:#999;margin-top:2px">
                        {case['transaction_id']}
                        {f' · {txn["merchant"]} · ${txn["amount"]:,.2f} · {txn["location"]}' if txn is not None else ''}
                    </div>
                    {f'<div style="font-size:0.75rem;color:#aaa;margin-top:4px;font-style:italic">{str(txn["ai_explanation"])[:120]}…</div>' if txn is not None and txn["ai_explanation"] else ''}
                </div>
                <div style="display:flex;align-items:center;gap:16px">
                    <span style="font-family:'IBM Plex Mono',monospace;font-size:0.85rem;color:#ff3b30">{case['risk_score']:.2f}</span>
                    {status_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

            b1, b2, b3, _ = st.columns([1,1,1,6])
            with b1:
                if st.button("Investigate", key=f"i_{case['id']}"):
                    update_case(case["id"], "investigating")
                    st.rerun()
            with b2:
                if st.button("Resolve", key=f"r_{case['id']}"):
                    update_case(case["id"], "resolved")
                    st.rerun()
            with b3:
                if st.button("Reopen", key=f"o_{case['id']}"):
                    update_case(case["id"], "open")
                    st.rerun()


# ── ANALYTICS ─────────────────────────────────────────────────────────────────
elif st.session_state.page == "analytics":
    st.markdown('<div class="section-label">Fraud analytics</div>', unsafe_allow_html=True)

    dl_col, _ = st.columns([2, 8])
    with dl_col:
        full_csv = to_csv(df[["transaction_id","account_id","amount","merchant","location","risk_score","anomaly_flags","ai_explanation","status"]])
        st.download_button("⬇ Export Full Dataset", data=full_csv, file_name=f"all_transactions_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")

    plot_cfg = dict(plot_bgcolor="#faf9f5", paper_bgcolor="#faf9f5",
                    margin=dict(l=0,r=0,t=10,b=0),
                    font=dict(family="IBM Plex Mono", color="#999", size=10))

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Avg risk score by merchant</div>', unsafe_allow_html=True)
        mr = df.groupby("merchant")["risk_score"].mean().sort_values().tail(12)
        fig = go.Figure(go.Bar(x=mr.values, y=mr.index, orientation="h", marker_line_width=0,
                               marker_color=["#ff3b30" if v>=0.7 else "#ff9500" if v>=0.4 else "#007aff" for v in mr.values]))
        fig.update_layout(**plot_cfg, height=300, xaxis=dict(gridcolor="#e8e4db", range=[0,1]), yaxis=dict(gridcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Avg risk score by location</div>', unsafe_allow_html=True)
        lr = df.groupby("location")["risk_score"].mean().sort_values().tail(12)
        fig2 = go.Figure(go.Bar(x=lr.values, y=lr.index, orientation="h", marker_line_width=0,
                                marker_color=["#ff3b30" if v>=0.7 else "#ff9500" if v>=0.4 else "#34c759" for v in lr.values]))
        fig2.update_layout(**plot_cfg, height=300, xaxis=dict(gridcolor="#e8e4db", range=[0,1]), yaxis=dict(gridcolor="rgba(0,0,0,0)"))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Amount vs risk score — all transactions</div>', unsafe_allow_html=True)
    color_map = {"Critical":"#ff3b30","High":"#ff9500","Medium":"#007aff","Low":"#34c759","Clean":"#d4d0c8"}
    fig3 = px.scatter(df, x="amount", y="risk_score", color="risk_level",
                      color_discrete_map=color_map,
                      hover_data=["transaction_id","merchant","location"],
                      template="simple_white")
    fig3.update_layout(**plot_cfg, height=280,
                       xaxis=dict(title="Amount ($)", gridcolor="#e8e4db"),
                       yaxis=dict(title="Risk score", gridcolor="#e8e4db", range=[0,1.05]))
    fig3.update_traces(marker=dict(size=7, opacity=0.85, line=dict(width=0)))
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Transaction volume by merchant</div>', unsafe_allow_html=True)
        mc = df["merchant"].value_counts().head(10).reset_index()
        mc.columns = ["Merchant","Count"]
        fig4 = px.bar(mc, x="Count", y="Merchant", orientation="h", template="simple_white", color_discrete_sequence=["#1a1a1a"])
        fig4.update_layout(**plot_cfg, height=260, showlegend=False, xaxis=dict(gridcolor="#e8e4db"), yaxis=dict(gridcolor="rgba(0,0,0,0)"))
        fig4.update_traces(marker_line_width=0)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="chart-box">', unsafe_allow_html=True)
        st.markdown('<div class="section-label">Flagged transactions</div>', unsafe_allow_html=True)
        flagged_df = df[df["risk_score"]>=0.7][["transaction_id","merchant","amount","risk_score","location"]].sort_values("risk_score",ascending=False).copy()
        flagged_df["amount"] = flagged_df["amount"].apply(lambda x: f"${x:,.2f}")
        flagged_df["risk_score"] = flagged_df["risk_score"].round(2)
        st.dataframe(flagged_df.rename(columns={"transaction_id":"TXN","merchant":"Merchant","amount":"Amount","risk_score":"Score","location":"Location"}),
                     use_container_width=True, height=260, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
