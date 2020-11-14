import os
import ray
import tqdm
import argparse
import FinanceDataReader as fdr


@ray.remote
def download_and_save_ticker(target_dir, ticker):
    path = os.path.join(target_dir, ticker + ".csv")
    fdr.DataReader(ticker).to_csv(path)


def download_and_save_exchange(target_dir, exchange):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    ret = [download_and_save_ticker.remote(target_dir, t) for t in fdr.StockListing(exchange)["Symbol"].values]
    [ray.get(r) for r in tqdm.tqdm(ret, desc=exchange)]

if __name__ == "__main__":
    ray.init()
    parser = argparse.ArgumentParser()
    parser.add_argument('-exchanges', nargs="+", required=True)
    parser.add_argument("-target_dir", type=str)
    args = parser.parse_args()
    for exchange in args.exchanges:
        download_and_save_exchange(
            os.path.join(args.target_dir, exchange), exchange)

# python QDABacktest/data_downloader/fdr.py -exchanges KRX KOSPI KOSDAQ KONEX NASDAQ NYSE AMEX SSE SZSE HKEX TSE -target_dir ~/Storage/fdr_data/

