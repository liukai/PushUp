#!/bin/sh -e

project="../chatroom"
cd $project

case "$1" in
start)
#paster serve --daemon --pid-file=paster.pid --log-file=paster.log --reload development.ini start
paster serve --daemon --pid-file=paster.pid --log-file=paster.log development.ini start
;;
stop)
paster serve --daemon --pid-file=paster.pid --log-file=paster.log  development.ini stop
;;
restart)
paster serve  --daemon --pid-file=paster.pid --log-file=paster.log development.ini restart
;;
*)
echo Usage: $0 {start|stop|restart}
exit 1
esac
