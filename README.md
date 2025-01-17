# Neuraltoolkit

## Installation

### Download neuraltoolkit
git clone https://github.com/hengenlab/neuraltoolkit.git 
Enter your username and password

#### Windows
My Computer > Properties > Advanced System Settings > Environment Variables >  
In system variables, create a new variable  
    Variable name  : PYTHONPATH  
    Variable value : location where neuraltoolkit is located  
    Click OK


#### Linux
If you are using bash shell  
In terminal open .barshrc or .bash_profile  
add this line  
export PYTHONPATH=/location_of_neuraltoolkit:$PYTHONPATH


#### Mac
If you are using bash shell  
In terminal cd ~/  
then open  .profile using your favourite text editor (open -a TextEdit .profile)
to add location where neuraltoolkit is located add the line below

export PYTHONPATH=/location_of_neuraltoolkit:$PYTHONPATH




## load ecube data
#### List of functions

* load_raw_binary                 : To load plain raw data
* load_raw_binary_gain            : To load raw data with gain
* load_raw_binary_gain_chmap      : To load raw data with gain and channel mapping
* load_raw_binary_gain_chmap_nsec : To load nsec of raw data with gain and channel mapping

```
import neuraltoolkit as ntk
import numpy as np
from matplotlib import pyplot as plt

# Get filename
rawfile = 'neuraltoolkit/Headstages_64_Channels_int16_2018-04-06_10-01-57.bin'

# Get number of channels
print("Enter total number of channels : ")
number_of_channels = np.int16(eval(input()))

# Time and data
t, dgc = ntk.load_raw_binary_gain_chmap(rawfile, number_of_channels, 'hs64')

# Time only
t = ntk.load_raw_binary_gain_chmap(rawfile, number_of_channels, 'hs64', t_only=1)

# Time and data for multiple probes with same number of channels
hstype = ['Si_64_KS_chmap', 'Si_64_KT_T1_K2_chmap', 'Si_64_KT_T1_K2_chmap', 'Si_64_KS_chmap']
nprobes = 4
# number_of_channels here is total number of channels in all probes (64 * nprobes = 256)
t, dgc = ntk.load_raw_binary_gain_chmap(rawfile, number_of_channels, hstype, nprobes)

# bandpass filter
bdgc = ntk.butter_bandpass(dgc, 500, 7500, 25000, 3)

# plot raw data
ntk.plot_data(dgc, 0, 25000, 1)

# plot bandpassed data
ntk.plot_data(bdgc, 0, 25000, 1)

# plot data in channel list
l = np.array([5, 13, 31, 32, 42, 46, 47, 49, 51, 52, 53, 54 ])
ntk.plot_data_chlist(bdgc, 25000, 50000, l )

# Time and data from rawdata for nsec
# For single probe
tt, ddgc = ntk.load_raw_binary_gain_chmap_nsec(rawfile, number_of_channels, 'hs64', 25000, 2)
# For multiple probes
# hstype = ['Si_64_KS_chmap', 'Si_64_KT_T1_K2_chmap', 'Si_64_KT_T1_K2_chmap', 'Si_64_KS_chmap']
# nprobes = 4
tt, ddgc = ntk.load_raw_binary_gain_chmap_nsec(rawfile, number_of_channels, hstype, 25000, 2, nprobes)

# Load digital data for cameras, etc
digitalrawfile = '/home/kbn/Digital_64_Channels_int64_2018-11-04_11-18-12.bin'
t_only  : if t_only=1, just return  timestamp
          (Default 0, returns timestamp and data)
lcheckdigi64 : Default 1, check for digital file with 64 channel
          (atypical recordings) and correct values of -11 to 0 and -9 to 1
          lcheckdigi64=0, no checks are done, just read the file and
          returns timestamp and data
tdig, ddig = ntk.load_digital_binary(digitalrawfile, t_only=0, lcheckdigi64=1)

# Load time only from digital data for cameras, etc
tdig = ntk.load_digital_binary(digitalrawfile, t_only=1)

# Light dark transition
datadir = '/media/data/D1/d1_c1/'
l7ampm = 0 # if 1 just check files around 7:00 am and 7:00 pm
lplot = 0
ldt = ntk.light_dark_transition(datadir, l7ampm=0, lplot=0)
ldt - list contains
      [filename, index of light-dark transition in file, start time of the file]

# For example
[['Digital_1_Channels_int64_10.bin', 2743961, 24082251921475],
 ['Digital_1_Channels_int64_13.bin', 2677067, 67284509201475]]

# Visual grating transition
datadir = '/media/bs003r/D1/d1_vg1/'
transition_list = ntk.visual_grating_transition(datadir)
transition_list - list contains
      [filename, indices of visual grating transition in file, time in file]
#For example
Filename Digital_1_Channels_int64_1.bin
index  [  73042  273202  473699  674109  874218 1074640 1275357 1476104 1676162
 7287946 7488659]  time  3783012466437
Filename Digital_1_Channels_int64_2.bin
index  [ 189390  390242  590800  791281  991778 1192327 1392627 1593098 1793569
6005899 6206417 6406882 6607754 6808203 7008951 7209624]  time  4083006706437
Filename Digital_1_Channels_int64_3.bin
index  [5573869 5774268 5974585 6175289 6375922 6576758 6777207 6977770 7177962
7378361]  time  4983018546437

# Load preprocessed data file
pdata = ntk.load_raw_binary_preprocessed(preprocessedfilename, number_of_channels)

# Load one channel from data
number_of_channels = 64
channel_number = 4
# lraw is 1 for raw file and for prepocessed file lraw is 0
ch_data = ntk.load_a_ch(rawfile, number_of_channels, channel_number,
                    lraw=1)

# Load ecube data and returns time(if raw) and data in range
number_of_channels = 64
lraw is 1 for raw file and for prepocessed file lraw is 0
hstype,  linear if preprocessed file
ts = 0, start from begining of file or can be any sample number
te = 2500, read 2500 sample points from ts ( te greater than ts)
if ts =0 and te = -1,  read from begining to end of file
t, bdgc = ntk.load_raw_binary_gain_chmap_range(rawfile, number_of_channels,
                                           hstype, nprobes=1,
                                           lraw=1, ts=0, te=25000)

# Create channel mapping file for Open Ephys
import neuraltoolkit as ntk
ntk.create_chanmap_file_for_oe()
Enter total number of probes:
1
Enter total number of channels :
64
Enter probe type :
hs64
Enter filename to save data:
channelmap_hs64.txt


# make_binaryfiles_ecubeformat
import numpy as np
import neuraltoolkit as ntk
filename = '/home/kbn/HH.bin'
ltype = 2 # digital files
t = np.uint64(101)
if ltype == 1:
    data_low = -32000
    data_high = 32000
    data_rows = 64
    data_length = 25000*60*5
    data_type = 'int16'
elif ltype == 2:
    data_low = 0
    data_high = 2
    data_rows = 1
    data_length = 25000*60*5
    data_type = 'int64'
d = np.random.randint(data_low, data_high, (data_rows, data_length),
                      dtype=data_type)
ntk.make_binaryfiles_ecubeformat(t, d, filename, ltype)
```

