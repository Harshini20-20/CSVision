import streamlit as st
import pandas as pd

from insights import generate_ai_insights

from charts import (
    show_histogram,
    show_scatter,
    show_boxplot,
    show_piechart,
    show_heatmap
)

from reports import (
    create_excel_report,
    create_ppt_report
)

from ml_models import (
    run_ml_model
)

st.set_page_config(
    page_title="AI CSVision",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI CSVision")
st.caption(
    "AI Powered CSV Analytics Dashboard"
)

uploaded_file = st.file_uploader(
    "Upload CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    try:

        df = pd.read_csv(uploaded_file)

        st.success(
            f"Loaded {df.shape[0]} rows and {df.shape[1]} columns"
        )

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "Overview",
                "Visualizations",
                "AI Insights",
                "Machine Learning",
                "Data Cleaning"
            ]
        )

        # -------------------
        # OVERVIEW
        # -------------------

        with tab1:

            st.subheader(
                "Dataset Preview"
            )

            st.dataframe(
                df.head()
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Rows",
                df.shape[0]
            )

            c2.metric(
                "Columns",
                df.shape[1]
            )

            c3.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )

            st.subheader(
                "Column Information"
            )

            info_df = pd.DataFrame({
                "Column": df.columns,
                "Datatype": df.dtypes.astype(str),
                "Missing Values": df.isnull().sum().values
            })

            st.dataframe(info_df)

            st.subheader(
                "Reports"
            )

            if st.button(
                "Generate Excel Report"
            ):

                excel_file = create_excel_report(
                    df
                )

                with open(
                    excel_file,
                    "rb"
                ) as f:

                    st.download_button(
                        "Download Excel Report",
                        f,
                        file_name="AI_CSVision_Report.xlsx"
                    )

            if st.button(
                "Generate PPT Report"
            ):

                insights = generate_ai_insights(
                    df
                )

                ppt_file = create_ppt_report(
                    insights
                )

                with open(
                    ppt_file,
                    "rb"
                ) as f:

                    st.download_button(
                        "Download PPT Report",
                        f,
                        file_name="AI_CSVision_Report.pptx"
                    )

        # -------------------
        # VISUALIZATIONS
        # -------------------

        with tab2:

            st.subheader(
                "Interactive Charts"
            )

            chart_type = st.selectbox(
                "Choose Chart",
                [
                    "Histogram",
                    "Scatter",
                    "Box Plot",
                    "Pie Chart",
                    "Heatmap"
                ]
            )

            if chart_type == "Histogram":
                show_histogram(df)

            elif chart_type == "Scatter":
                show_scatter(df)

            elif chart_type == "Box Plot":
                show_boxplot(df)

            elif chart_type == "Pie Chart":
                show_piechart(df)

            elif chart_type == "Heatmap":
                show_heatmap(df)

        # -------------------
        # AI INSIGHTS
        # -------------------

        with tab3:

            st.subheader(
                "🤖 AI Generated Insights"
            )

            insights = generate_ai_insights(
                df
            )

            for item in insights:

                st.info(item)

        # -------------------
        # MACHINE LEARNING
        # -------------------

        with tab4:

            st.subheader(
                "Machine Learning"
            )

            target_column = st.selectbox(
                "Select Target Column",
                df.columns
            )

            if st.button(
                "Run ML Model"
            ):

                model_type, score = run_ml_model(
                    df,
                    target_column
                )

                st.success(
                    f"Model Type: {model_type}"
                )

                if model_type == "Classification":

                    st.metric(
                        "Accuracy",
                        f"{score:.2%}"
                    )

                else:

                    st.metric(
                        "R² Score",
                        f"{score:.4f}"
                    )

        # -------------------
        # DATA CLEANING
        # -------------------

        with tab5:

            st.subheader(
                "Data Cleaning Tools"
            )

            if st.button(
                "Remove Duplicates"
            ):

                before = len(df)

                df = df.drop_duplicates()

                after = len(df)

                st.success(
                    f"Removed {before-after} duplicate rows"
                )

            if st.button(
                "Drop Missing Rows"
            ):

                before = len(df)

                df = df.dropna()

                after = len(df)

                st.success(
                    f"Removed {before-after} rows with missing values"
                )

            st.download_button(
                "Download Cleaned Dataset",
                df.to_csv(index=False),
                file_name="cleaned_dataset.csv",
                mime="text/csv"
            )

    except Exception as e:

        st.error(
            f"Error loading file: {e}"
        )

else:

    st.info(
        "Upload a CSV file to start analysis."
    )