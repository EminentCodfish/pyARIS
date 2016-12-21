# -*- coding: utf-8 -*-
"""
===================================================
Read ARIS files into python
===================================================

Insert stuff as needed.

"""

#Need to fix tmatrix
#Create ARIS file object
#Move the import procedure to a function
#Import file header data
#Import frame data

print __doc__

import struct, array
import numpy as np
import matplotlib.pyplot as plt

#Import open file
filename = 'C:/Coding_Projects/PyARIS/2013-12-06_132430.aris'
data = open(filename, 'rb')

#Start reading file header
version_number      = struct.unpack('I', data.read(4))[0] #File format version DDF_05 = 0x05464444
#OBSOLETE: Calculate the number of frames from file size & beams*samples.
FrameCount          = struct.unpack('I', data.read(4))[0] #Total frames in file
#OBSOLETE: See frame header instead.
FrameRate           = struct.unpack('I', data.read(4))[0] #Initial recorded frame rate
#OBSOLETE: See frame header instead.
HighResolution      = struct.unpack('I', data.read(4))[0] #Non-zero if HF, zero if LF
#OBSOLETE: See frame header instead.
NumRawBeams         = struct.unpack('I', data.read(4))[0] #ARIS 3000 = 128/64, ARIS 1800 = 96/48, ARIS 1200 = 48
#OBSOLETE: See frame header instead.
SampleRate          = struct.unpack('f', data.read(4))[0] #1/Sample Period
#OBSOLETE: See frame header instead.
SamplesPerChannel   = struct.unpack('I', data.read(4))[0] #Number of range samples in each beam
#OBSOLETE: See frame header instead.
ReceiverGain        = struct.unpack('I', data.read(4))[0] #Relative gain in dB:  0 - 40
#OBSOLETE: See frame header instead.
WindowStart         = struct.unpack('f', data.read(4))[0] #Image window start range in meters (code [0..31] in DIDSON)
#OBSOLETE: See frame header instead.
WindowLength        = struct.unpack('f', data.read(4))[0] #Image window length in meters  (code [0..3] in DIDSON)
#OBSOLETE: See frame header instead.
Reverse             = struct.unpack('I', data.read(4))[0] #Non-zero = lens down (DIDSON) or lens up (ARIS), zero = opposite
SN                  = struct.unpack('I', data.read(4))[0] #Sonar serial number
strDate             = struct.unpack('32s', data.read(32))[0] #Date that file was recorded
strHeaderID         = struct.unpack('256s', data.read(256))[0] #User input to identify file in 256 characters
UserID1             = struct.unpack('i', data.read(4))[0] #User-defined integer quantity
UserID2             = struct.unpack('i', data.read(4))[0] #User-defined integer quantity
UserID3             = struct.unpack('i', data.read(4))[0] #User-defined integer quantity
UserID4             = struct.unpack('i', data.read(4))[0] #User-defined integer quantity
StartFrame          = struct.unpack('I', data.read(4))[0] #First frame number from source file (for DIDSON snippet files)
EndFrame            = struct.unpack('I', data.read(4))[0] #Last frame number from source file (for DIDSON snippet files)
TimeLapse           = struct.unpack('I', data.read(4))[0] #Non-zero indicates time lapse recording
RecordInterval      = struct.unpack('I', data.read(4))[0] #Number of frames/seconds between recorded frames
RadioSeconds        = struct.unpack('I', data.read(4))[0] #Frames or seconds interval
FrameInterval       = struct.unpack('I', data.read(4))[0] #Record every Nth frame
Flags               = struct.unpack('I', data.read(4))[0] #See DDF_04 file format document (OBSOLETE)
AuxFlags            = struct.unpack('I', data.read(4))[0] #See DDF_04 file format document
#OBSOLETE: See frame header instead.
Sspd                = struct.unpack('I', data.read(4))[0] #Sound velocity in water
Flags3D             = struct.unpack('I', data.read(4))[0] #See DDF_04 file format document
SoftwareVersion     = struct.unpack('I', data.read(4))[0] #DIDSON software version that recorded the file
WaterTemp           = struct.unpack('I', data.read(4))[0] #Water temperature code:  0 = 5-15C, 1 = 15-25C, 2 = 25-35C
Salinity            = struct.unpack('I', data.read(4))[0] #Salinity code:  0 = fresh, 1 = brackish, 2 = salt
PulseLength         = struct.unpack('I', data.read(4))[0] #Added for ARIS but not used
TxMode              = struct.unpack('I', data.read(4))[0] #Added for ARIS but not used
VersionFGPA         = struct.unpack('I', data.read(4))[0] #Reserved for future use
VersionPSuC         = struct.unpack('I', data.read(4))[0] #Reserved for future use
ThumbnailFI         = struct.unpack('I', data.read(4))[0] #Frame index of frame used for thumbnail image of file
#OBSOLETE: Do not use; query your filesystem instead.
FileSize            = struct.unpack('Q', data.read(8))[0] #Total file size in bytes
OptionalHeaderSize  = struct.unpack('Q', data.read(8))[0] #Reserved for future use (Obsolete, not used)
OptionalTailSize    = struct.unpack('Q', data.read(8))[0] #Reserved for future use (Obsolete, not used)
VersionMinor        = struct.unpack('I', data.read(4))[0] #DIDSON_ADJUSTED_VERSION_MINOR (Obsolete)
#OBSOLETE: See frame header instead.
LargeLens           = struct.unpack('I', data.read(4))[0] #Non-zero if telephoto lens (large lens, hi-res lens, big lens) is present


