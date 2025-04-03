from jaratoolbox import imagedatabase

mouse_name = 'wifi008'
sessions = []

# Session parameters: sessionNumber, date, imaging_type, LED_intensity, ISO, Oxy, soundIntensity, highestFrequency, ISI, soundDuration, type_of_sound
# sessionNumber = From timestamps.
# date = YYYYMMDD (manually). I see that in the info files the format is YYYY-MM-DD but since we save the files like YYYYMMDD, I'd suggest to keep it like that.
# imaging_type = [calcium, calthesia (Sounds funny but it makes sense, you can tell me if you prefer a different name), intrinsic]
# LED_intensity = [1,2,3,4,5,6,7]  Numbers refer to the tick (which would be a problem for intrinsic since we don't use a precise tick).
# ISO = [None, 0.75,0.8,1...] None in case there's no ANES. Floats specifying percentage in case there is. ->Actually, to keep all data with the same format, instead of None we can use 0.0<-.
# Oxy = [None, 1, 1.25, 1.5,...] None in case there's no ANES. Floats specifying percentage in case there is.
# soundIntensity = [65,70,...]
# highestFrequency = [26,28,32,...]
# ISI = [1, 1.2, 3, ..] #We can decide whether to do it in s or ms.
# soundDuration = [1, 3, ...] #We can decide whether to do it in s or ms.
# type_of_sound = ["ToneTrains", "PureTones",...]

# // Notes about the dynamic range:
# // Focused on:
# // Additional comments:

# Example session calcium
sess0 = imagedatabase.ImagingSession(
    mouse_name, '20250403', imaging_type='calcium', LED_intensity=7, 
    ISO=None, Oxy=None, soundIntensity=70, highestFrequency=28000, 
    ISI=1.2, soundDuration=1, type_of_sound='ToneTrains'
)


sessions.append(sess0)

# Example session with calcium + anesthesia
sess1 = imagedatabase.ImagingSession(
    mouse_name, '20250403', imaging_type='calthesia', LED_intensity=7, 
    ISO=1.5, Oxy=1.25, soundIntensity=80, highestFrequency=28000, 
    ISI=3, soundDuration=1, type_of_sound='ToneTrains'
)

sessions.append(sess1)

# Example session with intrinsic
sess2 = imagedatabase.ImagingSession(
    mouse_name, '20250403', imaging_type='intrinsic', LED_intensity=0, #<-How to specify this? 
    ISO=1.5, Oxy=1.25, soundIntensity=80, highestFrequency=28000, 
    ISI=3, soundDuration=1, type_of_sound='ToneTrains'
)


sessions.append(sess2)