## load intan data
#### List of functions
* load_intan_raw_gain_chanmap	: To load raw data with gain and channel mapping

```
# import libraries
import neuraltoolkit as ntk
import numpy as np
from matplotlib import pyplot as plt

# Get filename
rawfile = 'neuraltoolkit/intansimu_170807_205345.rhd'

# Get number of channels
print("Enter total number of channels : ")
number_of_channels = np.int16(eval(input()))

# Time and data
t, dgc = ntk.load_intan_raw_gain_chanmap(rawfile, number_of_channels, 'intan32')

# Time and data for multiple probes with same number of channels
hstype = ['intan32', 'linear']
nprobes = 2
# number_of_channels here is total number of channels in all probes (32 * nprobes = 64)
t, dgc = ntk.load_intan_raw_gain_chanmap(rawfile, number_of_channels, hstype, nprobes)

# Time, data, digital input ( for patch)
t, dgc, din = ntk.load_intan_raw_gain_chanmap(rawfile, number_of_channels, 'intan32', ldin=1)

# bandpass filter
bdgc = ntk.butter_bandpass(dgc, 500, 7500, 25000, 3)

# plot raw data
ntk.plot_data(dgc, 0, 25000, 1)

# plot bandpassed data
ntk.plot_data(bdgc, 0, 25000, 1)

# plot data in channel list
l = np.array([5, 13])
ntk.plot_data_chlist(bdgc, 25000, 50000, l )

# load aux binary data
import neuraltoolkit as ntk
import matplotlib.pyplot as plt
import numpy as np
aux_file = 'Acc_auxtest_191108_102919_t_0#145.8719_l_2917440_p_0_chg_1_aux3p74em5.bin'
auxd = ntk.load_aux_binary_data(aux_file, 3)
x_accel = auxd[0, :]
y_accel = auxd[1, :]
z_accel = auxd[2, :]
# sampling rate for aux is rawdata sampling rate/4
x = np.arange(0, auxd.shape[1]*4, 4)
plt.subplot(3, 1, 1)
plt.plot(x, x_accel, '.-')
plt.title('Plot accelorometer data')
plt.ylabel('X acceleration')
plt.ylim((0.0, 2.5))
plt.subplot(3, 1, 2)
plt.plot(x, y_accel, '.-')
plt.ylabel('Y acceleration')
plt.ylim(0.0, 2.5)
plt.subplot(3, 1, 3)
plt.plot(x, z_accel, '.-')
plt.xlabel('time')
plt.ylabel('Z acceleration')
plt.ylim(0.0, 2.5)
plt.show()
 

```

