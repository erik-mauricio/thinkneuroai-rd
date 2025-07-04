import pandas as pd
import plotly.express as px

class CsvReader:

    def __init__(self, csvFile):
        self.csvFile = csvFile
        self.readCSV = pd.read_csv(self.csvFile)


    def getReadCSV(self):
        return self.readCSV


    def kitTrackingData(self):
        csv = self.getReadCSV()
        shipping_statuses = csv['kit_shipping_status'].value_counts()
        data = {
            "Category": shipping_statuses.index,
            "Value": shipping_statuses.values
        }
        return data