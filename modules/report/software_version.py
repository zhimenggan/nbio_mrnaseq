#!/usr/bin/env python
import readline  # workaround for import rpy2 error
import re
import sys
import subprocess
from rpy2 import robjects
from collections import OrderedDict
import pandas as pd

output = sys.argv[1]

softwares = OrderedDict()

softwares["Pipeline"] = 'r20151102'
skewer_ver =  subprocess.check_output('echo `/mnt/software/skewer -v`', shell=True)
softwares["skewer"]=filter(None, re.split("[: ]+", skewer_ver))[2]
star_ver = subprocess.check_output("/mnt/software/STAR-dir/STAR-2.4.2a/STAR --version", stderr=subprocess.STDOUT, shell=True)
softwares["STAR"] = star_ver.split("_")[1]
rsem_ver = subprocess.check_output("/mnt/software/rsem-dir/rsem-1.2.22/rsem-calculate-expression -version", shell=True)
softwares["RSEM"] = rsem_ver.split()[-1]

version = robjects.r("""
function (p) {
     paste(packageVersion(p),collapse=".")
}""")
softwares["R"] = list(version("base"))[0]
softwares["EdgeR"] = list(version("edgeR"))[0]
softwares["EBSeq"] = list(version("EBSeq"))[0]

softwares_df = pd.DataFrame(softwares, index = [0]).T
softwares_df.columns=['Version']
softwares_html = softwares_df.to_html(classes="table table-bordered table-hover", escape=False)
with open(output, 'w') as f_out:
    f_out.write(softwares_html)
