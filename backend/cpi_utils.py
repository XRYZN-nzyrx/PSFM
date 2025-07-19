# cpi_utils.py
import pandas as pd
from datetime import datetime
import os

#  Base path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cpi_data_path = os.path.join(BASE_DIR, "datasets", "CPIndex_2014-To-2024.csv")

#  Load CPI data once globally
cpi_data_raw = pd.read_csv(cpi_data_path, skiprows=1)
cpi_data = cpi_data_raw[cpi_data_raw['State'] == 'ALL India']

#  Convert to long format for monthly lookup
cpi_long = cpi_data.melt(
    id_vars=['Year', 'State', 'Description'],
    value_vars=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    var_name='Month',
    value_name='Inflation_Rate'
)
cpi_long.dropna(subset=['Inflation_Rate'], inplace=True)

#  Month string → integer
month_map = {
    'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
    'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}
cpi_long['Month_Num'] = cpi_long['Month'].map(month_map)

#  Add full timestamp column
cpi_long['Timestamp'] = cpi_long.apply(
    lambda row: datetime(int(row['Year']), row['Month_Num'], 1), axis=1
)

#  Function: Get CPI for specific month
def get_inflation_rate_from_cpi(year, month):
    try:
        timestamp = datetime(year, month, 1)
        rate = cpi_long.loc[cpi_long['Timestamp'] == timestamp, 'Inflation_Rate'].values
        return float(rate[0]) if len(rate) > 0 else None
    except Exception as e:
        print(f"[CPI-ERROR] Failed to get CPI for {month}/{year}: {e}")
        return None

#  Function: Get yearly average inflation
def get_yearly_inflation_rate(year):
    try:
        yearly_df = cpi_long[cpi_long['Year'] == year]
        monthly_values = yearly_df['Inflation_Rate'].astype(float)
        if monthly_values.empty:
            print(f"[CPI] No CPI data available for year: {year}")
            return None
        return monthly_values.mean()
    except Exception as e:
        print(f"[CPI-ERROR] Failed to compute yearly CPI for {year}: {e}")
        return None
