import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pyathena import connect
import os

st.set_page_config(layout="wide", page_title="Stroke Prediction Dashboard")


st.header("Static Charts (CSV)")
static_container = st.container()

with static_container:
    df_static = pd.read_csv("stroke.csv")
    st.subheader("Raw Data (Top 10 rows)")
    st.dataframe(df_static.head(10))

    # Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Stroke Count by Gender (Static)")
        st.write("Total number of strokes for each gender.")
        gender_count = df_static.groupby("gender")["stroke"].sum().reset_index()
        fig1, ax1 = plt.subplots()
        sns.barplot(x="gender", y="stroke", data=gender_count, palette="coolwarm", ax=ax1)
        ax1.set_ylabel("Stroke Count")
        ax1.set_xlabel("Gender")
        ax1.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig1)

    with col2:
        st.subheader("Average BMI by Stroke (Static)")
        st.write("Average BMI for stroke vs non-stroke patients.")
        avg_bmi = df_static.groupby("stroke")["bmi"].mean().reset_index()
        fig2, ax2 = plt.subplots()
        sns.lineplot(x="stroke", y="bmi", data=avg_bmi, marker="o", color="purple", ax=ax2)
        ax2.set_ylabel("Average BMI")
        ax2.set_xlabel("Stroke (0=No, 1=Yes)")
        ax2.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig2)

    # Row 2
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Stroke by Hypertension (Static)")
        st.write("Counts strokes by hypertension status (0 = no, 1 = yes).")
        hyper_count = df_static[df_static["stroke"] == 1].groupby("hypertension")["stroke"].count().reset_index()
        fig3, ax3 = plt.subplots()
        sns.barplot(x="hypertension", y="stroke", data=hyper_count, palette="viridis", ax=ax3)
        ax3.set_ylabel("Stroke Count")
        ax3.set_xlabel("Hypertension")
        ax3.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig3)

    with col4:
        st.subheader("Stroke by Smoking Status (Static)")
        st.write("Number of strokes grouped by smoking status (never, formerly, smokes).")
        smoke_count = df_static[df_static["stroke"] == 1].groupby("smoking_status")["stroke"].count().reset_index()
        fig4, ax4 = plt.subplots()
        sns.lineplot(x="smoking_status", y="stroke", data=smoke_count, marker="o", color="green", ax=ax4)
        ax4.set_ylabel("Stroke Count")
        ax4.set_xlabel("Smoking Status")
        ax4.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig4)

# -----------------------------
# DYNAMIC CHARTS
# -----------------------------
st.header("Dynamic Charts (Live from Athena)")
dynamic_container = st.container()

with dynamic_container:
    conn = connect(
        aws_access_key_id=st.secrets["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
        s3_staging_dir="s3://cloud-computing-data-warehouse-stroke-prediction/Unsaved/",
        region_name="eu-west-1"
    )

    # Row 1
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Stroke Count by Gender (Dynamic)")
        st.write("Counts strokes for each gender from live Athena table (bar chart).")
        query_gender = """
            SELECT gender, COUNT(*) AS stroke_count
            FROM "stroke_db"."cloud_computing_data_warehouse_stroke_prediction"
            WHERE stroke = 1
            GROUP BY gender
        """
        df_gender = pd.read_sql(query_gender, conn)
        fig5, ax5 = plt.subplots()
        sns.barplot(x="gender", y="stroke_count", data=df_gender, palette="Set2", ax=ax5)
        ax5.set_ylabel("Stroke Count")
        ax5.set_xlabel("Gender")
        ax5.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig5)

    with col2:
        st.subheader("Average Age by Stroke (Dynamic)")
        st.write("Average age of stroke vs non-stroke patients (line chart).")
        query_age = """
            SELECT stroke, AVG(age) AS avg_age
            FROM "stroke_db"."cloud_computing_data_warehouse_stroke_prediction"
            GROUP BY stroke
        """
        df_age = pd.read_sql(query_age, conn)
        fig6, ax6 = plt.subplots()
        sns.lineplot(x="stroke", y="avg_age", data=df_age, marker="o", color="red", ax=ax6)
        ax6.set_ylabel("Average Age")
        ax6.set_xlabel("Stroke (0=No, 1=Yes)")
        ax6.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig6)

    # Row 2
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Stroke by Hypertension (Dynamic)")
        st.write("Counts strokes grouped by hypertension status (bar chart).")
        query_hyper = """
            SELECT hypertension, COUNT(*) AS stroke_count
            FROM "stroke_db"."cloud_computing_data_warehouse_stroke_prediction"
            WHERE stroke = 1
            GROUP BY hypertension
        """
        df_hyper = pd.read_sql(query_hyper, conn)
        fig7, ax7 = plt.subplots()
        sns.barplot(x="hypertension", y="stroke_count", data=df_hyper, palette="pastel", ax=ax7)
        ax7.set_ylabel("Stroke Count")
        ax7.set_xlabel("Hypertension")
        ax7.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig7)

    with col4:
        st.subheader("Stroke by Smoking Status (Dynamic)")
        st.write("Counts strokes grouped by smoking status (line chart).")
        query_smoke = """
            SELECT smoking_status, COUNT(*) AS stroke_count
            FROM "stroke_db"."cloud_computing_data_warehouse_stroke_prediction"
            WHERE stroke = 1
            GROUP BY smoking_status
        """
        df_smoke = pd.read_sql(query_smoke, conn)
        fig8, ax8 = plt.subplots()
        sns.lineplot(x="smoking_status", y="stroke_count", data=df_smoke, marker="o", color="orange", ax=ax8)
        ax8.set_ylabel("Stroke Count")
        ax8.set_xlabel("Smoking Status")
        ax8.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig8)

    # -----------------------------
    # CUSTOM USER QUERY
    # -----------------------------
    st.subheader("Custom Dynamic Query")
    st.write(
        "Enter a SQL query below (example: `SELECT gender, COUNT(*) AS stroke_count FROM \"stroke_db\".\"cloud_computing_data_warehouse_stroke_prediction\" WHERE stroke = 1 GROUP BY gender`) "
        "and choose chart type (bar or line)."
    )
    user_query = st.text_area("SQL Query", height=100)
    chart_type = st.selectbox("Chart Type", ["bar", "line"])

    if st.button("Generate Chart"):
        if user_query.strip() == "":
            st.error("Please enter a SQL query!")
        else:
            try:
                df_custom = pd.read_sql(user_query, conn)
                st.write(df_custom.head())
                fig_custom, ax_custom = plt.subplots()
                if chart_type == "bar":
                    sns.barplot(data=df_custom, x=df_custom.columns[0], y=df_custom.columns[1], palette="Set1", ax=ax_custom)
                elif chart_type == "line":
                    sns.lineplot(data=df_custom, x=df_custom.columns[0], y=df_custom.columns[1], marker="o", color="teal", ax=ax_custom)
                st.pyplot(fig_custom)
            except Exception as e:
                st.error(f"Error running query or generating chart: {e}")
