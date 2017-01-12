# -*- coding: utf-8 -*-
"""
===================================================
Read ARIS files into python
===================================================

Last modified on: December 20, 2016

@author: Rillahan
"""
import struct, array, pytz, datetime
import numpy as np
import beamLookUp

print __doc__

class ARIS_File:
    'This is a class container for the ARIS file headers'
    
    def __init__(self, filename, version_number, FrameCount, FrameRate, HighResolution, NumRawBeams, SampleRate, SamplesPerChannel, ReceiverGain,
                 WindowStart, WindowLength, Reverse, SN, strDate, strHeaderID, UserID1, UserID2, UserID3, UserID4, StartFrame,EndFrame, 
                 TimeLapse, RecordInterval, RadioSeconds, FrameInterval, Flags, AuxFlags, Sspd, Flags3D, SoftwareVersion, WaterTemp,
                 Salinity, PulseLength, TxMode, VersionFGPA, VersionPSuC, ThumbnailFI, FileSize, OptionalHeaderSize, OptionalTailSize, 
                 VersionMinor, LargeLens):
                     self.filename = filename #Name of the ARIS file
                     self.version_number = version_number #File format version DDF_05 = 0x05464444
                     #OBSOLETE: Calculate the number of frames from file size & beams*samples.
                     self.FrameCount = FrameCount #Total frames in file
                     #OBSOLETE: See frame header instead.
                     self.FrameRate = FrameRate #Initial recorded frame rate 
                     #OBSOLETE: See frame header instead.
                     self.HighResolution = HighResolution #Non-zero if HF, zero if LF
                     #OBSOLETE: See frame header instead.
                     self.NumRawBeams = NumRawBeams #ARIS 3000 = 128/64, ARIS 1800 = 96/48, ARIS 1200 = 48
                     #OBSOLETE: See frame header instead.
                     self.SampleRate = SampleRate #1/Sample Period
                     #OBSOLETE: See frame header instead.
                     self.SamplesPerChannel = SamplesPerChannel #Number of range samples in each beam
                     #OBSOLETE: See frame header instead.
                     self.ReceiverGain = ReceiverGain #Relative gain in dB:  0 - 40
                     #OBSOLETE: See frame header instead.
                     self.WindowStart = WindowStart #Image window start range in meters (code [0..31] in DIDSON)
                     #OBSOLETE: See frame header instead.
                     self.WindowLength = WindowLength #Image window length in meters  (code [0..3] in DIDSON)
                     #OBSOLETE: See frame header instead.
                     self.Reverse = Reverse #Non-zero = lens down (DIDSON) or lens up (ARIS), zero = opposite
                     self.SN = SN  #Sonar serial number
                     self.strDate = strDate #Date that file was recorded
                     self.strHeaderID = strHeaderID #User input to identify file in 256 characters
                     self.UserID1 = UserID1 #User-defined integer quantity
                     self.UserID2 = UserID2 #User-defined integer quantity
                     self.UserID3 = UserID3 #User-defined integer quantity
                     self.UserID4 = UserID4 #User-defined integer quantity
                     self.StartFrame = StartFrame #First frame number from source file (for DIDSON snippet files)
                     self.EndFrame = EndFrame #Last frame number from source file (for DIDSON snippet files) 
                     self.TimeLapse = TimeLapse #Non-zero indicates time lapse recording
                     self.RecordInterval = RecordInterval #Number of frames/seconds between recorded frames
                     self.RadioSeconds = RadioSeconds #Frames or seconds interval
                     self.FrameInterval = FrameInterval #Record every Nth frame
                     self.Flags = Flags #See DDF_04 file format document (OBSOLETE)
                     self.AuxFlags = AuxFlags #See DDF_04 file format document
                     #OBSOLETE: See frame header instead.
                     self.Sspd = Sspd #Sound velocity in water
                     self.Flags3D = Flags3D #See DDF_04 file format document
                     self.SoftwareVersion = SoftwareVersion #DIDSON software version that recorded the file
                     self.WaterTemp = WaterTemp #Water temperature code:  0 = 5-15C, 1 = 15-25C, 2 = 25-35C
                     self.Salinity = Salinity #Salinity code:  0 = fresh, 1 = brackish, 2 = salt
                     self.PulseLength = PulseLength #Added for ARIS but not used
                     self.TxMode = TxMode #Added for ARIS but not used
                     self.VersionFGPA = VersionFGPA #Reserved for future use
                     self.VersionPSuC = VersionPSuC #Reserved for future use
                     self.ThumbnailFI = ThumbnailFI #Frame index of frame used for thumbnail image of file
                     #OBSOLETE: Do not use; query your filesystem instead.
                     self.FileSize = FileSize #Total file size in bytes
                     self.OptionalHeaderSize = OptionalHeaderSize#Reserved for future use (Obsolete, not used)
                     self.OptionalTailSize = OptionalTailSize #Reserved for future use (Obsolete, not used)
                     self.VersionMinor = VersionMinor #DIDSON_ADJUSTED_VERSION_MINOR (Obsolete)
                     self.LargeLens = LargeLens #Non-zero if telephoto lens (large lens, hi-res lens, big lens) is present
                     
    def __len__(self):
         return self.FrameCount
        
    def __repr__(self):
        return 'ARIS File: ' + self.filename
        
    def info(self):
        print('Filename: ' + str(self.filename))
        print('Software Version: ' + str(self.SoftwareVersion))
        print('ARIS S/N: ' + str(self.SN))
        print('File size: ' + str(self.FileSize))
        print('Number of Frames: ' + str(self.FrameCount))
        print('Beam Count: ' + str(self.NumRawBeams))
        print('Samples/Beam: ' + str(self.SamplesPerChannel))

