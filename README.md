bottle-api-skeleton
===================

* Info: Minimal rest skeleton build on top of bottle micro-framework.
* Author: Hugues MAILLET (maillet.hugues.dev@gmail.com)

About bottle api skeleton
-------------------------

``BAS`` for ``bottle-api-skeleton``  is a skeleton framework to exploit the bottle micro-framework in a restful context.
I lean on the work of Miguel Grinberg.
http://blog.miguelgrinberg.com/post/restful-authentication-with-flask

The aim is to bottle covered the basics of setting up a project to rest beings piloted on android and other platform.

## Features

* standard rest api
* mvc oriented and object oriented
* exploit mongo db to store data
* basic authentication
* token and public key with token authentication
* multithread using gevent
* token are encrypted

Requirements
------------

* ubuntu or debian distribution
* mongodb install for ubuntu    
* curl

Ubuntu MongoDb installation:
----------------------------

    apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10
    echo "deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen" | tee -a /etc/apt/sources.list.d/10gen.list
    apt-get -y update
    apt-get -y install mongodb-10gen
    mongo --version
    sudo service mongodb start
    ps aux | grep mongo

Installation application and dependencies:
------------------------------------------

    cd ~
    git clone https://github.com/logorn/bottle-api-skeleton
    cd bottle-api-skeleton
    mkvirtualenv -p /usr/bin/python2.7 bottle-api-skeleton
    pip install -e .
    pip install -e ."[contribute]"
    workon bottle-api-skeleton

Run server:
----------

    python run.py

Example curl command
--------------------

sign up:

	curl -i -H "Content-Type: application/json; charset=UTF-8" -X POST -d '{"username":"Jason", "password":"abc"}' http://localhost:8080/api/v1.0/signup

sign in:

	curl -i -H "Content-Type: application/json; charset=UTF-8" -X POST -d '{"username":"Jason", "name": "Jason Borne", "password":"abc"}' http://localhost:8080/api/v1.0/login

basic authentication:

	curl -i -H "Content-Type: application/json; charset=UTF-8" -X GET  http://localhost:8080/api/v1.0/basicauth -u Jason:abc

session test (not neded here):

	curl -i -H "Content-Type: application/json; charset=UTF-8" -X GET  http://localhost:8080/api/v1.0/session

authentication token generator:

	curl -i -H "Content-Type: application/json; charset=UTF-8" -X GET  http://localhost:8080/api/v1.0/token -u Jason:abc

