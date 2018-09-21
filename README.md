# acquisition-framework
Light weight data acquisition framework for orchestrating beamline experiments.

The code is organized as a library containing various classes. A beamline is set up simply by making instances for detectors, motors, and any other devices directly in ipython. See `dummy_beamline.py` for example.

## macros
A macro is a short expression in command line syntax which can be directly run at the ipython prompt. The following is a macro.
```
mv samx 12.4
```

In this framework, macros are created by writing a class with certain properties and marking that class with a decorator. This registers the macro as a magic ipython command. All available macros are stored in a central list, and can be listed with the `lsmac` command. The macro syntax is similar to sardana and spec.
```
In [2]: lsmac

name       class                                        
--------------------------------------------------------
dscan      <class 'lib.scans.Scan.DScan'>               
lsrec      <class 'lib.recorders.Recorder.LsRec'>       
loopscan   <class 'lib.scans.Scan.LoopScan'>            
lsm        <class 'lib.motors.Motor.LsM'>               
mv         <class 'lib.motors.Motor.Mv'>                
lsmac      <class 'lib.environment.LsMac'>              
lsdet      <class 'lib.detectors.Detector.LsDet'>       
wm         <class 'lib.motors.Motor.Wm'>                
wa         <class 'lib.motors.Motor.Wa'>                
ascan      <class 'lib.scans.Scan.AScan'>               
mvr        <class 'lib.motors.Motor.Mvr'>               
liveplot   <class 'lib.recorders.PlotRecorder.LivePlot'>
lsgrp      <class 'lib.detectors.Detector.LsGrp'>       

```
Note how macros aren't stored in a special library. They are written throughout the library wherever they make sense. For example, in `Detector.py` where the detector base classes are defined, the `lsdet` macro is defined as follows.
```
@macro
class LsDet(object):
    def run(self):
        dct = {d.name: d.__class__ for d in Detector.getinstances()}
        print(utils.dict_to_table(dct, titles=('name', 'class')))
```

Note that a macro is different from a script. Anyone can easily write a macro, but for composite operations where existing macros are just combined it is faster to write a script. The following is a script, not a macro, but uses a special `runCommand` function to interface with the command line syntax.
```
import lib.environment as env

for i in range(5):
    env.runCommand('mv samy %d' % new_y_pos)
    env.runCommand('ascan samx 0 1 5 .1')

```

## environment variables
No global environment variables are used. Instead, a central object called in the environment module is used to store values such as scan number, current detector group, etc.
```
In [24]: from lib.environment import env

In [25]: env.nextScanID
Out[25]: 1

In [26]: env.currentDetectorGroup
Out[26]: <lib.detectors.Detector.DetectorGroup at 0x7f5af40189b0>

In [27]: env.currentDetectorGroup.name
Out[27]: 'detgrp'
```

## instance tracking
The framework has no databases or central registries. Instead, objects are related through inheritance. A common base class `Gadget`
 is inherited by detectors, motors, as all the rest. `Gadget` and all of its subclasses keep track of their instances. An example follows.
```
In [1]: [m.name for m in Motor.getinstances()]
Out[1]: ['gap', 'samy', 'samx']

In [2]: [d.name for d in Detector.getinstances()]
Out[2]: ['det1', 'det3', 'det2']

In [3]: [g.name for g in Gadget.getinstances()]
Out[3]: ['gap', 'detgrp', 'det1', 'samy', 'samx', 'det3', 'det2', 'hdf5recorder']
```
 
## detector groups
Detectors are chosen through detector groups. The variable `lib.environment.env.currentDetectorGroup` selects which detector group to read out when scanning. A detector can be a member of many groups, but only one group can be selected at the same time. `DetectorGroup` objects are iterable and generally nice.
```
In [3]: [d.name for d in detgrp]
Out[3]: ['det1', 'det2', 'det3']
```

## recorders
Data is captured by recorders. Recorders are run in separate processes and get data through queues, avoiding holding up the main acquisition loop because of I/O. They can do anything with the data, for example saving to `hdf5` files or live plotting. See the `Hdf5Recorder` and `PlotRecorder` classes for examples. The former is very primitive still, but the latter is quite nice.

Note how easy it is to write these recorders, and how easy it would be to integrate online data analysis, for example writing a recorder which serves data (or links to data) for an on-the-fly ptycho engine to grab.

The `lsrec` macro lists currently running recorders.
```
In [30]: lsrec

name           class                                            
----------------------------------------------------------------
hdf5recorder   <class 'lib.recorders.Hdf5Recorder.Hdf5Recorder'>
name           <class 'lib.recorders.PlotRecorder.PlotRecorder'>
```

## user levels
All `Gadget` instances have an associated user level. This means that certain motors can be hidden and protected while others are exposed through the macros. In this example, two sample motors are available to everyone while the undulator gap is higher level. This is not a security feature but meant to simplify the environment and reduce the risk of mistakes
```
In [7]: env.userLevel
Out[7]: 1

In [8]: wa
samy 0.0
samx 0.0

In [9]: env.userLevel = 5

In [10]: wa
samy 0.0
gap 0.0
samx 0.0
```

## direct access to python objects
If `Gadget` objects operate on underlying Tango devices, then Tango attributes are directly accessible on the objects themselvs. PyTango provides tab completion and so these can be easily checked or corrected. Of course `Gadget`subclasses can provide nice getter and setter methods, but fixes are easily done.
```
In [7]: pilatus.det.energy
Out[7]: 10.0

In[8]: pilatus.lima.saving_mode
Out[8]: 'MANUAL'
```

