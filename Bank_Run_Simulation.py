import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Macroeconomics Simulation: Bank Run Model")

# 1. Pull data from Google Sheets
sheet_url_L = "https://docs.google.com/spreadsheets/d/1ocSW_aNHoc4l3e0MWEfRAWvtBxnopAcUa4GtSlkkops/export?format=csv&gid=1105227624"
sheet_url_R = "https://docs.google.com/spreadsheets/d/1ocSW_aNHoc4l3e0MWEfRAWvtBxnopAcUa4GtSlkkops/export?format=csv&gid=261151936"

# Loading data
df_L = pd.read_csv(sheet_url_L)
df_R = pd.read_csv(sheet_url_R)
input_L = df_L.iloc[:, 1]
input_R = df_R.iloc[:, 1]

st.sidebar.header("Global Economic Parameters")

N = st.sidebar.slider("Number of Depositors (N)", 4, 10, 7)

st.sidebar.subheader("Group L Parameters")
R_L = st.sidebar.slider("Long-term Project Return (R) of Group L", 1.0, 5.0, 1.2)
L_L = st.sidebar.slider("Liquidation Yield (L) of Group L", 0.0, 1.0, 0.2)

st.sidebar.subheader("Group R Parameters")
R_R = st.sidebar.slider("Long-term Project Return (R) of Group R", 1.0, 5.0, 2.0)
L_R = st.sidebar.slider("Liquidation Yield (L) of Group R", 0.0, 1.0, 0.8)

if st.button("Run Simulation and Calculate Results"):
    if len(input_L) == 0 or len(input_R) == 0:
        st.error("Please ensure both sheets have data before running the simulation.")
        st.stop()
    
    bootstrap_flag_L = len(input_L) < N
    bootstrap_flag_R = len(input_R) < N
    results_L = input_L.sample(n=N, replace=bootstrap_flag_L).reset_index(drop=True)
    results_R = input_R.sample(n=N, replace=bootstrap_flag_R).reset_index(drop=True)

    run_results_L = results_L.value_counts().get("Run", 0)
    stay_results_L = results_L.value_counts().get("Stay", 0)
    run_results_R = results_R.value_counts().get("Run", 0)
    stay_results_R = results_R.value_counts().get("Stay", 0)

    money_left_L = max(0, 10 * N - run_results_L * L_L)
    money_left_R = max(0, 10 * N - run_results_R * L_R)
    gain_run_L = min(10, 10*N*L_L/run_results_L)
    gain_run_R = min(10, 10*N*L_R/run_results_R)
    gain_stay_L = money_left_L * R_L / stay_results_L
    gain_stay_R = money_left_R * R_R / stay_results_R

    st.divider() # Visual line to separate inputs from results
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Group L Analysis")
        st.write(f"Group L: {run_results_L} Run, {stay_results_L} Stay")
        st.write(f"Expected Gain if Run: {gain_run_L:.2f}")
        st.write(f"Expected Gain if Stay: {gain_stay_L:.2f}")
        if gain_run_L > gain_stay_L:
            st.success("Run is the better choice for Group L.")
        elif gain_run_L < gain_stay_L:
            st.success("Stay is the better choice for Group L.")
        else:
            st.info("Run and Stay have the same expected gain for Group L.")
    with col2:
        st.subheader("Group R Analysis")
        st.write(f"Group R: {run_results_R} Run, {stay_results_R} Stay")
        st.write(f"Expected Gain if Run: {gain_run_R:.2f}")
        st.write(f"Expected Gain if Stay: {gain_stay_R:.2f}")
        if gain_run_R > gain_stay_R:
            st.success("Run is the better choice for Group R.")
        elif gain_run_R < gain_stay_R:
            st.success("Stay is the better choice for Group R.")
        else:
            st.info("Run and Stay have the same expected gain for Group R.")
else:
    st.info("Waiting for Depositor Decisions. Click the button above to see results.")