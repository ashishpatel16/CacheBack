#!/bin/bash
su -l postgres -c /usr/pgsql-11/bin/initdb
su -l postgres -c "/usr/pgsql-11/bin/pg_ctl -D /var/lib/pgsql/11/data -l /tmp/pg_logfile start"
createdb -U postgres baeldung