insert document:

	curl -H "Authorization: ApiAuth 9ebd226b1207473a92dc1f433343044e:MIc4xtC1/VdsX2N0JDS8y4HIIzC4IMBDf41+se6zZasTMeNaK7rqowRWUCYPFKfRcwnlO8bebLJ0AANRGhfkwxHl5j9QDDiV26RnJFCTrLgabmDnIanpCeCaT8S/epB6UBO5wd1o5ZSS09O2dgNBgte4vveYjnaBy5iY5K7RFQlPLzBYJbwpHh0s2DiPDExoQPOzvexZMgl5h4M+x+jQWUcnhIvneeVTjNdbjY+/dv2C+gNzXDnHv2G/BlJKt1K81NtxOMhM/uShOkrkTUDi480ZUCZzf2SB8n0kcfas43I69jj55KM4MeeUbgzllh6oPm7d5mNSIapze+hjsowH1q4TZ/Zatye4T5OiRECmZ8USi7RzYeH6plUKSEGWfiwnLwIkiOzigV+GBqqulS94yg==" -i -H "Accept: application/json" -X POST -d '{"_id": "doc1", "name": "Test Document 1"}' http://localhost:8080/api/v1.0/documents

	curl -H "Authorization: ApiAuth 9ebd226b1207473a92dc1f433343044e:MIc4xtC1/VdsX2N0JDS8y4HIIzC4IMBDf41+se6zZasTMeNaK7rqowRWUCYPFKfRcwnlO8bebLJ0AANRGhfkwxHl5j9QDDiV26RnJFCTrLgabmDnIanpCeCaT8S/epB6UBO5wd1o5ZSS09O2dgNBgte4vveYjnaBy5iY5K7RFQlPLzBYJbwpHh0s2DiPDExoQPOzvexZMgl5h4M+x+jQWUcnhIvneeVTjNdbjY+/dv2C+gNzXDnHv2G/BlJKt1K81NtxOMhM/uShOkrkTUDi480ZUCZzf2SB8n0kcfas43I69jj55KM4MeeUbgzllh6oPm7d5mNSIapze+hjsowH1q4TZ/Zatye4T5OiRECmZ8USi7RzYeH6plUKSEGWfiwnLwIkiOzigV+GBqqulS94yg==" -i -H "Content-Type: application/json; charset=UTF-8" -X POST -d '{"_id": "doc1", "name": "Test Document 1"}' http://localhost:8080/api/v1.0/documents

	curl -H "Authorization: ApiAuth 9ebd226b1207473a92dc1f433343044e:MIc4xtC1/VdsX2N0JDS8y4HIIzC4IMBDf41+se6zZasTMeNaK7rqowRWUCYPFKfRcwnlO8bebLJ0AANRGhfkwxHl5j9QDDiV26RnJFCTrLgabmDnIanpCeCaT8S/epB6UBO5wd1o5ZSS09O2dgNBgte4vveYjnaBy5iY5K7RFQlPLzBYJbwpHh0s2DiPDExoQPOzvexZMgl5h4M+x+jQWUcnhIvneeVTjNdbjY+/dv2C+gNzXDnHv2G/BlJKt1K81NtxOMhM/uShOkrkTUDi480ZUCZzf2SB8n0kcfas43I69jj55KM4MeeUbgzllh6oPm7d5mNSIapze+hjsowH1q4TZ/Zatye4T5OiRECmZ8USi7RzYeH6plUKSEGWfiwnLwIkiOzigV+GBqqulS94yg==" -i -H "Accept: application/json" -X POST -d '{"_id": "doc2", "name": "Other Document send"}' http://localhost:8080/api/v1.0/documents

update document:

	curl -H "Authorization: ApiAuth 9ebd226b1207473a92dc1f433343044e:MIc4xtC1/VdsX2N0JDS8y4HIIzC4IMBDf41+se6zZasTMeNaK7rqowRWUCYPFKfRcwnlO8bebLJ0AANRGhfkwxHl5j9QDDiV26RnJFCTrLgabmDnIanpCeCaT8S/epB6UBO5wd1o5ZSS09O2dgNBgte4vveYjnaBy5iY5K7RFQlPLzBYJbwpHh0s2DiPDExoQPOzvexZMgl5h4M+x+jQWUcnhIvneeVTjNdbjY+/dv2C+gNzXDnHv2G/BlJKt1K81NtxOMhM/uShOkrkTUDi480ZUCZzf2SB8n0kcfas43I69jj55KM4MeeUbgzllh6oPm7d5mNSIapze+hjsowH1q4TZ/Zatye4T5OiRECmZ8USi7RzYeH6plUKSEGWfiwnLwIkiOzigV+GBqqulS94yg==" -i -H "Accept: application/json" -X PUT -d '{"_id": "doc1", "name": "Test Document 2"}' http://localhost:8080/api/v1.0/documents/doc1

	curl -H "Authorization: ApiAuth 9ebd226b1207473a92dc1f433343044e:MIc4xtC1/VdsX2N0JDS8y4HIIzC4IMBDf41+se6zZasTMeNaK7rqowRWUCYPFKfRcwnlO8bebLJ0AANRGhfkwxHl5j9QDDiV26RnJFCTrLgabmDnIanpCeCaT8S/epB6UBO5wd1o5ZSS09O2dgNBgte4vveYjnaBy5iY5K7RFQlPLzBYJbwpHh0s2DiPDExoQPOzvexZMgl5h4M+x+jQWUcnhIvneeVTjNdbjY+/dv2C+gNzXDnHv2G/BlJKt1K81NtxOMhM/uShOkrkTUDi480ZUCZzf2SB8n0kcfas43I69jj55KM4MeeUbgzllh6oPm7d5mNSIapze+hjsowH1q4TZ/Zatye4T5OiRECmZ8USi7RzYeH6plUKSEGWfiwnLwIkiOzigV+GBqqulS94yg==" -i -H "Content-Type: application/json; charset=UTF-8" -X PUT -d '{"_id": "doc1", "name": "Test Document 2"}' http://localhost:8080/api/v1.0/documents/doc1

