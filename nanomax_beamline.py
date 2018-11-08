"""
Sets up a some actual nanomax hardware.
"""

# need this main guard here because Process.start() (so our recorders)
# import __main__, and we don't want the subprocess to start new sub-
# processes etc.
if __name__=='__main__':

    import lib
    from lib.environment import env
    from lib.recorders import Hdf5Recorder
    from lib.motors import DummyMotor
    from lib.motors.E727 import E727Motor
    from lib.motors.SardanaPoolMotor import SardanaPoolMotor
    from lib.motors.SmaractMotor import SmaractLinearMotor
    from lib.detectors import DetectorGroup
    from lib.detectors.Pilatus import Pilatus
    from lib.data import SdmPathFixer
    import os
    
    env.userLevel = 1
    # chosen these levels here:
    # 1 - simple user
    # 2 - power user
    # 3 - optics
    # 4 - potentially dangerous

    # sample piezos - these already have the right orientation so scale/offset not needed.
    samx = E727Motor(device='B303A-EH/CTL/PZCU-02', axis=1, name='samx')
    samy = E727Motor(device='B303A-EH/CTL/PZCU-02', axis=3, name='samy')
    samz = E727Motor(device='B303A-EH/CTL/PZCU-02', axis=2, name='samz')
    samx.limits = (0, 100)
    samy.limits = (0, 100)
    samz.limits = (0, 100)

    # smaracts
    # controller 1
    skb_top = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-03', axis=0, name='skb_top', userlevel=2)
    skb_bottom = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-03', axis=1, name='skb_bottom', userlevel=2)
    skb_left = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-03', axis=2, name='skb_left', userlevel=2)
    skb_right = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-03', axis=3, name='skb_right', userlevel=2)
    kbfluox = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-03', axis=4, name='kbfluox', userlevel=3)
    # controller 2
    dbpm2_x = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-04', axis=0, name='dbpm2_x', userlevel=3)
    dbpm2_y = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-04', axis=1, name='dbpm2_y', userlevel=3)
    seh_top = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-04', axis=2, name='seh_top', userlevel=3)
    seh_bottom = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-04', axis=3, name='seh_bottom', userlevel=3)
    seh_left = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-04', axis=4, name='seh_left', userlevel=3)
    seh_right = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-04', axis=5, name='seh_right', userlevel=3)
    attenuator1_x = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-04', axis=6, name='attenuator1_x', userlevel=2)
    attenuator2_x = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-04', axis=7, name='attenuator2_x', userlevel=2)
    attenuator3_x = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-04', axis=8, name='attenuator3_x', userlevel=2)
    attenuator4_x = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-04', axis=9, name='attenuator4_x', userlevel=2)
    fastshutter_x = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-04', axis=10, name='fastshutter_x', userlevel=3)
    diode_x = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-04', axis=11, name='diode_x', userlevel=3)
    # controller 3
    pindiode_y = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-05', axis=0, name='pindiode_y', userlevel=3)
    pindiode_z = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-05', axis=1, name='pindiode_z', userlevel=3)
    pindiode_x = SmaractLinearMotor(device='B303A-EH/CTL/PZCU-05', axis=2, name='pindiode_x', userlevel=3)

    # some steppers through sardana
    sams_x = SardanaPoolMotor(device='B303A-E02/DIA/SAMS-01-X', name='sams_x')
    sams_y = SardanaPoolMotor(device='B303A-E02/DIA/SAMS-01-Y', name='sams_y')
    sams_z = SardanaPoolMotor(device='B303A-E02/DIA/SAMS-01-Z', name='sams_z')
    sams_x.limits = (0, 25)
    sams_y.limits = (0, 25)
    sams_z.limits = (0, 25)

    # some sardana pseudo motors - these should really be reimplemented
    energy = SardanaPoolMotor(device='pseudomotor/nanomaxenergy_ctrl/1', name='energy')

    # some dummy motors
    dummy1 = DummyMotor(name='dummy1', userlevel=2)
    dummy2 = DummyMotor(name='dummy2', userlevel=2)

    # detectors
    pilatus = Pilatus(name='pilatus', 
                      lima_device='lima/limaccd/b-nanomax-mobile-ipc-01',
                      det_device='lima/pilatus/b-nanomax-mobile-ipc-01')

    # detector groups
    detgrp = DetectorGroup('detgrp')
    detgrp.append(pilatus)
    env.currentDetectorGroup = detgrp

    # the environment keeps track of where to write data
    env.paths = SdmPathFixer('B303A/CTL/SDM-01')

    # an hdf5 recorder
    h5rec = Hdf5Recorder(name='h5rec')
    h5rec.start()

