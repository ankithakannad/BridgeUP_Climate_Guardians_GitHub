def seasonal_mean(data, months):
    '''
    Find mean over months specificed.

    Inputs:
    data = monthly data (xarray format)
    months = list of months to average (for example: May to July is [5,6,7])

    Outputs:
    data_season = seasonal data for each year
    '''
    no_months = len(months)
    data_season = data.where(data['time.month'].isin(months))
    data_season = data_season.rolling(min_periods= no_months, center=True, time=no_months).mean()
    data_season = data_season.groupby('time.year').mean()
    data_season = data_season.rename({'year':'time'})
    data_season = data_season.dropna(dim = 'time',how = 'all')
    return data_season