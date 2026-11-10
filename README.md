# Portfolio Optimization Dashboard

A professional-grade portfolio optimization tool built with **Modern Portfolio Theory** (Markowitz), **machine learning predictions**, and an interactive **Streamlit dashboard**. This project demonstrates core quantitative finance concepts applicable to real-world investment decisions.

## 📊 Features

### Core Optimization Engine
- **Efficient Frontier Calculation**: Generates the mathematical boundary of optimal portfolios
- **Maximum Sharpe Ratio Optimization**: Finds the portfolio with the best risk-adjusted returns
- **Minimum Volatility Portfolio**: Identifies the least risky portfolio combination
- **Target Return Optimization**: Constructs optimal portfolios for specific return targets

### Interactive Dashboard
- **Efficient Frontier Visualization**: Interactive plot showing 5,000+ random portfolios vs. the optimal frontier
- **Real-time Optimization**: Compare different portfolio strategies instantly
- **Risk Analysis**: Comprehensive risk metrics including Value at Risk (VaR), Maximum Drawdown, Sortino Ratio
- **Correlation Analysis**: Visual heatmap of stock correlations
- **ML Price Predictions**: 30-day price forecasts using linear regression

### Data & Analysis
- **Yahoo Finance Integration**: Real-time stock data fetching
- **Customizable Date Range**: Analyze any historical period
- **Multi-stock Support**: Compare unlimited stocks (Nasdaq/NYSE)
- **Risk Metrics**: VaR, Maximum Drawdown, Sortino Ratio, Sharpe Ratio

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone or download the project
cd portfolio-optimizer

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## 📈 How It Works

### Modern Portfolio Theory (MPT)

The foundation of this project is **Harry Markowitz's Portfolio Theory** (1952), which proves that:

1. **Diversification reduces risk** without sacrificing returns
2. **The Efficient Frontier** contains all optimal portfolios
3. **The Sharpe Ratio** measures risk-adjusted performance: `(Return - Rf) / Volatility`

### Mathematical Framework

**Portfolio Return:**
```
E[Rp] = Σ(wi × E[Ri])
```
where wi = weight of asset i, E[Ri] = expected return of asset i

**Portfolio Volatility:**
```
σp = √(w^T × Σ × w)
```
where Σ = covariance matrix, w = weight vector

**Optimization Problem:**
```
maximize: (E[Rp] - Rf) / σp  (Sharpe Ratio)
subject to: Σwi = 1 (fully invested)
            wi ≥ 0 (no short-selling)
```

### Machine Learning Component

The dashboard includes a simple **linear regression model** that:
- Analyzes historical price trends
- Forecasts 30-day price movements
- Provides return predictions for portfolio weighting

*Note: This is for learning purposes. Production systems use LSTM, GRU, or more sophisticated models.*

## 📊 Dashboard Sections

### 1. **Efficient Frontier Tab**
- Visualizes thousands of random portfolios
- Shows the mathematical efficient frontier in red
- Highlights optimal portfolios (Max Sharpe, Min Volatility)
- Individual stock positions

### 2. **Optimization Tab**
- Compares Maximum Sharpe Ratio vs. Minimum Volatility portfolios
- Shows optimal weights for each stock
- Pie charts showing portfolio allocation
- Custom target-return optimization

### 3. **Analysis Tab**
- Risk metrics: VaR, Maximum Drawdown, Sortino Ratio
- Correlation heatmap between stocks
- Daily returns distribution
- Volatility comparison

### 4. **ML Predictions Tab**
- 30-day price forecasts
- Predicted returns for each stock
- Current vs. predicted prices

### 5. **Info Tab**
- Educational content on portfolio theory
- Metric explanations
- Usage tips

## 🧮 Risk Metrics Explained

| Metric | Definition | Interpretation |
|--------|-----------|-----------------|
| **Sharpe Ratio** | (Return - Risk-free) / Volatility | Higher = better risk-adjusted returns |
| **Volatility** | Std Dev of returns (annualized) | Higher = more fluctuation/risk |
| **VaR (95%)** | Daily loss at 95% confidence | Worst case loss 1 day in 20 |
| **Max Drawdown** | Largest peak-to-trough decline | Maximum historical loss from peak |
| **Sortino Ratio** | Like Sharpe, but ignores upside volatility | Focuses on downside risk |