## video
#### List of functions/Class
```
import neuraltoolkit as ntk
videofilename = '/home/user/e3v810a-20190307T0740-0840.mp4'
lstream = 0

# get video attributes
v = ntk.NTKVideos(videofilename, lstream)
print(v.fps)
30.00
print(v.width)
640.0
print(v.height)
480.0
print(v.length)
107998.0

# play video, please press q to exit
v.play_video()

# extract_frames and save to a folder
outpath = '/home/user/out/'
v.extract_frames(outpath)

# Grab a frame and write to disk
frame_num = 1
outpath = '/home/user/out/'
v.grab_frame_num(frame_num, outpath)

# Grab a frame and show
frame_num = 100
v.grab_frame_num(frame_num)

# Read video files and return list of all video lengths
v_lengths = ntk.get_video_length_list('/home/kbn/watchtower_current/data/')

# Convert video to grey
videofilename = '/media/bs001r/ckbn/opencv/e3v8102-20190711T0056-0156.mp4'
lstream = 0
output_path = '/media/bs001r/ckbn/opencv/'
v = ntk.NTKVideos(videofilename, lstream)
v.grayscale_video(output_path)

# diff video
v.graydiff_video(output_path)
# diff image
v.graydiff_img(output_path)




# Make video from images
imgpath = '/home/user/img/'
videopath = '/home/user/img/out/'
videofilename = video1.avi
ntk.make_video_from_images(imgpath, videopath, videofilename,
                           imgext='.jpg', codec='XVID', v_fps=30)

```

# dlc
```
import neuraltoolkit as ntk
dlc_h5file = 'D17_trial1DeepCut_resnet50_crickethuntJul18shuffle1_15000.h5'
cutoff : cutoff based on confidence
pos, fnames = ntk.dlc_get_position(dlc_h5file, cutoff=0.6)
pos : contains x, y positions for all features
fnames : name of all features
# For example
pos
array([[357.29413831, 439.93870854, 482.14195955, ..., 159.27687836,
        469.79700255, 183.82241535],
       ...,
       [         nan,          nan,          nan, ...,          nan,
                 nan,          nan]])
fnames
['cricket', 'snout', 'tailbase', 'leftear', 'rightear']
```