class ARIS_Frame(ARIS_File):
    'This is a class container for the ARIS frame data' 

    def __init__(self, frameindex, frametime, version, status, sonartimestamp, tsday, tshour, tsminute, tssecond, tshsecond, transmitmode,
                 windowstart, windowlength, threshold, intensity, receivergain, degc1, degc2, humidity, focus, battery, uservalue1, uservalue2, 
                 uservalue3,  uservalue4,  uservalue5, uservalue6, uservalue7, uservalue8,  velocity, depth, altitude, pitch, pitchrate, roll,
                 rollrate, heading, headingrate, compassheading, compasspitch, compassroll, latitude, longitude, sonarposition, configflags, 
                 beamtilt, targetrange, targetbearing, targetpresent, firmwarerevision, flags, sourceframe, watertemp, timerperiod, sonarx,
                 sonary, sonarz, sonarpan, sonartilt, sonarroll, panpnnl, tiltpnnl, rollpnnl, vehicletime, timeggk, dateggk, qualityggk, numsatsggk,
                 dopggk, ehtggk, heavetss, yeargps, monthgps, daygps, hourgps, minutegps, secondgps, hsecondgps, sonarpanoffset, sonartiltoffset,
                 sonarrolloffset, sonarxoffset, sonaryoffset, sonarzoffset, tmatrix, samplerate, accellx, accelly, accellz, pingmode, frequencyhilow,
                 pulsewidth, cycleperiod, sampleperiod, transmitenable, framerate, soundspeed, samplesperbeam, enable150v, samplestartdelay, largelens,
                 thesystemtype, sonarserialnumber, encryptedkey, ariserrorflagsuint, missedpackets, arisappversion, available2, reorderedsamples,
                 salinity, pressure, batteryvoltage, mainvoltage, switchvoltage, focusmotormoving, voltagechanging, focustimeoutfault, focusovercurrentfault, 
                 focusnotfoundfault, focusstalledfault, fpgatimeoutfault, fpgabusyfault, fpgastuckfault, cputempfault, psutempfault, watertempfault, 
                 humidityfault, pressurefault, voltagereadfault, voltagewritefault, focuscurrentposition, targetpan, targettilt, targetroll, panmotorerrorcode,
                 tiltmotorerrorcode, rollmotorerrorcode, panabsposition, tiltabsposition, rollabsposition, panaccelx, panaccely, panaccelz, tiltaccelx, 
                 tiltaccely, tiltaccelz, rollaccelx, rollaccely, rollaccelz, appliedsettings, constrainedsettings, invalidsettings, enableinterpacketdelay,
                 interpacketdelayperiod, uptime, arisappversionmajor, arisappversionminor, gotime, panvelocity, tiltvelocity, rollvelocity, sentinel):

                    self.frameindex = frameindex #Frame number in file
                    self.frametime = frametime #PC time stamp when recorded; microseconds since epoch (Jan 1st 1970)
                    self.version = version #ARIS file format version = 0x05464444
                    self.status = status
                    self.sonartimestamp = sonartimestamp #On-sonar microseconds since epoch (Jan 1st 1970)
                    self.tsday = tsday
                    self.tshour = tshour
                    self.tsminute = tsminute
                    self.tssecond = tssecond
                    self.tshsecond = tshsecond
                    self.transmitmode = transmitmode
                    self.windowstart = windowstart #Window start in meters
                    self.windowlength = windowlength #Window length in meters
                    self.threshold = threshold
                    self.intensity = intensity
                    self.receivergain = receivergain #Note: 0-24 dB
                    self.degc1 = degc1 #CPU temperature (C)
                    self.degc2 = degc2 #Power supply temperature (C)
                    self.humidity = humidity #% relative humidity
                    self.focus = focus #Focus units 0-1000
                    self.battery = battery #OBSOLETE: Unused.
                    self.uservalue1 = uservalue1
                    self.uservalue2 = uservalue2
                    self.uservalue3 = uservalue3
                    self.uservalue4 = uservalue4 
                    self.uservalue5 = uservalue5 
                    self.uservalue6 = uservalue6 
                    self.uservalue7 = uservalue7
                    self.uservalue8 = uservalue8 
                    self.velocity = velocity # Platform velocity from AUV integration
                    self.depth = depth # Platform depth from AUV integration
                    self.altitude = altitude # Platform altitude from AUV integration
                    self.pitch = pitch # Platform pitch from AUV integration
                    self.pitchrate = pitchrate # Platform pitch rate from AUV integration
                    self.roll = roll # Platform roll from AUV integration
                    self.rollrate = rollrate # Platform roll rate from AUV integration
                    self.heading = heading # Platform heading from AUV integration
                    self.headingrate = headingrate # Platform heading rate from AUV integration
                    self.compassheading = compassheading # Sonar compass heading output
                    self.compasspitch = compasspitch # Sonar compass pitch output
                    self.compassroll = compassroll # Sonar compass roll output
                    self.latitude = latitude # from auxiliary GPS sensor
                    self.longitude = longitude # from auxiliary GPS sensor
                    self.sonarposition = sonarposition # special for PNNL
                    self.configflags = configflags 
                    self.beamtilt = beamtilt  
                    self.targetrange = targetrange  
                    self.targetbearing = targetbearing
                    self.targetpresent = targetpresent
                    self.firmwarerevision = firmwarerevision #OBSOLETE: Unused.
                    self.flags = flags
                    self.sourceframe = sourceframe # Source file frame number for CSOT output files
                    self.watertemp = watertemp # Water temperature from housing temperature sensor
                    self.timerperiod = timerperiod 
                    self.sonarx = sonarx # Sonar X location for 3D processing
                    self.sonary = sonary # Sonar Y location for 3D processing
                    self.sonayz = sonarz # Sonar Z location for 3D processing
                    self.sonarpan = sonarpan # X2 pan output
                    self.sonartilt = sonartilt # X2 tilt output
                    self.sonarroll = sonarroll # X2 roll output                                                                                                                       **** End of DDF_03 frame header data ****
                    self.panpnnl = panpnnl
                    self.tiltpnnl = tiltpnnl 
                    self.rollpnnl = rollpnnl 
                    self.vehicletime = vehicletime # special for Bluefin Robotics HAUV or other AUV integration
                    self.timeggk = timeggk # GPS output from NMEA GGK message
                    self.dateggk = dateggk # GPS output from NMEA GGK message
                    self.qualityggk = qualityggk # GPS output from NMEA GGK message
                    self.numsatsggk = numsatsggk # GPS output from NMEA GGK message
                    self.dopggk = dopggk # GPS output from NMEA GGK message
                    self.ehtggk = ehtggk # GPS output from NMEA GGK message
                    self.heavetss = heavetss # external sensor
                    self.yeargps = yeargps # GPS year output
                    self.monthgps = monthgps # GPS month output
                    self.daygps = daygps # GPS day output
                    self.hourgps = hourgps # GPS hour output
                    self.minutegps = minutegps # GPS minute output
                    self.secondgps = secondgps # GPS second output
                    self.hsecondgps = hsecondgps # GPS 1/100th second output
                    self.sonarpanoffset = sonarpanoffset # Sonar mount location pan offset for 3D processing
                    self.sonartiltoffset = sonartiltoffset # Sonar mount location tilt offset for 3D processing
                    self.sonarrolloffset = sonarrolloffset # Sonar mount location roll offset for 3D processing
                    self.sonarxoffset = sonarxoffset # Sonar mount location X offset for 3D processing
                    self.sonaryoffset = sonaryoffset # Sonar mount location Y offset for 3D processing
                    self.sonarzoffset = sonarzoffset # Sonar mount location Z offset for 3D processing
                    self.tmatirx = tmatrix # 3D processing transformation matrix
                    self.samplerate = samplerate # Calculated as 1e6/SamplePeriod
                    self.accellx = accellx # X-axis sonar acceleration
                    self.accelly = accelly # Y-axis sonar acceleration
                    self.accellz = accellz # Z-axis sonar acceleration
                    self.pingmode = pingmode # ARIS ping mode [1..12]
                    self.frequencyhilow = frequencyhilow # 1 = HF, 0 = LF
                    self.pulsewidth = pulsewidth # Width of transmit pulse in usec, [4..100]
                    self.cycleperiod = cycleperiod # Ping cycle time in usec, [1802..65535]
                    self.sampleperiod = sampleperiod # Downrange sample rate in usec, [4..100]
                    self.tranmitenable = transmitenable # 1 = Transmit ON, 0 = Transmit OFF
                    self.framerate = framerate # Instantaneous frame rate between frame N and frame N-1
                    self.soundspeed = soundspeed # Sound velocity in water calculated from water temperature and salinity setting
                    self.samplesperbeam = samplesperbeam # Number of downrange samples in each beam
                    self.enable150v = enable150v # 1 = 150V ON (Max Power), 0 = 150V OFF (Min Power, 12V)
                    self.samplestartdelay = samplestartdelay # Delay from transmit until start of sampling (window start) in usec, [930..65535]
                    self.largelens = largelens # 1 = telephoto lens (large lens, big lens, hi-res lens) present
                    self.thesystemtype = thesystemtype # 1 = ARIS 3000, 0 = ARIS 1800, 2 = ARIS 1200
                    self.sonarserialnumber = sonarserialnumber # Sonar serial number as labeled on housing
                    self.encryptedkey = encryptedkey # Reserved for future use
                    self.ariserrorflagsuint = ariserrorflagsuint # Error flag code bits
                    self.missedpackets = missedpackets # Missed packet count for Ethernet statistics reporting
                    self.arisappversion = arisappversion # Version number of ArisApp sending frame data
                    self.available2 = available2 # Reserved for future use
                    self.reorderedsamples = reorderedsamples # 1 = frame data already ordered into [beam,sample] array, 0 = needs reordering
                    self.salinity = salinity # Water salinity code:  0 = fresh, 15 = brackish, 35 = salt
                    self.pressure = pressure # Depth sensor output in meters (psi)
                    self.batteryvoltage = batteryvoltage # Battery input voltage before power steering
                    self.mainvoltage = mainvoltage # Main cable input voltage before power steering
                    self.switchvoltage = switchvoltage # Input voltage after power steering
                    self.focusmotormoving = focusmotormoving # Added 14-Aug-2012 for AutomaticRecording
                    self.voltagechanging = voltagechanging # Added 16-Aug (first two bits = 12V, second two bits = 150V, 00 = not changing, 01 = turning on, 10 = turning off)
                    self.focustimeoutfault = focustimeoutfault 
                    self.focusovercurrentfault = focusovercurrentfault
                    self.focusnotfoundfault = focusnotfoundfault
                    self.focusstalledfault = focusstalledfault
                    self.fpgatimeoutfault = fpgatimeoutfault
                    self.fpgabusyfault = fpgabusyfault 
                    self.fpgastuckfault = fpgastuckfault
                    self.cputempfault = cputempfault
                    self.psutempfault = psutempfault
                    self.watertempfault = watertempfault
                    self.humidityfault = humidityfault 
                    self.pressurefault = pressurefault 
                    self.voltagereadfault = voltagereadfault
                    self.voltagewritefault = voltagewritefault 
                    self.focuscurrentposition = focuscurrentposition # Focus shaft current position in motor units [0.1000]
                    self.targetpan = targetpan # Commanded pan position
                    self.targettilt = targettilt # Commanded tilt position
                    self.targetroll = targetroll # Commanded roll position
                    self.panmotorerrorcode = panmotorerrorcode
                    self.tiltmotorerrorcode = tiltmotorerrorcode
                    self.rollmotorerrorcode = rollmotorerrorcode
                    self.panabsposition = panabsposition # Low-resolution magnetic encoder absolute pan position
                    self.tiltabsposition = tiltabsposition # Low-resolution magnetic encoder absolute tilt position
                    self.rollabsposition = rollabsposition # Low-resolution magnetic encoder absolute roll position
                    self.panaccelx = panaccelx # Accelerometer outputs from AR2 CPU board sensor
                    self.panaccely = panaccely 
                    self.panaccelz = panaccelz 
                    self.tiltaccelx = tiltaccelx 
                    self.tiltaccely = tiltaccely 
                    self.tiltaccelz = tiltaccelz 
                    self.rollaccelx = rollaccelx 
                    self.rollaccely = rollaccely 
                    self.rollccelz = rollaccelz
                    self.appliedsettings = appliedsettings # Cookie indices for command acknowlege in frame header
                    self.constrainedsettings = constrainedsettings
                    self.invalidsettings = invalidsettings
                    self.enableinterpacketdelay = enableinterpacketdelay # If true delay is added between sending out image data packets
                    self.interpacketdelayperiod = interpacketdelayperiod # packet delay factor in us (does not include function overhead time)
                    self.uptime = uptime # Total number of seconds sonar has been running
                    self.arisappverionmajor = arisappversionmajor # Major version number
                    self.arisappversionminor = arisappversionminor # Minor version number 
                    self.gotime = gotime # Sonar time when frame cycle is initiated in hardware
                    self.panvelocity = panvelocity # AR2 pan velocity in degrees/second
                    self.tiltvelocity = tiltvelocity # AR2 tilt velocity in degrees/second
                    self.rollvelocity = rollvelocity # AR2 roll velocity in degrees/second
                    self.sentinel = sentinel # Used to measure the frame header size

    def __repr__(self):
        return 'ARIS Frame Number: ' + str(self.frameindex)
        
    def info(self):
        print('Frame Number: ' + str(self.frameindex))
        print('Frame Time: ' + str(datetime.datetime.fromtimestamp(self.sonartimestamp/1000000, pytz.timezone('UTC')).strftime('%Y-%m-%d %H:%M:%S.%f')))
        print('Frame Rate: ' + str(self.framerate))
        print('Window Start: ' + str(self.windowstart))
        print('Window Length: ' + str(self.windowlength))
        print('Ping Mode: ' + str(self.pingmode))
        print('Frequency: ' + str(self.frequencyhilow))
                    

