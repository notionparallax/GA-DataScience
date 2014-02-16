import MySQLdb
import pandas as pd
from __future__ import division
from sklearn import preprocessing

from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq

def queryAsTable(query, maxrows=5, how=2):
    """This queries a db and returns the response as a pandas dataframe"""
    # Open database connection
    db = MySQLdb.connect(user = 'root',
                         passwd = 'password',
                         db = 'mysql',
                         host = 'localhost')
    db.query(query)
    result = db.store_result()
    rdict = list(result.fetch_row(maxrows=maxrows, how=how)) #max=0 means all, how=0 means tuple, how=1-dict, how=2 dict with fully qualified names
    df = pd.DataFrame(rdict)
    # disconnect from server
    db.close()
    return df

def binConfidence(predictions):
    confBins = {}
    for b in range(0,110,10):
        confBins[b] = 0   #produces: {0: 0, 100: 0, 70: 0, 40: 0, 10: 0, 80: 0, 50: 0, 20: 0, 90: 0, 60: 0, 30: 0} (dicts are unordered)

    for p in predictions.values:
        count = p[0]
        conf  = p[1]
        binNum = int(round(conf/10.0)*10)
        confBins[binNum] += count
    return confBins

def makeLables(mid):
    if mid == 0:
        return "{}-{}".format(mid, mid+5)
    elif mid == 100:
        return "{}-{}".format(mid-5, mid)
    else:
        return "{}-{}".format(mid-5, mid+5)

def sqError(target, actual):
    if actual == 0 or target == 0:
        return 0
    return (target-actual) ** 2

def signedSqError(target, actual):
    dif = target-actual
    sign = 1 if dif<0 else -1
    return sqError(target, actual) * sign

def pc_col(col1, col2):
        if col2==0:
            return 0
        else:
            return col1 / col2

def binTimes(delta):
    """
produces a dict with the bin number and the name
0: postHoc
1: simultanious
2: day
3: week
4: month
5: year
6: fiveYear
7: tenYear
8: FiftyYear
9: overFiftyYear
"""
    if type(delta) != datetime.timedelta:
        print delta, "not a datetime.timedelta"
    outlookClassification = {'bin':0, 'bin_name':''}

    if delta < datetime.timedelta(days=0):
        outlookClassification['bin'] = 0
        outlookClassification['bin_name'] = "    postHoc"

    elif delta == datetime.timedelta(days=0):
        outlookClassification['bin'] = 1
        outlookClassification['bin_name'] = "simultanious"

    elif delta < datetime.timedelta(days=1):
        outlookClassification['bin'] = 2
        outlookClassification['bin_name'] = "        day"

    elif delta < datetime.timedelta(days=7):
        outlookClassification['bin'] = 3
        outlookClassification['bin_name'] = "       week"

    elif delta < datetime.timedelta(days=30):
        outlookClassification['bin'] = 4
        outlookClassification['bin_name'] = "      month"

    elif delta < datetime.timedelta(days=365):
        outlookClassification['bin'] = 5
        outlookClassification['bin_name'] = "       year"

    elif delta < datetime.timedelta(days=365*5):
        outlookClassification['bin'] = 6
        outlookClassification['bin_name'] = "   fiveYear"

    elif delta < datetime.timedelta(days=365*10):
        outlookClassification['bin'] = 7
        outlookClassification['bin_name'] = "    tenYear"

    elif delta < datetime.timedelta(days=365*50):
        outlookClassification['bin'] = 8
        outlookClassification['bin_name'] = "  FiftyYear"

    else:
        outlookClassification['bin'] = 9
        outlookClassification['bin_name'] = "overFiftyYear"

    return outlookClassification

def times_are_legit(thing_that_should_be_a_time):
    """This checks the type. It seems that very long predictions aren't pandas dates, they default to python dates, so you need to check for both."""
    isPD = type(thing_that_should_be_a_time) == pd.tslib.Timestamp
    isDS = type(thing_that_should_be_a_time) == datetime.datetime
    return isPD or isDS

def timeDelta(created, deadline):
    if times_are_legit(created) and times_are_legit(deadline): #check that the inputs are well formed
        return  binTimes(deadline - created)

def make_prediction_count_profile(this_user = 500):
    userQ = "WHERE predictions.creator_id = '{}'".format(this_user)
    query = """select * from  mysql.predictions {}""".format(userQ)
    predictions = queryAsTable(query, maxrows=0)
    #this all feels very ugly, especially the part where I make a coumn, split it and then delete it :(
    pair = zip(predictions["predictions.created_at"], predictions["predictions.deadline"])

    predictions["outlook"] = [timeDelta(x[0],x[1]) for x in pair]
    predictions["outlook_bin"] = [x["bin"] for x in predictions["outlook"]]
    predictions["outlook_bin_name"] = [x["bin_name"] for x in predictions["outlook"]]
    firstPredDate = predictions["predictions.created_at"].min()
    predictions["time_since_start"] = [x-firstPredDate for x in predictions["predictions.created_at"]]
    predictions["seconds_since_start"] = [x.total_seconds() for x in predictions["time_since_start"]]

    predictions = predictions.drop(["outlook","predictions.uuid"],1)

    desc = predictions["outlook_bin"].describe()

    prediction_count_profile = dict(predictions["outlook_bin_name"].value_counts().to_dict(), **desc.to_dict())

    pcp = {}
    for k in prediction_count_profile:
        pcp["prediction_count_profile_"+k.strip()] = prediction_count_profile[k]

    return pcp


