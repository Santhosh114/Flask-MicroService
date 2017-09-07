from flask import Flask
from DataProcessor import *
app = Flask(__name__)


@app.route("/getData/")
def getData():
    return getndx()

@app.route("/avg/<aggregators>/<targetColumn>")
def getAggregates(aggregators,targetColumn):
    print(aggregators.split(","),targetColumn)
    return avgAggregator(aggregators.split(","),targetColumn)

@app.route("/count/<aggregators>/<targetColumn>")
def getAggregatesCount(aggregators, targetColumn):
    return countAggregator(aggregators.split(","), targetColumn)

@app.route("/getCust/<custID>")
def getCustData(custID):
    return getCustomer(custID)


@app.route("/getLocData/<loc>")
def getLocData(loc):
    return getLocSpecificData(loc)

@app.route("/groupLocationSector")
def groupLocationSector():
    return groupLocSector()



if __name__=='__main__':
    app.debug=True
    app.run()
