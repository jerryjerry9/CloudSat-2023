###hdf file package
from pyhdf.SD  import SD, SDC
###
###data processing assoicated package
import numpy as np
#### Fuction for extracting variable names from hdf file
def HDFvars(File):
    hdfFile = SD(File, SDC.READ)
    dsets = hdfFile.datasets()
    k = []
    for key in dsets.keys():
        k.append(key)
    k.sort()
    hdfFile.end() # close the file
    return k
####

#### ec grid function
def region_latlon2grid(lon_cen,lat_cen,lon_ran,lat_ran,lon,lat):
##real grid[lon_cen,lat_cen,left_lon,right_lon,south_lat,north_lat]
  real_grid=np.zeros((6))
  real_grid[:]=12
##center test
  for xx in range(0,480):
     dis_x=abs(lon[xx]-lon_cen)
     if dis_x<0.375:
       real_grid[0]=xx
       break
  for yy in range(0,241):
     dis_y=abs(lat[yy]-lat_cen)
     if dis_y<0.375:
       real_grid[1]=yy
       break
##lon region
  if lon_ran==1:
     real_grid[2]=real_grid[0]
     real_grid[3]=real_grid[0]
  else:
     s_lon=lon_cen-lon_ran
     e_lon=lon_cen+lon_ran
     for xx in range(0,480):
       s_dis=abs(lon[xx]-s_lon)
       e_dis=abs(lon[xx]-e_lon)
       if s_dis<=0.375:
         real_grid[2]=xx
       if e_dis<=0.375:
         real_grid[3]=xx
##lat region
  if lat_ran==1:
     real_grid[4]=real_grid[1]
     real_grid[5]=real_grid[1]
  else:
     s_lat=lat_cen+lat_ran
     e_lat=lat_cen-lat_ran
     for yy in range(0,241):
       s_dis=abs(lat[yy]-s_lat)
       e_dis=abs(lat[yy]-e_lat)
       if s_dis<=0.375:
         real_grid[4]=yy
       if e_dis<=0.375:
         real_grid[5]=yy
  return real_grid
#### 

#### CloudSat region filter
def rFilter(lon,lat,lon_ran,lat_ran):
    arr_siz=len(lon)
    lon = np.array(lon)
    lon = lon[:,0]
    lon = np.where(lon >= 0, lon, lon+360)
    lat = np.array(lat)
    lat = lat[:,0]
    tem_mask = np.zeros((arr_siz))
    tem_mask = np.where((lon >= lon_ran[0]) & (lon <= lon_ran[1]) & (lat >= lat_ran[0]) & (lat <= lat_ran[1]), tem_mask+1, tem_mask)
    mask = np.zeros((arr_siz,1))
    mask[:,0] = tem_mask
    return np.array(mask)
#### finction end

#### trmm grid convert
def lat_lon_trmm(s_lon,e_lon,s_lat,e_lat):
###
  trmm_s_lon=[]
  trmm_e_lon=[]
  if s_lon>=180:
   trmm_s_lon.append(s_lon-360+0.125)
   trmm_e_lon.append(e_lon-360-0.125)
  elif e_lon>=180 and s_lon<180:
   trmm_s_lon.append(s_lon+0.125)
   trmm_e_lon.append(180-0.125)
   trmm_s_lon.append(-180+0.125)
   trmm_e_lon.append(e_lon-360-0.125)
  else:
   trmm_s_lon.append(s_lon+0.125)
   trmm_e_lon.append(e_lon-0.125)
  trmm_s_lat=s_lat+0.125
  trmm_e_lat=e_lat-0.125
###
###
  trmm_x = np.arange(-179.875,180.,0.25)
  trmm_y = np.arange(-49.875,50.,0.25)
  lon_num=len(trmm_s_lon)
  s_lon_pos=np.zeros((lon_num))
  e_lon_pos=np.zeros((lon_num))
  for i in range(0,len(trmm_s_lon)):
    ta_s = np.where((trmm_x[:]==trmm_s_lon[i]))
    ta_e = np.where((trmm_x[:]==trmm_e_lon[i]))
    s_lon_pos[i]=ta_s[0]
    e_lon_pos[i]=ta_e[0]
  s_lat_pos = np.where((trmm_y[:]==trmm_s_lat))
  e_lat_pos = np.where((trmm_y[:]==trmm_e_lat))
  return(s_lon_pos,e_lon_pos,lon_num,s_lat_pos,e_lat_pos)
#### function end

#### CWV bin
def CWV_bin(bin_size,bin_start,mer_bot,mer_top):
 cwv_bin=bin_size # cwv bin_size
 cwv_interval=[]
 ## create cwv interval array
 start_bin=bin_start # first bin
 while(start_bin<101):
  cwv_interval.append(start_bin)
  start_bin=start_bin+cwv_bin

 bin_num=len(cwv_interval)
 ### merge CWV lower than specific value
 bot=cwv_interval.index(mer_bot)
 ### merge CWV higher than specific value
 top=cwv_interval.index(mer_top)
 return(cwv_interval,bin_num,bot,top)
#### CWV bin

#### Merge function
def merge_fun(pre_array,bin_num,bot,top):
 ssize=pre_array.shape
 mer_array = np.zeros((int(ssize[0]),bin_num))
 mer_array[:,bot] = np.sum(pre_array[:,0:bot+1],axis=1)
 mer_array[:,bot+1:top+1] = pre_array[:,bot+1:top+1]
 mer_array[:,top+1] = np.sum(pre_array[:,top+1:],axis=1)
 return(mer_array)
