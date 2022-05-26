import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime

from statsmodels.graphics.tsaplots import plot_acf
from statsmodels.tsa.stattools import adfuller as ADF
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox
from statsmodels.tsa.arima_model import ARIMA

import pmdarima as pm
from pmdarima.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import os
import tensorflow as tf
from keras.models import Sequential, model_from_json
from keras.layers import Dense, LSTM, Dropout


bitcoin_price_history_path = '../data/Bitcoin_price_history.csv'
ethereum_price_history_path = '../data/Ethereum_price_history.csv'
gold_price_history_path = '../data/Gold_price_history.csv'

forecastnum = 5

def basic_analysis(price_Bitcoin):
    # Series graph
    price_Bitcoin.plot()
    plt.show()

    # Autocorrelation
    plot_acf(price_Bitcoin).show()

    # Stalibility
    ADF_test = ADF(price_Bitcoin)
    print('ADF:')
    print(ADF_test)
    # return value: adf、pvalue、usedlag、nobs、critical values、icbest、regresults、

    # --First difference method
    diff_data = price_Bitcoin.diff().dropna()
    diff_data.columns = ['price_diff']
    diff_data.plot()
    plt.show()

    plot_acf(diff_data).show()
    plot_pacf(diff_data).show()
    ADF_diff = ADF(diff_data)
    print('ADF diff:')
    print(ADF_diff)

    # noise
    print('Noise:', acorr_ljungbox(diff_data, lags=1))

def arima_continuous_prediction(price_Bitcoin, train_size):
    # Load/split your data
    train, test = train_test_split(price_Bitcoin, train_size=train_size)
    print('price:')
    print(price_Bitcoin.shape[0])
    print('train:')
    print(train.shape[0])
    print('test:')
    print(test.shape[0])

    # Fit your model
    model = pm.auto_arima(train,
                          start_p=1, start_q=1,
                          information_criterion='aic',
                          test='adf',  # use adftest to find optimal 'd'
                          max_p=3, max_q=3,  # maximum p and q
                          m=1,  # frequency of series
                          d=None,  # let model determine 'd'
                          seasonal=False,  # No Seasonality
                          start_P=0,
                          D=0,
                          trace=True,
                          error_action='ignore',
                          suppress_warnings=True,
                          stepwise=True)

    model.fit(train)
    print(model.summary())

    # make your forecasts
    forecasts = model.predict(test.shape[0])  # predict N steps into the future
    print(forecasts)
    print(test)

    print("Test RMSE: %.3f" % np.sqrt(mean_squared_error(test, forecasts)))

    # Visualize the forecasts (blue=train, green=forecasts)
    x = np.arange(price_Bitcoin.shape[0])
    #plt.plot(x[:train_size], train, c='blue')
    plt.plot(x[train_size:], forecasts, c='red')
    plt.plot(x[:], price_Bitcoin, c = 'blue')
    plt.show()

def arima_one_prediction(price):
    train, test = train_test_split(price, train_size=int(price.shape[0]-1))

    # Fit your model
    model = pm.auto_arima(train,
                          start_p=1, start_q=1,
                          information_criterion='aic',
                          test='adf',  # use adftest to find optimal 'd'
                          max_p=3, max_q=3,  # maximum p and q
                          m=1,  # frequency of series
                          d=None,  # let model determine 'd'
                          seasonal=False,  # No Seasonality
                          start_P=0,
                          D=0,
                          trace=True,
                          error_action='ignore',
                          suppress_warnings=True,
                          stepwise=True)

    model.fit(train)

    # make your forecasts
    forecast = model.predict(test.shape[0])  # predict N steps into the future
    rese = np.sqrt(mean_squared_error(test, forecast))

    return forecast, rese


def arima_realtime_prediction(price_Bitcoin):
    rolling_size = 40
    forecasts = []
    reses = []

    price_Bitcoin.index = [i for i in range(0, price_Bitcoin.shape[0])]

    for i in range(price_Bitcoin.shape[0]-rolling_size):
        forecast, rese = arima_one_prediction(price_Bitcoin[i:i + rolling_size])
        forecasts.append(forecast)
        reses.append(rese)

    print(forecasts)
    print(reses)
    x = np.arange(price_Bitcoin.shape[0])
    # plt.plot(x[:train_size], train, c='blue')
    plt.plot(x[rolling_size:], forecasts, c='red', label='Prediction')
    plt.plot(x[:], price_Bitcoin, c='blue', label='Observation')
    plt.legend()
    plt.show()

    plt.plot(x[rolling_size:], reses, c='blue', label='RESE')
    plt.legend()
    plt.show()

def lstm_prediction(price_Bitcoin, train_size):
    train, test = train_test_split(price_Bitcoin, train_size=train_size)

    #train.index = [i for i in range(0, train.shape[0])]
    # Data preprocess
    train_set = train.values
    train_set = np.reshape(train_set, (len(train_set),1))
    from sklearn.preprocessing import MinMaxScaler
    sc = MinMaxScaler()
    train_set = sc.fit_transform(train_set)
    X_train = train_set[0:len(train_set)-1]
    y_train = train_set[1:len(train_set)]
    X_train = np.reshape(X_train, (len(X_train), 1, 1))

    # Fit your model
    model = Sequential()
    model.add(LSTM(128, activation='sigmoid', input_shape=(1,1)))
    model.add(Dropout(0.0))
    model.add(Dense(1))
    model.compile(loss="mean_squared_error", optimizer='adam')
    model.fit(X_train, y_train, epochs=200, batch_size=50, verbose=2)
    print(model.summary())

    # make your forecasts
    train_Predict = model.predict(X_train)
    train_Predict = sc.inverse_transform(train_Predict)
    y_train = sc.inverse_transform(y_train)

    rese = np.sqrt(mean_squared_error(train_Predict, y_train))
    print(rese)

    # plt.plot(x[:train_size], train, c='blue')
    plt.plot(train_Predict, c='red', label='Prediction')
    plt.plot(y_train, c='blue', label='Observation')
    plt.legend()
    plt.show()

    reses = []
    for i in range(len(train_Predict)-1):
        #print(train_Predict[i])
        #print(y_train[i])
        reses.append(np.sqrt(mean_squared_error(train_Predict[i], y_train[i])))
    plt.plot(reses, c='blue', label='RESE')
    plt.legend()
    plt.show()


