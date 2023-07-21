# WroclawTech.AIR - Large Dataset of High-Frequency Air Quality Measurements from a Dense Sensor Network on University Campuses

We release a four-year dataset of air quality measurements collected using a dense sensor network of 20 sensors deployed on four campuses of the Wrocław University of Science and Technology. The sensors were programmed to measure various air quality parameters every ten seconds, providing high-frequency and time-resolved data. The dataset provides an extensive and unique opportunity to understand the temporal dynamics of air quality in an urban environment, both short-term and long-term. The collected data include particulate matter (PM) measurements and local environmental characteristics. The dataset will be of great value to researchers in air quality monitoring and prediction. Alongside the dataset, we provide a background on the state of the short-term, high-frequency, sub-hour air quality data sets and an extensive exploratory analysis of the released dataset.

The raw data files are hosted on the Kraina AI server:
- 2019: https://labs.kraina.ai/wroclawtech.air/raw_2019.tar.bz2
- 2020: https://labs.kraina.ai/wroclawtech.air/raw_2020.tar.bz2
- 2021: https://labs.kraina.ai/wroclawtech.air/raw_2021.tar.bz2
- 2022: https://labs.kraina.ai/wroclawtech.air/raw_2022.tar.bz2

To generate an averaged variant of the data sets, use the following command:

```python generate_data.py "15min" "input_dir" "output_dir"```

The arguments are in order:

1. window - a time window the data will be averaged with, e.g. '15min'. Other possible windows: https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
2. input_dir - path to the input directory, where you should untar the raw data, so it contains the .feather files with readings from the sensor nodes from different months and years
3. output_dir - path to the output directory which will contain output .csv files for the years 2019, 2020, 2021 and 2022.

The processed data, with the 15 minute window, as described in the paper, is available here: https://labs.kraina.ai/wroclawtech.air/15min_averages.tar.bz2
