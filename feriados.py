import pandas as pd


def create_feriados_sp(df):
    # Generate a range of dates from the minimum to maximum date in the DataFrame
    all_dates = pd.date_range(start=df['ds'].min(), end=df['ds'].max(), freq='D')

    # Identify missing dates excluding weekends
    missing_dates = all_dates[~all_dates.isin(df['ds'])]

    # Exclude weekends (Saturday and Sunday)
    missing_dates = missing_dates[~missing_dates.dayofweek.isin([5, 6])]

    # Create a DataFrame in the format of 'feriados_sp' using missing dates
    feriados_sp_missing = pd.DataFrame({
        'holiday': 'feriados_sp',
        'ds': missing_dates,
        'lower_window': 0,
        'upper_window': 0,
    })

    return feriados_sp_missing