def DataImport(filename):
    data = open(filename, 'rb')

    #Start reading file header
    version_number      = struct.unpack('I', data.read(4))[0]
    FrameCount          = struct.unpack('I', data.read(4))[0]
    FrameRate           = struct.unpack('I', data.read(4))[0]
    HighResolution      = struct.unpack('I', data.read(4))[0]
    NumRawBeams         = struct.unpack('I', data.read(4))[0]
    SampleRate          = struct.unpack('f', data.read(4))[0]
    SamplesPerChannel   = struct.unpack('I', data.read(4))[0]
    ReceiverGain        = struct.unpack('I', data.read(4))[0]
    WindowStart         = struct.unpack('f', data.read(4))[0]
    WindowLength        = struct.unpack('f', data.read(4))[0]
    Reverse             = struct.unpack('I', data.read(4))[0]
    SN                  = struct.unpack('I', data.read(4))[0]
    strDate             = struct.unpack('32s', data.read(32))[0]
    strHeaderID         = struct.unpack('256s', data.read(256))[0]
    UserID1             = struct.unpack('i', data.read(4))[0]
    UserID2             = struct.unpack('i', data.read(4))[0]
    UserID3             = struct.unpack('i', data.read(4))[0]
    UserID4             = struct.unpack('i', data.read(4))[0]
    StartFrame          = struct.unpack('I', data.read(4))[0]
    EndFrame            = struct.unpack('I', data.read(4))[0]
    TimeLapse           = struct.unpack('I', data.read(4))[0]
    RecordInterval      = struct.unpack('I', data.read(4))[0]
    RadioSeconds        = struct.unpack('I', data.read(4))[0]
    FrameInterval       = struct.unpack('I', data.read(4))[0]
    Flags               = struct.unpack('I', data.read(4))[0]
    AuxFlags            = struct.unpack('I', data.read(4))[0]
    Sspd                = struct.unpack('I', data.read(4))[0]
    Flags3D             = struct.unpack('I', data.read(4))[0]
    SoftwareVersion     = struct.unpack('I', data.read(4))[0]
    WaterTemp           = struct.unpack('I', data.read(4))[0]
    Salinity            = struct.unpack('I', data.read(4))[0]
    PulseLength         = struct.unpack('I', data.read(4))[0]
    TxMode              = struct.unpack('I', data.read(4))[0]
    VersionFGPA         = struct.unpack('I', data.read(4))[0]
    VersionPSuC         = struct.unpack('I', data.read(4))[0]
    ThumbnailFI         = struct.unpack('I', data.read(4))[0]
    FileSize            = struct.unpack('Q', data.read(8))[0]
    OptionalHeaderSize  = struct.unpack('Q', data.read(8))[0]
    OptionalTailSize    = struct.unpack('Q', data.read(8))[0]
    VersionMinor        = struct.unpack('I', data.read(4))[0]
    LargeLens           = struct.unpack('I', data.read(4))[0]
    
    #Create data structure
    output_data = ARIS_File(filename, version_number, FrameCount, FrameRate, HighResolution, NumRawBeams, SampleRate, SamplesPerChannel, ReceiverGain,
                 WindowStart, WindowLength, Reverse, SN, strDate, strHeaderID, UserID1, UserID2, UserID3, UserID4, StartFrame,EndFrame, 
                 TimeLapse, RecordInterval, RadioSeconds, FrameInterval, Flags, AuxFlags, Sspd, Flags3D, SoftwareVersion, WaterTemp,
                 Salinity, PulseLength, TxMode, VersionFGPA, VersionPSuC, ThumbnailFI, FileSize, OptionalHeaderSize, OptionalTailSize, 
                 VersionMinor, LargeLens)
    
    #Close data file
    data.close()
                 
    #Return the data structure
    return output_data
    