def lstm_extend(price_Bitcoin, price_Eth, train_size):
    train, test = train_test_split(price_Bitcoin, train_size=train_size)
    train_Eth, test_Eth = train_test_split(price_Eth, train_size=train_size)


    # train.index = [i for i in range(0, train.shape[0])]
    # Data preprocess
    train_set = train.values
    train_set = np.reshape(train_set, (len(train_set), 1))
    train_extend = pd.DataFrame({'Bitcoin': train.values, 'Eth': train_Eth.values}).values


    from sklearn.preprocessing import MinMaxScaler
    sc = MinMaxScaler()
    train_set = sc.fit_transform(train_set)
    train_extend = sc.fit_transform(train_extend)


    #train_extend = np.reshape(train_extend, (len(train_set), 2, 1))
    #print(train_extend.shape)

    X_train = train_extend[0:len(train_extend) - 1]

    y_train = train_set[1:len(train_set)]
    X_train = np.reshape(X_train, (len(X_train), 2, 1))

    # Fit your model
    model = Sequential()
    model.add(LSTM(128, activation='sigmoid', input_shape=(2, 1)))
    model.add(Dropout(0.0))
    model.add(Dense(1))
    model.compile(loss="mean_squared_error", optimizer='adam')
    model.fit(X_train, y_train, epochs=200, batch_size=50, verbose=2)
    print(model.summary())

    # make your forecasts
    train_Predict = model.predict(X_train)

    X_train = X_train.reshape((len(X_train), 2))

    data_predict = pd.DataFrame(X_train)
    data_predict.iloc[:,0] = train_Predict
    data_predict = sc.inverse_transform(data_predict)
    train_Predict = data_predict[:,0]

    data_y = pd.DataFrame(X_train)
    data_y.iloc[:,0] = y_train
    data_y = sc.inverse_transform(data_y)
    y_train = data_y[:,0]
    #y_train = sc.inverse_transform(y_train)

    rese = np.sqrt(mean_squared_error(train_Predict, y_train))
    print(rese)

    # plt.plot(x[:train_size], train, c='blue')
    plt.plot(train_Predict, c='red', label='Prediction')
    plt.plot(y_train, c='blue', label='Observation')
    plt.legend()
    plt.show()

    reses = []
    for i in range(len(train_Predict) - 1):
        #print(train_Predict[i])
        #print(y_train[i])
        reses.append(np.sqrt(mean_squared_error([train_Predict[i]], [y_train[i]])))
    plt.plot(reses, c='blue', label='RESE')
    plt.legend()
    plt.show()


def main():
    bitcoin_price_history = pd.read_csv(bitcoin_price_history_path)
    bitcoin_price_history['Date'] = bitcoin_price_history['Date'].apply(pd.to_datetime)
    bitcoin_price_history['Close'] = bitcoin_price_history['Close'].astype('float64')
    bitcoin_price_history = bitcoin_price_history.sort_values(by=["Date"])

    s_date_Bitcoin = datetime.datetime.strptime('20181015', '%Y%m%d').date()
    e_date_Bitcoin = datetime.datetime.strptime('20181215', '%Y%m%d').date()
    test_Bitcoin = bitcoin_price_history[(bitcoin_price_history['Date'] >= s_date_Bitcoin) & (bitcoin_price_history['Date'] <= e_date_Bitcoin)]

    price_Bitcoin = test_Bitcoin['Close']
    price_Bitcoin.index = (pd.date_range(s_date_Bitcoin, periods=test_Bitcoin.shape[0]))

    # basic analysis
    #basic_analysis(price_Bitcoin)


    #ARIMA fit
    train_size = int(price_Bitcoin.shape[0]*0.98)
    #arima_continuous_prediction(price_Bitcoin, train_size)
    #arima_realtime_prediction(price_Bitcoin)

    #LSTM fit
    lstm_prediction(price_Bitcoin, train_size)

    #LSTM + feature of Eth
    #ethereum_price_history = pd.read_csv(ethereum_price_history_path)
    #ethereum_price_history['Date'] = ethereum_price_history['Date'].apply(pd.to_datetime)
    #ethereum_price_history['Close'] = ethereum_price_history['Close'].astype('float64')
    #ethereum_price_history = ethereum_price_history.sort_values(by=["Date"])
    #s_date_Eth = datetime.datetime.strptime('20170701', '%Y%m%d').date()
    #e_date_Eth = datetime.datetime.strptime('20180831', '%Y%m%d').date()
    #test_Eth = ethereum_price_history[(ethereum_price_history['Date'] >= s_date_Eth) & (ethereum_price_history['Date'] <= e_date_Eth)]
    #price_Eth = test_Eth['Close']
    #price_Eth.index = (pd.date_range(s_date_Bitcoin, periods=test_Bitcoin.shape[0]))

    #lstm_extend(price_Bitcoin, price_Eth, train_size)



if __name__ == "__main__":

    main()