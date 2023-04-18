"""This script generates an air quality dataset that can be used in further experiments.

The script takes in three arguments:
1. window - a time window the data will be averaged with, e.g. '15min'. Other possible windows: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
2. input_dir - path to the input directory with .feather files containing readings from the sensor nodes from different months and years
3. output_dir - path to the output directory which will contain output .csv files for the years 2019, 2020, 2021 and 2022.
"""

import pandas as pd
import os
pd.options.plotting.backend = "plotly"
import plotly.io as pio
pio.renderers.default = "browser"
import numpy as np
import argparse


def rename_columns(df, suffix):
    new_column_names = dict()
    for column_name in df.columns:
        if column_name != 'timestamp':
            new_column_names[column_name] = f"{suffix}.{column_name}"
    df.rename(columns=new_column_names, inplace=True)


def filter_df_on_dates(df, dates: dict):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    dfs = []
    for year, months in dates.items():
        months_int = [int(x) for x in months]
        mask = (df['timestamp'].dt.year == int(year)) & (df['timestamp'].dt.month.isin(months_int))
        year_df = df.loc[mask]
        dfs.append(year_df)
    return pd.concat(dfs)


def generate_dataset(window: str, input_dir: str, output_dir: str, year: str):
    dates_dict = dict()

    readings_features = ['PM2.5[calibrated]', 'Temperature[OUT, C]', 'RelativeHumidity[OUT, %]', 'Pressure [hPa]']

    if year == '2019':
        dates_dict['2018'] = ['12']
        months = [str(i).zfill(2) for i in range(1, 11)]
        dates_dict['2019'] = months
    elif year == '2020':
        dates_dict['2019'] = ['11', '12']
        months = [str(i).zfill(2) for i in range(1, 11)]
        dates_dict['2020'] = months
    elif year == '2021':
        dates_dict['2020'] = ['11', '12']
        months = [str(i).zfill(2) for i in range(1, 11)]
        dates_dict['2021'] = months
    elif year == '2022':
        dates_dict['2021'] = ['11', '12']
        months = [str(i).zfill(2) for i in range(1, 7)]
        dates_dict['2022'] = months

    sensor_ids = [f'10{str(x).zfill(2)}' for x in range(1, 21)]

    all_years_dfs = []

    for year, months in dates_dict.items():
        for i, month in enumerate(months):
            month_dfs = []
            print(f'Processing: {year}-{month}')
            for sensor_id in sensor_ids:
                for file_name in os.listdir(input_dir):
                    fname_sensor_id = file_name[:file_name.find('_')]
                    fname_year = file_name[file_name.find('_') + 1:file_name.rfind('_')]
                    fname_month = file_name[file_name.rfind('_') + 1: file_name.find('.')]
                    if fname_month == month and fname_year == year and fname_sensor_id == sensor_id:
                        m_df = pd.read_feather(os.path.join(input_dir, file_name), columns=readings_features + ['timestamp']).set_index('timestamp')              
                        m_df[m_df.select_dtypes(np.float64).columns] = m_df.select_dtypes(np.float64).astype(np.float16)
                        if window != "10s":
                            m_df = m_df.resample(window).mean()
                        rename_columns(m_df, sensor_id)
                        month_dfs.append(m_df)
                        del(m_df)

            if len(month_dfs):
                all_columns_df = month_dfs[0].join(month_dfs[1:])
                all_years_dfs.append(all_columns_df)
                del(all_columns_df)

    all_years_df = pd.concat(all_years_dfs)

    if not os.path.exists(output_dir):
      os.makedirs(output_dir)

    output_file = os.path.join(output_dir, f'{year}.csv')
    all_years_df.to_csv(output_file)
    print(f"{year} done. Output files saved in: {output_dir}.")



parser = argparse.ArgumentParser()
parser.add_argument("window", help="averaging window")
parser.add_argument("input_dir", help="path do the raw .feather files directory")
parser.add_argument("output_dir", help="path do the output .csv files directory")
args = parser.parse_args()

years = ['2019', '2020', '2021', '2022']

for year in years:
    # possible windows: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
    generate_dataset(window=args.window, input_dir=args.input_dir, output_dir=args.output_dir, year=year)