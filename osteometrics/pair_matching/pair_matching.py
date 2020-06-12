import scipy.stats as st
import numpy as np
import sys


class PairMatch:
    def __init__(self):
        self.ref_d_value_means = None
        self.ref_d_value_std = None

    def paired_elements_measurements_to_d_values(self, l_meas, r_meas):
        return l_meas - r_meas

    def d_values_means(self, d_values):
        return np.nanmean(d_values, axis=0)

    def d_values_std(self, d_values):
        return np.nanstd(d_values, axis=0, ddof=1)

    def d_values_to_folded_t_scores(self, d_values, means, std):
        return np.divide(np.absolute(d_values - means), std)

    def folded_t_scores_to_p_values(self, t_scores, df):
        return 2 * st.t.sf(t_scores, df)

    def unweighted_z_weights(self, number_of_tests, num_measurement_types):
        return np.ones((number_of_tests, num_measurement_types))

    def effect_size_z_weights(self, t_scores, number_of_tests, num_measurement_types, measurement_counts):
        weights = np.ones((number_of_tests, num_measurement_types)) * np.sqrt(measurement_counts)
        np.multiply(weights, t_scores, out=weights)
        np.nan_to_num(weights, copy=False)
        return weights

    def standard_error_z_weights(self, std, number_of_tests, num_measurement_types, measurement_counts):
        weights = np.ones((number_of_tests, num_measurement_types)) * np.sqrt(measurement_counts)
        np.divide(weights, std, out=weights)
        return weights

    def p_values_to_z_scores(self, p_values):
        z_scores = st.norm.ppf(np.int64(1) - p_values)
        z_scores[z_scores == -np.inf] = -sys.maxsize - 1
        z_scores[z_scores == np.inf] = sys.maxsize
        return z_scores

    def z_scores_correlation(self, z_scores):
        return np.ma.corrcoef(z_scores, rowvar=False)

    def adjusted_correlation(self, corr, measurement_counts):
        return np.multiply(corr, (1 + np.divide((1 - corr ** 2), (2 * measurement_counts))))

    def combine_z_scores_to_p_value(self, z_scores, weights, z_value_correlation_coefficients):
        np.multiply(weights, (~np.isnan(z_scores)).astype(int), out=weights)
        ss_weights = np.sum(np.square(weights), axis=1)

        numerators = np.nansum(np.multiply(z_scores, weights), axis=1)

        #run through columns rather than rows ... only as many loops as measurements

        correlation_adjustment_terms = np.zeros(weights.shape[0])
        for i in range(0, weights.shape[1]):
            for j in range(i+1, weights.shape[1]):
                correlation_adjustment_terms += np.multiply(np.multiply(weights[:, i], weights[:, j]),
                                                               z_value_correlation_coefficients[i, j])
        print(numerators)
        print(z_scores)
        print(weights)
        denominators = np.sqrt(ss_weights + 2 * correlation_adjustment_terms)
        denominators[denominators == 0] = np.nan
        numerators[numerators == 0] = np.nan

        combined_z_score = numerators/denominators
        print(numerators/denominators)

        return st.norm.sf(combined_z_score)

    def pair_match_z(self, l_ref, r_ref, l_test, l_test_ids, r_test, r_test_ids, method):

        ref_d_values = self.paired_elements_measurements_to_d_values(l_ref, r_ref)
        ref_d_value_counts = np.sum(~np.isnan(ref_d_values), axis=0)
        self.ref_d_value_means = self.d_values_means(ref_d_values)
        self.ref_d_value_std = self.d_values_std(ref_d_values)
        ref_t_scores = self.d_values_to_folded_t_scores(ref_d_values, self.ref_d_value_means, self.ref_d_value_std)
        ref_p_values = self.folded_t_scores_to_p_values(ref_t_scores, ref_d_value_counts-1)
        ref_z_scores = self.p_values_to_z_scores(ref_p_values)

        ref_z_corr = self.z_scores_correlation(ref_z_scores)

        test_d_values = (l_test[:, np.newaxis] - r_test).reshape(-1, l_test.shape[1])
        number_of_measurements = (~np.isnan(test_d_values)).sum(1)

        test_t_scores = self.d_values_to_folded_t_scores(test_d_values, self.ref_d_value_means, self.ref_d_value_std)
        test_p_values = self.folded_t_scores_to_p_values(test_t_scores, ref_d_value_counts-1) #Minus one?
        test_z_scores = self.p_values_to_z_scores(test_p_values)

        num_measurement_types = ref_d_values.shape[1]
        number_of_tests = test_p_values.shape[0]

        test_ids = np.column_stack((np.repeat(l_test_ids, r_test_ids.shape[0]),
                                     np.tile(r_test_ids, l_test_ids.shape[0])))

        weights = 0

        if method == "uweightedZ":
            weights = self.unweighted_z_weights(number_of_tests, num_measurement_types)

        if method == "standardErrorZ":
            weights = self.standard_error_z_weights(self.ref_d_value_std, number_of_tests,
                                                    num_measurement_types, ref_d_value_counts)

        if method == "effectSizeZ":
            weights = self.effect_size_z_weights(test_t_scores, number_of_tests,
                                                 num_measurement_types, ref_d_value_counts)

        combined_p_values = self.combine_z_scores_to_p_value(test_z_scores, weights, ref_z_corr)

        combined_p_values = combined_p_values.round(5)

        combined_p_values = np.column_stack((test_ids, combined_p_values, number_of_measurements,
                                             ~np.isnan(test_d_values)))

        return combined_p_values
