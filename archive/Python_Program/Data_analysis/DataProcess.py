# Yifei Wang Nov.13.2024
import pandas as pd
import matplotlib.pyplot as plt

solar_data = pd.read_csv('./Dataset/solar_data.csv')
site_params = pd.read_csv('./Dataset/site_params.csv')

# Extract site parameters
site_1_para = site_params.iloc[0, :]
site_2_para = site_params.iloc[1, :]
site_3_para = site_params.iloc[2, :]
site_4_para = site_params.iloc[3, :]

# Split solar_data by the first column values (1, 2, 3, 4)
solar_data_1 = solar_data[solar_data.iloc[:, 0] == 1]
solar_data_2 = solar_data[solar_data.iloc[:, 0] == 2]
solar_data_3 = solar_data[solar_data.iloc[:, 0] == 3]
solar_data_4 = solar_data[solar_data.iloc[:, 0] == 4]


from datetime import datetime
def print_date_info(solar_data, site_id):
    site_data = solar_data[solar_data['site_id'] == site_id]
    start_date = site_data['timestamp_utc'].min()
    end_date = site_data['timestamp_utc'].max()
    num_days = (datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S') - datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')).days
    print(f"Site {site_id}:")
    print(f"  Start Date: {start_date}")
    print(f"  End Date: {end_date}")
    print(f"  Number of Days: {num_days}\n")

# Print date info for each site
for site_id in solar_data['site_id'].unique():
    print_date_info(solar_data, site_id)


# Adjust the plotting by start date, end date, and site number
def plot_solar_data_by_date(solar_data, site_id, start_date, end_date):
    site_data = solar_data[(solar_data['site_id'] == site_id) & 
                           (solar_data['timestamp_utc'] >= start_date) & 
                           (solar_data['timestamp_utc'] <= end_date)]
    plt.plot(site_data['timestamp_utc'], site_data['solar_gen_kwh'])
    plt.xlabel('Timestamp')
    plt.ylabel('Solar Generation (kWh)')
    plt.title(f'Solar Data Visualization for Site {site_id}')
    # plt.xticks([])
    plt.xticks([site_data['timestamp_utc'].iloc[0], site_data['timestamp_utc'].iloc[-1]], 
               [site_data['timestamp_utc'].iloc[0], site_data['timestamp_utc'].iloc[-1]], rotation=0)
    plt.show()
# Example usage
# plot_solar_data_by_date(solar_data, site_id=2, start_date='2019-03-01', end_date='2019-09-30')
# plot_solar_data_by_date(solar_data, site_id=1, start_date='2019-03-01', end_date='2020-03-01')

plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plot_solar_data_by_date(solar_data, site_id=1, start_date='2019-03-01', end_date='2019-03-02')
plt.subplot(1, 2, 2)
plot_solar_data_by_date(solar_data, site_id=2, start_date='2019-03-01', end_date='2019-03-02')
# plt.tight_layout()
# plt.show()


# plot_solar_data_by_date(solar_data, site_id=1, start_date='2019-03-01', end_date='2019-09-30')
# plot_solar_data_by_date(solar_data, site_id=4, start_date='2019-03-01', end_date='2019-09-30')