get documents:

	curl -H "Authorization: ApiAuth 9ebd226b1207473a92dc1f433343044e:MIc4xtC1/VdsX2N0JDS8y4HIIzC4IMBDf41+se6zZasTMeNaK7rqowRWUCYPFKfRcwnlO8bebLJ0AANRGhfkwxHl5j9QDDiV26RnJFCTrLgabmDnIanpCeCaT8S/epB6UBO5wd1o5ZSS09O2dgNBgte4vveYjnaBy5iY5K7RFQlPLzBYJbwpHh0s2DiPDExoQPOzvexZMgl5h4M+x+jQWUcnhIvneeVTjNdbjY+/dv2C+gNzXDnHv2G/BlJKt1K81NtxOMhM/uShOkrkTUDi480ZUCZzf2SB8n0kcfas43I69jj55KM4MeeUbgzllh6oPm7d5mNSIapze+hjsowH1q4TZ/Zatye4T5OiRECmZ8USi7RzYeH6plUKSEGWfiwnLwIkiOzigV+GBqqulS94yg==" -i -H "Accept: application/json" -X GET http://localhost:8080/api/v1.0/documents

	curl -H "Authorization: ApiAuth 9ebd226b1207473a92dc1f433343044e:MIc4xtC1/VdsX2N0JDS8y4HIIzC4IMBDf41+se6zZasTMeNaK7rqowRWUCYPFKfRcwnlO8bebLJ0AANRGhfkwxHl5j9QDDiV26RnJFCTrLgabmDnIanpCeCaT8S/epB6UBO5wd1o5ZSS09O2dgNBgte4vveYjnaBy5iY5K7RFQlPLzBYJbwpHh0s2DiPDExoQPOzvexZMgl5h4M+x+jQWUcnhIvneeVTjNdbjY+/dv2C+gNzXDnHv2G/BlJKt1K81NtxOMhM/uShOkrkTUDi480ZUCZzf2SB8n0kcfas43I69jj55KM4MeeUbgzllh6oPm7d5mNSIapze+hjsowH1q4TZ/Zatye4T5OiRECmZ8USi7RzYeH6plUKSEGWfiwnLwIkiOzigV+GBqqulS94yg==" -i -H "Content-Type: application/json; charset=UTF-8" -X GET http://localhost:8080/api/v1.0/documents

