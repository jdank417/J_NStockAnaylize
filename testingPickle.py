import pickle

stock_data = {"2023-10-06": "171.32", "2023-10-13": "178.4"}

pickle.dump(stock_data, open("save.p", "wb"))