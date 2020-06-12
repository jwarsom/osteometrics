import pandas as pd
import sys


def parse_osteometric_data(df):

    try:
        clavicle_df = df.loc[df['Element'] == 'Clavicle'][['Id', 'Side', 'Element',
                                                                 'Cla_01', 'Cla_04', 'Cla_05']]

        clavicle_l = clavicle_df.loc[clavicle_df['Side'] == 'Left']
        clavicle_r = clavicle_df.loc[clavicle_df['Side'] == 'Right']
    except KeyError:
        try:
            clavicle_l = df[['Id', 'Cla_01', 'Cla_04', 'Cla_05']]
            clavicle_r = df[['Id', 'Cla_01R', 'Cla_04R', 'Cla_05R']]
            clavicle_r.rename(columns={'Cla_01R': 'Cla_01', 'Cla_04R': 'Cla_04', 'Cla_05R': 'Cla_05'}, inplace=True)

            clavicle_l.loc[:, 'Side'] = 'Left'
            clavicle_l.loc[:, 'Element'] = 'Clavicle'

            clavicle_r.loc[:, 'Side'] = 'Right'
            clavicle_r.loc[:, 'Element'] = 'Clavicle'

        except KeyError:
                clavicle_df = pd.DataFrame(columns={'Id', 'Side', 'Element', 'Cla_01', 'Cla_04', 'Cla_05'})
                clavicle_l = clavicle_df.loc[clavicle_df['Side'] == 'Left']
                clavicle_r = clavicle_df.loc[clavicle_df['Side'] == 'Right']

    clavicle_l = clavicle_l.dropna(subset=['Cla_01', 'Cla_04', 'Cla_05'], thresh=1)
    clavicle_r = clavicle_r.dropna(subset=['Cla_01', 'Cla_04', 'Cla_05'], thresh=1)

    try:
        femur_df = df.loc[df['Element'] == 'Femur'][['Id', 'Side', 'Element',
                                                           'Fem_01', 'Fem_02', 'Fem_03', 'Fem_04',
                                                           'Fem_05', 'Fem_06', 'Fem_07']]

        femur_l = femur_df.loc[femur_df['Side'] == 'Left']
        femur_r = femur_df.loc[femur_df['Side'] == 'Right']
    except KeyError:
        try:
            femur_l = df[['Id', 'Fem_01', 'Fem_02', 'Fem_03', 'Fem_04', 'Fem_05', 'Fem_06', 'Fem_07']]
            femur_r = df[['Id', 'Fem_01R', 'Fem_02R', 'Fem_03R', 'Fem_04R', 'Fem_05R', 'Fem_06R', 'Fem_07R']]

            femur_r.rename(columns={'Fem_01R': 'Fem_01', 'Fem_02R': 'Fem_02', 'Fem_03R': 'Fem_03',
                                    'Fem_04R': 'Fem_04', 'Fem_05R': 'Fem_05', 'Fem_06R': 'Fem_06',
                                    'Fem_07R': 'Fem_07'
                                    }, inplace=True)

            femur_l.loc[:, 'Side'] = 'Left'
            femur_l.loc[:, 'Element'] = 'Femur'

            femur_r.loc[:, 'Side'] = 'Right'
            femur_r.loc[:, 'Element'] = 'Femur'

        except KeyError:
            femur_df = pd.DataFrame(columns={'Id', 'Side', 'Element', 'Fem_01', 'Fem_02', 'Fem_03', 'Fem_04',
                                             'Fem_05', 'Fem_06', 'Fem_07'})

            femur_l = femur_df.loc[femur_df['Side'] == 'Left']
            femur_r = femur_df.loc[femur_df['Side'] == 'Right']

    femur_l = femur_l.dropna(subset=['Fem_01', 'Fem_02', 'Fem_03', 'Fem_04', 'Fem_05', 'Fem_06', 'Fem_07'],
                   thresh=1)
    femur_r = femur_r.dropna(subset=['Fem_01', 'Fem_02', 'Fem_03', 'Fem_04', 'Fem_05', 'Fem_06', 'Fem_07'],
                   thresh=1)

    try:
        fibula_df = df.loc[df['Element'] == 'Fibula'][['Id', 'Side', 'Element', 'Fib_01', 'Fib_02']]
        fibula_l = fibula_df.loc[fibula_df['Side'] == 'Left']
        fibula_r = fibula_df.loc[fibula_df['Side'] == 'Right']

    except KeyError:
        try:
            fibula_l = df[['Id', 'Fib_01', 'Fib_02']]
            fibula_r = df[['Id', 'Fib_01R', 'Fib_02R']]

            fibula_r.rename(columns={'Fib_01R': 'Fib_01', 'Fib_02R': 'Fib_02'}, inplace=True)

            fibula_l.loc[:, 'Side'] = 'Left'
            fibula_l.loc[:, 'Element'] = 'Fibula'

            fibula_r.loc[:, 'Side'] = 'Right'
            fibula_r.loc[:, 'Element'] = 'Fibula'
        except:
            fibula_df = pd.DataFrame(columns={'Id', 'Side', 'Element', 'Fib_01', 'Fib_02'})

            fibula_l = fibula_df.loc[fibula_df['Side'] == 'Left']
            fibula_r = fibula_df.loc[fibula_df['Side'] == 'Right']

    fibula_l = fibula_l.dropna(subset=['Fib_01', 'Fib_02'])
    fibula_r = fibula_r.dropna(subset=['Fib_01', 'Fib_02'])

    try:
        humerus_df = df.loc[df['Element'] == 'Humerus'][['Id', 'Side', 'Element',
                                                               'Hum_01', 'Hum_02', 'Hum_03', 'Hum_04',
                                                               'Hum_05']]

        humerus_l = humerus_df.loc[humerus_df['Side'] == 'Left']
        humerus_r = humerus_df.loc[humerus_df['Side'] == 'Right']

    except KeyError:
        try:
            humerus_l = df[['Id', 'Hum_01', 'Hum_02', 'Hum_03', 'Hum_04',
                            'Hum_05']]
            humerus_r = df[['Id', 'Hum_01R', 'Hum_02R', 'Hum_03R', 'Hum_04R',
                            'Hum_05R']]

            humerus_r.rename(columns={'Hum_01R': 'Hum_01', 'Hum_02R': 'Hum_02',
                                      'Hum_03R': 'Hum_03', 'Hum_04R': 'Hum_04',
                                      'Hum_05R': 'Hum_05'}, inplace=True)

            humerus_l.loc[:, 'Side'] = 'Left'
            humerus_l.loc[:, 'Element'] = 'Humerus'

            humerus_r.loc[:, 'Side'] = 'Right'
            humerus_r.loc[:, 'Element'] = 'Humerus'
        except KeyError:
            humerus_df = pd.DataFrame(columns={'Id', 'Side', 'Element', 'Hum_01', 'Hum_02', 'Hum_03', 'Hum_04',
                                           'Hum_05'})

            humerus_l = humerus_df.loc[humerus_df['Side'] == 'Left']
            humerus_r = humerus_df.loc[humerus_df['Side'] == 'Right']

    humerus_l = humerus_l.dropna(subset=['Hum_01', 'Hum_02', 'Hum_03', 'Hum_04','Hum_05'], thresh=1)
    humerus_r = humerus_r.dropna(subset=['Hum_01', 'Hum_02', 'Hum_03', 'Hum_04', 'Hum_05'], thresh=1)

    try:
        os_coxa_df = df.loc[df['Element'] == 'Os coxa'][['Id', 'Side', 'Element',
                                                               'Osc_01', 'Osc_02']]

        os_coxa_l = os_coxa_df.loc[os_coxa_df['Side'] == 'Left']
        os_coxa_r = os_coxa_df.loc[os_coxa_df['Side'] == 'Right']

    except KeyError:
        try:
            os_coxa_l = df[['Id', 'Osc_01', 'Osc_02']]
            os_coxa_r = df[['Id', 'Osc_01R', 'Osc_02R']]

            os_coxa_r.rename(columns={'Osc_01R': 'Osc_01', 'Osc_02R': 'Osc_02'}, inplace=True)

            os_coxa_l.loc[:, 'Side'] = 'Left'
            os_coxa_l.loc[:, 'Element'] = 'Os coxa'

            os_coxa_r.loc[:, 'Side'] = 'Right'
            os_coxa_r.loc[:, 'Element'] = 'Os coxa'
        except KeyError:
            os_coxa_df = pd.DataFrame(columns={'Id', 'Side', 'Element', 'Osc_01', 'Osc_02'})

            os_coxa_l = os_coxa_df.loc[os_coxa_df['Side'] == 'Left']
            os_coxa_r = os_coxa_df.loc[os_coxa_df['Side'] == 'Right']

    os_coxa_l = os_coxa_l.dropna(subset=['Osc_01', 'Osc_02'], thresh=1)
    os_coxa_r = os_coxa_r.dropna(subset=['Osc_01', 'Osc_02'], thresh=1)

    try:
        radius_df = df.loc[df['Element'] == 'Radius'][['Id', 'Side', 'Element',
                                                       'Rad_01', 'Rad_05', 'Rad_06']]

        radius_l = radius_df.loc[radius_df['Side'] == 'Left']
        radius_r = radius_df.loc[radius_df['Side'] == 'Right']

    except KeyError:
        try:
            radius_l = df[['Id', 'Rad_01', 'Rad_05', 'Rad_06']]
            radius_r = df[['Id', 'Rad_01R', 'Rad_05R', 'Rad_06R']]

            radius_r.rename(columns={'Rad_01R': 'Rad_01', 'Rad_05R': 'Rad_05', 'Rad_06R': 'Rad_06'}, inplace=True)

            radius_l.loc[:, 'Side'] = 'Left'
            radius_l.loc[:, 'Element'] = 'Radius'

            radius_r.loc[:, 'Side'] = 'Right'
            radius_r.loc[:, 'Element'] = 'Radius'
        except KeyError:
            radius_df = pd.DataFrame(columns={'Id', 'Side', 'Element', 'Rad_01', 'Rad_05', 'Rad_06'})

            radius_l = radius_df.loc[radius_df['Side'] == 'Left']
            radius_r = radius_df.loc[radius_df['Side'] == 'Right']

    radius_l = radius_l.dropna(subset=['Rad_01', 'Rad_05', 'Rad_06'], thresh=1)
    radius_r = radius_r.dropna(subset=['Rad_01', 'Rad_05', 'Rad_06'], thresh=1)

    try:
        scapula_df = df.loc[df['Element'] == 'Scapula'][['Id', 'Side', 'Element',
                                                               'Sca_01', 'Sca_02']]

        scapula_l = scapula_df.loc[scapula_df['Side'] == 'Left']
        scapula_r = scapula_df.loc[scapula_df['Side'] == 'Right']
    except KeyError:
        try:
            scapula_l = df[['Id', 'Sca_01', 'Sca_02']]
            scapula_r = df[['Id', 'Sca_01R', 'Sca_02R']]

            scapula_r.rename(columns={'Sca_01R': 'Sca_01', 'Sca_02R': 'Sca_02'}, inplace=True)

            scapula_l.loc[:, 'Side'] = 'Left'
            scapula_l.loc[:, 'Element'] = 'Scapula'

            scapula_r.loc[:, 'Side'] = 'Right'
            scapula_r.loc[:, 'Element'] = 'Scapula'
        except KeyError:
            scapula_df = pd.DataFrame(columns={'Id', 'Side', 'Element', 'Sca_01', 'Sca_02'})

            scapula_l = scapula_df.loc[scapula_df['Side'] == 'Left']
            scapula_r = scapula_df.loc[scapula_df['Side'] == 'Right']

    scapula_l = scapula_l.dropna(subset=['Sca_01', 'Sca_02'], thresh=1)
    scapula_r = scapula_r.dropna(subset=['Sca_01', 'Sca_02'], thresh=1)

    try:
        tibia_df = df.loc[df['Element'] == 'Tibia'][['Id', 'Side', 'Element',
                                                           'Tib_01', 'Tib_02', 'Tib_03', 'Tib_04',
                                                           'Tib_05']]
        tibia_l = tibia_df.loc[tibia_df['Side'] == 'Left']
        tibia_r = tibia_df.loc[tibia_df['Side'] == 'Right']

    except KeyError:
        try:
            tibia_l = df[['Id', 'Tib_01', 'Tib_02', 'Tib_03', 'Tib_04', 'Tib_05']]
            tibia_r = df[['Id', 'Tib_01R', 'Tib_02R', 'Tib_03R', 'Tib_04R', 'Tib_05R']]

            tibia_r.rename(columns={'Tib_01R': 'Tib_01', 'Tib_02R': 'Tib_02', 'Tib_03R': 'Tib_03',
                                    'Tib_04R': 'Tib_04', 'Tib_05R': 'Tib_05'}, inplace=True)

            tibia_l.loc[:, 'Side'] = 'Left'
            tibia_l.loc[:, 'Element'] = 'Tibia'

            tibia_r.loc[:, 'Side'] = 'Right'
            tibia_r.loc[:, 'Element'] = 'Tibia'
        except KeyError:
            tibia_df = pd.DataFrame(columns={'Id', 'Side', 'Element', 'Tib_01', 'Tib_02', 'Tib_03', 'Tib_04', 'Tib_05'})

            tibia_l = tibia_df.loc[tibia_df['Side'] == 'Left']
            tibia_r = tibia_df.loc[tibia_df['Side'] == 'Right']

    tibia_l = tibia_l.dropna(subset=['Tib_01', 'Tib_02', 'Tib_03', 'Tib_04', 'Tib_05'], thresh=1)
    tibia_r = tibia_r.dropna(subset=['Tib_01', 'Tib_02', 'Tib_03', 'Tib_04', 'Tib_05'], thresh=1)

    try:
        ulna_df = df.loc[df['Element'] == 'Ulna'][['Id', 'Side', 'Element',
                                                         'Uln_01', 'Uln_04', 'Uln_05', 'Uln_06']]

        ulna_l = ulna_df.loc[ulna_df['Side'] == 'Left']
        ulna_r = ulna_df.loc[ulna_df['Side'] == 'Right']

    except KeyError:
        try:
            ulna_l = df[['Id', 'Uln_01', 'Uln_04', 'Uln_05', 'Uln_06']]
            ulna_r = df[['Id', 'Uln_01R', 'Uln_04R', 'Uln_05R', 'Uln_06R']]

            ulna_r.rename(columns={'Uln_01R': 'Uln_01', 'Uln_04R': 'Uln_04', 'Uln_05R': 'Uln_05',
                                    'Uln_06R': 'Uln_06'}, inplace=True)

            ulna_l.loc[:, 'Side'] = 'Left'
            ulna_l.loc[:, 'Element'] = 'Ulna'

            ulna_r.loc[:, 'Side'] = 'Right'
            ulna_r.loc[:, 'Element'] = 'Ulna'
        except KeyError:
            ulna_df = pd.DataFrame(columns={'Id', 'Side', 'Element', 'Uln_01', 'Uln_04', 'Uln_05', 'Uln_06'})

            ulna_l = ulna_df.loc[ulna_df['Side'] == 'Left']
            ulna_r = ulna_df.loc[ulna_df['Side'] == 'Right']

    ulna_l = ulna_l.dropna(subset=['Uln_01', 'Uln_04', 'Uln_05', 'Uln_06'], thresh=1)
    ulna_r = ulna_r.dropna(subset=['Uln_01', 'Uln_04', 'Uln_05', 'Uln_06'], thresh=1)

    return {'Tibia': (tibia_l, tibia_r), 'Fibula': (fibula_l, fibula_r),
            'Femur': (femur_l, femur_r), 'Os_coxa': (os_coxa_l, os_coxa_r),
            'Humerus': (humerus_l, humerus_r),'Radius': (radius_l, radius_r),
            'Ulna': (ulna_l, ulna_r), 'Scapula': (scapula_l, scapula_r),
            'Clavicle': (clavicle_l, clavicle_r)}


