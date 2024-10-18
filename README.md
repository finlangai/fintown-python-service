### Python version >=3.12.3

run `pip install -r requirements.txt` to install dependencies

#### The list of stock symbols seeders will seed lie in `config/seeder/stock_list.py`

### **Invoke** commands to use after install dependencies

- `invoke dev` start fastapi dev server
- `invoke seed {seeder name}` seed the corresponding data. e.g. `invoke seed companies`

#### Formula Category:

- 0 financial metric
- 1 stock valuation
