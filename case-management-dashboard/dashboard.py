import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os
import uuid

# ─── CONFIG ────────────────────────────────────────────────────────────────────
def get_secret(name: str, default: str = "") -> str:
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


AIRTABLE_TOKEN = os.environ.get("AIRTABLE_TOKEN") or get_secret("AIRTABLE_TOKEN")
BASE_ID        = os.environ.get("AIRTABLE_BASE_ID") or get_secret("AIRTABLE_BASE_ID", "appOBt37iEsQy2Nbd")
CASES_TABLE    = os.environ.get("AIRTABLE_CASES_TABLE", "Cases")
TXN_TABLE      = os.environ.get("AIRTABLE_TRANSACTIONS_TABLE", "Transactions")

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_TOKEN}",
    "Content-Type": "application/json"
}

# ─── AIRTABLE HELPERS ──────────────────────────────────────────────────────────
def fetch_table(table_name: str, formula: str = "") -> list[dict]:
    if not AIRTABLE_TOKEN:
        raise RuntimeError("Missing AIRTABLE_TOKEN. Set it as an environment variable or Streamlit secret.")

    url = f"https://api.airtable.com/v0/{BASE_ID}/{requests.utils.quote(table_name)}"
    params = {}
    if formula:
        params["filterByFormula"] = formula
    records, offset = [], None
    while True:
        if offset:
            params["offset"] = offset
        r = requests.get(url, headers=HEADERS, params=params)
        r.raise_for_status()
        data = r.json()
        records.extend(data.get("records", []))
        offset = data.get("offset")
        if not offset:
            break
    return records


def update_record(table_name: str, record_id: str, fields: dict):
    if not AIRTABLE_TOKEN:
        raise RuntimeError("Missing AIRTABLE_TOKEN. Set it as an environment variable or Streamlit secret.")

    url = f"https://api.airtable.com/v0/{BASE_ID}/{requests.utils.quote(table_name)}/{record_id}"
    r = requests.patch(url, headers=HEADERS, json={"fields": fields})
    r.raise_for_status()
    return r.json()


def create_record(table_name: str, fields: dict):
    if not AIRTABLE_TOKEN:
        raise RuntimeError("Missing AIRTABLE_TOKEN. Set it as an environment variable or Streamlit secret.")

    url = f"https://api.airtable.com/v0/{BASE_ID}/{requests.utils.quote(table_name)}"
    r = requests.post(url, headers=HEADERS, json={"fields": fields})
    r.raise_for_status()
    return r.json()


@st.cache_data(ttl=30)
def load_cases():
    records = fetch_table(CASES_TABLE)
    rows = []
    for rec in records:
        f = rec["fields"]
        rows.append({
            "record_id":      rec["id"],
            "case_id":        f.get("case_id", ""),
            "transaction_id": f.get("transaction_id", ""),
            "risk_score":     float(f.get("risk_score", 0)),
            "status":         f.get("status", "open"),
            "assigned_to":    f.get("assigned_to", ""),
            "ai_explanation": f.get("ai_explanation", ""),
            "created_at":     f.get("created_at", ""),
            "resolved_at":    f.get("resolved_at", ""),
        })
    return pd.DataFrame(rows)


@st.cache_data(ttl=30)
def load_transactions():
    records = fetch_table(TXN_TABLE)
    rows = []
    for rec in records:
        f = rec["fields"]
        rows.append({
            "record_id":      rec["id"],
            "transaction_id": f.get("transaction_id", ""),
            "account_id":     f.get("account_id", ""),
            "amount":         float(f.get("amount", 0)),
            "merchant":       f.get("merchant", ""),
            "location":       f.get("location", ""),
            "status":         f.get("status", ""),
            "risk_score":     float(f.get("risk_score", 0)),
            "anomaly_flags":  f.get("anomaly_flags", ""),
            "ai_explanation": f.get("ai_explanation", ""),
            "timestamp":      f.get("timestamp", ""),
        })
    return pd.DataFrame(rows)


def risk_badge(score: float) -> str:
    if score >= 0.85:
        return "🔴 CRITICAL"
    elif score >= 0.7:
        return "🟠 HIGH"
    elif score >= 0.5:
        return "🟡 MEDIUM"
    else:
        return "🟢 LOW"


