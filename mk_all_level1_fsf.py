""" mk_all_level1_fsf.py - make fsf files for all subjects
"""

## Copyright 2011, Russell Poldrack. All rights reserved.

## Redistribution and use in source and binary forms, with or without modification, are
## permitted provided that the following conditions are met:

##    1. Redistributions of source code must retain the above copyright notice, this list of
##       conditions and the following disclaimer.

##    2. Redistributions in binary form must reproduce the above copyright notice, this list
##       of conditions and the following disclaimer in the documentation and/or other materials
##       provided with the distribution.

## THIS SOFTWARE IS PROVIDED BY RUSSELL POLDRACK ``AS IS'' AND ANY EXPRESS OR IMPLIED
## WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
## FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL RUSSELL POLDRACK OR
## CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
## CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
## SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
## ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
## NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
## ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import os
from mk_level1_fsf import *
dataset='ds001'
basedir='/corral/utexas/poldracklab/openfmri/staged/'
outfile=open('mk_all_level1_fsf.sh','w')

smoothing=6
tr=2.0
use_inplane=1

for root,dirs,files in os.walk(basedir):
    for f in files:
        if f.rfind('bold_mcf.nii.gz')>-1 and root.find(dataset)>-1:
            f_split=root.split('/')
            scankey='/'+'/'.join(f_split[1:7])+'/scan_key.txt'
            taskid=f_split[6]
            subnum=int(f_split[7].lstrip('sub'))
            taskinfo=f_split[9].split('_')
            tasknum=int(taskinfo[0].lstrip('task'))
            runnum=int(taskinfo[1].lstrip('run'))
            tr=float(load_scankey(scankey)['TR'])
            # check for inplane
            inplane='/'+'/'.join(f_split[1:8])+'/anatomy/inplane001_brain.nii.gz'
            if os.path.exists(inplane):
                use_inplane=1
            else:
                use_inplane=0
            print 'mk_fsf("%s",%d,%d,%d,%d,%f,%d,"%s")'%(taskid,subnum,tasknum,runnum,smoothing,tr,use_inplane,basedir)
            mk_level1_fsf(taskid,subnum,tasknum,runnum,smoothing,tr,use_inplane,basedir)

outfile.close()

print 'now run all feats using:'
print "find ds*/sub*/model/*.fsf |sed 's/^/feat /' > run_all_feats.sh; sh run_all_feats.sh"
            
