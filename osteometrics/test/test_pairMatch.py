from unittest import TestCase
from osteometrics.pair_matching.pair_matching import PairMatch
import numpy as np
import scipy.stats as st


class TestPairMatch(TestCase):
    def setUp(self):
        self.pm = PairMatch()
        self.l_meas = \
            np.array([
                [489, 483, 92, 49, 30, 28, 30],
                [466, 463, 89, 51, 34, 30, 33],
                [445, 441, 82, 49, 33, 30, 31],
                [427, 425, 76, 41, 29, 26, 31]
            ])
        self.r_meas = \
            np.array([
                [487, 480, 91, 49, 30, 28, 31],
                [466, 462, 88, 50, 36, 30, 33],
                [450, 447, 83, 48, 33, 31, 31],
                [431, 426, 76, 42, 30, 26, 30],
                [451, 448, 81, 47, 35, 30, 30]
            ])
        self.l_meas_ref = \
            np.array([
                [489, 484, 82, 49, 35, 28, 30],
                [423, 419, 83, 46, 25, 30, 27],
                [425, 420, 81, 46, 35, 30, 35],
                [474, 471, 87, 50, 33, 29, 30],
                [477, 472, 89, 51, 33, 30, 32],
                [458, 457, 78, 46, 32, 28, 28],
                [415, 412, 72, 41, 30, 22, 25],
                [444, 441, 79, 47, 35, 29, 31]
            ])
        self.r_meas_ref = \
            np.array([
                [486, 481, 81, 49, 35, 27, 30],
                [423, 419, 82, 45, 24, 30, 27],
                [420, 416, 80, 47, 35, 30, 35],
                [470, 468, 88, 51, 34, 28, 29],
                [476, 472, 89, 52, 30, 30, 31],
                [465, 463, 79, 46, 30, 25, 26],
                [412, 410, 73, 40, 30, 23, 25],
                [440, 437, 78, 47, 32, 30, 32]
            ])
        self.l_ids_ref = np.array(['idl1', 'idl2','idl3', 'idl4', 'idl5', 'idl6','idl7', 'idl8'])
        self.r_ids_ref = np.array(['idr1', 'idr2', 'idr3', 'idr4', 'idr5', 'idr6', 'idr7', 'idr8'])
        self.l_ids_test = np.array(['idl1', 'idl2', 'idl3', 'idl4'])
        self.r_ids_test = np.array(['idr1', 'idr2', 'idr3', 'idr4', 'idr5'])
        self.paired_d_values = \
            np.array([
                [2, 3, 1, 0, 0, 0, -1],
                [0, 1, 1, 1, -2, 0, 0],
                [-5, -6, -1, 1, 0, -1, 0],
                [-4, -1, 0, -1, -1, 0, 1]
            ])

        self.paired_t_scores = \
            np.array([[1.31055608, 1.12115264, 0.90453403, 0.30151134, 0.90453403, 0.57735027, 1.41421356],
                      [0.61159284, 0.52320456, 0.90453403, 0.90453403, 1.50755672, 0.57735027, 0],
                      [1.13581527, 1.56961369, 1.50755672, 0.90453403, 0.90453403, 1.73205082, 0],
                      [0.78633365, 0.07474351, 0.30151134, 1.50755672, 0.30151134, 0.57735027, 1.41421356]])

        self.paired_p_values = np.array([[0.28131099, 0.34387433, 0.432389, 0.78271638, 0.432389, 0.6041813, 0.2522155],
                                         [0.58403575, 0.63701813, 0.432389, 0.432389, 0.2287778, 0.6041813, 1],
                                         [0.3385625, 0.21452287, 0.2287778, 0.432389, 0.432389, 0.18169011, 1],
                                         [0.489064, 0.94512375, 0.78271638, 0.2287778, 0.78271638, 0.6041813,
                                          0.2522155]])

        self.paired_z_scores = np.array(
            [[0.57895138, 0.40191218, 0.17029518, -0.78140005, 0.17029518, -0.26418496, 0.66753416],
             [-0.21222885, -0.35049967, 0.17029518, 0.17029518, 0.74287791, -0.26418496, 10],
             [0.41638951, 0.79082565, 0.74287791, 0.17029518, 0.17029518, 0.90894299, 10],
             [0.02741592, -1.59930657, -0.78140005, 0.74287791, -0.78140005, -0.26418496, 0.66753416]])

    def test_paired_elements_measurements_to_d_values(self):
        result = self.pm.paired_elements_measurements_to_d_values(self.l_meas, self.r_meas[0:4, :])
        assert (np.array_equal(result, self.paired_d_values))

    def test_d_values_means(self):
        result = self.pm.d_values_means(self.paired_d_values)
        assert (np.array_equal(result, np.mean(self.paired_d_values, axis=0)))

    def test_d_values_std(self):
        result = self.pm.d_values_std(self.paired_d_values)
        assert (np.array_equal(result, np.std(self.paired_d_values, axis=0)))

    def test_d_values_to_folded_t_scores(self):
        means = [-1.75, -0.75, 0.25, 0.25, -0.75, -0.25, 0]
        std = [2.86138079, 3.34477204, 0.8291562, 0.8291562, 0.8291562, 0.4330127, 0.70710678]
        result = self.pm.d_values_to_folded_t_scores(self.paired_d_values, means, std)
        print(result)
        assert (np.array_equal(result, np.divide(np.absolute(self.paired_d_values - means), std)))

    def test_folded_t_scores_to_p_values(self):
        df = np.array([4, 4, 4, 4, 4, 4, 4])
        result = self.pm.folded_t_scores_to_p_values(self.paired_t_scores, df)
        assert (np.array_equal(result, 2 * st.t.sf(self.paired_t_scores, df - 1)))

    def test_unweighted_z_weights(self):
        result = self.pm.unweighted_z_weights(4, 7)
        assert (np.array_equal(result, np.ones((4, 7))))

    def test_effect_size_z_weights(self):
        std = [2.86138079, 3.34477204, 0.8291562, 0.8291562, 0.8291562, 0.4330127, 0.70710678]
        measurement_counts = np.array([4, 4, 4, 4, 4, 4, 4])
        result = self.pm.effect_size_z_weights(self.paired_t_scores, std, 4, 7, measurement_counts)

        weights = np.zeros((4, 7)) + np.sqrt(measurement_counts)
        np.divide(weights, std, out=weights)
        np.multiply(weights, self.paired_t_scores, out=weights)

        assert (np.array_equal(result, weights))

    def test_standard_error_z_weights(self):
        std = [2.86138079, 3.34477204, 0.8291562, 0.8291562, 0.8291562, 0.4330127, 0.70710678]
        measurement_counts = np.array([4, 4, 4, 4, 4, 4, 4])
        result = self.pm.standard_error_z_weights(std, 4, 7, measurement_counts)

    def test_p_values_to_z_values(self):
        result = self.pm.p_values_to_z_values(self.paired_p_values)

    def test_z_scores_correlation(self):
        result = self.pm.z_scores_correlation(self.paired_z_scores)
        assert (np.array_equal(result[~np.isnan(result)], np.corrcoef(self.paired_z_scores, rowvar=False)
        [~np.isnan(np.corrcoef(self.paired_z_scores, rowvar=False))]))

    def test_adjusted_correlation(self):
        measurement_counts = np.array([4, 4, 4, 4, 4, 4, 4])
        result = self.pm.adjusted_correlation(np.corrcoef(self.paired_z_scores, rowvar=False), measurement_counts)

    def test_combine_p_values(self):
        weights = self.pm.unweighted_z_weights(4, 7)
        result = self.pm.combine_p_values(self.paired_p_values, weights,
                                          np.corrcoef(self.paired_z_scores, rowvar=False))

    def test_pair_match_z_unweighted(self):
        result = self.pm.pair_match_z(self.l_meas_ref, self.r_meas_ref, self.l_meas,
                             self.l_ids_test, self.r_meas, self.r_ids_test, "uweightedZ")

        print(result)

