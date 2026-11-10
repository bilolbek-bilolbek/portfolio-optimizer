import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
from portfolio_optimizer import PortfolioOptimizer
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Portfolio Optimizer", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .header {
        color: #1f77b4;
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="header">📊 Portfolio Optimization Dashboard</div>', unsafe_allow_html=True)
st.write("Build optimal investment portfolios using Modern Portfolio Theory (Markowitz) and machine learning predictions")

# Sidebar
st.sidebar.header("⚙️ Configuration")

# Stock selection
default_stocks = ["TTWO", "MSFT", "AAPL", "GOOGL", "NVDA"]
selected_stocks = st.sidebar.multiselect(
    "Select Stocks",
    default_stocks,
    default=["TTWO", "MSFT", "AAPL"],
    help="Add stocks to your portfolio (TTWO = Take Two Interactive)"
)

# Custom stock input
custom_stock = st.sidebar.text_input("Add custom ticker (e.g., TSLA):", "")
if custom_stock:
    selected_stocks = list(set(selected_stocks + [custom_stock.upper()]))

if not selected_stocks:
    st.warning("⚠️ Please select at least 2 stocks")
    st.stop()

# Date range
col1, col2 = st.sidebar.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime.now() - timedelta(days=365))
with col2:
    end_date = st.date_input("End Date", datetime.now())

# Fetch and process data
st.sidebar.info("Loading data and calculating metrics...")
try:
    optimizer = PortfolioOptimizer(selected_stocks, start_date, end_date)
    prices, returns = optimizer.fetch_data()
    st.sidebar.success("✅ Data loaded successfully!")
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📈 Efficient Frontier", "🎯 Optimization", "📊 Analysis", "🤖 ML Predictions", "📋 Info"]
)

# TAB 1: Efficient Frontier
with tab1:
    st.subheader("Efficient Frontier & Random Portfolios")

    col1, col2 = st.columns([3, 1])

    with col2:
        num_random = st.slider("Random Portfolios", 1000, 10000, 5000, step=1000)
        show_individual = st.checkbox("Show Individual Stocks", True)

    # Calculate efficient frontier
    with st.spinner("Calculating efficient frontier..."):
        frontier_returns, frontier_vols, frontier_weights = optimizer.efficient_frontier(100)
        random_results = optimizer.random_portfolios(num_random)

        # Optimal portfolios
        max_sharpe_weights, max_sharpe_stats = optimizer.optimize_max_sharpe()
        min_vol_weights, min_vol_stats = optimizer.optimize_min_volatility()

    # Create interactive plot
    fig = go.Figure()

    # Random portfolios
    fig.add_trace(go.Scatter(
        x=random_results[1], y=random_results[0],
        mode='markers',
        marker=dict(
            size=5,
            color=random_results[2],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="Sharpe Ratio")
        ),
        name='Random Portfolios',
        text=[f"Sharpe: {s:.2f}" for s in random_results[2]],
        hovertemplate='<b>Risk: %{x:.3f}</b><br>Return: %{y:.3f}<br>%{text}<extra></extra>'
    ))

    # Efficient frontier
    fig.add_trace(go.Scatter(
        x=frontier_vols, y=frontier_returns,
        mode='lines',
        name='Efficient Frontier',
        line=dict(color='red', width=3),
        hovertemplate='<b>Risk: %{x:.3f}</b><br>Return: %{y:.3f}<extra></extra>'
    ))

    # Max Sharpe portfolio
    fig.add_trace(go.Scatter(
        x=[max_sharpe_stats[1]], y=[max_sharpe_stats[0]],
        mode='markers+text',
        marker=dict(size=15, color='gold', symbol='star'),
        name='Max Sharpe Ratio',
        text=['Max Sharpe'],
        textposition='top center',
        hovertemplate='<b>Max Sharpe Portfolio</b><br>Risk: %{x:.3f}<br>Return: %{y:.3f}<br>Sharpe: ' + f'{max_sharpe_stats[2]:.3f}<extra></extra>'
    ))

    # Min volatility portfolio
    fig.add_trace(go.Scatter(
        x=[min_vol_stats[1]], y=[min_vol_stats[0]],
        mode='markers+text',
        marker=dict(size=15, color='green', symbol='diamond'),
        name='Min Volatility',
        text=['Min Vol'],
        textposition='top center',
        hovertemplate='<b>Min Volatility Portfolio</b><br>Risk: %{x:.3f}<br>Return: %{y:.3f}<br>Sharpe: ' + f'{min_vol_stats[2]:.3f}<extra></extra>'
    ))

    # Individual stocks
    if show_individual:
        for ticker in selected_stocks:
            annual_return = optimizer.mean_returns[ticker]
            annual_vol = np.sqrt(optimizer.cov_matrix.loc[ticker, ticker])
            fig.add_trace(go.Scatter(
                x=[annual_vol], y=[annual_return],
                mode='markers+text',
                marker=dict(size=10, symbol='circle'),
                name=ticker,
                text=[ticker],
                textposition='top center'
            ))

    fig.update_layout(
        title='Efficient Frontier Analysis',
        xaxis_title='Volatility (Risk)',
        yaxis_title='Expected Return',
        height=600,
        hovermode='closest',
        template='plotly_white'
    )

    st.plotly_chart(fig, use_container_width=True)

