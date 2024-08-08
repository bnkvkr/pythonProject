import subprocess

def run_spider(stock_name):
    result = subprocess.run(['scrapy', 'crawl', 'news_spider', '-a', f'stock_name={stock_name}'], capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
    else:
        print(result.stdout)
    return result.returncode

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        stock_name = sys.argv[1]
        run_spider(stock_name)
    else:
        print("Please provide a stock name.")