#Start reading frame header
data.seek(1024, 0)
frameindex          = struct.unpack('I', data.read(4))[0] #Frame number in file
frametime           = struct.unpack('Q', data.read(8))[0] #PC time stamp when recorded; microseconds since epoch (Jan 1st 1970)
version             = struct.unpack('I', data.read(4))[0] #ARIS file format version = 0x05464444
status              = struct.unpack('I', data.read(4))[0]
sonartimestamp      = struct.unpack('Q', data.read(8))[0] #On-sonar microseconds since epoch (Jan 1st 1970)
tsday               = struct.unpack('I', data.read(4))[0]
tshour              = struct.unpack('I', data.read(4))[0]
tsminute            = struct.unpack('I', data.read(4))[0]
tssecond            = struct.unpack('I', data.read(4))[0]
tshsecond           = struct.unpack('I', data.read(4))[0]
transmitmode        = struct.unpack('I', data.read(4))[0]
windowstart         = struct.unpack('f', data.read(4))[0] #Window start in meters
windowlength        = struct.unpack('f', data.read(4))[0] #Window length in meters
threshold           = struct.unpack('I', data.read(4))[0]
intensity           = struct.unpack('i', data.read(4))[0]
receivergain        = struct.unpack('I', data.read(4))[0] #Note: 0-24 dB
degc1               = struct.unpack('I', data.read(4))[0] #CPU temperature (C)
degc2               = struct.unpack('I', data.read(4))[0] #Power supply temperature (C)
humidity            = struct.unpack('I', data.read(4))[0] #% relative humidity
focus               = struct.unpack('I', data.read(4))[0] #Focus units 0-1000
battery             = struct.unpack('I', data.read(4))[0] #OBSOLETE: Unused.
uservalue1          = struct.unpack('f', data.read(4))[0]
uservalue2          = struct.unpack('f', data.read(4))[0] 
uservalue3          = struct.unpack('f', data.read(4))[0] 
uservalue4          = struct.unpack('f', data.read(4))[0] 
uservalue5          = struct.unpack('f', data.read(4))[0] 
uservalue6          = struct.unpack('f', data.read(4))[0] 
uservalue7          = struct.unpack('f', data.read(4))[0]
uservalue8          = struct.unpack('f', data.read(4))[0] 
velocity            = struct.unpack('f', data.read(4))[0] # Platform velocity from AUV integration
depth               = struct.unpack('f', data.read(4))[0] # Platform depth from AUV integration
altitude            = struct.unpack('f', data.read(4))[0] # Platform altitude from AUV integration
pitch               = struct.unpack('f', data.read(4))[0] # Platform pitch from AUV integration
pitchrate           = struct.unpack('f', data.read(4))[0] # Platform pitch rate from AUV integration
roll                = struct.unpack('f', data.read(4))[0] # Platform roll from AUV integration
rollrate            = struct.unpack('f', data.read(4))[0] # Platform roll rate from AUV integration
heading             = struct.unpack('f', data.read(4))[0] # Platform heading from AUV integration
headingrate         = struct.unpack('f', data.read(4))[0] # Platform heading rate from AUV integration
compassheading      = struct.unpack('f', data.read(4))[0] # Sonar compass heading output
compasspitch        = struct.unpack('f', data.read(4))[0] # Sonar compass pitch output
compassroll         = struct.unpack('f', data.read(4))[0] # Sonar compass roll output
latitude            = struct.unpack('d', data.read(8))[0] # from auxiliary GPS sensor
longitude           = struct.unpack('d', data.read(8))[0] # from auxiliary GPS sensor
sonarposition       = struct.unpack('f', data.read(4))[0] # special for PNNL
configflags         = struct.unpack('I', data.read(4))[0] 
beamtilt            = struct.unpack('f', data.read(4))[0]  
targetrange         = struct.unpack('f', data.read(4))[0]  
targetbearing       = struct.unpack('f', data.read(4))[0] 
targetpresent       = struct.unpack('I', data.read(4))[0] 
firmwarerevision    = struct.unpack('I', data.read(4))[0] #OBSOLETE: Unused.
flags               = struct.unpack('I', data.read(4))[0] 
sourceframe         = struct.unpack('I', data.read(4))[0] # Source file frame number for CSOT output files
watertemp           = struct.unpack('f', data.read(4))[0] # Water temperature from housing temperature sensor
timerperiod         = struct.unpack('I', data.read(4))[0] 
sonarx              = struct.unpack('f', data.read(4))[0] # Sonar X location for 3D processing
sonary              = struct.unpack('f', data.read(4))[0] # Sonar Y location for 3D processing
sonarz              = struct.unpack('f', data.read(4))[0] # Sonar Z location for 3D processing
sonarpan            = struct.unpack('f', data.read(4))[0] # X2 pan output
sonartilt           = struct.unpack('f', data.read(4))[0] # X2 tilt output
sonarroll           = struct.unpack('f', data.read(4))[0] # X2 roll output                                                                                                                       **** End of DDF_03 frame header data ****
panpnnl             = struct.unpack('f', data.read(4))[0]
tiltpnnl            = struct.unpack('f', data.read(4))[0] 
rollpnnl            = struct.unpack('f', data.read(4))[0] 
vehicletime         = struct.unpack('d', data.read(8))[0] # special for Bluefin Robotics HAUV or other AUV integration
timeggk             = struct.unpack('f', data.read(4))[0] # GPS output from NMEA GGK message
dateggk             = struct.unpack('I', data.read(4))[0] # GPS output from NMEA GGK message
qualityggk          = struct.unpack('I', data.read(4))[0] # GPS output from NMEA GGK message
numsatsggk          = struct.unpack('I', data.read(4))[0] # GPS output from NMEA GGK message
dopggk              = struct.unpack('f', data.read(4))[0] # GPS output from NMEA GGK message
ehtggk              = struct.unpack('f', data.read(4))[0] # GPS output from NMEA GGK message
heavetss            = struct.unpack('f', data.read(4))[0] # external sensor
yeargps             = struct.unpack('I', data.read(4))[0] # GPS year output
monthgps            = struct.unpack('I', data.read(4))[0] # GPS month output
daygps              = struct.unpack('I', data.read(4))[0] # GPS day output
hourgps             = struct.unpack('I', data.read(4))[0] # GPS hour output
minutegps           = struct.unpack('I', data.read(4))[0] # GPS minute output
secondgps           = struct.unpack('I', data.read(4))[0] # GPS second output
hsecondgps          = struct.unpack('I', data.read(4))[0] # GPS 1/100th second output
sonarpanoffset      = struct.unpack('f', data.read(4))[0] # Sonar mount location pan offset for 3D processing
sonartiltoffset     = struct.unpack('f', data.read(4))[0] # Sonar mount location tilt offset for 3D processing
sonarrolloffset     = struct.unpack('f', data.read(4))[0] # Sonar mount location roll offset for 3D processing
sonarxoffset        = struct.unpack('f', data.read(4))[0] # Sonar mount location X offset for 3D processing
sonaryoffset        = struct.unpack('f', data.read(4))[0] # Sonar mount location Y offset for 3D processing
sonarzoffset        = struct.unpack('f', data.read(4))[0] # Sonar mount location Z offset for 3D processing
tmatrix = array.array('f')                                # 3D processing transformation matrix
for i in range(16):
    tmatrix.append(struct.unpack('f', data.read(4))[0])
