from QDABacktest.brokers.backtest import *
from QDABacktest.core import BacktestEngine
from QDABacktest.analysis.backtest.analyzer import BacktestAnalyzer
from QDABacktest.analysis.technical import RateOfChange
from QDABacktest.visualizers.backtest_visualizer import BasicVisualizer
from QDABacktest.strategies.trend import ActualMomentumStratagy
from QDABacktest.callbacks import PositionWeightPrinterCallback
from QDABacktest import reporters
import matplotlib.pyplot as plt
import FinanceDataReader as fdr

def main(tickers, name="NAME", n=200, momentum_threshold=1, rebalance_period=TimeFrames.day * 28):
    dp = BacktestDataProvider()
    dp.add_yf_tickers(*tickers)
    dp.add_technical_indicators(tickers, [TimeFrames.day], [RateOfChange(n)])

    indexer = TimeIndexer(dp.get_longest_timestamp_seq())
    dp.set_indexer(indexer)

    brk = BacktestBroker(dp, initial_margin=10000)
    [brk.add_asset(Asset(ticker=ticker)) for ticker in tickers]

    strategy = ActualMomentumStratagy(
        momentum_threshold=momentum_threshold,
        rebalance_period=rebalance_period,
        momentum_label=f"ROCR{n}",
    )

    engine = BacktestEngine()
    engine.register_broker(brk)
    engine.register_strategy(strategy)
    log = engine.run()
    
    reporters.make_html(log, "^IXIC", output=f"{name}_dualmomentum.html")

if __name__ == '__main__':
    
    main([
            "AAPL",
            "FB",
            "NFLX",
            "GOOGL",
            "NVDA",
            "TSLA",
            "AMZN",
            "TWTR",
            "BIDU",
            "BABA"
    ], name="FANG+")