def FrameRead(ARIS_data, frameIndex):

    FrameSize = ARIS_data.NumRawBeams*ARIS_data.SamplesPerChannel
        
    frameoffset = (1024+(frameIndex*(1024+(FrameSize))))

    data = open(ARIS_data.filename, 'rb')   
    data.seek(frameoffset, 0)

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
    
    #Create the ARIS_frame data structure and add the meta-data
    output = ARIS_Frame(frameindex, frametime, version, status, sonartimestamp, tsday, tshour, tsminute, tssecond, tshsecond, transmitmode,
                 windowstart, windowlength, threshold, intensity, receivergain, degc1, degc2, humidity, focus, battery, uservalue1, uservalue2, 
                 uservalue3,  uservalue4,  uservalue5, uservalue6, uservalue7, uservalue8,  velocity, depth, altitude, pitch, pitchrate, roll,
                 rollrate, heading, headingrate, compassheading, compasspitch, compassroll, latitude, longitude, sonarposition, configflags, 
                 beamtilt, targetrange, targetbearing, targetpresent, firmwarerevision, flags, sourceframe, watertemp, timerperiod, sonarx,
                 sonary, sonarz, sonarpan, sonartilt, sonarroll, panpnnl, tiltpnnl, rollpnnl, vehicletime, timeggk, dateggk, qualityggk, numsatsggk,
                 dopggk, ehtggk, heavetss, yeargps, monthgps, daygps, hourgps, minutegps, secondgps, hsecondgps, sonarpanoffset, sonartiltoffset,
                 sonarrolloffset, sonarxoffset, sonaryoffset, sonarzoffset, tmatrix, samplerate, accellx, accelly, accellz, pingmode, frequencyhilow,
                 pulsewidth, cycleperiod, sampleperiod, transmitenable, framerate, soundspeed, samplesperbeam, enable150v, samplestartdelay, largelens,
                 thesystemtype, sonarserialnumber, encryptedkey, ariserrorflagsuint, missedpackets, arisappversion, available2, reorderedsamples,
                 salinity, pressure, batteryvoltage, mainvoltage, switchvoltage, focusmotormoving, voltagechanging, focustimeoutfault, focusovercurrentfault, 
                 focusnotfoundfault, focusstalledfault, fpgatimeoutfault, fpgabusyfault, fpgastuckfault, cputempfault, psutempfault, watertempfault, 
                 humidityfault, pressurefault, voltagereadfault, voltagewritefault, focuscurrentposition, targetpan, targettilt, targetroll, panmotorerrorcode,
                 tiltmotorerrorcode, rollmotorerrorcode, panabsposition, tiltabsposition, rollabsposition, panaccelx, panaccely, panaccelz, tiltaccelx, 
                 tiltaccely, tiltaccelz, rollaccelx, rollaccely, rollaccelz, appliedsettings, constrainedsettings, invalidsettings, enableinterpacketdelay,
                 interpacketdelayperiod, uptime, arisappversionmajor, arisappversionminor, gotime, panvelocity, tiltvelocity, rollvelocity, sentinel)
    
    #Add the frame data
    if pingmode == 9:
        ARIS_Frame.BeamCount = 128
    
    data.seek(frameoffset+1024, 0)
    frame = np.empty([samplesperbeam, ARIS_Frame.BeamCount], dtype=float)
    for r in range(len(frame)):
        for c in range(len(frame[r])):
            frame[r][c] = struct.unpack('B', data.read(1))[0]
    frame = np.fliplr(frame)
    
    #Remap the data from 0-255 to 0-80 dB
    remap = lambda t: (t * 80)/255
    vfunc = np.vectorize(remap)
    frame = vfunc(frame)
    
    output.frame_data = frame
    
    data.close()
    
    return output
    
