# Hadoop Single Node cluster powered Cloud storage in Django



## Requirements
Python 3.9.0
```
django==3.2.5
```
Hadoop 2.7.6

## How to Use
Hadoop must be installed system-wide.


`hadoop` Environment variable must be exist.

All the necessary nodes such as `Hadoop daemons, the NameNode, DataNodes, the jobtracker and tasktrackers` must be initialized before the Django server is run
(use start-all.sh or start-all.bat to do this process)

Create your own superuser to access the Database entries created during the application performs its tasks with


`python manage.py createsuperuser`

Create the folders C:/files_uploaded and D:/files_uploaded to use the local storage as a temporary environment to receive the files that every user would upload. A simple load-balancer has been implemeneted to keep both the C and D drives to be equally occupied to reduce hardware wear-out.

The file stored in this temporary location is then uploaded to a Hadoop single node cluster into the users' respective allocated folders with Python's OS calls which invoke a shell of the respective Operating Sytem to execute `hdfs` commands






