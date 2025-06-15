import pandas as pd


def avg_freq(data: list):
    count = len(data) - 1 # Minor 1 to be more accurate
    date_delta = pd.to_datetime(data[-1][0]) - pd.to_datetime(data[0][0])
    avg = count / date_delta.days * 30.417
    return round(avg, 2)

def avg_int(data: list):
    dates = [row[0] for row in data]
    timestamps = pd.to_datetime(dates)
    diffs = timestamps.diff().dropna() # dropna() : drop first value which has no diff
    avg = diffs.mean().days
    return round(avg, 2)
