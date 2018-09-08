#!/bin/sh
# chkconfig: 123456 90 10
#nagios_read
#
workdir=/etc/init.d

daemon_start() {
    cd $workdir
    nohup /usr/bin/python /etc/init.d/nagios_read.py &
    echo "Server started."
}

daemon_stop() {
    pid=`ps -ef | grep '[p]ython /etc/init.d/nagios_read.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    sleep 2
    echo "Server killed."
}

case "$1" in
  start)
    daemon_start
    ;;
  stop)
    daemon_stop
    ;;
  restart)
    daemon_stop
    daemon_start
    ;;
  *)
    echo "Usage: /etc/init.d/nagios_read.sh {start|stop|restart}"
    exit 1
esac
exit 0
