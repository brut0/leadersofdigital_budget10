import numpy as np
import pandas as pd
from model import BudgetModel


def main():
    PATH = '../data/'
    try:
        X = pd.read_csv(PATH + 'features.csv', index_col=0)
        y = pd.read_csv(PATH + 'target.csv', index_col=0)
        inflation = pd.read_csv(PATH+'inflation.csv', index_col=0)
        print('All of the data has been loaded successfully!')
    except Exception as err:
        print(repr(err))

    y.loc[y.iloc[-1].name + 1, :] = np.nan
    y.loc[y.iloc[-1].name + 1, :] = np.nan
    X = pd.concat([X, inflation['Прогноз (%)']], axis=1)

    tmp = BudgetModel(X, y, 3)
    predicts = tmp.predict()
    #print(df_predict)
    output = pd.DataFrame({'Год': y.index[-3:],
                           f'{y.columns[0]}': predicts[0],
                           f'{y.columns[1]}': predicts[1]})
    print(output)
    output.to_csv('prediction.csv', index=False, encoding='utf-8-sig')


if __name__ == "__main__":
    # execute only if run as a script
    main()