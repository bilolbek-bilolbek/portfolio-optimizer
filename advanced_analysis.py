import numpy as np
import pandas as pd
from scipy.optimize import minimize
from portfolio_optimizer import PortfolioOptimizer
import warnings
warnings.filterwarnings('ignore')

class AdvancedPortfolioAnalysis:
    """
    Advanced portfolio analysis tools:
    - Capital Allocation Line (CAL)
    - Black-Litterman Model (simplified)
    - Risk decomposition
    - Factor analysis
    """

    def __init__(self, optimizer: PortfolioOptimizer):
        self.optimizer = optimizer
        self.risk_free_rate = 0.05

    def capital_allocation_line(self, weights):
        """
        Calculate the Capital Allocation Line (CAL).
        Shows the tradeoff between risk and expected return.
        All portfolios on the CAL have the same Sharpe ratio.
        """
        ret, vol, sharpe = self.optimizer.portfolio_stats(weights)

        # CAL equation: E[Rp] = Rf + Sharpe * σp
        # Returns the function to plot CAL
        return {
            'sharpe_ratio': sharpe,
            'return': ret,
            'volatility': vol,
            'cal_function': lambda x: self.risk_free_rate + sharpe * x
        }

    def risk_decomposition(self, weights):
        """
        Decompose portfolio risk into contributions from each asset.
        Shows how much each position contributes to total portfolio volatility.
        """
        portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(self.optimizer.cov_matrix, weights)))

        # Marginal contribution to risk
        marginal_contrib = np.dot(self.optimizer.cov_matrix, weights) / portfolio_vol

        # Component contribution to risk
        contrib_to_risk = weights * marginal_contrib

        # Risk contribution (%)
        risk_contrib_pct = contrib_to_risk / contrib_to_risk.sum()

        return {
            'marginal_contrib': marginal_contrib,
            'component_contrib': contrib_to_risk,
            'risk_contrib_pct': risk_contrib_pct,
            'total_vol': portfolio_vol
        }

    def covariance_eigenvalues(self):
        """
        Analyze covariance matrix eigenvalues.
        High eigenvalues indicate market-wide systematic risk (market factor).
        Low eigenvalues indicate idiosyncratic risk (stock-specific).
        """
        eigenvalues, eigenvectors = np.linalg.eig(self.optimizer.cov_matrix)

        # Sort by magnitude
        idx = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        # Variance explained by each principal component
        variance_explained = eigenvalues / eigenvalues.sum()
        cumulative_variance = np.cumsum(variance_explained)

        return {
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'variance_explained': variance_explained,
            'cumulative_variance': cumulative_variance
        }

    def rolling_correlation(self, window=60):
        """
        Calculate rolling correlation to see how correlations change over time.
        Useful for understanding regime changes and diversification stability.
        """
        rolling_corr = self.optimizer.returns.rolling(window).corr()
        return rolling_corr

    def value_at_risk(self, weights, confidence_level=0.95, periods=252):
        """
        Calculate multiple VaR estimates:
        - Historical VaR
        - Parametric VaR (Gaussian)
        - Conditional VaR (Expected Shortfall)
        """
        portfolio_returns = (self.optimizer.returns * weights).sum(axis=1)

        # Historical VaR
        var_historical = np.percentile(portfolio_returns, (1 - confidence_level) * 100)

        # Parametric VaR (assuming normal distribution)
        from scipy.stats import norm
        mean_ret = portfolio_returns.mean()
        std_ret = portfolio_returns.std()
        var_parametric = mean_ret + std_ret * norm.ppf(1 - confidence_level)

        # Conditional VaR (Expected Shortfall)
        cvar = portfolio_returns[portfolio_returns <= var_historical].mean()

        return {
            'var_historical': var_historical,
            'var_parametric': var_parametric,
            'cvar': cvar,
            'confidence_level': confidence_level
        }

    def monte_carlo_simulation(self, weights, days=252, simulations=1000):
        """
        Monte Carlo simulation of portfolio paths.
        Useful for understanding possible future portfolio values.
        """
        portfolio_returns = (self.optimizer.returns * weights).sum(axis=1)

        mean_return = portfolio_returns.mean()
        std_return = portfolio_returns.std()

        # Simulate paths
        np.random.seed(42)
        simulated_paths = np.zeros((days, simulations))

        current_price = 100  # Start at 100
        simulated_paths[0] = current_price

        for t in range(1, days):
            random_returns = np.random.normal(mean_return, std_return, simulations)
            simulated_paths[t] = simulated_paths[t-1] * (1 + random_returns)

        # Calculate statistics
        final_values = simulated_paths[-1]
        percentile_5 = np.percentile(final_values, 5)
        percentile_95 = np.percentile(final_values, 95)
        median = np.percentile(final_values, 50)

        return {
            'paths': simulated_paths,
            'final_values': final_values,
            'median': median,
            'percentile_5': percentile_5,
            'percentile_95': percentile_95,
            'expected_final': current_price * (1 + mean_return * days) ** (1/252)
        }

    def portfolio_rebalancing_analysis(self, weights, rebalance_frequency='monthly'):
        """
        Analyze the impact of periodic portfolio rebalancing.
        Shows the cost/benefit of maintaining fixed weights.
        """
        if rebalance_frequency == 'monthly':
            rebalance_periods = self.optimizer.returns.groupby(
                pd.Grouper(freq='M')
            )
        else:  # quarterly
            rebalance_periods = self.optimizer.returns.groupby(
                pd.Grouper(freq='Q')
            )

        results = []
        current_weights = weights.copy()

        for period, group_returns in rebalance_periods:
            # Calculate portfolio return without rebalancing
            period_return = (current_weights * group_returns).sum(axis=1).sum()

            # Update weights based on performance
            cumulative_return = (1 + group_returns).cumprod().iloc[-1]
            current_weights = weights * cumulative_return
            current_weights = current_weights / current_weights.sum()

            results.append({
                'period': period,
                'return': period_return,
                'weights': current_weights.copy()
            })

        return results

    def drawdown_analysis(self, weights):
        """
        Detailed drawdown analysis.
        Helps understand the severity and duration of portfolio declines.
        """
        portfolio_returns = (self.optimizer.returns * weights).sum(axis=1)
        cumulative = (1 + portfolio_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max

        # Find drawdown periods
        drawdown_start = cumulative.idxmax()  # Last peak

        max_dd = drawdown.min()
        max_dd_date = drawdown.idxmin()

        # Duration of max drawdown (in days)
        recovery_date = cumulative[cumulative >= running_max.iloc[-1]].index[-1]
        duration = (recovery_date - drawdown_start).days

        return {
            'max_drawdown': max_dd,
            'max_drawdown_date': max_dd_date,
            'drawdown_duration_days': duration,
            'drawdown_series': drawdown,
            'cumulative_returns': cumulative
        }

    def style_analysis(self, weights):
        """
        Decompose portfolio returns into systematic and idiosyncratic components.
        Shows what portion of returns come from factor exposure vs. stock-picking.
        """
        portfolio_returns = (self.optimizer.returns * weights).sum(axis=1)

        # Market proxy (equal-weighted index)
        market_returns = self.optimizer.returns.mean(axis=1)

        # Regression: Portfolio_Return = Alpha + Beta * Market_Return + Epsilon
        X = market_returns.values.reshape(-1, 1)
        y = portfolio_returns.values

        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(X, y)

        alpha = model.intercept_
        beta = model.coef_[0]

        # R-squared (how much variance explained by market)
        from sklearn.metrics import r2_score
        r_squared = r2_score(y, model.predict(X))

        return {
            'alpha': alpha,
            'beta': beta,
            'r_squared': r_squared,
            'systematic_return': beta * market_returns.mean(),
            'idiosyncratic_return': alpha,
            'total_return': (beta * market_returns.mean()) + alpha
        }


if __name__ == "__main__":
    # Example usage
    from datetime import datetime, timedelta

    tickers = ["TTWO", "MSFT", "AAPL"]
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()

    optimizer = PortfolioOptimizer(tickers, start_date, end_date)
    optimizer.fetch_data()

    analysis = AdvancedPortfolioAnalysis(optimizer)

    # Get optimal portfolio
    weights, stats = optimizer.optimize_max_sharpe()

    print("=== Risk Decomposition ===")
    risk_decomp = analysis.risk_decomposition(weights)
    for ticker, contrib in zip(tickers, risk_decomp['risk_contrib_pct']):
        print(f"{ticker}: {contrib:.2%}")

    print("\n=== VaR Analysis ===")
    var = analysis.value_at_risk(weights)
    print(f"Historical VaR (95%): {var['var_historical']:.4f}")
    print(f"Parametric VaR (95%): {var['var_parametric']:.4f}")
    print(f"Expected Shortfall: {var['cvar']:.4f}")

    print("\n=== Drawdown Analysis ===")
    dd = analysis.drawdown_analysis(weights)
    print(f"Max Drawdown: {dd['max_drawdown']:.2%}")
    print(f"Duration: {dd['drawdown_duration_days']} days")
