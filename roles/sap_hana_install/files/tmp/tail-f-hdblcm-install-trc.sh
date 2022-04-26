#/bin/bash

while true; do
   ps -ef | awk '/\/usr\/sap\/hostctrl\/exe\/sapdsigner/&&!/awk/{print}'
   _HDBLCM_PID=$(ps -ef | awk '/hdblcm/&&/instlog_dir/&&!/awk/{print $2}')
   if [[ ${_HDBLCM_PID}. != "." ]]; then
      _HDBLCM_TRC_FILE=/var/tmp/hdblcm_$(ps -ef | grep hdblcm | \
        awk 'BEGIN{RS=" "}/instlog_dir/{split ($0, a, "install_"); print a[2]}')*.trc
      echo "hdblcm trace file: ${_HDBLCM_TRC_FILE}"
      tail -100f ${_HDBLCM_TRC_FILE}
   else
      echo "Still waiting for hdblcm."
   fi
   sleep 2
done
