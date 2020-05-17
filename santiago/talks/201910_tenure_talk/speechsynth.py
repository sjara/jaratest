'''
Module for speech sounds synthesis.
'''

import os
import parselmouth as pm
import numpy as np


def show_spectrogram(spectrogram, dynamic_range=70,cmap='Greys'):
    from matplotlib import pyplot as plt
    Xg, Yg = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values)
    #cmap = 'Greys' #'afmhot'
    plt.pcolormesh(Xg, Yg, sg_db, vmin=sg_db.max() - dynamic_range, cmap=cmap)
    plt.ylim([spectrogram.ymin, spectrogram.ymax])
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")

def BaPaRange(nItems, sampFreq=44100, freqFactor=1, outputDir=''):
    burstDuration = 0.004
    vowelDuration = 0.315
    formantTransitionDuration = 0.035
    prevoiceDuration = 0
    aspPointLimits = [0, 0.08]
    aspPointValues = np.linspace(aspPointLimits[0], aspPointLimits[1], nItems)
    aspPointPercent = np.linspace(0, 100, nItems)
    sounds = []
    for inds,aspPoint in enumerate(aspPointValues):
        syllableObj = Syllable(vowelDuration, formantTransitionDuration, aspPoint,
                                burstDuration, prevoiceDuration, nFormants=5, sampFreq=sampFreq)
        syllableObj.set_pitch(80*freqFactor, 100*freqFactor)
        syllableObj.set_formant(1, 220*freqFactor, 710*freqFactor, 50*freqFactor)
        syllableObj.set_formant(2, 900*freqFactor, 1240*freqFactor, 70*freqFactor)
        syllableObj.set_formant(3, 2000*freqFactor, 2500*freqFactor, 110*freqFactor)
        syllableObj.set_formant(4, 3600*freqFactor, 3600*freqFactor, 170*freqFactor)
        syllableObj.set_formant(5, 4500*freqFactor, 4500*freqFactor, 250*freqFactor)
        sound = syllableObj.create_sound()
        sounds.append(sound)
        if outputDir:
            fileName = 'bapa_{0}x_{1:03.0f}.wav'.format(freqFactor,aspPointPercent[inds])
            fullFileName = os.path.join(outputDir,fileName)
            print('Saving {}'.format(fullFileName))
            sound.save(fullFileName,'WAV')
    return sounds

def BaDaRange(nItems, sampFreq=44100, freqFactor=1, outputDir=''):
    burstDuration = 0.004
    vowelDuration = 0.315
    formantTransitionDuration = 0.035
    prevoiceDuration = 0
    aspPoint = 0
    formant2onset = np.geomspace(1240/1.4, 1240*1.4, nItems)
    formant3onset = np.geomspace(2500/1.25, 2500*1.25, nItems)
    changePercent = np.linspace(0, 100, nItems)
    sounds = []
    for inds in range(nItems):
        syllableObj = Syllable(vowelDuration, formantTransitionDuration, aspPoint,
                                burstDuration, prevoiceDuration, nFormants=5, sampFreq=sampFreq)
        syllableObj.set_pitch(80*freqFactor, 100*freqFactor)
        syllableObj.set_formant(1, 220*freqFactor, 710*freqFactor, 50*freqFactor)
        syllableObj.set_formant(2, formant2onset[inds]*freqFactor, 1240*freqFactor, 70*freqFactor)
        syllableObj.set_formant(3, formant3onset[inds]*freqFactor, 2500*freqFactor, 110*freqFactor)
        syllableObj.set_formant(4, 3600*freqFactor, 3600*freqFactor, 170*freqFactor)
        syllableObj.set_formant(5, 4500*freqFactor, 4500*freqFactor, 250*freqFactor)
        sound = syllableObj.create_sound()
        sounds.append(sound)
        if outputDir:
            fileName = 'bada_{0}x_{1:03.0f}.wav'.format(freqFactor,changePercent[inds])
            #fileName = 'bada_{:03.0f}.wav'.format(changePercent[inds])
            fullFileName = os.path.join(outputDir,fileName)
            print('Saving {}'.format(fullFileName))
            sound.save(fullFileName,'WAV')
    return sounds


