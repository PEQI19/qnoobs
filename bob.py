#
# Copyright (c) 2017, Stephanie Wehner and Axel Dahlberg
# All rights reserved.
#
# Copyright (c) 2019, Audrey Boixel, Alain Chancé, Daniel Mills and Antoine Sinton
# All rights reserved.  
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#    This product includes software developed by Stephanie Wehner, QuTech.
# 4. Neither the name of the QuTech organization nor the
#    names of its contributors may be used to endorse or promote products
#    derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDER ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# adapted from https://github.com/SoftwareQuTech/CQC-Python/blob/master/examples/pythonLib/extendGHZ/bobTest.py

from cqc.pythonLib import CQCConnection, qubit
from random import randint


def main(agents):
    print("running Bob")

    # Initialize the connection
    with CQCConnection(agents[1]) as Bob:

        # Make an EPR pair with Alice
        qB = Bob.recvEPR()


        for agent in agents[2:]:
            # Create a fresh qubit
            qC = qubit(Bob)

            # Entangle the new qubit
            qB.cnot(qC)

            # Send qubit to Charlie
            Bob.sendQubit(qC, agent)

        mCharlies = []
        for charlie in agents[2:]:
            mCharlies.append(list(Bob.recvClassical())[0])

        bp = randint(0, 1)
        b = list(Bob.recvClassical())[0]

        if (bp + sum(mCharlies)) % 2 == 1:
            qB.Z()



        data = Bob.recvClassical()
        message = list(data)
        
        a = message[0]
        b = message[1]

        # Apply corrections
        if b == 1:
            qB.X()
        if a == 1:
            qB.Z()

            # Measure qubit

        m = qB.measure()

        print("Bob received message", m)

if __name__ == "__main__":
    main()
