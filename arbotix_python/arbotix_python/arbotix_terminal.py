#!/usr/bin/env python3


"""
  ArbotiX Terminal - command line terminal to interact with an ArbotiX
  Copyright (c) 2019-2020 ECAM Makers.  All right reserved.
  Copyright (c) 2008-2011 Vanadium Labs LLC.  All right reserved.

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions are met:
      * Redistributions of source code must retain the above copyright
        notice, this list of conditions and the following disclaimer.
      * Redistributions in binary form must reproduce the above copyright
        notice, this list of conditions and the following disclaimer in the
        documentation and/or other materials provided with the distribution.
      * Neither the name of Vanadium Labs LLC nor the names of its
        contributors may be used to endorse or promote products derived
        from this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
  ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
  WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
  DISCLAIMED. IN NO EVENT SHALL VANADIUM LABS BE LIABLE FOR ANY DIRECT, INDIRECT,
  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
  OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
  OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
  ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys

from arbotix_python.arbotix.arbotix import ArbotiX
from arbotix_python.arbotix.ax12 import P_BAUD_RATE, P_ID

# help phrases
help = ["ArbotiX Terminal V0.2",
        "",
        "valid commands:",
        " ls [i b]- list the servos found on the bus. Optional parameters: i - highest ID to query, b - baudrate to query at.",
        " mv id id2 - rename any servo with ID=id, to id2",
        " baud b - set baud rate of bus to b",
        " get param id - get a parameter value from a servo",
        " set param id val - set parameter on servo ID=id to val",
        "",
        "valid parameters",
        " pos - current position of a servo, 0-1023",
        " spd - current goal speed of a servo, 0-1023",
        " baud - baud rate",
        " temp - current temperature, degrees C, READ ONLY"]


class Terminal(ArbotiX):
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def __init__(self, port="/dev/ttyUSB0", baud=115200):
        # start
        ArbotiX.__init__(self, port, baud)
        print("ArbotiX Terminal --- Version 2.0")
        print("Copyright 2019 ECAM Makers")
        print("Copyright 2011 Vanadium Labs LLC")

        # loop
        while True:
            cmd = input(">> ").split(" ")
            try:
                if cmd[0] == "help":        # display help data
                    if len(cmd) > 1:        # for a particular command
                        if cmd[1] == "ls":
                            print(help[3])
                        elif cmd[1] == "mv":
                            print(help[4])
                        elif cmd[1] == "baud":
                            print(help[5])
                        elif cmd[1] == "get":
                            print(help[6])
                        elif cmd[1] == "set":
                            print(help[7])
                        else:
                            print("help: unrecognized command")
                    else:
                        for h in help:
                            print(h)

                elif cmd[0] == "ls":       # list servos
                    self._ser.timeout = 0.25
                    if len(cmd) > 2:
                        self.write(253, P_BAUD_RATE, [
                                   self.convertBaud(int(cmd[1]))])
                        self.query()
                    self.query()

                elif cmd[0] == "mv":         # rename a servo
                    if self.write(int(cmd[1]), P_ID, [int(cmd[2]), ]) == 0:
                        print(self.OKBLUE + "OK" + self.ENDC)

                elif cmd[0] == "baud":      # set bus baud rate
                    self.write(253, P_BAUD_RATE, [
                               self.convertBaud(int(cmd[1]))])
                    print(self.OKBLUE + "OK" + self.ENDC)

                elif cmd[0] == "set":
                    if cmd[1] == "baud":
                        self.write(int(cmd[2]), P_BAUD_RATE, [
                                   self.convertBaud(int(cmd[3]))])
                        print(self.OKBLUE + "OK" + self.ENDC)
                    elif cmd[1] == "pos" or cmd[1] == "position":
                        self.setPosition(int(cmd[2]), int(cmd[3]))
                        print(self.OKBLUE + "OK" + self.ENDC)
                    elif cmd[1] == "spd" or cmd[1] == "speed":
                        self.setSpeed(int(cmd[2]), int(cmd[3]))
                        print(self.OKBLUE + "OK" + self.ENDC)

                elif cmd[0] == "get":
                    if cmd[1] == "temp":
                        value = self.getTemperature(int(cmd[2]))
                        if value >= 60 or value < 0:
                            print(self.FAIL + str(value) + self.ENDC)
                        elif value > 40:
                            print(self.WARNING + str(value) + self.ENDC)
                        else:
                            print(self.OKGREEN + str(value) + self.ENDC)
                    elif cmd[1] == "pos" or cmd[1] == "position":
                        value = self.getPosition(int(cmd[2]))
                        if value >= 0:
                            print(self.OKGREEN + str(value) + self.ENDC)
                        else:
                            print(self.FAIL + str(value) + self.ENDC)
                    elif cmd[1] == "spd" or cmd[1] == "speed":
                        value = self.getGoalSpeed(int(cmd[2]))
                        if value >= 0:
                            print(self.OKGREEN + str(value) + self.ENDC)
                        else:
                            print(self.FAIL + str(value) + self.ENDC)

            except Exception as e:
                print(self.FAIL + "ERROR", e, self.ENDC)

    def query(self, max_id=18, baud=1000000):
        k = 0                   # how many id's have we printed
        for i in range(max_id):
            if self.getPosition(i + 1) != -1:
                if k > 8:
                    k = 0
                    print("")
                print(repr(i + 1).rjust(4))
                k = k + 1
            else:
                if k > 8:
                    k = 0
                    print("")
                print("....")
                k = k + 1
            sys.stdout.flush()
        print("")

    def convertBaud(self, b):
        if b == 500000:
            return 3
        elif b == 400000:
            return 4
        elif b == 250000:
            return 7
        elif b == 200000:
            return 9
        elif b == 115200:
            return 16
        elif b == 57600:
            return 34
        elif b == 19200:
            return 103
        elif b == 9600:
            return 207
        else:
            return 1    # default to 1Mbps


def main():
    try:
        if len(sys.argv) > 2:
            t = Terminal(sys.argv[1], int(sys.argv[2]))
        elif len(sys.argv) > 1:
            t = Terminal(sys.argv[1])
        else:
            t = Terminal()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting...")


if __name__ == "__main__":
    main()
