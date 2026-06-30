"""
Weather Analytics Dashboard

Streamlit application providing interactive weather data analysis.
Features: dataset overview, search, statistics, ranking, and charts.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ─── Page Configuration ───────────────────────────────────────────
st.set_page_config(
    page_title="Weather Analytics Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data
def load_dataset():
    """Load and prepare the weather dataset."""
    df = pd.read_csv("datasets/weather_dataset.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month_name()
    df["month_num"] = df["date"].dt.month
    df["weekday"] = df["date"].dt.day_name()
    return df


def get_daily_averages(df, selected_date):
    """
    Get average weather metrics for a given date.

    Args:
        df (pd.DataFrame): The weather dataset.
        selected_date (str or datetime): The date to query.

    Returns:
        pd.Series or None: Average metrics for the date.
    """
    daily = df[df["date"] == pd.to_datetime(selected_date)]
    if daily.empty:
        return None
    return daily[
        ["temperature", "humidity", "wind_speed",
         "pressure", "rainfall", "air_quality"]
    ].mean()


def get_record_by_datetime(df, selected_date, selected_time):
    """
    Get the exact weather record for a given date and time.

    Args:
        df (pd.DataFrame): The weather dataset.
        selected_date (str or datetime): The date to query.
        selected_time (str): The time to query (HH:00 format).

    Returns:
        pd.DataFrame: Matching records.
    """
    mask = (
        (df["date"] == pd.to_datetime(selected_date))
        & (df["time"] == selected_time)
    )
    return df[mask]


# ─── Load Data ────────────────────────────────────────────────────
df = load_dataset()

# ─── Sidebar Navigation ──────────────────────────────────────────
st.sidebar.title("Navigation")
section = st.sidebar.radio(
    "Go to",
    [
        "Dataset Overview",
        "Search",
        "Statistics",
        "Ranking",
        "Charts",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Dataset Info")
st.sidebar.metric("Total Records", f"{len(df):,}")
st.sidebar.metric("Cities", df["city"].nunique())
st.sidebar.metric(
    "Date Range",
    f"{df['date'].min().strftime('%Y-%m-%d')} → "
    f"{df['date'].max().strftime('%Y-%m-%d')}",
)


# ─── Section: Dataset Overview ────────────────────────────────────
if section == "Dataset Overview":
    st.title("Dataset Overview")
    st.markdown(
        "Explore the full synthetic weather dataset "
        "generated using **Faker**."
    )

    # Summary cards
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "Avg Temperature",
        f"{df['temperature'].mean():.1f}°C",
    )
    col2.metric(
        "Avg Humidity",
        f"{df['humidity'].mean():.0f}%",
    )
    col3.metric(
        "Rainy Hours",
        f"{(df['rainfall'] > 0).sum():,}",
    )
    col4.metric(
        "Cities",
        df["city"].nunique(),
    )

    st.markdown("---")

    # City filter
    city_filter = st.multiselect(
        "Filter by City",
        options=df["city"].unique(),
        default=df["city"].unique(),
    )
    filtered = df[df["city"].isin(city_filter)]

    st.dataframe(
        filtered,
        use_container_width=True,
        height=500,
    )

    st.markdown(f"**Showing {len(filtered):,} records**")


# ─── Section: Search ─────────────────────────────────────────────
elif section == "Search":
    st.title("Search Weather Records")

    tab1, tab2 = st.tabs([
        "Search by Date",
        "Search by Date & Time",
    ])

    with tab1:
        st.subheader("Daily Averages")
        selected_date = st.date_input(
            "Select a date",
            value=pd.to_datetime("2025-04-10"),
            min_value=df["date"].min(),
            max_value=df["date"].max(),
            key="date_search",
        )

        averages = get_daily_averages(df, selected_date)
        if averages is not None:
            st.success(
                f"Average weather for "
                f"**{selected_date.strftime('%B %d, %Y')}**"
            )
            col1, col2, col3 = st.columns(3)
            col1.metric(
                "Avg Temperature",
                f"{averages['temperature']:.1f}°C",
            )
            col2.metric(
                "Avg Humidity",
                f"{averages['humidity']:.0f}%",
            )
            col3.metric(
                "Avg Rainfall",
                f"{averages['rainfall']:.1f} mm",
            )

            col4, col5, col6 = st.columns(3)
            col4.metric(
                "Avg Wind Speed",
                f"{averages['wind_speed']:.1f} km/h",
            )
            col5.metric(
                "Avg Pressure",
                f"{averages['pressure']:.1f} hPa",
            )
            col6.metric(
                "Avg AQI",
                f"{averages['air_quality']:.0f}",
            )

            # Show all records for that day
            st.markdown("---")
            st.subheader("All Records for This Day")
            day_records = df[
                df["date"] == pd.to_datetime(selected_date)
            ]
            st.dataframe(
                day_records, use_container_width=True
            )
        else:
            st.warning("No records found for this date.")

    with tab2:
        st.subheader("Exact Record Lookup")
        col_d, col_t = st.columns(2)
        with col_d:
            search_date = st.date_input(
                "Select a date",
                value=pd.to_datetime("2025-04-10"),
                min_value=df["date"].min(),
                max_value=df["date"].max(),
                key="datetime_search",
            )
        with col_t:
            search_hour = st.selectbox(
                "Select hour",
                options=[f"{h:02d}:00" for h in range(24)],
                index=14,
            )

        record = get_record_by_datetime(
            df, search_date, search_hour
        )
        if not record.empty:
            st.success(
                f"Record for **{search_date}** at "
                f"**{search_hour}**"
            )
            for _, row in record.iterrows():
                col1, col2, col3 = st.columns(3)
                col1.metric("City", row["city"])
                col2.metric(
                    "Temperature",
                    f"{row['temperature']}°C",
                )
                col3.metric(
                    "Humidity",
                    f"{row['humidity']}%",
                )

                col4, col5, col6 = st.columns(3)
                col4.metric(
                    "Pressure",
                    f"{row['pressure']} hPa",
                )
                col5.metric(
                    "Rainfall",
                    f"{row['rainfall']} mm",
                )
                col6.metric(
                    "Wind Speed",
                    f"{row['wind_speed']} km/h",
                )

                col7, col8 = st.columns(2)
                col7.metric(
                    "UV Index",
                    row["uv_index"],
                )
                col8.metric(
                    "Air Quality (AQI)",
                    row["air_quality"],
                )
        else:
            st.warning(
                "No record found for this date and time."
            )


# ─── Section: Statistics ─────────────────────────────────────────
elif section == "Statistics":
    st.title("Statistical Analysis")

    # City filter for statistics
    stat_city = st.selectbox(
        "Select City (or All)",
        options=["All Cities"] + list(df["city"].unique()),
    )
    if stat_city == "All Cities":
        stat_df = df
    else:
        stat_df = df[df["city"] == stat_city]

    st.subheader("Descriptive Statistics")

    metrics = [
        "temperature", "humidity", "wind_speed",
        "pressure", "rainfall", "air_quality",
    ]

    stats_data = []
    for metric in metrics:
        col = stat_df[metric]
        mode_val = col.mode()
        mode_display = mode_val.iloc[0] if not mode_val.empty else "N/A"

        stats_data.append({
            "Metric": metric.replace("_", " ").title(),
            "Mean": round(col.mean(), 2),
            "Median": round(col.median(), 2),
            "Mode": mode_display,
            "Variance": round(col.var(), 2),
            "Std Dev": round(col.std(), 2),
            "Min": round(col.min(), 2),
            "Max": round(col.max(), 2),
        })

    st.dataframe(
        pd.DataFrame(stats_data),
        use_container_width=True,
        hide_index=True,
    )

    # Percentiles
    st.markdown("---")
    st.subheader("Percentiles")

    percentile_data = []
    for metric in metrics:
        col = stat_df[metric]
        percentile_data.append({
            "Metric": metric.replace("_", " ").title(),
            "P90": round(col.quantile(0.90), 2),
            "P95": round(col.quantile(0.95), 2),
            "P99": round(col.quantile(0.99), 2),
        })

    st.dataframe(
        pd.DataFrame(percentile_data),
        use_container_width=True,
        hide_index=True,
    )


# ─── Section: Ranking ────────────────────────────────────────────
elif section == "Ranking":
    st.title("Temperature Rankings")

    n_records = st.number_input(
        "Number of records to show (N)",
        min_value=1,
        max_value=100,
        value=10)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Top {n_records} Highest Temperatures")
        top_n = df.nlargest(n_records, "temperature")
        st.dataframe(
            top_n[
                ["date", "time", "city", "temperature",
                 "humidity", "pressure"]
            ],
            use_container_width=True,
            hide_index=True,
        )
        nth_max = top_n.iloc[-1]
        st.info(
            f"The {n_records}th highest temperature is "
            f"**{nth_max['temperature']}°C** "
            f"in **{nth_max['city']}** on "
            f"**{nth_max['date'].strftime('%Y-%m-%d')}** "
            f"at **{nth_max['time']}**"
        )

    with col2:
        st.subheader(f"Top {n_records} Lowest Temperatures")
        bottom_n = df.nsmallest(n_records, "temperature")
        st.dataframe(
            bottom_n[
                ["date", "time", "city", "temperature",
                 "humidity", "pressure"]
            ],
            use_container_width=True,
            hide_index=True,
        )
        nth_min = bottom_n.iloc[-1]
        st.info(
            f"The {n_records}th lowest temperature is "
            f"**{nth_min['temperature']}°C** "
            f"in **{nth_min['city']}** on "
            f"**{nth_min['date'].strftime('%Y-%m-%d')}** "
            f"at **{nth_min['time']}**"
        )


# ─── Section: Charts ─────────────────────────────────────────────
elif section == "Charts":
    st.title("Weather Charts")

    # City filter for charts
    chart_city = st.selectbox(
        "Select City (or All)",
        options=["All Cities"] + list(df["city"].unique()),
        key="chart_city",
    )
    if chart_city == "All Cities":
        chart_df = df.copy()
    else:
        chart_df = df[df["city"] == chart_city].copy()

    # Daily averages for trend charts
    daily_avg = (
        chart_df
        .groupby("date")
        .agg({
            "temperature": "mean",
            "humidity": "mean",
            "rainfall": "sum",
        })
        .reset_index()
    )

    # Temperature Trend
    st.subheader("Temperature Trend (Daily Average)")
    fig_temp = px.line(
        daily_avg,
        x="date",
        y="temperature",
        labels={
            "date": "Date",
            "temperature": "Temperature (°C)",
        },
    )
    fig_temp.update_traces(
        line=dict(color="#FF6B6B", width=1.5)
    )
    fig_temp.update_layout(
        template="plotly_dark",
        height=400,
    )
    st.plotly_chart(fig_temp, use_container_width=True)

    # Humidity Trend
    st.subheader("Humidity Trend (Daily Average)")
    fig_hum = px.line(
        daily_avg,
        x="date",
        y="humidity",
        labels={
            "date": "Date",
            "humidity": "Humidity (%)",
        },
    )
    fig_hum.update_traces(
        line=dict(color="#4ECDC4", width=1.5)
    )
    fig_hum.update_layout(
        template="plotly_dark",
        height=400,
    )
    st.plotly_chart(fig_hum, use_container_width=True)

    # Rainfall Trend
    st.subheader("Rainfall Trend (Daily Total)")
    fig_rain = px.bar(
        daily_avg,
        x="date",
        y="rainfall",
        labels={
            "date": "Date",
            "rainfall": "Rainfall (mm)",
        },
    )
    fig_rain.update_traces(
        marker_color="#45B7D1"
    )
    fig_rain.update_layout(
        template="plotly_dark",
        height=400,
    )
    st.plotly_chart(fig_rain, use_container_width=True)

    # Monthly Averages
    st.subheader("Monthly Average Temperature by City")
    monthly = (
        df
        .groupby(["month_num", "month", "city"])["temperature"]
        .mean()
        .reset_index()
        .sort_values("month_num")
    )
    fig_monthly = px.bar(
        monthly,
        x="month",
        y="temperature",
        color="city",
        barmode="group",
        labels={
            "month": "Month",
            "temperature": "Avg Temperature (°C)",
            "city": "City",
        },
    )
    fig_monthly.update_layout(
        template="plotly_dark",
        height=500,
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

    # Histogram
    st.subheader("Temperature Distribution")
    fig_hist = px.histogram(
        chart_df,
        x="temperature",
        nbins=50,
        color="city" if chart_city == "All Cities" else None,
        labels={"temperature": "Temperature (°C)"},
    )
    fig_hist.update_layout(
        template="plotly_dark",
        height=400,
    )
    st.plotly_chart(fig_hist, use_container_width=True)
