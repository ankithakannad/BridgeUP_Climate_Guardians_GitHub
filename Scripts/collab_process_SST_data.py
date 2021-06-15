#Import Python libraries
import setup
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import functions
from matplotlib import animation
from matplotlib.animation import FuncAnimation

#When file is run on Terminal, do this
if __name__ == '__main__':
  	
	#set up variables
	file_SST = 'HadISST_sst.nc'
	file_NAO = 'Hurrell_NAO_station.xlsx'

	#import file
	data_SST = xr.open_dataset(file_SST)
	data_NAO = pd.read_excel(file_NAO)
	data_NAO = data_NAO[6:]
	data_SST = data_SST.where((data_SST.longitude <= 50) & (data_SST.longitude >= -100))
	data_SST = data_SST.where(data_SST >= -5)
	print(data_NAO.head())
	print(data_SST.head())

	#set up the variables
	sst = data_SST.sst
	mean = sst.mean('time')
	time_NAO = data_NAO["time"]
	avg_NAO = data_NAO["NAO index"].mean()
	index_NAO = data_NAO["NAO index"]
	months = [12, 1, 2, 3]	
	MAK=time_NAO.where(index_NAO>=avg_NAO)  
	MAK2 = MAK.dropna()
	MAK3 = MAK2.to_list()
	
	#finding anomolies


	#defining our function for seasonal means
	def seasonal_mean(data,months):
		no_months=len(months)
		data_season=data.where(data['time.month'].isin(months))
		data_season=data_season.rolling(min_periods=mo_months, center=True, time=no_months).mean()
		data_season=data_season.groupby('time.year').mean()
		data_season=data_season.rename({'year':'time'})
		data_season=data_season.dropna(dim='time', how='all')
		return data_season

	#finding the winter mean
	winter_mean = functions.seasonal_mean(sst,months)
	winter_years = winter_mean - winter_mean.mean(dim= 'time') #calculate winter anomolies
	abnormal_years = winter_years.loc[MAK3,:,:]
	print('winter mean', winter_mean.mean(dim = 'time').values)
	print('max ', abnormal_years.max(), 'min', abnormal_years.min())


	#animation of SST
	fig, ax = plt.subplots(figsize=[10, 10])

	contour_opts = {'levels': np.linspace(-3, 5, 50), 'cmap':'coolwarm', 'lw': 2}
	cax = ax.contourf(abnormal_years.longitude, abnormal_years.latitude, abnormal_years[0,:,:], **contour_opts)
	#ax.set_title(sst[i])
	ax.set_xlabel("Longitude")
	ax.set_ylabel("Latitude")

	fig.colorbar(cax, label = "Temp Anomalies")

	def animate(i): 
		ax.collections = []
		ax.contourf(abnormal_years.longitude, abnormal_years.latitude, abnormal_years[i,:,:], **contour_opts)
		ax.set_title(abnormal_years.time[i].values)

	anim = FuncAnimation(fig, animate, interval=10000, frames=77)
	fig.show()

	writervideo = animation.PillowWriter(fps=4)
	anim.save("animated_sst_test.gif", writer=writervideo)


	#plotting
  plt.figure()
	plt.contourf(sst.longitude,sst.latitude,sst.where(sst >= -5).mean(dim="time"), cmap= "cool")
	plt.colorbar(label = 'Temperature')
	plt.xlabel('longitude')
	plt.ylabel('latitude')
	plt.savefig("Global Ocean SST", dpi =300)
	plt.show()

	#variables for the Atlantic Ocean plot
	atlantic1 = sst.where(sst.longitude <= 50)
	atlantic2 = atlantic1.where(atlantic1.longitude >= -100)

	#plotting the Atlantic Ocean
	plt.figure()
	plt.contourf(atlantic2.longitude,atlantic2.latitude,atlantic2.where(sst >= -5).mean(dim="time"), cmap= "cool")
	plt.colorbar(label = 'Temperature')
	plt.title("Ocean Temperatures of the Atlantic Ocean")
	plt.xlabel('longitude')
	plt.ylabel('latitude')
	plt.savefig("Atlantic Ocean SST", dpi =300)
	plt.show()
	

