# Copyright (c) 2012 The Regents of The University of Michigan
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: ICS-FORTH, Polydoros Petrakis <ppetrak@ics.forth.gr>

# Based on previous model for ARM Cortex A72 provided by Adria Armejach (BSC)
# and information from the following links regarding Cortex-A76:
# https://en.wikichip.org/wiki/arm_holdings/microarchitectures/cortex-a76
# https://www.anandtech.com/show/12785/arm-cortex-a76-cpu
#-unveiled-7nm-powerhouse/2
# https://www.anandtech.com/show/12785/arm-cortex-a76-cpu
#-unveiled-7nm-powerhouse/3

from m5.objects import *

# Simple ALU Instructions have a latency of 1
class O3_ARM_v7a_Simple_Int(FUDesc):
    opList = [ OpDesc(opClass='IntAlu', opLat=1) ]
    count = 3

# Complex ALU instructions have a variable latencies
class O3_ARM_v7a_Complex_Int(FUDesc):
    opList = [ OpDesc(opClass='IntMult', opLat=3, pipelined=True),
               OpDesc(opClass='IntDiv', opLat=12, pipelined=False),
               OpDesc(opClass='IprAccess', opLat=3, pipelined=True) ]
    count = 2

# Floating point
class O3_ARM_v7a_FP(FUDesc):
    opList = [ OpDesc(opClass='FloatAdd', opLat=5),
               OpDesc(opClass='FloatCmp', opLat=5),
               OpDesc(opClass='FloatCvt', opLat=5),
               OpDesc(opClass='FloatDiv', opLat=9, pipelined=False),
               OpDesc(opClass='FloatSqrt', opLat=33, pipelined=False),
               OpDesc(opClass='FloatMult', opLat=4),
               OpDesc(opClass='FloatMultAcc', opLat=5),
               OpDesc(opClass='FloatMisc', opLat=3) ]
    count = 2
    widthCap = 128
    floatp = True

# SIMD instructions
class O3_ARM_v7a_AdvSimd(FUDesc):
    opList = [ OpDesc(opClass='SimdAdd', opLat=4),
               OpDesc(opClass='SimdAddAcc', opLat=4),
               OpDesc(opClass='SimdAlu', opLat=4),
               OpDesc(opClass='SimdCmp', opLat=4),
               OpDesc(opClass='SimdCvt', opLat=3),
               OpDesc(opClass='SimdMisc', opLat=3),
               OpDesc(opClass='SimdMult',opLat=5),
               OpDesc(opClass='SimdMultAcc',opLat=5),
               OpDesc(opClass='SimdShift',opLat=3),
               OpDesc(opClass='SimdShiftAcc', opLat=3),
               OpDesc(opClass='SimdDiv', opLat=9, pipelined=False),
               OpDesc(opClass='SimdSqrt', opLat=9),
               OpDesc(opClass='SimdFloatAdd',opLat=5),
               OpDesc(opClass='SimdFloatAlu',opLat=5),
               OpDesc(opClass='SimdFloatCmp', opLat=3),
               OpDesc(opClass='SimdFloatCvt', opLat=3),
               OpDesc(opClass='SimdFloatDiv', opLat=3),
               OpDesc(opClass='SimdFloatMisc', opLat=3),
               OpDesc(opClass='SimdFloatMult', opLat=3),
               OpDesc(opClass='SimdFloatMultAcc',opLat=5),
               OpDesc(opClass='SimdFloatSqrt', opLat=9),
               OpDesc(opClass='SimdReduceAdd'),
               OpDesc(opClass='SimdReduceAlu'),
               OpDesc(opClass='SimdReduceCmp'),
               OpDesc(opClass='SimdFloatReduceAdd'),
               OpDesc(opClass='SimdFloatReduceCmp') ]
    count = 2
    fuseCap = 3
    widthCap = 128
    simd = True


# Load/Store Units
class O3_ARM_v7a_Load(FUDesc):
    opList = [ OpDesc(opClass='MemRead'),
               OpDesc(opClass='FloatMemRead') ]
    count = 2
    widthCap = 128

