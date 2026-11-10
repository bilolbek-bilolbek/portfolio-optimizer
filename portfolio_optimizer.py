import numpy as np
import pandas as pd
from scipy.optimize import minimize
import yfinance as yf
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')

class PortfolioOptimizer:
    """
    Portfolio Optimizer using Modern Portfolio Theory (Markowitz)
    Supports efficient frontier calculation, optimization, and ML-based predictions
    """

    def __init__(self, tickers, start_date, end_date):
        self.tickers = tickers
        self.start_date = start_date
        self.end_date = end_date
        self.returns = None
        self.cov_matrix = None
        self.mean_returns = None
        self.prices = None
        self.risk_free_rate = 0.05  # 5% risk-free rate

    def fetch_data(self):
        """Fetch historical price data from Yahoo Finance"""
        try:
            data = yf.download(self.tickers, start=self.start_date, end=self.end_date, progress=False)

            if len(self.tickers) == 1:
                self.prices = data['Adj Close'].to_frame()
                self.prices.columns = self.tickers
            else:
                self.prices = data['Adj Close']

            self.returns = self.prices.pct_change().dropna()
            self.mean_returns = self.returns.mean() * 252  # Annualize
            self.cov_matrix = self.returns.cov() * 252

            return self.prices, self.returns
        except Exception as e:
            raise ValueError(f"Error fetching data: {str(e)}")

    def portfolio_stats(self, weights):
        """Calculate portfolio return, volatility, and Sharpe ratio"""
        portfolio_return = np.sum(weights * self.mean_returns)
        portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(self.cov_matrix, weights)))
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_vol

        return portfolio_return, portfolio_vol, sharpe_ratio

    def negative_sharpe(self, weights):
        """Objective function: minimize negative Sharpe ratio"""
        return -self.portfolio_stats(weights)[2]

    def portfolio_volatility(self, weights):
        """Objective function: minimize volatility"""
        return self.portfolio_stats(weights)[1]

    def optimize_max_sharpe(self):
        """Find portfolio with maximum Sharpe ratio"""
        n_assets = len(self.tickers)
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = tuple((0, 1) for _ in range(n_assets))
        init_guess = np.array([1/n_assets] * n_assets)

        result = minimize(self.negative_sharpe, init_guess, method='SLSQP',
                         bounds=bounds, constraints=constraints)

        return result.x, self.portfolio_stats(result.x)

    def optimize_min_volatility(self):
        """Find portfolio with minimum volatility"""
        n_assets = len(self.tickers)
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = tuple((0, 1) for _ in range(n_assets))
        init_guess = np.array([1/n_assets] * n_assets)

        result = minimize(self.portfolio_volatility, init_guess, method='SLSQP',
                         bounds=bounds, constraints=constraints)

        return result.x, self.portfolio_stats(result.x)

    def optimize_target_return(self, target_return):
        """Find portfolio with minimum volatility for target return"""
        n_assets = len(self.tickers)
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
            {'type': 'eq', 'fun': lambda x: np.sum(x * self.mean_returns) - target_return}
        ]
        bounds = tuple((0, 1) for _ in range(n_assets))
        init_guess = np.array([1/n_assets] * n_assets)

        try:
            result = minimize(self.portfolio_volatility, init_guess, method='SLSQP',
                             bounds=bounds, constraints=constraints)
            if result.success:
                return result.x, self.portfolio_stats(result.x)
            return None, None
        except:
            return None, None

    def efficient_frontier(self, num_points=100):
        """Generate efficient frontier"""
        min_ret = self.mean_returns.min()
        max_ret = self.mean_returns.max()
        target_returns = np.linspace(min_ret, max_ret, num_points)

        frontier_vols = []
        frontier_weights = []

        for target in target_returns:
            weights, stats = self.optimize_target_return(target)
            if weights is not None:
                frontier_vols.append(stats[1])
                frontier_weights.append(weights)

        return target_returns[:len(frontier_vols)], frontier_vols, frontier_weights

    def random_portfolios(self, num_portfolios=5000):
        """Generate random portfolios for comparison"""
        n_assets = len(self.tickers)
        results = np.zeros((3, num_portfolios))

        np.random.seed(42)
        for i in range(num_portfolios):
            weights = np.random.random(n_assets)
            weights /= np.sum(weights)

            ret, vol, sharpe = self.portfolio_stats(weights)
            results[0,i] = ret
            results[1,i] = vol
            results[2,i] = sharpe

        return results

    def predict_future_returns(self, lookback=252, forecast_days=30):
        """Use ML (linear regression) to predict future returns"""
        predictions = {}

        for ticker in self.tickers:
            prices = self.prices[ticker].values
            X = np.arange(len(prices)).reshape(-1, 1)
            y = prices

            model = LinearRegression()
            model.fit(X, y)

            # Predict next forecast_days
            future_X = np.arange(len(prices), len(prices) + forecast_days).reshape(-1, 1)
            future_prices = model.predict(future_X)

            current_price = prices[-1]
            predicted_return = (future_prices[-1] - current_price) / current_price
            predictions[ticker] = {
                'predicted_return': predicted_return,
                'current_price': current_price,
                'forecast_price': future_prices[-1]
            }

        return predictions

    def calculate_risk_metrics(self, weights):
        """Calculate detailed risk metrics for a portfolio"""
        portfolio_returns = (self.returns * weights).sum(axis=1)

        # Value at Risk (95% confidence)
        var_95 = np.percentile(portfolio_returns, 5)

        # Maximum Drawdown
        cumulative = (1 + portfolio_returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min()

        # Sortino Ratio (penalizes downside volatility)
        downside_returns = portfolio_returns[portfolio_returns < 0]
        downside_vol = downside_returns.std() * np.sqrt(252)
        sortino = (portfolio_returns.mean() * 252 - self.risk_free_rate) / downside_vol if downside_vol > 0 else 0

        return {
            'var_95': var_95,
            'max_drawdown': max_drawdown,
            'sortino_ratio': sortino,
            'annual_return': portfolio_returns.mean() * 252,
            'annual_volatility': portfolio_returns.std() * np.sqrt(252)
        }