samplerate          = struct.unpack('f', data.read(4))[0] # Calculated as 1e6/SamplePeriod
accellx             = struct.unpack('f', data.read(4))[0] # X-axis sonar acceleration
accelly             = struct.unpack('f', data.read(4))[0] # Y-axis sonar acceleration
accellz             = struct.unpack('f', data.read(4))[0] # Z-axis sonar acceleration
pingmode            = struct.unpack('I', data.read(4))[0] # ARIS ping mode [1..12]
frequencyhilow      = struct.unpack('I', data.read(4))[0] # 1 = HF, 0 = LF
pulsewidth          = struct.unpack('I', data.read(4))[0] # Width of transmit pulse in usec, [4..100]
cycleperiod         = struct.unpack('I', data.read(4))[0] # Ping cycle time in usec, [1802..65535]
sampleperiod        = struct.unpack('I', data.read(4))[0] # Downrange sample rate in usec, [4..100]
transmitenable      = struct.unpack('I', data.read(4))[0] # 1 = Transmit ON, 0 = Transmit OFF
framerate           = struct.unpack('f', data.read(4))[0] # Instantaneous frame rate between frame N and frame N-1
soundspeed          = struct.unpack('f', data.read(4))[0] # Sound velocity in water calculated from water temperature and salinity setting
samplesperbeam      = struct.unpack('I', data.read(4))[0] # Number of downrange samples in each beam
enable150v          = struct.unpack('I', data.read(4))[0] # 1 = 150V ON (Max Power), 0 = 150V OFF (Min Power, 12V)
samplestartdelay    = struct.unpack('I', data.read(4))[0] # Delay from transmit until start of sampling (window start) in usec, [930..65535]
largelens           = struct.unpack('I', data.read(4))[0] # 1 = telephoto lens (large lens, big lens, hi-res lens) present
thesystemtype       = struct.unpack('I', data.read(4))[0] # 1 = ARIS 3000, 0 = ARIS 1800, 2 = ARIS 1200
sonarserialnumber   = struct.unpack('I', data.read(4))[0] # Sonar serial number as labeled on housing
encryptedkey        = struct.unpack('Q', data.read(8))[0] # Reserved for future use
ariserrorflagsuint  = struct.unpack('I', data.read(4))[0] # Error flag code bits
missedpackets       = struct.unpack('I', data.read(4))[0] # Missed packet count for Ethernet statistics reporting
arisappversion      = struct.unpack('I', data.read(4))[0] # Version number of ArisApp sending frame data
available2          = struct.unpack('I', data.read(4))[0] # Reserved for future use
reorderedsamples    = struct.unpack('I', data.read(4))[0] # 1 = frame data already ordered into [beam,sample] array, 0 = needs reordering
salinity            = struct.unpack('I', data.read(4))[0] # Water salinity code:  0 = fresh, 15 = brackish, 35 = salt
pressure            = struct.unpack('f', data.read(4))[0] # Depth sensor output in meters (psi)
batteryvoltage      = struct.unpack('f', data.read(4))[0] # Battery input voltage before power steering
mainvoltage         = struct.unpack('f', data.read(4))[0] # Main cable input voltage before power steering
switchvoltage       = struct.unpack('f', data.read(4))[0] # Input voltage after power steering
focusmotormoving    = struct.unpack('I', data.read(4))[0] # Added 14-Aug-2012 for AutomaticRecording
voltagechanging     = struct.unpack('I', data.read(4))[0] # Added 16-Aug (first two bits = 12V, second two bits = 150V, 00 = not changing, 01 = turning on, 10 = turning off)
focustimeoutfault   = struct.unpack('I', data.read(4))[0]  
focusovercurrentfault = struct.unpack('I', data.read(4))[0] 
focusnotfoundfault  = struct.unpack('I', data.read(4))[0] 
focusstalledfault   = struct.unpack('I', data.read(4))[0]  
fpgatimeoutfault    = struct.unpack('I', data.read(4))[0]
fpgabusyfault       = struct.unpack('I', data.read(4))[0]  
fpgastuckfault      = struct.unpack('I', data.read(4))[0]  
cputempfault        = struct.unpack('I', data.read(4))[0]  
psutempfault        = struct.unpack('I', data.read(4))[0]  
watertempfault      = struct.unpack('I', data.read(4))[0]  
humidityfault       = struct.unpack('I', data.read(4))[0]  
pressurefault       = struct.unpack('I', data.read(4))[0]  
voltagereadfault    = struct.unpack('I', data.read(4))[0] 
voltagewritefault   = struct.unpack('I', data.read(4))[0] 
focuscurrentposition = struct.unpack('I', data.read(4))[0] # Focus shaft current position in motor units [0.1000]
targetpan           = struct.unpack('f', data.read(4))[0] # Commanded pan position
targettilt          = struct.unpack('f', data.read(4))[0] # Commanded tilt position
targetroll          = struct.unpack('f', data.read(4))[0] # Commanded roll position
panmotorerrorcode   = struct.unpack('I', data.read(4))[0]
tiltmotorerrorcode  = struct.unpack('I', data.read(4))[0]
rollmotorerrorcode  = struct.unpack('I', data.read(4))[0]
panabsposition      = struct.unpack('f', data.read(4))[0] # Low-resolution magnetic encoder absolute pan position
tiltabsposition     = struct.unpack('f', data.read(4))[0] # Low-resolution magnetic encoder absolute tilt position
rollabsposition     = struct.unpack('f', data.read(4))[0] # Low-resolution magnetic encoder absolute roll position
panaccelx           = struct.unpack('f', data.read(4))[0] # Accelerometer outputs from AR2 CPU board sensor
panaccely           = struct.unpack('f', data.read(4))[0] 
panaccelz           = struct.unpack('f', data.read(4))[0] 
tiltaccelx          = struct.unpack('f', data.read(4))[0] 
tiltaccely          = struct.unpack('f', data.read(4))[0] 
tiltaccelz          = struct.unpack('f', data.read(4))[0] 
rollaccelx          = struct.unpack('f', data.read(4))[0] 
rollaccely          = struct.unpack('f', data.read(4))[0] 
rollaccelz          = struct.unpack('f', data.read(4))[0]
appliedsettings     = struct.unpack('I', data.read(4))[0] # Cookie indices for command acknowlege in frame header
constrainedsettings = struct.unpack('I', data.read(4))[0] 
invalidsettings     = struct.unpack('I', data.read(4))[0] 
enableinterpacketdelay = struct.unpack('I', data.read(4))[0] # If true delay is added between sending out image data packets
interpacketdelayperiod = struct.unpack('I', data.read(4))[0] # packet delay factor in us (does not include function overhead time)
uptime              = struct.unpack('I', data.read(4))[0] # Total number of seconds sonar has been running
arisappversionmajor = struct.unpack('H', data.read(2))[0] # Major version number
arisappversionminor = struct.unpack('H', data.read(2))[0] # Minor version number 
gotime              = struct.unpack('Q', data.read(8))[0] # Sonar time when frame cycle is initiated in hardware
panvelocity         = struct.unpack('f', data.read(4))[0] # AR2 pan velocity in degrees/second
tiltvelocity        = struct.unpack('f', data.read(4))[0] # AR2 tilt velocity in degrees/second
rollvelocity        = struct.unpack('f', data.read(4))[0] # AR2 roll velocity in degrees/second
sentinel            = struct.unpack('I', data.read(4))[0] # Used to measure the frame header size

