from osteometrics.utils.util import *
from sklearn.model_selection import LeaveOneOut
from osteometrics.pair_matching.pair_matching import PairMatch
from osteometrics.pair_association.pair_association import PairAssociation
from itertools import combinations
import pandas as pd
import numpy as np
import argparse
import csv
import sys


def main(args=None):
    parser = argparse.ArgumentParser(description='Osteometric Sorting')

    parser.add_argument("--input", type=str, help="The input file containing skeletal elements to be analyzed",
                        action="store")

    parser.add_argument("--reference", type=str, help="The reference data", required=True, action="store")

    parser.add_argument("--p_method", type=str,
                        choices=['uweightedZ', 'effectSizeZ', 'standardErrorZ', 'sumTTest', 'absTTest', 'sumTTest_wMean'],
                        help="Methods for osteometric sorting pair matching", action="store")

    parser.add_argument("--a_method", type=str,
                        choices=['sumLRegression'],
                        help="Method for  osteometric sorting association matching", action="store")

    parser.add_argument("--alpha_p_method", type=float, help="Minimum p-value for pair-matching: default 0.1",
                        default=.1, action="store")

    parser.add_argument("--alpha_a_method", type=float, help="Minimum p-value for association matching: default 0.1",
                        default=.1, action="store")

    parser.add_argument("--loocv", help="Perform leave-one-out cross validation of the reference data",
                        action="store_true")

    parser.add_argument("--basename", type=str,
                        help="Base name for output files", action="store", required=True)

    parser.add_argument("--time", help="Output runtime of the program", action="store_true")

    args = parser.parse_args(args=args)
    sniffer = csv.Sniffer()

    if args.input:
        try:
            with open(args.input, 'r') as infile:
                dialect = sniffer.sniff(infile.readline())
                if dialect.delimiter != ',' and dialect.delimiter != '\t':
                    print("Program accepts comma-delimited or tab-delimited files", file=sys.stderr)
                    sys.exit(1)
                test_df = pd.read_csv(args.input, sep=dialect.delimiter, dtype={'Id': object})
                test_elements = parse_osteometric_data(test_df)
        except IOError:
            print("Error Opening Input File", file=sys.stderr)
            sys.exit(1)

    try:
        with open(args.reference, 'r') as infile:
            dialect = sniffer.sniff(
                infile.readline())
            if dialect.delimiter != ',' and dialect.delimiter != '\t':
                print("Program accepts comma-delimited or tab-delimited files", file=sys.stderr)
                sys.exit(1)
            ref_df = pd.read_csv(args.reference, sep=dialect.delimiter, dtype={'Id': object})
            reference_elements = parse_osteometric_data(ref_df)
    except IOError:
        print("Error Opening Input File", file=sys.stderr)
        sys.exit(1)

    pm = PairMatch()

    if args.p_method in ['uweightedZ', 'effectSizeZ', 'standardErrorZ'] and args.loocv:
        loo_l = LeaveOneOut()
        loo_r = LeaveOneOut()
        filename = args.basename + "_" + args.p_method + "_" + "loocv" + ".tsv"

        info = ref_df.loc[:, 'Id':'Element']
        if 'Element' in info.columns:
            del info['Element']

        if 'Side' in info.columns:
            del info['Side']

        with open(filename, "a+", newline='') as f:
            for element, (left, right) in reference_elements.items():
                result_list = []

                measurement_keys = get_measurement_keys(element)
                left.dropna(subset=measurement_keys, inplace=True)
                right.dropna(subset=measurement_keys, inplace=True)

                idx1 = pd.Index(left['Id'])
                idx2 = pd.Index(right['Id'])
                idx = idx1.intersection(idx2)

                left = left.loc[left['Id'].isin(idx)]
                right = right.loc[right['Id'].isin(idx)]

                left['Id'] = left['Id'] + "_" + element + "_left"
                right['Id'] = right['Id'] + "_" + element + "_right"

                if left.shape[0] >= 30 and right.shape[0] >= 30:
                    for train_indexL, test_indexL in loo_l.split(left.to_numpy()):
                        for train_indexR, test_indexR in loo_r.split(right.to_numpy()):
                            train_index = np.intersect1d(train_indexL, train_indexR)
                            iteration_result = pm.pair_match_z(left.iloc[train_index][measurement_keys].to_numpy(),
                                                               right.iloc[train_index][measurement_keys].to_numpy(),
                                                               left.iloc[test_indexL][measurement_keys].to_numpy(),
                                                               left.iloc[test_indexL]['Id'].to_numpy(),
                                                               right.iloc[test_indexR][measurement_keys].to_numpy(),
                                                               right.iloc[test_indexR]['Id'].to_numpy(),
                                                               args.p_method)
                            result_list.append(iteration_result)
                else:
                    print("Less than 30 elements in the reference set. Skipping:", element)

                if result_list:
                    results = pd.DataFrame(data=np.vstack(np.concatenate(result_list)),
                                           columns=['Id1', 'Id2', 'Pvalue'])

                    if info.shape[1] > 1:
                        results = np.split(results.to_numpy(), 2, axis=1)

                        results[0] = results[0].merge(info, left_on='Id1', right_on='Id', how='left')
                        del results[0]['Id']
                        results[0] = results[0].merge(info, left_on='Id2',
                                                      right_on='Id', how='left', suffixes=('_left', '_right'))
                        del results[0]['Id']

                        results = pd.concat(results, axis=1)

                    results = results.astype({'Id1': 'str', 'Id2': 'str', 'Pvalue': 'float'})
                    results['Element'] = element
                    results['Method'] = args.p_method
                    results['Excluded'] = 'Yes'
                    results.loc[results['Pvalue'] >= args.alpha_p_method, 'Excluded'] = 'No'

                    results.merge()
                    results.to_csv(f, sep='\t', index=False)

    if args.p_method in ['uweightedZ', 'effectSizeZ', 'standardErrorZ'] and args.input:
        filename = args.basename + "_" + args.p_method + ".tsv"
        with open(filename, "a+", newline='') as f:
            for element, (ref_left, ref_right) in reference_elements.items():
                measurement_keys = get_measurement_keys(element)
                ref_left.dropna(subset=measurement_keys, inplace=True)
                ref_right.dropna(subset=measurement_keys, inplace=True)

                idx1 = pd.Index(ref_left['Id'])
                idx2 = pd.Index(ref_right['Id'])
                idx = idx1.intersection(idx2)

                info = test_df.loc[:, 'Id':'Element']
                if 'Element' in info.columns:
                    del info['Element']

                if 'Side' in info.columns:
                    del info['Side']

                ref_left = ref_left.loc[ref_left['Id'].isin(idx)]
                ref_right = ref_right.loc[ref_right['Id'].isin(idx)]

                if ref_left.shape[0] >= 30 and ref_right.shape[0] >= 30:
                    (test_left, test_right) = test_elements.get(element)
                    if test_left.shape[0] > 0 and test_right.shape[0] > 0:
                        iteration_result = pm.pair_match_z(ref_left[measurement_keys].to_numpy(),
                                                           ref_right[measurement_keys].to_numpy(),
                                                           test_left[measurement_keys].to_numpy(),
                                                           test_left['Id'].to_numpy(),
                                                           test_right[measurement_keys].to_numpy(),
                                                           test_right['Id'].to_numpy(),
                                                           args.p_method)

                        columns = ['Id1', 'Id2', 'Pvalue', 'Number of Measurements']
                        columns.extend(measurement_keys)
                        results = pd.DataFrame(data=iteration_result, columns=columns)
                        results = results.astype({'Id1': 'str', 'Id2': 'str', 'Pvalue': 'float'})
                        results.insert(2, 'Element', element)

                        results.insert(3, 'Method', args.p_method)
                        results.insert(5, 'Excluded', 'Yes')
                        results.loc[(results['Pvalue'] >= args.alpha_p_method) | (pd.isnull(results['Pvalue'])),
                                    'Excluded'] = 'No'

                        if info.shape[1] > 1:
                            results = np.split(results, [2], axis=1)

                            results[0] = results[0].merge(info, left_on='Id1', right_on='Id', how='left')
                            del results[0]['Id']
                            results[0] = results[0].merge(info, left_on='Id2',
                                                          right_on='Id', how='left', suffixes=('_left', '_right'))
                            del results[0]['Id']

                            results = pd.concat(results, axis=1)

                        measurements_used = results[measurement_keys].to_dict(orient='records')
                        measurement_means = dict(zip(measurement_keys, pm.ref_d_value_means.round(5)))
                        measurement_stds = dict(zip(measurement_keys, pm.ref_d_value_std.round(5)))

                        results.drop(measurement_keys, axis=1, inplace=True)
                        results['Measurements Used'] = np.asarray([str(measurements) for
                                                                   measurements in measurements_used])
                        results['Measurement Means'] = str(measurement_means)
                        results['Measurement Standard Deviations'] = str(measurement_stds)

                        results.to_csv(f, sep='\t', index=False)
                    else:
                        print("Left and/or Right test sets have zero records. Skipping:", element)
                else:
                    print("Left and Right reference sets are not the same length"
                          " or less than 30 elements in the reference set. Skipping:", element)

    if args.a_method and args.loocv:
        loo_x = LeaveOneOut()
        loo_y = LeaveOneOut()
        filename = args.basename + "_" + args.a_method + "_" + "loocv" + ".tsv"
        for element, (left, right) in reference_elements.items():
            left.loc[:, 'Id'] = left['Id'] + "_left"
            right.loc[:, 'Id'] = right['Id'] + "_right"

        with open(filename, "a+", newline='') as f:
            for key1, key2 in combinations(reference_elements.keys(), r=2):
                left_x = reference_elements[key1][0]
                right_x = reference_elements[key1][1]
                left_y = reference_elements[key2][0]
                right_y = reference_elements[key2][1]

                x = pd.concat([left_x, right_x])
                y = pd.concat([left_y, right_y])

                measurement_keys1 = get_measurement_keys(key1)
                measurement_keys2 = get_measurement_keys(key2)

                x.dropna(subset=measurement_keys1, inplace=True)
                y.dropna(subset=measurement_keys2, inplace=True)

                idx1 = pd.Index(x['Id'])
                idx2 = pd.Index(y['Id'])
                idx = idx1.intersection(idx2)

                x = x.loc[x['Id'].isin(idx)]
                y = y.loc[y['Id'].isin(idx)]

                x.sort_values(by=['Id'], inplace=True)
                y.sort_values(by=['Id'], inplace=True)

                result_list = []
                if x.shape[0] >= 30 and x.shape[0] >= 30 and key1 != key2:
                    for train_index_x, test_index_x in loo_x.split(x.to_numpy()):
                        for train_index_y, test_index_y in loo_y.split(y.to_numpy()):
                            train_index = np.intersect1d(train_index_x, train_index_y)
                            ar = PairAssociation()
                            ar.build_osl_regression(x.iloc[train_index][measurement_keys1].to_numpy(),
                                                    y.iloc[train_index][measurement_keys2].to_numpy())

                            iteration_result = ar.classify_new_associations\
                                (x.iloc[test_index_x][measurement_keys1],
                                 x.iloc[train_index][measurement_keys1],
                                 y.iloc[test_index_y][measurement_keys2],
                                 y.iloc[train_index][measurement_keys2],
                                 x.iloc[test_index_x]['Id'], y.iloc[test_index_y]['Id'], args.alpha_a_method)

                            result_list.append(iteration_result)
                else:
                    print("Less than 30 elements in the reference set. Skipping:", key1, key2)

                if result_list:
                    results = pd.DataFrame(data=np.vstack(np.concatenate(result_list)),
                                           columns=['Id1', 'Id2', 'Excluded'])
                    results = results.astype({'Id1': 'str', 'Id2': 'str', 'Excluded': 'bool'})
                    results.replace({'Excluded': {True: "Yes", False: "No"}})
                    results['Element1'] = key1
                    results['Element2'] = key2
                    results['Method'] = args.a_method
                    results['Alpha'] = args.alpha_a_method
                    results.to_csv(f, sep='\t', index=False)

    if args.a_method and args.input:
            filename = args.basename + "_" + args.a_method + ".tsv"
            for element, (left, right) in reference_elements.items():
                left.loc[:, 'Id'] = left['Id'] + "_left"
                right.loc[:, 'Id'] = right['Id'] + "_right"

            with open(filename, "a+", newline='') as f:
                for key1, key2 in combinations(reference_elements.keys(), r=2):
                    left_x = reference_elements[key1][0]
                    right_x = reference_elements[key1][1]
                    left_y = reference_elements[key2][0]
                    right_y = reference_elements[key2][1]

                    x = pd.concat([left_x, right_x])
                    y = pd.concat([left_y, right_y])

                    measurement_keys1 = get_measurement_keys(key1)
                    measurement_keys2 = get_measurement_keys(key2)

                    x.dropna(subset=measurement_keys1, inplace=True)
                    y.dropna(subset=measurement_keys2, inplace=True)

                    idx1 = pd.Index(x['Id'])
                    idx2 = pd.Index(y['Id'])
                    idx = idx1.intersection(idx2)

                    x = x.loc[x['Id'].isin(idx)]
                    y = y.loc[y['Id'].isin(idx)]

                    x.sort_values(by=['Id'], inplace=True)
                    y.sort_values(by=['Id'], inplace=True)

                    ar = PairAssociation()

                    if x.shape[0] >= 30 and y.shape[0] >= 30:
                        ar.build_osl_regression(x[measurement_keys1].to_numpy(),
                                                y[measurement_keys2].to_numpy())
                        print("Analyzing:", key1, key2)
                        (test_left_x, test_right_x) = test_elements.get(key1)
                        (test_left_y, test_right_y) = test_elements.get(key2)
                        test_x = pd.concat([test_left_x, test_right_x])
                        test_y = pd.concat([test_left_y, test_right_y])
                        if test_left_x.shape[0] > 0 and test_right_y.shape[0] > 0:
                            measurement_keys1 = get_measurement_keys(key1)
                            measurement_keys2 = get_measurement_keys(key2)

                            iteration_result = ar.classify_new_associations\
                                (test_x[measurement_keys1],
                                x[measurement_keys1],
                                test_y[measurement_keys2],
                                y[measurement_keys2],
                                test_x['Id'], test_y['Id'], args.alpha_a_method)

                            results = pd.DataFrame(data=iteration_result,
                                                columns=['Id1', 'Id2', 'Excluded'])

                            results = results.astype({'Id1': 'str', 'Id2': 'str', 'Excluded': 'bool'})
                            results.replace({'Excluded': {True: "Yes", False: "No"}})
                            results['Element1'] = key1
                            results['Element2'] = key2
                            results['Method'] = args.a_method
                            results['Alpha'] = args.alpha_a_method
                            results.to_csv(f, sep='\t', index=False)
                        else:
                            print("Left and/or Right test sets have zero records. Skipping:", key1, key2)
                    else:
                        print("Left and Right reference sets are not the same length" 
                              " or less than 30 elements in the reference set. Skipping:", key1, key2)


if __name__ == "__main__":
    main()
