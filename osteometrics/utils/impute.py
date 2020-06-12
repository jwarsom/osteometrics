from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import ExtraTreesRegressor


def impute_data(x):
    imp = IterativeImputer(random_state=0,
                           estimator=ExtraTreesRegressor(n_estimators=10, random_state=0), initial_strategy="median")

    return imp.fit_transform(x)