def summarise_conf_profile(cp):
        cps = {}
        for b in range(11):
            numLabel = str(cp["Confidence"][b])
            cps[numLabel + "_truePC"] = cp["truePC"][b]
            cps[numLabel + "_falsePC"] = cp["falsePC"][b]

            cps[numLabel + "_sqErrorPC"] = cp["sqError"][b]
            cps[numLabel + "_signedSqErrorPC"] = cp["signedSqError"][b]
        return cps


def quantifyUser(this_user = 500):

    columns = [ 'j.outcome',                                                            #from judgements
                #'p.withdrawn',                                                          #from predictions
                'r.confidence', 'r.created_at', 'r.id', 'r.prediction_id', 'r.user_id'] #from responses
    columns = ", ".join(columns) #make the array into a string

    query = """
        SELECT myp.confidence        AS conf,
               Count(myp.confidence) AS cnt
        FROM   (SELECT {0}
                FROM   mysql.responses r
                       LEFT OUTER JOIN mysql.judgements j
                                    ON r.prediction_id = j.prediction_id
                WHERE  j.outcome IS NOT NULL AND
                       r.confidence IS NOT NULL AND
                       r.user_id = '{1}' AND
                       j.outcome = '{2}'
        ) AS myp
        GROUP BY myp.confidence
        ORDER BY myp.confidence
    """

    #Q is this really a good way to do this? Can sql do this for me better?
    trueP  = queryAsTable(query.format(columns, this_user, 1), maxrows=0, how=2)
    falseP = queryAsTable(query.format(columns, this_user, 0), maxrows=0, how=2)

    trueConfBins  = binConfidence(trueP)
    falseConfBins = binConfidence(falseP)

    trueDF = pd.DataFrame(trueConfBins.items(), columns=['Confidence', 'True_Prediction_count']).sort(columns="Confidence")
    falseDF = pd.DataFrame(falseConfBins.items(), columns=['Confidence', 'False_Prediction_count']).sort(columns="Confidence")

    #merge the true anf false data frames on the confidence bins
    conf_profile = pd.merge(trueDF, falseDF, on="Confidence")
    #make a new column that gives the total number of predictions in that bracket
    conf_profile["PredictionCountTotal"] = conf_profile["True_Prediction_count"] + conf_profile["False_Prediction_count"]
    #make a new column that gives the % of predictions that came true at in that bracket
    conf_profile["truePC"]  = [pc_col(x[0],x[1]) for x in zip(conf_profile["True_Prediction_count"],  conf_profile["PredictionCountTotal"])]
    conf_profile["falsePC"] = [pc_col(x[0],x[1]) for x in zip(conf_profile["False_Prediction_count"],  conf_profile["PredictionCountTotal"])] # not needed, but used in sanity check

    #make labels for the x axis
    conf_profile["ConfidenceIntervals"] = conf_profile["Confidence"].map(lambda x: makeLables(x))
    #sanity check
    conf_profile["check"] = conf_profile["truePC"] + conf_profile["falsePC"]

    pair = zip(conf_profile["Confidence"],conf_profile["truePC"])
    conf_profile["sqError"]       = [      sqError(x[0]/100,x[1]) for x in pair]
    conf_profile["signedSqError"] = [signedSqError(x[0]/100,x[1]) for x in pair]

    """
    calibrationPlot = plt.figure(1)
    plt.subplot(211)

    #calibrationPlot = Figure()#(figsize=None, dpi=None, facecolor=None, edgecolor=None, linewidth=0.0, frameon=None, subplotpars=None, tight_layout=None)
    #Plot the scatter, x is confidences
    plt.scatter( conf_profile["Confidence"].map(lambda x: x/10).tolist(),   #vector of y values (currently [0,1,2,3,4,5,6,7,8,9,10])
                      conf_profile.truePC,                                       #vector of x values
                      s=conf_profile.PredictionCountTotal*3)                     #vector of sizes
    #draw a diagonal line across the graph
    plt.plot([0, 10], [0, 1], 'k-', lw=1)
    #set the limits of the graph
    pylab.ylim([0,1])
    pylab.xlim([0,10])
    #add a background grid
    plt.grid()
    #make the ticks and labels
    plt.xticks([x    for x in range(11)], [x           for x in conf_profile["ConfidenceIntervals"].tolist()]) #locations, labels
    plt.yticks([x/10 for x in range(11)], [str(x)+ "%" for x in conf_profile["Confidence"].tolist()])

    plt.subplot(212)

    plt.plot( conf_profile["Confidence"].map(lambda x: x/10).tolist(),   #vector of y values (currently [0,1,2,3,4,5,6,7,8,9,10])
              conf_profile["PredictionCountTotal"])                      #vector of x values
    """
    #sum of squared errors is an attempt to capture overall calibration
    sqe = sum(conf_profile["sqError"].tolist())
    #sum of signed squared errors is an attempt to capture the direction of calibration. If the result comes up negative then the predictor is generally overconfident.
    ssqe = sum(conf_profile["signedSqError"].tolist())

    #print sqe
    #print ssqe
    #print this_user
    #print sum(conf_profile["PredictionCountTotal"].tolist())
    #print conf_profile

    rtn = {}
    rtn["user"]                     = this_user
    #rtn["calibrationPlot"]          = calibrationPlot
    rtn["summedSquaredError"]       = sqe
    rtn["signedSummedSquaredError"] = ssqe
    rtn["totalPredictions"]         = sum(conf_profile["PredictionCountTotal"].tolist())
    rtn = dict(rtn, **summarise_conf_profile(conf_profile))
    rtn = dict(rtn, **make_prediction_count_profile(this_user))

    return rtn
