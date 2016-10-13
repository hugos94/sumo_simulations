#!/usr/bin/env python

"""
@file   runner.py
@author Hugo Santos Piauilino
@date   10-10-2016

Traffic Light Control via TraCI interface
"""

from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import subprocess
import random

# we need to import python modules from the $SUMO_HOME/tools directory
try:
    sys.path.append(os.path.join(os.path.dirname(
        __file__), '..', '..', '..', '..', "tools"))  # tutorial in tests
    sys.path.append(os.path.join(os.environ.get("SUMO_HOME", os.path.join(
        os.path.dirname(__file__), "..", "..", "..")), "tools"))  # tutorial in docs
    from sumolib import checkBinary
except ImportError:
    sys.exit("please declare environment variable 'SUMO_HOME' as the root directory of your sumo installation (it should contain folders 'bin', 'tools' and 'docs')")

import traci

# the port used for communicating with your sumo instance
PORT = 8873

def generate_routefile():
    random.seed(42)
    N = 1000 # Numero de time steps
    #Demanda por segundo de diferentes direcoes
    p1to2 = 1. /10
    p1to3 = 1. /10
    p2to1 = 1. /10
    p2to4 = 1. /10
    p3to2 = 1. /10
    p3to4 = 1. /10
    p4to1 = 1. /10
    p4to3 = 1. /10

    with open("data/cross.rou.xml", "w") as routes:
        print("""<?xml version="1.0" encoding="UTF-8"?>
            <routes>
            <!--Tipo de Automoveis | sigma: drivers imperfection in driving (between 0 and 1)-->
            <vType accel="3.0" decel="6.0" id="CarA" color="1,0,0" length="5.0" minGap="2.5" maxSpeed="16.67" sigma="0.2" />
            <vType accel="2.0" decel="6.0" id="CarB" color="0,1,0" length="7.5" minGap="3" maxSpeed="25.0" sigma="0.4" />
            <vType accel="1.0" decel="5.0" id="CarC" color="0,0,1" length="5.0" minGap="2.5" maxSpeed="40.0" sigma="0.6" guiShape="passenger"/>
            <vType accel="1.0" decel="5.0" id="CarD" color="1,0,1" length="7.5" minGap="3" maxSpeed="30.0" sigma="0.8" guiShape="bus"/>

            <!--Tipos de Rotas-->
            <route id="r1to2" edges="1to0 0to2"/>
            <route id="r1to3" edges="1to0 0to3"/>
            <route id="r2to1" edges="2to0 0to1"/>
            <route id="r2to4" edges="2to0 0to4"/>
            <route id="r3to2" edges="3to0 0to2"/>
            <route id="r3to4" edges="3to0 0to4"/>
            <route id="r4to1" edges="4to0 0to1"/>
            <route id="r4to3" edges="4to0 0to3"/>
        """, file=routes)
        lastVeh = 0
        vehNr = 0
        for i in range(N):
            if random.uniform(0,1) < p1to2:
                print('     <vehicle id="p1to2_%i" type="CarA" route="r1to2" depart="%i" departLane="free" />' % (vehNr, i), file=routes)
                vehNr +=1
                lastVeh = i
            if random.uniform(0,1) < p1to3:
                print('     <vehicle id="p1to3_%i" type="CarB" route="r1to3" depart="%i" departLane="free" />' % (vehNr, i), file=routes)
                vehNr +=1
                lastVeh = i
            if random.uniform(0,1) < p2to1:
                print('     <vehicle id="p2to1_%i" type="CarC" route="r2to1" depart="%i" departLane="free" />' % (vehNr, i), file=routes)
                vehNr +=1
                lastVeh = i
            if random.uniform(0,1) < p2to4:
                print('     <vehicle id="p2to4_%i" type="CarD" route="r2to4" depart="%i" departLane="free" />' % (vehNr, i), file=routes)
                vehNr +=1
                lastVeh = i
            if random.uniform(0,1) < p3to2:
                print('     <vehicle id="p3to2_%i" type="CarA" route="r3to2" depart="%i" departLane="free" />' % (vehNr, i), file=routes)
                vehNr +=1
                lastVeh = i
            if random.uniform(0,1) < p3to4:
                print('     <vehicle id="p3to4_%i" type="CarB" route="r3to4" depart="%i" departLane="free" />' % (vehNr, i), file=routes)
                vehNr +=1
                lastVeh = i
            if random.uniform(0,1) < p4to1:
                print('     <vehicle id="p4to1_%i" type="CarC" route="r4to1" depart="%i" departLane="free" />' % (vehNr, i), file=routes)
                vehNr +=1
                lastVeh = i
            if random.uniform(0,1) < p4to3:
                print('     <vehicle id="p4to3_%i" type="CarD" route="r4to3" depart="%i" departLane="free" />' % (vehNr, i), file=routes)
                vehNr +=1
                lastVeh = i
        print("</routes>", file=routes)

def run():
    """Execute the TraCI control loop"""
    traci.init(PORT)
    step = 0
    traci.trafficlights.setPhase("0", 2)
    while traci.simulation.getMinExpectedNumber () > 0:
        traci.simulationStep()
        if traci.trafficlights.getPhase("0") == 2:
            if traci.inductionloop.getLastStepVehicleNumber("1to0_0") > 0:
                # there is a vehicle from the north, switch
                traci.trafficlights.setPhase("0", 3)
            else:
                # otherwise try to keep green for EW
                traci.trafficlights.setPhase("0", 2)
        step += 1
    traci.close()
    sys.stdout.flush()

def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true", default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options

if __name__ == "__main__":
    options = get_options()

    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    #Gerando arquivos de rotas para a simulacao
    generate_routefile()

    sumoProcess = subprocess.Popen([sumoBinary, "-c", "data/cross.sumocfg", "--tripinfo-output", "tripinfo.xml", "--remote-port", str(PORT)], stdout=sys.stdout, stderr=sys.stderr)

    run()
    sumoProcess.wait()