## filters
#### List of functions
* butter_bandpass
* butter_highpass
* butter_lowpass
* welch_power
* notch_filter
```

# import libraries
import neuraltoolkit as ntk
import numpy as np
from matplotlib import pyplot as plt

# load raw data
rawdata = np.load('P_Headstages_64_Channels_int16_2018-11-15_14-30-49.npy')

# bandpass filter
help(ntk.butter_bandpass)
result = ntk.butter_bandpass(rawdata, 500, 4000, 25000, 3)

# Plot result
plt.plot(result[1,0:25000])
plt.show()
```

## high dimensional data
#### List of functions

```
# TSNE
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import neuraltoolkit as ntk
data = np.random.rand(800, 4)
# Please adjust parameters, according to data
# This is just an interface
u = ntk.highd_data_tsne(data, perplexity=30.0, n_components=2,
                        metric='euclidean', n_iter=3000,
                        verbose=True)
plt.scatter(u[:,0], u[:,1], c=data)

# UMAP
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns
import neuraltoolkit as ntk
data = np.random.rand(800, 4)
# Please adjust parameters, according to data
# This is just an interface
u = ntk.highd_data_umap(data, n_neighbors=40, n_components=2,
                        metric='euclidean', min_dist=0.2,
                        verbose=True)
plt.scatter(u[:,0], u[:,1], c=data)
```

## math
#### List of functions

```
# import libraries
import neuraltoolkit as ntk
import numpy as np
from matplotlib import pyplot as plt

# interpolate
t = np.arange(0, 10)
d = np.cos(t)
plt.figure(1)
plt.plot(t,d)
plt.show(block=False)
tn, d_tn = ntk.data_intpl(t, d, 4, intpl_kind='cubic')
plt.figure(2)
plt.plot(tn,d_tn)
plt.show(block=False)
```

#### Channel mappings
###### 'hs64'
      [26, 30, 6,  2,  18, 22, 14, 10, 12, 16, 8,  4,  28, 32, 24, 20, 
      48,  44, 36, 40, 64, 60, 52, 56, 54, 50, 42, 46, 62, 58, 34, 38, 
      39,  35, 59, 63, 47, 43, 51, 55, 53, 49, 57, 61, 37, 33, 41, 45, 
      17,  21, 29, 25, 1,  5 , 13, 9,  11, 15, 23, 19, 3,  7,  31, 27]
 
###### 'eibless-hs64_port32'
      [1,  5,  9,  13, 3,  7,  11, 15, 17, 21, 25, 29, 19, 23, 27, 31, 
      33,  37, 41, 45, 35, 39, 43, 47, 49, 53, 57, 61, 51, 55, 59, 63, 
      2,   6,  10, 14, 4,  8,  12, 16, 18, 22, 26, 30, 20, 24, 28, 32, 
      34,  38, 42, 46, 36, 40, 44, 48, 50, 54, 58, 62, 52, 56, 60, 64]
       
###### 'eibless-hs64_port64'
      [1,  5,  3,  7,  9,  13, 11, 15, 17, 21, 19, 23, 25, 29, 27, 31, 
      33,  37, 35, 39, 41, 45, 43, 47, 49, 53, 51, 55, 57, 61, 59, 63, 
      2,   6,  4,  8,  10, 14, 12, 16, 18, 22, 20, 24, 26, 30, 28, 32, 
      34,  38, 36, 40, 42, 46, 44, 48, 50, 54, 52, 56, 58, 62, 60, 64 ]
       
###### 'intan32'
      [25, 26, 27, 28, 29, 30, 31, 32, 1,  2,  3,  4,  5,  6,  7,  8, 
      24,  23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9]
       
###### 'Si_64_KS_chmap'
      [7,  45, 5,  56, 4,  48, 1,  62, 9,  53, 10, 42, 14, 59, 13, 39, 
      18,  49, 16, 36, 23, 44, 19, 33, 26, 40, 22, 30, 31, 35, 25, 27, 
      3,   51, 2,  63, 8,  64, 6,  61, 12, 60, 11, 57, 17, 58, 15, 54, 
      21,  55, 20, 52, 29, 50, 24, 46, 34, 43, 28, 41, 38, 47, 32, 37]
       
