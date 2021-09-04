import pandas as pd
from model import BudgetModel

def main():
    PATH = './data/'
    try:
        X = pd.read_csv(PATH + 'features.csv', index_col=0)
        y = pd.read_csv(PATH + 'target.csv', index_col=0)
        print('All of the data has been loaded successfully!')
    except Exception as err:
        print(repr(err))
    print()

    tmp = BudgetModel(X, y)
    tmp.train()
    predicts = tmp.predict()
    #print(df_predict)
    for i, p in enumerate(predicts):
        p.to_csv(f'predict_{i+1}.csv', index=False)

if __name__ == "__main__":
    # execute only if run as a script
    main()