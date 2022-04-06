#!/bin/bash

# default font color: Light Cyan, which should be readable on both bright and dark background
__FONT_COLOR=36m

if [[ ${1}. == "font_light_gray". ]]; then
   __FONT_COLOR=37m
elif [[ ${1}. == "font_no_color". ]]; then
   __FONT_COLOR=30m
fi

if [[ ${2}. == "reset." ]]; then
   awk 'BEGIN{printf ("\033['${__FONT_COLOR}'Resetting font color\n")}'
   exit
fi

awk '{sub ("    \"msg\": ", "")}
  /TASK/{task_line=$0}
  /fatal:/{fatal_line=$0; nfatal[host]++}
  /...ignoring/{nfatal[host]--; if (nfatal[host]<0) nfatal[host]=0}
  /^[a-z]/&&/: \[/{gsub ("\\[", ""); gsub ("]", ""); gsub (":", ""); host=$2}
  /SAP note/{print "\033['${__FONT_COLOR}'[" host"] "$0}
  /FAIL:/{nfail[host]++; print "\033[31m[" host"] "$0}
  /WARN:/{nwarn[host]++; print "\033[33m[" host"] "$0}
  /PASS:/{npass[host]++; print "\033[32m[" host"] "$0}
  /INFO:/{print "\033[34m[" host"] "$0}
  /changed/&&/unreachable/{print "\033['${__FONT_COLOR}'[" host"] "$0}
  END{print ("---"); for (var in npass) {printf ("[%s] ", var); if (nfatal[var]>0) {
        printf ("\033[31mFATAL ERROR!!! Playbook might have been aborted!!!\033['${__FONT_COLOR}' Last TASK and fatal output:\n"); print task_line, fatal_line
        exit 199
     }
     else printf ("\033[31mFAIL: %d  \033[33mWARN: %d  \033[32mPASS: %d\033['${__FONT_COLOR}'\n", nfail[var], nwarn[var], npass[var])}
     if (nfail[var] != 0) exit (nfail[var])
  }'