# TAB 2: Optimization
with tab2:
    st.subheader("Portfolio Optimization")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Maximum Sharpe Ratio Portfolio")
        st.metric("Sharpe Ratio", f"{max_sharpe_stats[2]:.3f}")
        st.metric("Expected Return", f"{max_sharpe_stats[0]:.2%}")
        st.metric("Volatility", f"{max_sharpe_stats[1]:.2%}")

        weights_df = pd.DataFrame({
            'Stock': selected_stocks,
            'Weight': max_sharpe_weights,
            'Allocation': max_sharpe_weights * 100
        }).sort_values('Weight', ascending=False)

        st.dataframe(weights_df, use_container_width=True, hide_index=True)

        # Pie chart
        fig_pie = go.Figure(data=[go.Pie(
            labels=weights_df['Stock'],
            values=weights_df['Weight'],
            hovertemplate='<b>%{label}</b><br>Weight: %{percent}<extra></extra>'
        )])
        fig_pie.update_layout(height=400, title="Max Sharpe Portfolio Allocation")
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.write("### Minimum Volatility Portfolio")
        st.metric("Sharpe Ratio", f"{min_vol_stats[2]:.3f}")
        st.metric("Expected Return", f"{min_vol_stats[0]:.2%}")
        st.metric("Volatility", f"{min_vol_stats[1]:.2%}")

        weights_df_minvol = pd.DataFrame({
            'Stock': selected_stocks,
            'Weight': min_vol_weights,
            'Allocation': min_vol_weights * 100
        }).sort_values('Weight', ascending=False)

        st.dataframe(weights_df_minvol, use_container_width=True, hide_index=True)

        # Pie chart
        fig_pie2 = go.Figure(data=[go.Pie(
            labels=weights_df_minvol['Stock'],
            values=min_vol_weights,
            hovertemplate='<b>%{label}</b><br>Weight: %{percent}<extra></extra>'
        )])
        fig_pie2.update_layout(height=400, title="Min Volatility Portfolio Allocation")
        st.plotly_chart(fig_pie2, use_container_width=True)

    # Target return optimization
    st.divider()
    st.write("### Custom Target Return")
    target_ret = st.slider(
        "Target Annual Return",
        min_value=float(optimizer.mean_returns.min()),
        max_value=float(optimizer.mean_returns.max()),
        value=float(optimizer.mean_returns.mean()),
        format="%.2%"
    )

    weights_custom, stats_custom = optimizer.optimize_target_return(target_ret)

    if weights_custom is not None:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Expected Return", f"{stats_custom[0]:.2%}")
        with col2:
            st.metric("Volatility", f"{stats_custom[1]:.2%}")
        with col3:
            st.metric("Sharpe Ratio", f"{stats_custom[2]:.3f}")

        weights_custom_df = pd.DataFrame({
            'Stock': selected_stocks,
            'Weight': weights_custom,
            'Allocation': weights_custom * 100
        }).sort_values('Weight', ascending=False)

        st.dataframe(weights_custom_df, use_container_width=True, hide_index=True)
    else:
        st.warning("Target return not achievable with current stock selection")