class Syllable():
    def __init__(self, vowelDuration, formantTransitionDuration, aspPoint, burstDuration,
                 prevoiceDuration=0, nFormants=5, sampFreq=44100):
        self.nFormants = nFormants
        self.sampFreq = sampFreq
        self.pitch = {}
        self.formants = (nFormants)*[{}]
        self.formantTransitionDuration = formantTransitionDuration
        self.vowelDuration = vowelDuration
        self.aspPoint = aspPoint
        self.burstDuration = burstDuration
        self.prevoiceDuration = prevoiceDuration
        self.silenceSound = None
        self.vowelSound = None
        self.burstSound = None
        self.sound = None
    def set_pitch(self, onset, stable):
        self.pitch = {'onset':onset, 'stable':stable}
    def set_formant(self, formantID, onset, stable, bandwidth):
        self.formants[formantID-1] = {'onset':onset, 'stable':stable,
                                    'bandwidth':bandwidth}
    def create_sound(self):
        self.silence = pm.praat.call('Create Sound from formula', 'silence', 1, 0, 0.05,
                                self.sampFreq, '0') # Last argument must be string.
        self.create_burst()
        self.create_vowel()
        if self.prevoiceDuration:
            self.create_prevoicing()
            self.sound  = self.silence.concatenate([self.silence, self.burstSound, self.prevoiceSound, self.vowelSound])
        else:
            self.sound  = self.silence.concatenate([self.silence, self.burstSound, self.vowelSound])
        return self.sound
    def create_burst(self):
        burstKG = pm.praat.call('Create KlattGrid', 'burst', 0, self.burstDuration,
                                0, 0, 0, 1, 0, 0, 0)
        pm.praat.call(burstKG, 'Add frication formant frequency point', 1, 0, 300)
        pm.praat.call(burstKG, 'Add frication formant bandwidth point', 1, 0, 100)
        pm.praat.call(burstKG, 'Add frication formant amplitude point', 1, 0, 0.005)
        pm.praat.call(burstKG, 'Add frication amplitude point', 0, 0)
        pm.praat.call(burstKG, 'Add frication amplitude point', 0.001, 25)
        pm.praat.call(burstKG, 'Add frication amplitude point', 0.001, 25)
        pm.praat.call(burstKG, 'Add frication amplitude point', self.burstDuration, 0)
        pm.praat.call(burstKG, 'Add voicing amplitude point', 0, 25)
        self.burstSound = pm.praat.call(burstKG, 'To Sound (special)', 0, 0, self.sampFreq,
                                            'yes', 'no', 'yes', 'yes', 'yes', 'yes',
                                            'Powers in tiers', 'yes', 'yes', 'yes',
                                            'Cascade', 1, 5, 1, 1,  1, 1, 1, 1,
                                            1, 1, 1, 1,  1, 1, 1, 6, 'yes')
        pm.praat.call(self.burstSound, 'Scale intensity', 50)
        return self.burstSound
    def create_vowel(self):
        vowelKG = pm.praat.call('Create KlattGrid', 'creation', 0, self.vowelDuration,
                                5, 0, 0, 1, 0, 0, 0)
        for indf in range(self.nFormants):
            pm.praat.call(vowelKG, 'Add oral formant frequency point', indf+1,
                          0, self.formants[indf]['onset'])
            pm.praat.call(vowelKG, 'Add oral formant frequency point', indf+1,
                          self.formantTransitionDuration,
                          self.formants[indf]['stable'])
            pm.praat.call(vowelKG, 'Add oral formant bandwidth point', indf+1,
                          0, self.formants[indf]['bandwidth'])

        pm.praat.call(vowelKG, 'Add pitch point', self.aspPoint, self.pitch['onset'])
        pm.praat.call(vowelKG, 'Add pitch point', self.aspPoint+0.1, self.pitch['stable'])
        pm.praat.call(vowelKG, 'Add pitch point', self.vowelDuration-0.04, 90)
        pm.praat.call(vowelKG, 'Add pitch point', self.vowelDuration, 50)

        pm.praat.call(vowelKG, 'Add voicing amplitude point', 0, 0)
        pm.praat.call(vowelKG, 'Add voicing amplitude point', self.aspPoint, 0)
        pm.praat.call(vowelKG, 'Add voicing amplitude point', self.aspPoint+0.00001, 60)
        pm.praat.call(vowelKG, 'Add voicing amplitude point', self.aspPoint+0.02, 60)
        pm.praat.call(vowelKG, 'Add voicing amplitude point', self.vowelDuration, 50)

        pm.praat.call(vowelKG, 'Add aspiration amplitude point', self.burstDuration, 20)
        pm.praat.call(vowelKG, 'Add aspiration amplitude point', self.burstDuration+0.001, 25)
        pm.praat.call(vowelKG, 'Add aspiration amplitude point', self.aspPoint-0.001, 25)
        pm.praat.call(vowelKG, 'Add aspiration amplitude point', self.aspPoint, 0)

        self.vowelSound = pm.praat.call(vowelKG, 'To Sound (special)', 0, 0.315, self.sampFreq,
                                        'yes', 'yes', 'yes', 'yes', 'yes', 'yes',
                                        'Powers in tiers', 'yes', 'yes', 'yes' ,
                                        'Cascade', 1, 5, 1, 1,  1, 1, 1, 1,  1, 1, 1, 1,
                                        1, 1, 1, 6, 'yes')
        return self.vowelSound
    def create_prevoicing(self):
        prevoiceKG = pm.praat.call('Create KlattGrid', 'prevoice', 0, self.prevoiceDuration,
                                   1, 0, 0, 1, 0, 0, 0)
        pm.praat.call(prevoiceKG, 'Add oral formant frequency point', 1, 0, 120)
        pm.praat.call(prevoiceKG, 'Add oral formant frequency point', 1, 0, 100)
        pm.praat.call(prevoiceKG, 'Add pitch point', 0, 120)
        pm.praat.call(prevoiceKG, 'Add voicing amplitude point', 0, 50)
        self.prevoiceSound = pm.praat.call(prevoiceKG, 'To Sound (special)', 0,
                                           self.prevoiceDuration, self.sampFreq,
                                          'yes', 'yes', 'yes', 'yes', 'yes', 'yes',
                                          'Powers in tiers', 'yes', 'yes', 'yes',
                                          'Cascade', 1, 5, 1, 1,  1, 1, 1, 1,
                                          1, 1, 1, 1,  1, 1, 1, 6, 'yes')
        pm.praat.call(self.prevoiceSound, 'Scale intensity', 50)
        return self.prevoiceSound
    def play(self):
        self.sound.save('/tmp/soundtemp.wav','WAV')
        os.system('aplay /tmp/soundtemp.wav')


