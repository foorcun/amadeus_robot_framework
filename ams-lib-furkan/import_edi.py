"""This script helps transform an EDIFACT message into a Python dictionary."""

import json
import os
import ediPath

# Register the grammars
grammar = ediPath.GrammarPool()
grammar.add_dir("edifact-verb-name" + os.sep + "grammar")

# pylint: disable=invalid-name
edifact_str = r"""UNH+1+PNRADD:14:1:1A+09AC1495'&
OPT+10'&
EMS+++NM'&
TIF+UTOD:PAX:1+NXLS:ADT'&
ODI'&
EMS++SR:1+AIR'&
TVL+120222+CDG+FRA+6X+ 501:Y'&
MSG+1'&
RPI+1+NN'&
SDT+P10'&
DUM'&
EMS+++TK'&
TKE+PAX+OK'&
EMS+++AP'&
LFT+3:5+EoT R351'&
EMS+++RF'&
LFT+3:P22+SS'&
UNT+18+1'&"""

# Transform the raw edifact message thanks to the registered grammars
edifact = grammar.read_message(edifact_str)
print(json.dumps(edifact.to_dict(), indent=4))
