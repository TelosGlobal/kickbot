#!/bin/sh
cd <KICKBOT_LOCATION>
<TELOS_FULL_PATH>/teclos get table -l 500 eosio eosio producers > producers.json
python get_producer_status.py