if __name__=='__main__':
    sampFreq = 96000
    #BaPaRange(6, freqFactor=8, sampFreq=sampFreq, outputDir='~/tmp/soundsBaPa/')
    #BaDaRange(6, freqFactor=8, sampFreq=sampFreq, outputDir='/home/sjara/src/jarasounds/')
    #BaDaRange(6, outputDir='~/tmp/soundsBaDa/')

    '''
    burstDuration = 0.004
    vowelDuration = 0.315
    formantTransitionDuration = 0.035
    aspPoint = 0.08 #0
    prevoiceDuration = 0#0.06

    syllableObj = Syllable(vowelDuration, formantTransitionDuration, aspPoint,
                            burstDuration, prevoiceDuration, nFormants=5)
    syllableObj.set_pitch(80, 100)
    syllableObj.set_formant(1, 220, 710, 50)
    syllableObj.set_formant(2, 900, 1240, 70)
    syllableObj.set_formant(3, 2000, 2500, 110)
    syllableObj.set_formant(4, 3600, 3600, 170)
    syllableObj.set_formant(5, 4500, 4500, 250)
    sound = syllableObj.create_sound()
    #sound.save('~/tmp/test03.wav','WAV')
    syllableObj.play()

    from matplotlib import pyplot as plt
    plt.clf()
    spectrogram = sound.to_spectrogram(window_length=0.02, time_step=0.0001)
    show_spectrogram(spectrogram)
    plt.show()
    '''
