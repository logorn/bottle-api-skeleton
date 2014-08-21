bottle-api-skeleton
===================

**bottle api skeleton**

This is a skeleton framework to exploit the bottle in a restful context.
I lean on the work of Miguel Grinberg.
http://blog.miguelgrinberg.com/post/restful-authentication-with-flask

**mongodb install for ubuntu**

    apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
    echo "deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen" | tee -a /etc/apt/sources.list.d/10gen.list
    apt-get -y update
    apt-get -y install mongodb-10gen
    mongo --version
    sudo service mongodb start
    ps aux | grep mongo

**installation:**

    cd ~
    git clone https://github.com/logorn/bottle-api-skeleton
    cd bottle-api-skeleton
    mkvirtualenv -p /usr/bin/python2.7 bottle-api-skeleton
    pip install -e .
    pip install -e ."[contribute]"

destroy bottle-api-skeleton environment :

    cd bottle-api-skeleton
    deactivate
    rmvirtualenv bottle-api-skeleton

**check modules**

    pip freeze > requirements.txt
