#!/bin/bash

#set your variables
#please set these variables
TOKEN=1234567
BASE_URL=http://bestoon1.ir
curl --data "token=$TOKEN&amount=$1&text=$2" $BASE_URL/submit/income/
