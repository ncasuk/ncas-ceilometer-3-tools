from netCDF4 import Dataset
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.image as image
from matplotlib.colors import LogNorm
import numpy as np
import datetime as dt



"""
Useful functions
"""

def set_major_minor_date_ticks(ax):
    ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=range(0,24,2)))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter("%H:%M"))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M\n%Y/%m/%d"))

    
    
"""
Plots for today's data
"""

def aerosol_backscatter_today(today_file, output_location = '.', image_file = 'NCAS_national_centre_logo_transparent-768x184.png'):
    """
    Create plot of aerosol-backscatter
    """
    today_nc = Dataset(today_file)

    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)

    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in today_nc['time'][:] ]

    c = ax.pcolormesh(x,today_nc['altitude'][:],today_nc['attenuated_aerosol_backscatter_coefficient'][:].T,norm = LogNorm(vmin=(10**-7),vmax=(10**-3)))

    set_major_minor_date_ticks(ax)

    ax.grid(which='both')
    ax.set_ylabel('Altitude (m)')
    ax.set_xlabel('Time (UTC)')

    cbar = fig.colorbar(c, ax = ax)
    cbar.ax.set_ylabel(f"Attenuated aerosol backscatter coefficient ({today_nc['attenuated_aerosol_backscatter_coefficient'].units})")

    im = image.imread(image_file)
    newax = fig.add_axes([0.62,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    plt.savefig(f'{output_location}/plot_ncas-ceilometer-3_aerosol-backscatter_today.png')
    plt.close()
    
    
    
def cloud_base_height_today(today_file, output_location = '.', image_file = 'NCAS_national_centre_logo_transparent-768x184.png'):
    """
    Create plot of cloud-base-height
    """
    today_nc = Dataset(today_file)           
    
    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in today_nc['time'][:] ]

    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)

    ax.plot(x,today_nc['cloud_base_altitude'][:,0], label = 'Cloud base height 1')
    ax.plot(x,today_nc['cloud_base_altitude'][:,1], label = 'Cloud base height 2')
    ax.plot(x,today_nc['cloud_base_altitude'][:,2], label = 'Cloud base height 3')
    ax.plot(x,today_nc['cloud_base_altitude'][:,3], label = 'Cloud base height 4')

    set_major_minor_date_ticks(ax)

    ax.grid(which = 'both')
    ax.legend(loc='upper left')
    ax.set_xlabel('Time (UTC)')
    ax.set_ylabel('Altitude (m)')

    ax.set_xlim([x[0],x[-1]])

    im = image.imread(image_file)
    newax = fig.add_axes([0.78,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    plt.savefig(f'{output_location}/plot_ncas-ceilometer-3_cloud-base-height_today.png')
    plt.close()
    
    
    
"""
Plots for last 24 hours
"""

def aerosol_backscatter_last24(yesterday_file, today_file, output_location = '.', image_file = 'NCAS_national_centre_logo_transparent-768x184.png'):
    """
    Create plot of aerosol-backscatter for last 24 hours
    """
    yesterday_nc = Dataset(yesterday_file)
    today_nc = Dataset(today_file)
    
    current_time = dt.datetime.now(dt.timezone.utc)
    current_time = dt.datetime.strptime("2022-02-18T17:54:48 +00:00","%Y-%m-%dT%H:%M:%S %z")
    time_minus_24 = current_time - dt.timedelta(days=1)
    time_minus_24_timestamp = time_minus_24.timestamp()
    
    y_locs = np.where(yesterday_nc['time'][:] > time_minus_24_timestamp)[0]
    
    y_times = yesterday_nc['time'][:][y_locs]
    t_times = today_nc['time'][:]
    times = np.hstack((y_times,t_times))
    
    y_ab = yesterday_nc['attenuated_aerosol_backscatter_coefficient'][y_locs,:]
    t_ab = today_nc['attenuated_aerosol_backscatter_coefficient'][:]
    aeroback = np.vstack((y_ab,t_ab))
    
    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)
    
    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in times ]
    
    c = ax.pcolormesh(x,today_nc['altitude'][:],aeroback.T,norm = LogNorm(vmin=(10**-7),vmax=(10**-3)))
    
    set_major_minor_date_ticks(ax)
    
    ax.grid(which='both')
    ax.set_ylabel('Altitude (m)')
    ax.set_xlabel('Time (UTC)')
    
    cbar = fig.colorbar(c, ax = ax)
    cbar.ax.set_ylabel(f"Attenuated aerosol backscatter coefficient ({today_nc['attenuated_aerosol_backscatter_coefficient'].units})")
    
    im = image.imread(image_file)
    newax = fig.add_axes([0.62,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    plt.savefig(f'{output_location}/plot_ncas-ceilometer-3_aerosol-backscatter_last24.png')
    plt.close()
    
    
    
def cloud_base_height_last24(yesterday_file, today_file, output_location = '.', image_file = 'NCAS_national_centre_logo_transparent-768x184.png'):
    """
    Create plot of cloud base height for last 24 hours
    """
    yesterday_nc = Dataset(yesterday_file)
    today_nc = Dataset(today_file)
    
    current_time = dt.datetime.now(dt.timezone.utc)
    current_time = dt.datetime.strptime("2022-02-18T17:54:48 +00:00","%Y-%m-%dT%H:%M:%S %z")
    time_minus_24 = current_time - dt.timedelta(days=1)
    time_minus_24_timestamp = time_minus_24.timestamp()
    
    y_locs = np.where(yesterday_nc['time'][:] > time_minus_24_timestamp)[0]
    
    y_times = yesterday_nc['time'][:][y_locs]
    t_times = today_nc['time'][:]
    times = np.hstack((y_times,t_times))
    
    y_cba = yesterday_nc['cloud_base_altitude'][y_locs,:]
    t_cba = today_nc['cloud_base_altitude'][:]
    cba = np.vstack((y_cba,t_cba))         
    
    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in times ]

    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)

    ax.plot(x,cba[:,0], label = 'Cloud base height 1')
    ax.plot(x,cba[:,1], label = 'Cloud base height 2')
    ax.plot(x,cba[:,2], label = 'Cloud base height 3')
    ax.plot(x,cba[:,3], label = 'Cloud base height 4')

    set_major_minor_date_ticks(ax)

    ax.grid(which = 'both')
    ax.legend(loc='upper left')
    ax.set_xlabel('Time (UTC)')
    ax.set_ylabel('Altitude (m)')

    ax.set_xlim([x[0],x[-1]])

    im = image.imread(image_file)
    newax = fig.add_axes([0.78,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    plt.savefig(f'{output_location}/plot_ncas-ceilometer-3_cloud-base-height_last24.png')
    plt.close()
    
    
    
"""
Plots for last 48 hours
"""

def aerosol_backscatter_last48(day_before_yesterday_file, yesterday_file, today_file, output_location = '.', image_file = 'NCAS_national_centre_logo_transparent-768x184.png'):
    """
    Create plot of aerosol-backscatter for last 48 hours
    """
    day_before_yesterday_nc = Dataset(day_before_yesterday_file)
    yesterday_nc = Dataset(yesterday_file)
    today_nc = Dataset(today_file)
    
    current_time = dt.datetime.now(dt.timezone.utc)
    current_time = dt.datetime.strptime("2022-02-18T17:54:48 +00:00","%Y-%m-%dT%H:%M:%S %z")
    time_minus_48 = current_time - dt.timedelta(days=2)
    time_minus_48_timestamp = time_minus_48.timestamp()
    
    dby_locs = np.where(day_before_yesterday_nc['time'][:] > time_minus_48_timestamp)[0]
    
    dby_times = day_before_yesterday_nc['time'][:][dby_locs]
    y_times = yesterday_nc['time'][:]
    t_times = today_nc['time'][:]
    times = np.hstack((dby_times,y_times,t_times))
    
    dby_ab = day_before_yesterday_nc['attenuated_aerosol_backscatter_coefficient'][dby_locs,:]
    y_ab = yesterday_nc['attenuated_aerosol_backscatter_coefficient'][:]
    t_ab = today_nc['attenuated_aerosol_backscatter_coefficient'][:]
    aeroback = np.vstack((dby_ab,y_ab,t_ab))
    
    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)
    
    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in times ]
    
    c = ax.pcolormesh(x,today_nc['altitude'][:],aeroback.T,norm = LogNorm(vmin=(10**-7),vmax=(10**-3)))
    
    set_major_minor_date_ticks(ax)
    
    ax.grid(which='both')
    ax.set_ylabel('Altitude (m)')
    ax.set_xlabel('Time (UTC)')
    
    cbar = fig.colorbar(c, ax = ax)
    cbar.ax.set_ylabel(f"Attenuated aerosol backscatter coefficient ({today_nc['attenuated_aerosol_backscatter_coefficient'].units})")
    
    im = image.imread(image_file)
    newax = fig.add_axes([0.62,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    plt.savefig(f'{output_location}/plot_ncas-ceilometer-3_aerosol-backscatter_last48.png')
    plt.close()
    
    
    
def cloud_base_height_last48(day_before_yesterday_file, yesterday_file, today_file, output_location = '.', image_file = 'NCAS_national_centre_logo_transparent-768x184.png'):
    """
    Create plot of cloud base height for last 48 hours
    """
    day_before_yesterday_nc = Dataset(day_before_yesterday_file)
    yesterday_nc = Dataset(yesterday_file)
    today_nc = Dataset(today_file)
    
    current_time = dt.datetime.now(dt.timezone.utc)
    current_time = dt.datetime.strptime("2022-02-18T17:54:48 +00:00","%Y-%m-%dT%H:%M:%S %z")
    time_minus_48 = current_time - dt.timedelta(days=2)
    time_minus_48_timestamp = time_minus_48.timestamp()
    
    dby_locs = np.where(day_before_yesterday_nc['time'][:] > time_minus_48_timestamp)[0]
    
    dby_times = day_before_yesterday_nc['time'][:][dby_locs]
    y_times = yesterday_nc['time'][:]
    t_times = today_nc['time'][:]
    times = np.hstack((dby_times,y_times,t_times))
    
    dby_cba = day_before_yesterday_nc['cloud_base_altitude'][dby_locs,:]
    y_cba = yesterday_nc['cloud_base_altitude'][:]
    t_cba = today_nc['cloud_base_altitude'][:]
    cba = np.vstack((dby_cba,y_cba,t_cba))         
    
    x = [ dt.datetime.fromtimestamp(i, dt.timezone.utc) for i in times ]

    fig = plt.figure(figsize=(20,8))
    fig.set_facecolor('white')
    ax = fig.add_subplot(111)

    ax.plot(x,cba[:,0], label = 'Cloud base height 1')
    ax.plot(x,cba[:,1], label = 'Cloud base height 2')
    ax.plot(x,cba[:,2], label = 'Cloud base height 3')
    ax.plot(x,cba[:,3], label = 'Cloud base height 4')
    
    set_major_minor_date_ticks(ax)

    ax.grid(which = 'both')
    ax.legend(loc='upper left')
    ax.set_xlabel('Time (UTC)')
    ax.set_ylabel('Altitude (m)')

    ax.set_xlim([x[0],x[-1]])

    im = image.imread(image_file)
    newax = fig.add_axes([0.78,0.75,0.12,0.12], anchor='NE')
    newax.imshow(im)
    newax.axis('off')
    
    plt.savefig(f'{output_location}/plot_ncas-ceilometer-3_cloud-base-height_last48.png')
    plt.close()
    
    
if __name__ == "__main__":
    from collections import Counter
    import argparse
    parser = argparse.ArgumentParser(description = 'Make plots for ncas-ceilometer-3.', allow_abbrev=False, argument_default=argparse.SUPPRESS)
    parser.add_argument('netCDFs', nargs = '+', help = "netCDF files with data to be plotted. At minimum today's file should be given, \
                                                        as well as yesterday's for 24 hour plots and the day before yesterday's for 48 hour plots.")
    parser.add_argument('-o','--output-location', default = ".", help = "Location of where to save plots. Default is '.'.")
    parser.add_argument('-a','--aerosol-backscatter-today', action='store_true', help = 'Make plot of aerosol backscatter for today.')
    parser.add_argument('-c','--cloud-base-height-today', action='store_true', help = 'Make plot of cloud base height for today.')
    parser.add_argument('-a24','--aerosol-backscatter-last24', action='store_true', help = 'Make plot of aerosol backscatter for past 24 hours.')
    parser.add_argument('-c24','--cloud-base-height-last24', action='store_true', help = 'Make plot of cloud base height for past 24 hours.')
    parser.add_argument('-a48','--aerosol-backscatter-last48', action='store_true', help = 'Make plot of aerosol backscatter for past 48 hours.')
    parser.add_argument('-c48','--cloud-base-height-last48', action='store_true', help = 'Make plot of cloud base height for past 48 hours.')
    parser.add_argument('-i','--image-file', default = 'NCAS_national_centre_logo_transparent-768x184.png', help = 'logo image for plots.')
    args = parser.parse_args()
    
    
    given_args = args._get_kwargs()
    netcdf_files = args.netCDFs
    
    # Check no repeated netCDF files
    if len(set(netcdf_files)) != len(netcdf_files):
        counter = Counter(netcdf_files)
        msg = 'the following files have been given more than once:'
        for i in counter.items():
            if i[1] > 1:
                msg += ' '
                msg += str(i[0])
                msg += ','
        msg = msg[:-1]  # remove trailing comma
        raise ValueError(msg)
    
    
    # Check not too many netCDF files
    aerosol_netcdfs = [ f for f in netcdf_files if 'aerosol-backscatter' in f ]
    if len(aerosol_netcdfs) > 3:
        msg = "Too many netCDF files for aerosol-backscatter"
        raise ValueError(msg)
    aerosol_dates = [ f.split('ncas-ceilometer-3')[1].split('_')[2] for f in aerosol_netcdfs ]

    # Check no repeated dates
    if len(set(aerosol_dates)) != len(aerosol_dates):
        counter = Counter(aerosol_dates)
        msg = 'the following dates have been given more than once for aerosol-backscatter:'
        for i in counter.items():
            if i[1] > 1:
                msg += ' '
                msg += str(i[0])
                msg += ','
        msg = msg[:-1]  # remove trailing comma
        raise ValueError(msg)
        
    # order files by date in reverse, i.e. today's file first
    reversed_dates = sorted(aerosol_dates, reverse=True)
    aerosol_netcdf_ordered = []
    for d in reversed_dates:
        for f in aerosol_netcdfs:
            if d in f:
                aerosol_netcdf_ordered.append(f)
                break
    
    # Check not too many netCDF files
    cbh_netcdfs = [ f for f in netcdf_files if 'cloud-base' in f ]
    if len(cbh_netcdfs) > 3:
        msg = "Too many netCDF files for cloud-base"
        raise ValueError(msg)
    cbh_dates = [ f.split('ncas-ceilometer-3')[1].split('_')[2] for f in cbh_netcdfs ]
    
    # Check no repeated dates
    if len(set(cbh_dates)) != len(cbh_dates):
        counter = Counter(cbh_dates)
        msg = 'the following dates have been given more than once for cloud-base:'
        for i in counter.items():
            if i[1] > 1:
                msg += ' '
                msg += str(i[0])
                msg += ','
        msg = msg[:-1]  # remove trailing comma
        raise ValueError(msg)
        
    # order files by date in reverse, i.e. today's file first
    reversed_dates = sorted(cbh_dates, reverse=True)
    cbh_netcdf_ordered = []
    for d in reversed_dates:
        for f in cbh_netcdfs:
            if d in f:
                cbh_netcdf_ordered.append(f)
                break
    
   
    # make the requested plots
    for i in given_args:
        if i[0] not in  ['netCDFs', 'output_location', 'image_file']:
            if i[0] == 'aerosol_backscatter_today':
                print('Making aerosol_backscatter_today')
                aerosol_backscatter_today(aerosol_netcdf_ordered[0], output_location = args.output_location, image_file = args.image_file)
            elif i[0] == 'aerosol_backscatter_last24':
                print('Making aerosol_backscatter_last24')
                aerosol_backscatter_last24(aerosol_netcdf_ordered[1], aerosol_netcdf_ordered[0], output_location = args.output_location, image_file = args.image_file)
            elif i[0] == 'aerosol_backscatter_last48':
                print('Making aerosol_backscatter_last48')
                aerosol_backscatter_last48(aerosol_netcdf_ordered[2], aerosol_netcdf_ordered[1], aerosol_netcdf_ordered[0], output_location = args.output_location, image_file = args.image_file)
            elif i[0] == 'cloud_base_height_today':
                print('Making cloud_base_height_today')
                cloud_base_height_today(cbh_netcdf_ordered[0], output_location = args.output_location, image_file = args.image_file)
            elif i[0] == 'cloud_base_height_last24':
                print('Making cloud_base_height_last24')
                cloud_base_height_last24(cbh_netcdf_ordered[1], cbh_netcdf_ordered[0], output_location = args.output_location, image_file = args.image_file)
            elif i[0] == 'cloud_base_height_last48':
                print('Making cloud_base_height_last48')
                cloud_base_height_last48(cbh_netcdf_ordered[2], cbh_netcdf_ordered[1], cbh_netcdf_ordered[0], output_location = args.output_location, image_file = args.image_file)
            else:
                print(f'Unexpected option {i}, not sure how to deal with it, skipping... ')