## 💡 Example Usage

### Scenario 1: Conservative Investor
1. Set date range (e.g., last 5 years)
2. Select defensive stocks (low volatility tech like MSFT)
3. Go to Optimization tab → Find **Min Volatility Portfolio**
4. Review Risk Metrics → Check Maximum Drawdown

### Scenario 2: Growth-Focused Investor
1. Select growth stocks (high volatility: NVDA, TSLA)
2. Go to Efficient Frontier tab
3. Identify **Max Sharpe Ratio Portfolio**
4. Check if forecasted returns meet your goals (ML tab)

### Scenario 3: Target-Return Portfolio
1. Decide on target return (e.g., 15% annually)
2. Optimization tab → Slide "Target Annual Return"
3. Review required volatility
4. Evaluate if acceptable for your risk tolerance

## 🔬 Technical Stack

| Component | Technology |
|-----------|-----------|
| **Language** | Python 3.8+ |
| **Dashboard** | Streamlit |
| **Data Fetching** | yfinance |
| **Numerical Computing** | NumPy, Pandas |
| **Optimization** | SciPy (SLSQP algorithm) |
| **ML** | Scikit-learn |
| **Visualization** | Plotly |

## 📚 Learning Outcomes

By building this project, I've learned:

- **Quantitative Finance**: Modern Portfolio Theory, risk metrics, portfolio optimization
- **Mathematical Optimization**: Constraint optimization, Lagrange multipliers, SLSQP algorithm
- **Machine Learning**: Linear regression, time-series forecasting
- **Data Engineering**: Real-time data fetching, data cleaning, data transformation
- **Software Engineering**: Object-oriented design, modular architecture, UI/UX
- **Data Visualization**: Interactive charts, heatmaps, distribution analysis

## 🎓 College Application Relevance

This project demonstrates:

1. **Strong mathematical foundation** in linear algebra, optimization, and statistics
2. **Real-world application** of academic theory (Markowitz, CAPM)
3. **Full-stack development**: Data fetching → computation → visualization
4. **Professional software practices**: Clean code, documentation, error handling
5. **Problem-solving**: From problem definition to production dashboard
6. **Intellectual curiosity**: Self-directed learning in quantitative finance

## ⚠️ Disclaimer

This tool is for **educational purposes**. The machine learning predictions are simplified and should **NOT** be used as the sole basis for investment decisions. Always:

- Conduct thorough due diligence
- Diversify across multiple asset classes
- Consider your personal risk tolerance
- Consult professional financial advisors before investing

Historical performance ≠ future results.

## 🚀 Future Enhancements

- [ ] Multi-asset class support (bonds, crypto, commodities)
- [ ] Black-Litterman model for improved return estimates
- [ ] Constraint handling (sector limits, ESG scoring)
- [ ] Advanced ML models (LSTM, ensemble methods)
- [ ] Real-time portfolio tracking
- [ ] Risk factor analysis (Fama-French factors)
- [ ] Backtesting framework
- [ ] Cloud deployment (Heroku, AWS)

## 📖 Resources & References

### Academic
- Markowitz, H. (1952). "Portfolio Selection". *Journal of Finance*
- Sharpe, W. F. (1966). "Mutual Fund Performance". *Journal of Business*

### Books
- "A Random Walk Down Wall Street" - Burton Malkiel
- "Advances in Financial Machine Learning" - Marcos López de Prado
- "Python for Finance" - Yves Hilpisch

### Online
- Efficient Frontier: https://en.wikipedia.org/wiki/Efficient_frontier
- Sharpe Ratio: https://en.wikipedia.org/wiki/Sharpe_ratio
- Yahoo Finance API: https://finance.yahoo.com/

## 📧 Contact

Built as a portfolio project for college applications.

---

**Last Updated**: September 2026
