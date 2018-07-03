import pickle

data = pickle.load(open("Zipline_Test_Pickle", "rb"))
data.to_csv("Zipline_Test.csv")