class O3_ARM_v7a_Store(FUDesc):
    opList = [ OpDesc(opClass='MemWrite'),
               OpDesc(opClass='FloatMemWrite') ]
    count = 1
    widthCap = 128

class O3_ARM_v7a_PredALU(FUDesc):
    opList = [ OpDesc(opClass='SimdPredAlu') ]
    count = 1
    widthCap = 128

# Functional Units for this CPU
class ARM_Cortex_A76_FUP(FUPool):
    FUList = [O3_ARM_v7a_Simple_Int(),
              O3_ARM_v7a_Complex_Int(),
              O3_ARM_v7a_Load(),
              O3_ARM_v7a_Store(),
              O3_ARM_v7a_PredALU(),
              O3_ARM_v7a_FP(),
              O3_ARM_v7a_AdvSimd()]

# Bi-Mode Branch Predictor
class O3_ARM_v7a_BP(BiModeBP):
    globalPredictorSize = 8192
    globalCtrBits = 2
    choicePredictorSize = 8192
    choiceCtrBits = 2
    BTBEntries = 4096
    BTBTagSize = 16
    RASSize = 16
    instShiftAmt = 2

class O3_ARM_v7a_3(DerivO3CPU):
    LQEntries = 68
    SQEntries = 72
    LSQDepCheckShift = 0
    LFSTSize = 1024
    SSITSize = 1024
    decodeToFetchDelay = 1
    renameToFetchDelay = 1
    iewToFetchDelay = 1
    commitToFetchDelay = 1
    renameToDecodeDelay = 1
    iewToDecodeDelay = 1
    commitToDecodeDelay = 1
    iewToRenameDelay = 1
    commitToRenameDelay = 1
    commitToIEWDelay = 1
    fetchWidth = 4
    fetchBufferSize = 16
    fetchToDecodeDelay = 1
    decodeWidth = 4
    decodeToRenameDelay = 1
    renameWidth = 4
    renameToIEWDelay = 1
    issueToExecuteDelay = 1
    dispatchWidth = 8
    issueWidth = 8
    wbWidth = 8
    fuPool = ARM_Cortex_A76_FUP()
    iewToCommitDelay = 1
    renameToROBDelay = 1
    commitWidth = 8
    squashWidth = 8
    trapLatency = 13
    backComSize = 5
    forwardComSize = 5
    numPhysIntRegs = 256
    numPhysFloatRegs = 256
    numPhysPredRegs = 32
    numPhysVecRegs = 256
    numIQEntries = 120
    numROBEntries = 192

    switched_out = False
    # branchPred = ARM_Cortex_A76_BP()
    branchPred = Param.BranchPredictor(TournamentBP(
        numThreads = Parent.numThreads), "Branch Predictor")

# Instruction Cache
class O3_ARM_v7a_ICache(Cache):
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 8
    tgts_per_mshr = 8
    size = '64kB'
    assoc = 4
    is_read_only = True
    # Writeback clean lines as well
    writeback_clean = True

# Data Cache
class O3_ARM_v7a_DCache(Cache):
    tag_latency = 2
    data_latency = 2
    response_latency = 1
    mshrs = 24
    tgts_per_mshr = 16
    size = '64kB'
    assoc = 4
    write_buffers = 24
    # Consider the L2 a victim cache also for clean lines
    writeback_clean = True

# TLB Cache
# Use a cache as a L2 TLB
class O3_ARM_v7aWalkCache(Cache):
    tag_latency = 4
    data_latency = 4
    response_latency = 4
    mshrs = 6
    tgts_per_mshr = 8
    size = '1kB'
    assoc = 8
    write_buffers = 16
    is_read_only = True
    # Writeback clean lines as well
    writeback_clean = True

# L2 Cache
class O3_ARM_v7aL2(Cache):
    tag_latency = 9
    data_latency = 9
    response_latency = 5
    mshrs = 24
    tgts_per_mshr = 16
    size = '256kB'
    assoc = 8
    write_buffers = 24
    prefetch_on_access = True
    clusivity = 'mostly_incl'
    # Simple stride prefetcher
    prefetcher = StridePrefetcher(degree=8, latency = 1)
    tags = BaseSetAssoc()
    repl_policy = RandomRP()