FI = frameindex
if pingmode == 9:
    BeamCount = 128
FrameSize = BeamCount*samplesperbeam
frameoffset = (1024+(FI*(1024+(FrameSize))))

data.seek(frameoffset+1024, 0)
frame = np.empty([samplesperbeam, BeamCount], dtype=int)
for r in range(len(frame)):
    for c in range(len(frame[r])):
        frame[r][c] = struct.unpack('B', data.read(1))[0]
frame = np.fliplr(frame)
      
x_factor = 6

for x in range(0,BeamCount*x_factor,x_factor):
    for y in range(x_factor-1):
        frame = np.insert(frame, x, frame[:,(x+y)], axis=1)

plt.imshow(frame, origin = "lower")
plt.show()


#Start reading frame header
data.seek(frameoffset, 0)
frameindex          = struct.unpack('I', data.read(4))[0] #Frame number in file
frametime           = struct.unpack('Q', data.read(8))[0] #PC time stamp when recorded; microseconds since epoch (Jan 1st 1970)
version             = struct.unpack('I', data.read(4))[0] #ARIS file format version = 0x05464444
status              = struct.unpack('I', data.read(4))[0]
sonartimestamp      = struct.unpack('Q', data.read(8))[0] #On-sonar microseconds since epoch (Jan 1st 1970)