.. _benchmarks:

Benchmarks
=============
We strongly believe that a statistical piece of software should **not** 
add an overhead to an application.

We are providing the following benchmarks done with `ab` the Apache 
Benchmarking Tool.

Environment
------------
For the environment, we used a Turbogears2 WSGI application with a local 
instance of MongoDB.

Since we knew we were going to be receiving a lot of requests, we set the 
cache level of waskr to 200. 

This basically means that waskr will hold data of 200 requests in memory
*before* writing to the database.

The benchmark options where set with the following:

 *  5 concurrent connections with KeepAlive enabled 
 *  30 seconds max

Without Middleware 
-------------------
The following results are with the WSGI application running their normal 
middleware::

    This is ApacheBench, Version 2.3 <$Revision: 655654 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/

    Benchmarking 10.0.0.164 (be patient)
    Finished 1201 requests


    Server Software:        PasteWSGIServer/0.5
    Server Hostname:        10.0.0.164
    Server Port:            8001

    Document Path:          /
    Document Length:        4414 bytes

    Concurrency Level:      5
    Time taken for tests:   30.012 seconds
    Complete requests:      1201
    Failed requests:        679
       (Connect: 0, Receive: 0, Length: 679, Exceptions: 0)
    Write errors:           0
    Keep-Alive requests:    0
    Total transferred:      5731087 bytes
    HTML transferred:       5048919 bytes
    Requests per second:    40.02 [#/sec] (mean)
    Time per request:       124.947 [ms] (mean)
    Time per request:       24.989 [ms] (mean, across all concurrent requests)
    Transfer rate:          186.48 [Kbytes/sec] received

    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        1    3   0.7      3       7
    Processing:    98  122  49.6    113     927
    Waiting:       97  120  49.6    112     925
    Total:        101  125  49.6    116     930

    Percentage of the requests served within a certain time (ms)
      50%    116
      66%    120
      75%    123
      80%    127
      90%    147
      95%    158
      98%    171
      99%    176
     100%    930 (longest request)



With RequestStatsMiddleware
------------------------------
The following was introducing waskr which is a valid point to say
it is so lean it does not make a difference in your app's performance::

    This is ApacheBench, Version 2.3 <$Revision: 655654 $>
    Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
    Licensed to The Apache Software Foundation, http://www.apache.org/

    Benchmarking 10.0.0.164 (be patient)
    Finished 1227 requests


    Server Software:        PasteWSGIServer/0.5
    Server Hostname:        10.0.0.164
    Server Port:            8001

    Document Path:          /
    Document Length:        4414 bytes

    Concurrency Level:      5
    Time taken for tests:   30.001 seconds
    Complete requests:      1227
    Failed requests:        707
       (Connect: 0, Receive: 0, Length: 707, Exceptions: 0)
    Write errors:           0
    Keep-Alive requests:    0
    Total transferred:      5848915 bytes
    HTML transferred:       5151979 bytes
    Requests per second:    40.90 [#/sec] (mean)
    Time per request:       122.255 [ms] (mean)
    Time per request:       24.451 [ms] (mean, across all concurrent requests)
    Transfer rate:          190.39 [Kbytes/sec] received

    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        3    7  40.4      5    1007
    Processing:    58  115  45.7    108     887
    Waiting:       56  113  45.7    106     885
    Total:         65  122  60.5    113    1105

    Percentage of the requests served within a certain time (ms)
      50%    113
      66%    116
      75%    118
      80%    120
      90%    142
      95%    156
      98%    164
      99%    212
     100%   1105 (longest request)