def get_measurement_keys(element):
    measurement_keys = []

    if 'Clavicle' == element:
        measurement_keys.extend(['Cla_01', 'Cla_04', 'Cla_05'])

    if 'Femur' == element:
        measurement_keys.extend(['Fem_01', 'Fem_02', 'Fem_03', 'Fem_04', 'Fem_05', 'Fem_06', 'Fem_07']) #Lowerr

    if 'Fibula' == element:
        measurement_keys.extend(['Fib_01', 'Fib_02'])

    if 'Humerus' == element:
        measurement_keys.extend(['Hum_01', 'Hum_02', 'Hum_03', 'Hum_04',
                                 'Hum_05'])

    if 'Os_coxa' == element:
        measurement_keys.extend(['Osc_01', 'Osc_02'])

    if 'Radius' == element:
        measurement_keys.extend(['Rad_01', 'Rad_05', 'Rad_06'])

    if 'Scapula' == element:
        measurement_keys.extend(['Sca_01', 'Sca_02'])

    if 'Tibia' == element:
        measurement_keys.extend(['Tib_01', 'Tib_02', 'Tib_03', 'Tib_04', 'Tib_05'])

    if 'Ulna' == element:
        measurement_keys.extend(['Uln_01', 'Uln_04', 'Uln_05', 'Uln_06'])

    return measurement_keys

