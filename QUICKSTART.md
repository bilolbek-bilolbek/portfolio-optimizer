# Quick Start Guide

## 30-Second Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py

# 3. Open browser
# Dashboard opens at http://localhost:8501
```

## What You'll See

### 🎯 Efficient Frontier Tab
- **Interactive chart** showing thousands of random portfolios
- **Red line**: The "frontier" - all mathematically optimal portfolios
- **Gold star**: Maximum Sharpe Ratio portfolio (best risk-adjusted returns)
- **Green diamond**: Minimum volatility portfolio (least risky)

**Action**: Hover over points to see individual portfolio stats

### 💼 Optimization Tab  
- **Max Sharpe Portfolio**: Best return per unit of risk
- **Min Volatility Portfolio**: Safest choice
- **Custom Target Return**: Slider to design portfolio for your goal

**Action**: Try different target returns - watch how weights change

### 📊 Analysis Tab
- **Risk Metrics**: VaR (worst-case loss), Maximum Drawdown, Sortino Ratio
- **Correlation Heatmap**: Which stocks move together?
- **Returns Distribution**: Where daily returns cluster

**Action**: Compare risk metrics between the two optimized portfolios

### 🤖 ML Predictions Tab
- **30-day forecasts** for each stock
- Predicted returns based on trend analysis

⚠️ **Remember**: These are simplified predictions. Don't trade on them alone!

### 📖 Info Tab
- Educational material on portfolio theory
- Detailed metric explanations
- How everything works

## Try These Experiments

### Experiment 1: Diversification Benefit
1. Select 2 stocks: TTWO + MSFT
2. Note the efficient frontier
3. Add 3 more tech stocks
4. Compare: Did the efficient frontier improve?
5. **Why?** More diversification = better portfolios possible

### Experiment 2: Tech vs. Everything
1. Create portfolio: TTWO, MSFT, AAPL (all tech)
2. Note volatility in Min Vol portfolio
3. Now add defensive stocks: JNJ, KO (healthcare, consumer staples)
4. Note the improvement in volatility
5. **Why?** Low-correlation assets reduce overall risk

### Experiment 3: Risk vs. Return
1. Adjust "Target Annual Return" slider from low to high
2. Watch volatility increase
3. Find the "sweet spot" - your desired return with acceptable risk
4. **Why?** Can't have high returns without accepting risk

## College Application Talking Points

When presenting this project, emphasize:

✅ **Mathematical Rigor**
- Implemented Modern Portfolio Theory (Markowitz)
- Solved constrained optimization problems
- Understood covariance matrices and correlation

✅ **Real-World Application**
- Fetches actual stock data from Yahoo Finance
- Produces actionable portfolio recommendations
- Demonstrates understanding of risk metrics

✅ **Full-Stack Execution**
- Backend: Python + optimization library
- Data layer: Real-time data fetching
- Frontend: Interactive Streamlit dashboard
- Visualization: Professional Plotly charts

✅ **Problem-Solving Approach**
- Identified a real problem (portfolio construction)
- Researched academic theory
- Implemented solution
- Built interactive tool to explore space

## Troubleshooting

**"ModuleNotFoundError: No module named 'streamlit'"**
```bash
pip install -r requirements.txt
```

**"No data found" error**
- Check your stock tickers are valid (AAPL, MSFT, NVDA, etc.)
- Ensure your internet connection works
- Yahoo Finance may be temporarily down - try again

**Dashboard is slow**
- Streamlit caches data, but first run takes time
- Reduce "Random Portfolios" slider to 1,000
- Reduce date range (use last 6 months instead of 1 year)

**Charts not showing**
- Clear browser cache (Cmd+Shift+R on Mac)
- Restart Streamlit: press Ctrl+C and run `streamlit run app.py` again

## Next Steps

### To Improve the Project

1. **Add more stocks** - compare different sectors (Tech, Healthcare, Finance)
2. **Backtest strategies** - see if historical optimal portfolios actually worked
3. **Add constraints** - limit exposure to any one sector
4. **Real-time dashboard** - track your portfolio daily
5. **Deploy online** - push to Heroku or AWS so you can share

### To Deepen Your Learning

- Read Harry Markowitz's original 1952 paper
- Study the Capital Asset Pricing Model (CAPM)
- Learn about factor models (Fama-French)
- Explore Monte Carlo simulations
- Study Bayesian optimization methods

## Resources

- **Yahoo Finance**: https://finance.yahoo.com/
- **Efficient Frontier**: https://en.wikipedia.org/wiki/Efficient_frontier
- **Streamlit Docs**: https://docs.streamlit.io/
- **Markowitz's Work**: https://scholar.google.com/citations?user=d4d4tNoAAAAJ

---

**Happy exploring! 🚀**
