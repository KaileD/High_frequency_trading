import pandas
import numpy
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
import matplotlib.pyplot as plt

CONST_TRAINING_SEQUENCE_LENGTH = 12  # 1 hour
CONST_TESTING_CASES = 5  # 5 hours


def data_normalization(data):
    return [(datum-data[0])/data[0] for datum in data]


def data_de_normalization(data, base):
    return [(datum+1)*base for datum in data]


def get_deep_learning_data(ticker):

    # Load data
    data = pandas.read_csv('../02. Data/01. IntradayCN/' + ticker + '.csv')['close'].tolist()
    # print(data)

    # Build traing model
    dataTraining = []
    for i in range(len(data)-CONST_TESTING_CASES*CONST_TRAINING_SEQUENCE_LENGTH):
        dataSegment = data[i:i+CONST_TRAINING_SEQUENCE_LENGTH+1]
        dataTraining.append(data_normalization(dataSegment))

    dataTraining = numpy.array(dataTraining)
    numpy.random.shuffle(dataTraining)
    # print(dataTraining)
    X_Training = dataTraining[:, :-1]
    Y_Training = dataTraining[:, -1]

    # test model
    X_Testing = []
    Y_Testing_Base = []
    for i in range(CONST_TESTING_CASES, 0, -1):
        dataSegment = data[-(i+1)*CONST_TRAINING_SEQUENCE_LENGTH:-i*CONST_TRAINING_SEQUENCE_LENGTH]
        Y_Testing_Base.append(dataSegment[0])
        X_Testing.append(data_normalization(dataSegment))

    Y_Testing = data[-CONST_TESTING_CASES*CONST_TRAINING_SEQUENCE_LENGTH:]

    X_Testing = numpy.array(X_Testing)
    Y_Testing = numpy.array(Y_Testing)

    # reshape
    X_Training = numpy.reshape(X_Training, (X_Training.shape[0], X_Training.shape[1],1))
    X_Testing = numpy.reshape(X_Testing, (X_Testing.shape[0], X_Testing.shape[1],1))

    return X_Training, Y_Training, X_Testing, Y_Testing, Y_Testing_Base


def predict(model, X):
    predictionsNormalized = []

    for i in range(len(X)):
        data = X[i]
        result = []

        for j in range(CONST_TRAINING_SEQUENCE_LENGTH):
            predicted = model.predict(data[numpy.newaxis, :, :])[0, 0]
            result.append(predicted)
            data = data[1:]
            data = numpy.insert(data, [CONST_TRAINING_SEQUENCE_LENGTH-1], predicted, axis=0)

        predictionsNormalized.append(result)

    return predictionsNormalized


def plot_results(Y_hat, Y):
    plt.plot(Y)

    for i in range(len(Y_hat)):
        padding = [None for _ in range(i*CONST_TRAINING_SEQUENCE_LENGTH)]
        plt.plot(padding+Y_hat[i])

    plt.show()


def predictLSTM(ticker):

    # Load data
    X_Training, Y_Training, X_Testing, Y_Testing, Y_Testing_Base = get_deep_learning_data(ticker)

    print(Y_Testing)

    # build model
    model = Sequential()
    # layer1
    model.add(LSTM(
        input_dim=1,
        output_dim=50,
        return_sequences=True
    ))
    model.add(Dropout(0.2))

    # layer2
    model.add(LSTM(
        100,
        return_sequences=False
    ))
    model.add(Dropout(0.1))

    # output layer
    model.add(Dense(output_dim=1))
    model.add(Activation('linear'))

    model.compile(loss='mse', optimizer='rmsprop')

    # Train Model
    model.fit(X_Training, Y_Training,
              batch_size=256,  # depends on memory size
              nb_epoch=5,
              validation_split=0.05
              )

    # predict
    predictionNormalized = predict(model, X_Testing)

    # De_normalize
    predictions = []
    for i, row in enumerate(predictionNormalized):
        predictions.append(data_de_normalization(row, Y_Testing_Base[i]))

    # todo: Plot
    plot_results(predictions, Y_Testing)


predictLSTM(ticker='600031')
