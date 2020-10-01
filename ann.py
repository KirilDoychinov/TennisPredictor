import pandas as pd
import numpy as np
from keras import models, layers, Sequential
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import mutual_info_classif
from matplotlib import pyplot
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import seaborn as sn
from functions import generate_attributes
from keras import models, layers
from keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.model_selection import train_test_split
from keras.models import load_model
import matplotlib.pyplot as plt
import tensorflow as tf

df = pd.read_csv('supervised_matches.csv')
df['diff_rank'] = ((df['Lower_rank'] - df['Higher_rank']) / 60)

# Feature list
features = [
    'diff_rank',
    'diff_match_win_ratio_hard',
    'diff_match_win_ratio_ao',
    'diff_match_win_ratio_last_year',
    'diff_match_win_ratio_last_year_hard',
    'diff_set_win_ratio_last_year_hard',
    'player_0_match_win_ratio_hh',
    'player_0_match_win_ratio_hh_hard',
    'player_0_set_win_ratio_hh_hard',
    'player_0_match_win_ratio_hh_ao',
    'player_0_match_win_ratio_hh_last_year',
    'player_0_set_win_ratio_hh_last_year',
    'player_0_match_win_ratio_hh_last_year_hard',
    'player_0_set_win_ratio_hh_last_year_hard'
]

X = df[features]
Y = df.result

model = Sequential()

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=1)

# 2 hidden layers with Rectified Linear Unit, Output layer with sigmoid
model.add(layers.Dense(units=14, activation='relu', input_shape=(len(X.columns),)))
model.add(layers.Dense(units=8, activation='relu')),
model.add(layers.Dense(units=1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

early_stop = EarlyStopping(monitor='val_loss', verbose=0, patience=750, mode='min')
checkpoint = ModelCheckpoint('best_model.h5', monitor='val_loss', verbose=2, mode='min', save_best_only=True)

hist = model.fit(X_train, Y_train,
          epochs=1000, verbose=0, batch_size=32,
          validation_data=(X_test, Y_test), callbacks=[early_stop, checkpoint])

best_model = load_model('best_model.h5')

_, train_acc = best_model.evaluate(X_train, Y_train, verbose=0)
_, test_acc = best_model.evaluate(X_test, Y_test, verbose=0)

print('Train Acc: %.2f Test Acc: %.2f' % (train_acc, test_acc))

df_ao2020 = pd.read_csv('ao2020.csv')
df_raw = pd.read_csv('all_matches.csv')

df_ao2020['Tournament'] = 'Australian Open'
df_ao2020['Surface'] = 'Hard'
df_ao2020['diff_rank'] = (df_ao2020['player_1_rank']) - (df_ao2020['player_0_rank']) / 60

df_ao2020 = generate_attributes(df_ao2020, df_raw)

X = df_ao2020[features]

df_ao2020['predicted_winner'] = best_model.predict_classes(X)

# predicting Australian Open Round of 16
print(df_ao2020[['player_0', 'player_1', 'predicted_winner']])


# alternative solution using logical regression
X = df[features]
Y = df.result

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

logistic_regression = LogisticRegression()
logistic_regression.fit(X_train, Y_train)
Y_pred = logistic_regression.predict(X_test)

confusion_matrix = pd.crosstab(Y_test, Y_pred, rownames=['Actual'], colnames=['Predicted'])
print(sn.heatmap(confusion_matrix, annot=True))

plt.show()
print('Accuracy: ', metrics.accuracy_score(Y_test, Y_pred))

fs = SelectKBest(score_func=mutual_info_classif, k='all')
fs.fit(X_train, Y_train)
X_train_fs = fs.transform(X_train)
X_test_fs = fs.transform(X_test)

for i in range(len(fs.scores_)):
    print('Feature %d: %f' % (i, fs.scores_[i]))

features_short = [
    'rank',
    'mh',
    'mao',
    'm1',
    'm1h',
    's1h',
    'mhh',
    'mhhh',
    'shhh',
    'mhhao',
    'mhh1',
    'shh1',
    'mhh1h',
    'shh1h'
]

# plotting the importance of the features
pyplot.bar([i for i in range(len(fs.scores_))], fs.scores_, tick_label=features_short)
pyplot.show()


