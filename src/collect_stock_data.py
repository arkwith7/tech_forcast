import yfinance as yf
import pandas as pd
import os

# 설정
start_date = "2016-01-01"
end_date = "2024-12-31"
output_dir = "/home/arkwith/SKKU/tech_forcast/data/raw"

# 종목 코드 (삼성전자, SK하이닉스)
tickers = {
    "samsung_stock": "005930.KS",
    "skhynix_stock": "000660.KS"
}

def fetch_and_save(name, ticker):
    print(f"Fetching data for {name} ({ticker})...")
    try:
        df = yf.download(ticker, start=start_date, end=end_date)
        if not df.empty:
            # 인덱스(날짜)를 컬럼으로 변환
            df.reset_index(inplace=True)
            # 컬럼명 소문자 변환
            df.columns = [c.lower() if isinstance(c, str) else c[0].lower() for c in df.columns]
            
            save_path = os.path.join(output_dir, f"{name}.csv")
            df.to_csv(save_path, index=False)
            print(f"Saved to {save_path}")
        else:
            print(f"No data found for {name}")
    except Exception as e:
        print(f"Error fetching {name}: {e}")

if __name__ == "__main__":
    os.makedirs(output_dir, exist_ok=True)
    for name, ticker in tickers.items():
        fetch_and_save(name, ticker)