###### 'Si_64_KT_T1_K2_chmap'
      chan_map = ...
      [14, 59, 10, 42, 9,  53, 1,  62, 4,  48, 5,  56, 7,  45, 13, 39,  
      18,  49, 16, 36, 23, 44, 19, 33, 26, 40, 22, 30, 31, 35, 25, 27,  
      3,   51, 2,  63, 8,  64, 6,  61, 12, 60, 11, 57, 17, 58, 15, 54,  
      21,  55, 20, 52, 29, 50, 24, 46, 34, 43, 28, 41, 38, 47, 32, 37]
       
###### 'PCB_tetrode'
        [2, 41, 50, 62, 6, 39, 42, 47, 34, 44, 51, 56,  
        38, 48, 59, 64, 35, 53, 3, 37, 54, 57, 40, 43,  
        45, 61, 46, 49, 36, 33, 52, 55, 15, 5, 58, 60,  
        18, 9, 63, 1, 32, 14, 4, 7, 26, 20, 10, 13, 19, 
        22, 16, 8, 28, 25, 12, 17, 23, 29, 27, 21, 11, 31, 30, 24]
       
###### 'linear'
        [1:number_of_channels]
 
## sync
Functions to sync data across: raw neural, sync pulse, video files and frames, sleep state labels, and deep lab cut labels.

#### List of functions
* `map_video_to_neural_data` 
Maps video to neural data and optionally maps sleeps state and DLC labels. 
See the function documentation in `ntk_sync.py` for detailed documentation on the output format.
* `map_videoframes_to_syncpulse`
Reads a set of Camera Sync Pulse data files and aggregates the sequences of 000's and 111's into a map of video frame numbers to the raw neural data file and offset across all files in a recording. The output includes an entry per each sequence of 000's and 111's in the Camera Sync Pulse data.
See the function documentation in `ntk_sync.py` for detailed documentation on the output format.

#### Command line functionality
* `python ntk_sync.py --help` 
  Get command line help output.
* `python ntk_sync.py save_neural_files_bom [--output_filename FILENAME.csv] [[--neural_files NEURAL_FILENAMES_GLOB] --neural_files ...]` 
  Produces a CSV containing the eCube timestamps of a set of neural files which can be used instead of passing the neural files to the functions below (useful when the neural files are large and possibly difficult to access on demand).
* `python ntk_sync.py save_output_matrix --syncpulse_files FILENAME_GLOBS --video_files FILENAME_GLOBS --neural_files FILENAME_GLOBS [--sleepstate_files FILENAME_GLOBS] [--dlclabel_files FILENAME_GLOBS] [--output_filename map_video_to_neural_data.npz] [--fs 25000] [--n_channels 256] [--manual_video_frame_offset 0] [--recording_config EAB40.cfg]`
Calls save_output_matrix(...) which saves the results of map_video_to_neural_data(...) to a NPZ file.

```
import neuraltoolkit as ntk

# map_video_to_neural_data example usage:
output_matrix, video_files, neural_files, sleepstate_files, syncpulse_files, dlclabel_files = \
    ntk.map_video_to_neural_data(
        syncpulse_files='EAB40Data/EAB40_Camera_Sync_Pulse/*.bin'
        video_files=['EAB40Data/EAB40_Video/3_29-4_02/*.mp4',
                     'EAB40Data/EAB40_Video/4_02-4_05/*.mp4'],
        neural_files='EAB40Data/EAB40_Neural_Data/3_29-4_02/*.bin',
        dlclabel_files='EAB40Data/EAB40_DLC_Labels/*.h5'
        sleepstate_files='EAB40Data/EAB40_Sleep_States/*.npy'
    )

# map_videoframes_to_syncpulse example usage:
output_matrix, pulse_ix, files = ntk.map_videoframes_to_syncpulse('EAB40_Dataset/CameraSyncPulse/*.bin')
```
