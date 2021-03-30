import statsmodels.api as sm
from statsmodels.sandbox.regression.predstd import wls_prediction_std
import numpy as np
from utils.impute import impute_data


class PairAssociation:
    def __init__(self):
        self.model = None
        self.results = None

    def get_meas_sums(self, meas):
        return np.sum(meas, axis=1)

    def summed_meas_log(self, meas):
        return np.log(meas)

    def build_osl_regression(self, x_meas, y_meas):
        x_sums = self.get_meas_sums(x_meas)
        x_sum_logs = self.summed_meas_log(x_sums)

        x_sum_logs = sm.add_constant(x_sum_logs.reshape(-1, 1), prepend=False)

        y_sums = self.get_meas_sums(y_meas)
        y_sum_logs = self.summed_meas_log(y_sums)

        self.model = sm.OLS(y_sum_logs, x_sum_logs)
        self.results = self.model.fit()

    def classify_new_associations(self, x_meas, x_train, y_meas, y_train,  x_ids, y_ids, alpha=0.05):
        try:
            x_meas_imputed = np.concatenate([x_meas, x_train])
            x_meas_imputed = np.split(impute_data(x_meas_imputed), [len(x_meas)])[0]

            y_meas_imputed = np.concatenate([y_meas, y_train])
            y_meas_imputed = np.split(impute_data(y_meas_imputed), [len(y_meas)])[0]


            x_sums = self.get_meas_sums(x_meas_imputed)
            x_sum_logs = self.summed_meas_log(x_sums)

            y_sums = self.get_meas_sums(y_meas_imputed)
            y_sum_logs = self.summed_meas_log(y_sums)

            x_sum_logs = sm.add_constant(x_sum_logs.reshape(-1, 1), prepend=False)
            if len(x_sum_logs) == 1:
                x_sum_logs = [np.append(x_sum_logs[0], 1)]

            y_meas_log_all_pairs = np.tile(y_sum_logs, x_sum_logs.shape[0])
            x_meas_log_all_pairs = np.repeat(x_sum_logs, y_sum_logs.shape[0], axis=0)
            prstd0, iv_l0, iv_u0 = wls_prediction_std(self.results, x_meas_log_all_pairs, None, alpha)

        except NameError:
            print("Models not initialized correctly")
            return

        test_ids = np.column_stack((np.repeat(x_ids, y_ids.shape[0]),
                                   np.tile(y_ids, x_ids.shape[0])))

        results = ~((y_meas_log_all_pairs <= iv_u0) & (y_meas_log_all_pairs >= iv_l0))

        results = np.column_stack((test_ids, results))

        return results



