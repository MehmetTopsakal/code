#!/usr/bin/env python




### USAGE:
### import CONFS
### 
### confs = CONFS.confs_sel('0 1')
### 
### 
### 
#### ========================================================

confs_all = []

confs_all.append("""\
0 0 0 0 0 0 0
""")

confs_all.append("""\
1 0 0 0 0 0 0
0 1 0 0 0 0 0
0 0 1 0 0 0 0
0 0 0 1 0 0 0
0 0 0 0 1 0 0
0 0 0 0 0 1 0
0 0 0 0 0 0 1
""")

confs_all.append("""\
0 0 0 0 0 1 1
0 0 0 0 1 0 1
0 0 0 0 1 1 0
0 0 0 1 0 0 1
0 0 0 1 0 1 0
0 0 0 1 1 0 0
0 0 1 0 0 0 1
0 0 1 0 0 1 0
0 0 1 0 1 0 0
0 0 1 1 0 0 0
0 1 0 0 0 0 1
0 1 0 0 0 1 0
0 1 0 0 1 0 0
0 1 0 1 0 0 0
0 1 1 0 0 0 0
0 1 0 0 0 0 1
0 1 0 0 0 1 0
0 1 0 0 1 0 0
0 1 0 1 0 0 0
0 1 1 0 0 0 0
0 1 1 0 0 0 0
""")

confs_all.append("""\
0 0 0 0 1 1 1
0 0 0 1 0 1 1
0 0 0 1 1 0 1
0 0 0 1 1 1 0
0 0 1 0 0 1 1
0 0 1 0 1 0 1
0 0 1 0 1 1 0
0 0 1 1 0 0 1
0 0 1 1 0 1 0
0 0 1 1 1 0 0
0 1 0 0 0 1 1
0 1 0 0 1 0 1
0 1 0 0 1 1 0
0 1 0 1 0 0 1
0 1 0 1 0 1 0
0 1 0 1 1 0 0
0 1 1 0 0 0 1
0 1 1 0 0 1 0
0 1 1 0 1 0 0
0 1 1 1 0 0 0
1 0 0 0 0 1 1
1 0 0 0 1 0 1
1 0 0 0 1 1 0
1 0 0 1 0 0 1
1 0 0 1 0 1 0
1 0 0 1 1 0 0
1 0 1 0 0 0 1
1 0 1 0 0 1 0
1 0 1 0 1 0 0
1 0 1 1 0 0 0
1 1 0 0 0 0 1
1 1 0 0 0 1 0
1 1 0 0 1 0 0
1 1 0 1 0 0 0
1 1 1 0 0 0 0
""")

confs_all.append("""\
1 1 1 1 0 0 0
1 1 1 0 1 0 0
1 1 1 0 0 1 0
1 1 1 0 0 0 1
1 1 0 1 1 0 0
1 1 0 1 0 1 0
1 1 0 1 0 0 1
1 1 0 0 1 1 0
1 1 0 0 1 0 1
1 1 0 0 0 1 1
1 0 1 1 1 0 0
1 0 1 1 0 1 0
1 0 1 1 0 0 1
1 0 1 0 1 1 0
1 0 1 0 1 0 1
1 0 1 0 0 1 1
1 0 0 1 1 1 0
1 0 0 1 1 0 1
1 0 0 1 0 1 1
1 0 0 0 1 1 1
0 1 1 1 1 0 0
0 1 1 1 0 1 0
0 1 1 1 0 0 1
0 1 1 0 1 1 0
0 1 1 0 1 0 1
0 1 1 0 0 1 1
0 1 0 1 1 1 0
0 1 0 1 1 0 1
0 1 0 1 0 1 1
0 1 0 0 1 1 1
0 0 1 1 1 1 0
0 0 1 1 1 0 1
0 0 1 1 0 1 1
0 0 1 0 1 1 1
0 0 0 1 1 1 1
""")

confs_all.append("""\
1 1 1 1 1 0 0
1 1 1 1 0 1 0
1 1 1 1 0 0 1
1 1 1 0 1 1 0
1 1 1 0 1 0 1
1 1 1 0 0 1 1
1 1 0 1 1 1 0
1 1 0 1 1 0 1
1 1 0 1 0 1 1
1 1 0 0 1 1 1
1 0 1 1 1 1 0
1 0 1 1 1 0 1
1 0 1 1 0 1 1
1 0 1 0 1 1 1
1 0 0 1 1 1 1
1 0 1 1 1 1 0
1 0 1 1 1 0 1
1 0 1 1 0 1 1
1 0 1 0 1 1 1
1 0 0 1 1 1 1
1 0 0 1 1 1 1
""")

confs_all.append("""\
0 1 1 1 1 1 1
1 0 1 1 1 1 1
1 1 0 1 1 1 1
1 1 1 0 1 1 1
1 1 1 1 0 1 1
1 1 1 1 1 0 1
1 1 1 1 1 1 0
""")

confs_all.append("""\
1 1 1 1 1 1 1
""")







def confs_sel(sel):
    
    sel = sel.split()

    confs_selected = ''

    for s in sel:
        confs_selected = ''.join( [confs_selected, confs_all[int(s)]] )

    return confs_selected.splitlines()

