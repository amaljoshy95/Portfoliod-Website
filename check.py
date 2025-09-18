import bse
from get_stock_data import get_stock_data


stock = "HDFCBANK"
b= bse.BSE(r"C:\Users\amaljoshykj\Downloads")
bsecode = b.getScripCode("HDFCBANK")

bsecode = str(bsecode)+".BO"

print(get_stock_data(bsecode))