get specific document by id:

	curl -H "Authorization: ApiAuth 9ebd226b1207473a92dc1f433343044e:MIc4xtC1/VdsX2N0JDS8y4HIIzC4IMBDf41+se6zZasTMeNaK7rqowRWUCYPFKfRcwnlO8bebLJ0AANRGhfkwxHl5j9QDDiV26RnJFCTrLgabmDnIanpCeCaT8S/epB6UBO5wd1o5ZSS09O2dgNBgte4vveYjnaBy5iY5K7RFQlPLzBYJbwpHh0s2DiPDExoQPOzvexZMgl5h4M+x+jQWUcnhIvneeVTjNdbjY+/dv2C+gNzXDnHv2G/BlJKt1K81NtxOMhM/uShOkrkTUDi480ZUCZzf2SB8n0kcfas43I69jj55KM4MeeUbgzllh6oPm7d5mNSIapze+hjsowH1q4TZ/Zatye4T5OiRECmZ8USi7RzYeH6plUKSEGWfiwnLwIkiOzigV+GBqqulS94yg==" -i -H "Accept: application/json" -X GET http://localhost:8080/api/v1.0/documents/doc1

	curl -H "Authorization: ApiAuth 9ebd226b1207473a92dc1f433343044e:MIc4xtC1/VdsX2N0JDS8y4HIIzC4IMBDf41+se6zZasTMeNaK7rqowRWUCYPFKfRcwnlO8bebLJ0AANRGhfkwxHl5j9QDDiV26RnJFCTrLgabmDnIanpCeCaT8S/epB6UBO5wd1o5ZSS09O2dgNBgte4vveYjnaBy5iY5K7RFQlPLzBYJbwpHh0s2DiPDExoQPOzvexZMgl5h4M+x+jQWUcnhIvneeVTjNdbjY+/dv2C+gNzXDnHv2G/BlJKt1K81NtxOMhM/uShOkrkTUDi480ZUCZzf2SB8n0kcfas43I69jj55KM4MeeUbgzllh6oPm7d5mNSIapze+hjsowH1q4TZ/Zatye4T5OiRECmZ8USi7RzYeH6plUKSEGWfiwnLwIkiOzigV+GBqqulS94yg==" -i -H "Content-Type: application/json; charset=UTF-8" -X GET http://localhost:8080/api/v1.0/documents/doc1

delete document:

	curl -H "Authorization: ApiAuth 9ebd226b1207473a92dc1f433343044e:MIc4xtC1/VdsX2N0JDS8y4HIIzC4IMBDf41+se6zZasTMeNaK7rqowRWUCYPFKfRcwnlO8bebLJ0AANRGhfkwxHl5j9QDDiV26RnJFCTrLgabmDnIanpCeCaT8S/epB6UBO5wd1o5ZSS09O2dgNBgte4vveYjnaBy5iY5K7RFQlPLzBYJbwpHh0s2DiPDExoQPOzvexZMgl5h4M+x+jQWUcnhIvneeVTjNdbjY+/dv2C+gNzXDnHv2G/BlJKt1K81NtxOMhM/uShOkrkTUDi480ZUCZzf2SB8n0kcfas43I69jj55KM4MeeUbgzllh6oPm7d5mNSIapze+hjsowH1q4TZ/Zatye4T5OiRECmZ8USi7RzYeH6plUKSEGWfiwnLwIkiOzigV+GBqqulS94yg==" -i -H "Accept: application/json" -X DELETE http://localhost:8080/api/v1.0/documents/doc1

	curl -H "Authorization: ApiAuth 9ebd226b1207473a92dc1f433343044e:MIc4xtC1/VdsX2N0JDS8y4HIIzC4IMBDf41+se6zZasTMeNaK7rqowRWUCYPFKfRcwnlO8bebLJ0AANRGhfkwxHl5j9QDDiV26RnJFCTrLgabmDnIanpCeCaT8S/epB6UBO5wd1o5ZSS09O2dgNBgte4vveYjnaBy5iY5K7RFQlPLzBYJbwpHh0s2DiPDExoQPOzvexZMgl5h4M+x+jQWUcnhIvneeVTjNdbjY+/dv2C+gNzXDnHv2G/BlJKt1K81NtxOMhM/uShOkrkTUDi480ZUCZzf2SB8n0kcfas43I69jj55KM4MeeUbgzllh6oPm7d5mNSIapze+hjsowH1q4TZ/Zatye4T5OiRECmZ8USi7RzYeH6plUKSEGWfiwnLwIkiOzigV+GBqqulS94yg==" -i -H "Content-Type: application/json; charset=UTF-8" -X DELETE http://localhost:8080/api/v1.0/documents/doc1

Destroy bottle-api-skeleton environment
---------------------------------------

    cd bottle-api-skeleton
    deactivate
    rmvirtualenv bottle-api-skeleton


Feedback welcome!
-----------------

Please email maillet.hugues.dev@gmail.com with comments, suggestions, or comment via https://github.com/logorn/bottle-api-skeleton