'''Data remapping functions'''


#WinLen = test_frame.sampleperiod * test_frame.samplesperbeam * 0.000001 * test_frame.soundspeed / 2
#RangeStart = WinStart
#RangeEnd = WinStart + WinLen
#SampleLength = test_frame.sampleperiod * 0.000001 * test_frame.soundspeed / 2

def getXY(beamnum, binnum, frame):
    WinStart = frame.samplestartdelay * 0.000001 * frame.soundspeed / 2
    bin_dist = WinStart + frame.sampleperiod * binnum * 0.000001 * frame.soundspeed / 2
    beam_angle = beamLookUp.beamAngle(beamnum)
    x = bin_dist*np.sin(np.deg2rad(-beam_angle))
    y = bin_dist*np.cos(np.deg2rad(-beam_angle))
    return x, y

def getBeamBin(x,y, frame):
    WinStart = frame.samplestartdelay * 0.000001 * frame.soundspeed / 2
    angle = np.rad2deg(np.tan(x/y))
    hyp = y/np.cos(np.deg2rad(angle))
    binnum2 = int((2*(hyp-WinStart))/(frame.sampleperiod * 0.000001 * frame.soundspeed))
    beamnum = beamLookUp.BeamLookUp(-angle)
    return beamnum, binnum2
    
