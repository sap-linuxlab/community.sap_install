#!/bin/bash

while true; do
# in case hdblcm has not yet started, we assume that it is waiting for sapdsigner to complete:
   ps -ef | awk '/\/usr\/sap\/hostctrl\/exe\/sapdsigner/&&!/awk/{print}'
   _HDBLCM_PID=$(ps -ef | awk '/hdblcm/&&/instlog_dir/&&!/awk/{print $2}')
   if [[ ${_HDBLCM_PID}. != "." ]]; then
# skip SC2046: No need to quote at "$(ps" because the awk statement should take
#                care of preventing word splitting
# skip SC2125: We are using braces inside awk, not inside the shell.
# shellcheck disable=SC2046,SC2125
      _HDBLCM_TRC_FILE=$(echo /var/tmp/hdblcm_$(ps -ef | awk '/hdblcm/{print}' | \
        awk 'BEGIN{RS=" "}/instlog_dir/{split ($0, a, "install_"); print a[2]}')*.trc)
      echo "hdblcm trace file: ${_HDBLCM_TRC_FILE}"
      tail -100f "${_HDBLCM_TRC_FILE}"
   else
      echo "Still waiting for hdblcm."
   fi
   sleep 2
done
