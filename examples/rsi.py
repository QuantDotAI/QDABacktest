from QDABacktest.brokers.backtest import *
from QDABacktest.core import BacktestEngine
from QDABacktest.analysis.backtest.analyzer import BacktestAnalyzer
from QDABacktest.analysis.technical import RSI
from QDABacktest.visualizers.backtest_visualizer import BasicVisualizer
from QDABacktest.strategies.basic import OscillatorStrategy
from QDABacktest.callbacks import PositionWeightPrinterCallback
from QDABacktest import reporters
import matplotlib.pyplot as plt
import yfinance as yf

def main(ticker, n=14, timecut_days=7):
    dp = BacktestDataProvider()
    dp.add_yf_tickers(ticker)
    dp.add_technical_indicators([ticker], [TimeFrames.day], [RSI(n)])

    indexer = TimeIndexer(dp.get_shortest_timestamp_seq())
    dp.set_indexer(indexer)
    dp.cut_data()

    brk = BacktestBroker(dp, initial_margin=10000)
    brk.add_asset(Asset(ticker=ticker))

    strategy = OscillatorStrategy(
        breakout_threshold=50, oversold_threshold=40, overbought_threshold=60, 
        osc_label=f"RSI{n}", use_short=False, 
        use_time_cut=False, timecut_params={"days" : timecut_days},
        use_stop_loss=True, stop_loss_params={"threshold": 5},
        use_n_perc_rule=False, n_perc_params={"n_percent" : 5, "loss_cut_percent" : 10}
    )

    engine = BacktestEngine()
    engine.register_broker(brk)
    engine.register_strategy(strategy)
    log = engine.run()
    
    reporters.make_html(log, ticker, output=f"{ticker}_rsi.html")


if __name__ == "__main__":
    main("^GSPC")
    main("^IXIC")