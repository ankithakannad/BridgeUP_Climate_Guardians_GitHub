#Import Python libraries
import setup
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import functions
from matplotlib import animation
from matplotlib.animation import FuncAnimation

#after importing "setup", implement it here
setup.dataPath

#When file is run on Terminal, do this
if __name__ == '__main__':
  	
	#set up variables
	file_SST = 'HadISST_sst.nc'
	file_NAO = 'Hurrell_NAO_station.xlsx'

	#here we imported our files
	data_SST = xr.open_dataset(file_SST) 
	data_NAO = pd.read_excel(file_NAO)
	data_NAO = data_NAO[6:] #we set the NAO to match with the SST's starting year 
	data_SST = data_SST.where((data_SST.longitude <= 50) & (data_SST.longitude >= -100)) #these are the longitude values for the atlantic ocean
	data_SST = data_SST.where(data_SST >= -5) #this masks sea ice data
	print(data_NAO.head())
	print(data_SST.head())

	#set up the variables
	sst = data_SST.sst #our sst values
	mean = sst.mean('time') #the mean of all the SST points over the years
	time_NAO = data_NAO["time"] #NAO time values
	avg_NAO = data_NAO["NAO index"].mean() #mean NAO values
	index_NAO = data_NAO["NAO index"] #seperates the NAO values
	months = [12, 1, 2, 3]	#represents December-March
	
	#In order to focus on the years where the NAO is strong, we averaged the NAO index and set it to a condition to return the years of high NAO values.
	MAK=time_NAO.where(index_NAO>=avg_NAO)  #shows the NAO years where the NAO index value is >= the NAO average
	MAK2 = MAK.dropna() #removes all the "NA" values
	MAK3 = MAK2.to_list() #sets the numbers to a list
	

	#defining our function for finding seasonal means
	def seasonal_mean(data,months):
		no_months=len(months)
		data_season=data.where(data['time.month'].isin(months))
		data_season=data_season.rolling(min_periods=mo_months, center=True, time=no_months).mean()
		data_season=data_season.groupby('time.year').mean()
		data_season=data_season.rename({'year':'time'})
		data_season=data_season.dropna(dim='time', how='all')
		return data_season

	#We isolated the SST variable in order to create an index for just the winter mean. That way, it would be easier when calculating the SST anomalies.
	winter_mean = functions.seasonal_mean(sst,months)
	winter_years = winter_mean - winter_mean.mean(dim= 'time') #calculate winter anomolies
	print('winter mean', winter_mean.mean(dim = 'time').values)
	
	#indexes our processed SST data corresponding to the years of strong NAO we had previously found
	abnormal_years = winter_years.loc[MAK3,:,:]
	

	#animation of the SST for the abnormal years
	fig, ax = plt.subplots(figsize=[10, 10])

	contour_opts = {'levels': np.linspace(-3, 5, 50), 'cmap':'coolwarm', 'lw': 2}
	cax = ax.contourf(abnormal_years.longitude, abnormal_years.latitude, abnormal_years[0,:,:], **contour_opts)
	ax.set_xlabel("Longitude")
	ax.set_ylabel("Latitude")

	fig.colorbar(cax, label = "Temp Anomalies")

	def animate(i): 
		ax.collections = []
		ax.contourf(abnormal_years.longitude, abnormal_years.latitude, abnormal_years[i,:,:], **contour_opts)
		ax.set_title(abnormal_years.time[i].values)

	anim = FuncAnimation(fig, animate, interval=10000, frames=77) #frames=77 because we want to animate all 77 abnormal years
	fig.show()

	writervideo = animation.PillowWriter(fps=4) #sets the frames per second 
	anim.save("animated_sst_test.gif", writer=writervideo) #saves our animation


	#plotting the average SST values 
  	plt.figure()
	plt.contourf(sst.longitude,sst.latitude,sst.where(sst >= -5).mean(dim="time"), cmap= "cool")
	plt.colorbar(label = 'Temperature')
	plt.xlabel('longitude')
	plt.ylabel('latitude')
	plt.savefig("Global Ocean SST", dpi =300)
	plt.show()

	#variables that cropped our plot into only showing the Atlantic Ocean
	atlantic1 = sst.where(sst.longitude <= 50)
	atlantic2 = atlantic1.where(atlantic1.longitude >= -100)

	#plotting the average SST values of specifically the Atlantic Ocean
	plt.figure()
	plt.contourf(atlantic2.longitude,atlantic2.latitude,atlantic2.where(sst >= -5).mean(dim="time"), cmap= "cool")
	plt.colorbar(label = 'Temperature')
	plt.title("Ocean Temperatures of the Atlantic Ocean")
	plt.xlabel('longitude')
	plt.ylabel('latitude')
	plt.savefig("Atlantic Ocean SST", dpi =300)
	plt.show()
	