# ─── PAGE SETUP ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .metric-card {
        background: #1e2130;
        border-radius: 10px;
        padding: 16px 20px;
        border-left: 4px solid #e05c5c;
    }
    .risk-critical { color: #ff4b4b; font-weight: bold; }
    .risk-high     { color: #ffa14a; font-weight: bold; }
    .risk-medium   { color: #ffd700; font-weight: bold; }
    .risk-low      { color: #2ecc71; font-weight: bold; }
    .stDataFrame   { font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("🔍 Fraud Monitor")
    st.markdown("**Financial Fraud Detection System**")
    st.markdown("Component 3 — Case Management")
    st.divider()

    page = st.radio("Navigate", ["📊 Overview", "🚨 Alert Queue", "📁 Case Manager", "📈 Analytics"])
    st.divider()

    st.markdown("**Filters**")
    min_risk = st.slider("Min Risk Score", 0.0, 1.0, 0.0, 0.05)
    status_filter = st.multiselect(
        "Case Status",
        ["open", "in_review", "resolved"],
        default=["open", "in_review"]
    )

    st.divider()
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.rerun()

# ─── LOAD DATA ─────────────────────────────────────────────────────────────────
try:
    cases_df = load_cases()
    txns_df  = load_transactions()
except Exception as e:
    st.error(f"⚠️ Could not connect to Airtable: {e}")
    st.info("Set your AIRTABLE_TOKEN environment variable and reload.")
    cases_df = pd.DataFrame(columns=["record_id","case_id","transaction_id","risk_score","status","assigned_to","ai_explanation","created_at","resolved_at"])
    txns_df  = pd.DataFrame(columns=["record_id","transaction_id","account_id","amount","merchant","location","status","risk_score","anomaly_flags","ai_explanation","timestamp"])

# Apply sidebar filters
filtered_cases = cases_df[
    (cases_df["risk_score"] >= min_risk) &
    (cases_df["status"].isin(status_filter) if status_filter else True)
] if not cases_df.empty else cases_df

# ─── OVERVIEW PAGE ─────────────────────────────────────────────────────────────
if page == "📊 Overview":
    st.title("📊 Fraud Detection Overview")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    col1, col2, col3, col4 = st.columns(4)

    total_txns   = len(txns_df)
    analyzed     = len(txns_df[txns_df["status"] == "analyzed"]) if not txns_df.empty else 0
    escalated    = len(txns_df[txns_df["status"] == "escalated"]) if not txns_df.empty else 0
    open_cases   = len(cases_df[cases_df["status"] == "open"]) if not cases_df.empty else 0

    col1.metric("Total Transactions", total_txns)
    col2.metric("Analyzed",           analyzed)
    col3.metric("Escalated",          escalated)
    col4.metric("Open Cases",         open_cases, delta=f"{open_cases} need review", delta_color="inverse")

    st.divider()

    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("📌 Recent High-Risk Cases")
        if not cases_df.empty:
            high_risk = cases_df[cases_df["risk_score"] >= 0.7].sort_values("risk_score", ascending=False).head(5)
            for _, row in high_risk.iterrows():
                with st.container():
                    c1, c2, c3 = st.columns([2, 1, 1])
                    c1.markdown(f"**{row['case_id'] or row['transaction_id']}**")
                    c2.markdown(f"{risk_badge(row['risk_score'])}")
                    c3.markdown(f"`{row['status']}`")
        else:
            st.info("No cases found.")

    with col_right:
        st.subheader("📋 Transaction Pipeline")
        if not txns_df.empty:
            status_counts = txns_df["status"].value_counts().reset_index()
            status_counts.columns = ["Status", "Count"]
            st.dataframe(status_counts, use_container_width=True, hide_index=True)
        else:
            st.info("No transactions loaded.")

# ─── ALERT QUEUE PAGE ──────────────────────────────────────────────────────────
elif page == "🚨 Alert Queue":
    st.title("🚨 Fraud Alert Queue")
    st.caption("High-risk transactions requiring analyst review")

    if filtered_cases.empty:
        st.info("No alerts match your current filters.")
    else:
        # Sort by risk descending
        queue = filtered_cases.sort_values("risk_score", ascending=False)

        for _, row in queue.iterrows():
            badge = risk_badge(row["risk_score"])
            with st.expander(f"{badge}  |  {row['case_id'] or row['transaction_id']}  —  Score: {row['risk_score']:.2f}  |  Status: {row['status']}"):
                c1, c2 = st.columns(2)
                c1.markdown(f"**Transaction ID:** `{row['transaction_id']}`")
                c1.markdown(f"**Case ID:** `{row['case_id']}`")
                c1.markdown(f"**Assigned To:** {row['assigned_to'] or '—'}")
                c2.markdown(f"**Created:** {row['created_at'][:10] if row['created_at'] else '—'}")
                c2.markdown(f"**Resolved:** {row['resolved_at'][:10] if row['resolved_at'] else '—'}")

                if row["ai_explanation"]:
                    st.markdown("**🤖 AI Explanation:**")
                    st.info(row["ai_explanation"])

                st.markdown("**Update Status:**")
                new_status = st.selectbox(
                    "Status",
                    ["open", "in_review", "resolved"],
                    index=["open", "in_review", "resolved"].index(row["status"]) if row["status"] in ["open","in_review","resolved"] else 0,
                    key=f"status_{row['record_id']}"
                )
                new_assignee = st.text_input("Assigned To", value=row["assigned_to"], key=f"assign_{row['record_id']}")

                if st.button("💾 Save Changes", key=f"save_{row['record_id']}"):
                    fields = {"status": new_status, "assigned_to": new_assignee}
                    if new_status == "resolved" and not row["resolved_at"]:
                        fields["resolved_at"] = datetime.utcnow().isoformat()
                    try:
                        update_record(CASES_TABLE, row["record_id"], fields)
                        st.success("Updated!")
                        st.cache_data.clear()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to update: {e}")

# ─── CASE MANAGER PAGE ─────────────────────────────────────────────────────────
elif page == "📁 Case Manager":
    st.title("📁 Case Manager")

    tab1, tab2 = st.tabs(["All Cases", "Create Manual Case"])

    with tab1:
        if cases_df.empty:
            st.info("No cases found.")
        else:
            display = cases_df[[
                "case_id","transaction_id","risk_score","status","assigned_to","created_at"
            ]].copy()
            display["risk_score"] = display["risk_score"].apply(lambda x: f"{x:.2f}")
            display["Risk"] = cases_df["risk_score"].apply(risk_badge)
            st.dataframe(display, use_container_width=True, hide_index=True)

            csv = cases_df.to_csv(index=False)
            st.download_button("⬇️ Export Cases CSV", csv, "cases_export.csv", "text/csv")

    with tab2:
        st.subheader("Manually Create a Case")
        with st.form("create_case"):
            txn_id    = st.text_input("Transaction ID")
            risk_val  = st.number_input("Risk Score", 0.0, 1.0, 0.75, 0.01)
            case_note = st.text_area("AI Explanation / Notes")
            assignee  = st.text_input("Assign To")
            submitted = st.form_submit_button("Create Case")

        if submitted and txn_id:
            new_case = {
                "case_id":        f"CASE-{str(uuid.uuid4())[:8].upper()}",
                "transaction_id": txn_id,
                "risk_score":     risk_val,
                "ai_explanation": case_note,
                "assigned_to":    assignee,
                "status":         "open",
                "created_at":     datetime.utcnow().isoformat(),
            }
            try:
                create_record(CASES_TABLE, new_case)
                st.success(f"Case {new_case['case_id']} created!")
                st.cache_data.clear()
            except Exception as e:
                st.error(f"Failed: {e}")

# ─── ANALYTICS PAGE ────────────────────────────────────────────────────────────
elif page == "📈 Analytics":
    st.title("📈 Fraud Analytics")

    if txns_df.empty:
        st.info("No transaction data available.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Risk Score Distribution")
            risk_bins = pd.cut(
                txns_df["risk_score"],
                bins=[0, 0.3, 0.5, 0.7, 0.85, 1.0],
                labels=["Very Low", "Low", "Medium", "High", "Critical"]
            ).value_counts().sort_index()
            st.bar_chart(risk_bins)

        with col2:
            st.subheader("Transaction Status Breakdown")
            st.bar_chart(txns_df["status"].value_counts())

        st.divider()
        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Top Flagged Merchants")
            if "merchant" in txns_df.columns:
                top_merchants = (
                    txns_df[txns_df["risk_score"] >= 0.7]
                    .groupby("merchant")["risk_score"]
                    .count()
                    .sort_values(ascending=False)
                    .head(8)
                )
                st.bar_chart(top_merchants)

        with col4:
            st.subheader("Top Flagged Locations")
            if "location" in txns_df.columns:
                top_locs = (
                    txns_df[txns_df["risk_score"] >= 0.7]
                    .groupby("location")["risk_score"]
                    .count()
                    .sort_values(ascending=False)
                    .head(8)
                )
                st.bar_chart(top_locs)

        st.divider()
        st.subheader("High-Risk Transaction Log (risk_score ≥ 0.7)")
        high_risk_txns = txns_df[txns_df["risk_score"] >= 0.7][[
            "transaction_id","account_id","amount","merchant","location","risk_score","anomaly_flags","status"
        ]].sort_values("risk_score", ascending=False)
        st.dataframe(high_risk_txns, use_container_width=True, hide_index=True)

# ─── FOOTER ────────────────────────────────────────────────────────────────────
st.divider()
st.caption("Financial Fraud Detection System — Component 3: Case Management & Dashboard | Andrew Skoblov | UGR 277-06")