def px2Meters(x,y, frame):
    WinStart = frame.samplestartdelay * 0.000001 * frame.soundspeed / 2
    pix2Meter = frame.sampleperiod * 0.000001 * frame.soundspeed / 2
    xdim = int(getXY(0,frame.samplesperbeam, frame)[0]*(1/pix2Meter)*2)
    x1 = (x - xdim/2) * pix2Meter #Convert X pixel to X dimension
    y1 = (y*pix2Meter)+(WinStart) #Convert Y pixel to y dimension
    return x1, y1    

def createLUP(ARISFile, frame):
    #Lookup dimensions
    SampleLength = frame.sampleperiod * 0.000001 * frame.soundspeed / 2
    ARISFile.ydim = int(frame.samplesperbeam)
    ARISFile.xdim = int(getXY(0,frame.samplesperbeam, frame)[0]*(1/SampleLength)*2)

    LUP = {}

    #Iterate through each point in the frame and lookup data
    for x in range(ARISFile.xdim):
        for y in range(ARISFile.ydim):
            x1, y1 = px2Meters(x, y, frame)
            Beam, Bin = getBeamBin(x1, y1, frame)
            if Beam != 999:
                if Bin < frame.samplesperbeam:
                    LUP[(x, y)] = (Bin, Beam)
                
    return LUP

def remapARIS(ARISFile, frame):                
    #Create an empty frame
    Remap = np.zeros([ARISFile.xdim,ARISFile.ydim])
    
    #Populate the empty frame
    for key in ARISFile.LUP:
        Remap[key[0],key[1]] = frame.frame_data[ARISFile.LUP[key][0], ARISFile.LUP[key][1]]
        
    #Add to frame data
    return Remap