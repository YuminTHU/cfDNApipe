# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 10:38:07 2019

@author: zhang
"""




import cfDNA_utils
import StepBase
import Configure
import Fun_inputProcess, Fun_fastqc, Fun_identifyAdapter, Fun_adapterremoval
import Fun_bowtie2, Fun_bismark, Fun_bamsort, Fun_rmDuplicate
from importlib import reload
reload(cfDNA_utils)
reload(StepBase)
reload(Fun_inputProcess)
reload(Fun_fastqc)
reload(Fun_identifyAdapter)
reload(Fun_adapterremoval)
reload(Fun_bowtie2)
reload(Fun_bamsort)
reload(Fun_rmDuplicate)

Configure.Configure.setGenome("hg19")
Configure.Configure.setRefDir(r'/home/wzhang/genome/hg19')
Configure.Configure.setThreads(5)
Configure.Configure.setOutDir(r'/home/wzhang/test')
Configure.Configure.pipeFolderInit()


res1 = Fun_inputProcess.inputprocess(inputFolder = r"/home/wzhang/test/inputs")
res2 = Fun_fastqc.fastqc(upstream = res1)
res3 = Fun_identifyAdapter.identifyAdapter(upstream = res1, formerrun = res2)
res4 = Fun_adapterremoval.adapterremoval(upstream = res3)
res5 = Fun_bowtie2.bowtie2(upstream = res4)
res6 = Fun_bamsort.bamsort(upstream = res5)
res7 = Fun_rmDuplicate.rmduplicate(upstream = res6)



Configure.Configure.setGenome("hg19")
Configure.Configure.setRefDir(r'/home/wzhang/genome/hg19_bismark')
Configure.Configure.setThreads(20)
Configure.Configure.setOutDir(r'/home/wzhang/test')
Configure.Configure.pipeFolderInit()


res1 = Fun_inputProcess.inputprocess(inputFolder = r"/home/wzhang/test/bsinputs")
res2 = Fun_fastqc.fastqc(upstream = res1)
res3 = Fun_identifyAdapter.identifyAdapter(upstream = res1, formerrun = res2)
res4 = Fun_adapterremoval.adapterremoval(upstream = res3)
res5 = Fun_bismark.bismark(upstream = res4)
res6 = Fun_bamsort.bamsort(upstream = res5)
res7 = Fun_rmDuplicate.rmduplicate(upstream = res6)



