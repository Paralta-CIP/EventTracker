import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


def plot_freq(data:list,name:str):
    df = pd.DataFrame(data)
    df['amount'] = 1
    df[0] = pd.to_datetime(df[0])
    df = df.resample('ME',on=0).sum()
    _, ax = plt.subplots()
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.title(f"{name} frequency of each month")
    ax.plot(df.index,df.amount,'o-')
    plt.ylabel('frequency')
    plt.xlabel('time')
    plt.xticks(rotation=45)
    plt.show()

def plot_int(data:list,name:str):
    df = pd.DataFrame(data)
    df[0] = df[1] = pd.to_datetime(df[0])
    df[1] = df[1].diff().shift(-1)
    df[1] = df[1].apply(lambda x:x.days)
    ax = plt.subplots()[1]
    ax.plot(df[0],df[1],'o-')
    plt.title(f"{name} date interval")
    plt.ylabel('interval(day)')
    plt.xlabel('time')
    plt.xticks(rotation=45)
    plt.show()

if __name__ == '__main__':
    import storage
    s = storage.Storage()
    plot_int(s.get('test'),'test')
