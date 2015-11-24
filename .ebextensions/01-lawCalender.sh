files:
  "/opt/elasticbeanstalk/hooks/appdeploy/post/run_supervised_celeryd.sh":
    mode: "000755"
    owner: root
    group: root
    content: |
      #!/usr/bin/env bash

      # Get django environment variables
      celeryenv=`cat /opt/python/current/env | tr '\n' ',' | sed 's/%/%%/g' | sed 's/export //g' | sed 's/$PATH/%(ENV_PATH)s/g' | sed 's/$PYTHONPATH//g' | sed 's/$LD_LIBRARY_PATH//g'`
      celeryenv=${celeryenv%?}

      # Create celery configuraiton script
      celeryconf="[program:celeryd]
      ; Set full path to celery program if using virtualenv
      command=/opt/python/run/venv/bin/celery worker -A lawCalender --loglevel=INFO

      directory=/opt/python/current/app
      user=nobody
      numprocs=1
      stdout_logfile=/var/log/celery-worker.log
      stderr_logfile=/var/log/celery-worker.log
      autostart=true
      autorestart=true
      startsecs=10

      ; Need to wait for currently executing tasks to finish at shutdown.
      ; Increase this if you have very long running tasks.
      stopwaitsecs = 600

      ; When resorting to send SIGKILL to the program to terminate it
      ; send SIGKILL to its whole process group instead,
      ; taking care of its children as well.
      killasgroup=true

      ; if rabbitmq is supervised, set its priority higher
      ; so it starts first
      priority=998

      environment=$celeryenv"

       # Create celerybeat configuraiton script
	  celerybeatconf="[program:celerybeat]
	  ; Set full path to celery program if using virtualenv
	  command=/opt/python/current/app/manage.py celery beat -A avtotest --loglevel=INFO

	  ; remove the -A avtotest argument if you are not using an app instance

	  directory=/opt/python/current/app
	  user=nobody
	  numprocs=1
	  stdout_logfile=/var/log/celerybeat.log
	  stderr_logfile=/var/log/celerybeat.log
	  autostart=true
	  autorestart=true
	  startsecs=10

	  ; Need to wait for currently executing tasks to finish at shutdown.
	  ; Increase this if you have very long running tasks.
	  stopwaitsecs = 600

	  ; When resorting to send SIGKILL to the program to terminate it
	  ; send SIGKILL to its whole process group instead,
	  ; taking care of its children as well.
	  killasgroup=true

	  ; if rabbitmq is supervised, set its priority higher
	  ; so it starts first
	  priority=999

  environment=$celeryenv"

      # Create the celery supervisord conf script
      echo "$celeryconf" | tee /opt/python/etc/celery.conf

      # Add configuration script to supervisord conf (if not there already)
      if ! grep -Fxq "[include]" /opt/python/etc/supervisord.conf
          then
          echo "[include]" | tee -a /opt/python/etc/supervisord.conf
          echo "files: celery.conf" | tee -a /opt/python/etc/supervisord.conf
      fi

      # Reread the supervisord config
      supervisorctl -c /opt/python/etc/supervisord.conf reread

      # Update supervisord in cache without restarting all services
      supervisorctl -c /opt/python/etc/supervisord.conf update

      # Start/Restart celeryd through supervisord
      supervisorctl -c /opt/python/etc/supervisord.conf restart celeryd