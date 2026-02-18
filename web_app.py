# basic imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from app import run_app

st.set_page_config(
    page_title="Portfolio Rebalancing Tool",
    layout="wide"
)

st.title("📊 Portfolio Rebalancing Suggestion Tool")
st.subheader("Agentic AI with CSV Upload & Visual Dashboard")

st.markdown(
    "Upload your portfolio CSV file and view AI-driven rebalancing insights "
    "with side-by-side visualizations for easy analysis."
)

# CSV file fetcher 
uploaded_file = st.file_uploader(
    "Upload Portfolio CSV",
    type=["csv"]
)

if uploaded_file:
    try:
        user_df = pd.read_csv(uploaded_file)

        required_columns = {
            "Asset",
            "Asset_Class",
            "Current_Value",
            "Target_Allocation"
        }

        if not required_columns.issubset(user_df.columns):
            st.error(
                f"CSV must contain columns: {', '.join(required_columns)}"
            )
        else:
            if st.button("Analyze Uploaded Portfolio"):
                with st.spinner("Analyzing portfolio using Agentic AI..."):
                    result = run_app(user_df)

                portfolio_df = result["portfolio"]  # Assuming it's a DataFrame or string; adjust if needed

                st.success("Analysis completed successfully!")

                # Portfolio Table
                st.header("📌 Uploaded Portfolio Data")
                st.dataframe(portfolio_df, use_container_width=True)

                # Visualization of graphs 
                st.header("📊 Portfolio Visual Analysis")

                col1, col2, col3 = st.columns(3)

                # 1. Pie Chart
                with col1:
                    st.subheader("Current Allocation")
                    fig1, ax1 = plt.subplots()
                    ax1.pie(
                        portfolio_df["Current_Value"],
                        labels=portfolio_df["Asset"],
                        autopct="%1.1f%%",
                        startangle=90
                    )
                    ax1.axis("equal")
                    st.pyplot(fig1)

                # 2. Target vs Current
                with col2:
                    st.subheader("Target vs Current")
                    fig2, ax2 = plt.subplots()
                    ax2.bar(
                        portfolio_df["Asset"],
                        portfolio_df["Current_Weight"],
                        label="Current"
                    )
                    ax2.bar(
                        portfolio_df["Asset"],
                        portfolio_df["Target_Allocation"],
                        alpha=0.7,
                        label="Target"
                    )
                    ax2.legend()
                    st.pyplot(fig2)

                # 3. Allocation Drift
                with col3:
                    st.subheader("Allocation Drift")
                    fig3, ax3 = plt.subplots()
                    ax3.bar(
                        portfolio_df["Asset"],
                        portfolio_df["Drift"]
                    )
                    ax3.axhline(0)
                    st.pyplot(fig3)

                # Output
                st.header("🔍 AI Portfolio Analysis")
                st.write(result["analysis"])

                st.header("📈 Rebalancing Recommendation")
                st.write(result["decision"])

                st.header("🧠 Final Explanation")
                st.write(result["explanation"])
    except Exception as e:
        st.error(f"Error processing file: {e}")