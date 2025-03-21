# PV Data Collector to CSV

A very simple script to collect PVs and write them to a CSV. 
Allows specification of runtime and sample rate. 

## Run Instructions:
* invoked via `python3 collect.py -f [filename] -r [run_time_seconds] -s [sample_period_seconds]`
* for more verbose help run `python3 collect.py -h`
* You can terminated an ongoing run with "ctrl + c" and collected data will be saved

## Install instructions
1. Clone repo to desired location
2. Run `make install`