# TAB 3: Analysis
with tab3:
    st.subheader("Portfolio Analysis & Risk Metrics")

    col1, col2 = st.columns(2)

    with col1:
        st.write("### Max Sharpe Portfolio - Risk Metrics")
        risk_metrics = optimizer.calculate_risk_metrics(max_sharpe_weights)

        for metric, value in risk_metrics.items():
            if 'volatility' in metric or 'drawdown' in metric:
                st.metric(metric.replace('_', ' ').title(), f"{value:.2%}")
            else:
                st.metric(metric.replace('_', ' ').title(), f"{value:.3f}")

    with col2:
        st.write("### Min Volatility Portfolio - Risk Metrics")
        risk_metrics_minvol = optimizer.calculate_risk_metrics(min_vol_weights)

        for metric, value in risk_metrics_minvol.items():
            if 'volatility' in metric or 'drawdown' in metric:
                st.metric(metric.replace('_', ' ').title(), f"{value:.2%}")
            else:
                st.metric(metric.replace('_', ' ').title(), f"{value:.3f}")

    st.divider()

    # Correlation heatmap
    st.write("### Correlation Matrix")

    correlation = returns.corr()
    fig_corr = go.Figure(data=go.Heatmap(
        z=correlation.values,
        x=correlation.columns,
        y=correlation.columns,
        colorscale='RdBu',
        zmid=0,
        text=np.round(correlation.values, 2),
        texttemplate='%{text:.2f}',
        textfont={"size": 10}
    ))
    fig_corr.update_layout(height=500, title="Stock Correlation Matrix")
    st.plotly_chart(fig_corr, use_container_width=True)

    # Returns distribution
    st.write("### Daily Returns Distribution")

    fig_returns = go.Figure()
    for ticker in selected_stocks:
        fig_returns.add_trace(go.Histogram(
            x=returns[ticker] * 100,
            name=ticker,
            opacity=0.7
        ))

    fig_returns.update_layout(
        title="Daily Returns Distribution",
        xaxis_title="Daily Return (%)",
        yaxis_title="Frequency",
        height=400,
        barmode='overlay'
    )
    st.plotly_chart(fig_returns, use_container_width=True)

# TAB 4: ML Predictions
with tab4:
    st.subheader("Machine Learning Price Predictions")
    st.write("Linear regression model trained on historical data to forecast 30-day returns")

    with st.spinner("Training ML models..."):
        predictions = optimizer.predict_future_returns()

    pred_df = pd.DataFrame([
        {
            'Stock': ticker,
            'Current Price': f"${data['current_price']:.2f}",
            'Predicted Price': f"${data['forecast_price']:.2f}",
            'Predicted Return': f"{data['predicted_return']:.2%}"
        }
        for ticker, data in predictions.items()
    ])

    st.dataframe(pred_df, use_container_width=True, hide_index=True)

    st.info(
        "⚠️ **Disclaimer**: These predictions are based on simple linear regression and historical data. "
        "They should NOT be used as the sole basis for investment decisions. Always conduct thorough due diligence."
    )

# TAB 5: Information
with tab5:
    st.subheader("📖 About This Project")

    st.write("""
    ### Modern Portfolio Theory (Markowitz Optimization)

    This dashboard implements the groundbreaking portfolio optimization theory developed by Harry Markowitz.
    Key concepts:

    - **Efficient Frontier**: The curve showing portfolios with maximum return for each risk level
    - **Sharpe Ratio**: (Return - Risk-free rate) / Volatility — measures risk-adjusted performance
    - **Diversification**: Combining uncorrelated assets reduces overall portfolio risk

    ### Key Metrics Explained

    - **Volatility**: Standard deviation of returns (annualized) — higher = riskier
    - **VaR (95%)**: 95% confidence that daily loss won't exceed this amount
    - **Max Drawdown**: Largest peak-to-trough decline in portfolio value
    - **Sortino Ratio**: Like Sharpe, but only penalizes downside volatility

    ### Machine Learning Component

    The dashboard uses linear regression to forecast 30-day returns based on price trends.
    This is simplified for learning purposes; production systems use more sophisticated models.

    ### Usage Tips

    1. Start with the **Efficient Frontier** tab to understand risk-return tradeoff
    2. Use **Optimization** to compare different portfolio strategies
    3. Check **Risk Metrics** to understand downside protection
    4. Review **ML Predictions** with healthy skepticism
    """)

    st.divider()
    st.write("**Built by**: College portfolio project  |  **Tech**: Python + Streamlit + Scikit-learn")
    st.write("**Data Source**: Yahoo Finance  |  **Analysis Period**: Last 1 year")
