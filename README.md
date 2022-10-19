# General description


### First demo: 
+ Script is checking if there are any SFPs on selected devices which are showing TX or RX power below certain threshold.
+ List of SFPs that meet defined conditions is shown together with their serial numbers. 
### Second demo:
+ Script is checking content of table tah_sun_prx_dhs_ff_ctl1 and verifying if there are any incorrect values of "drop_size" field.
+ Additionally script is able to correct those problematic values.

### Third demo:
+ Script is checking if there are any VPC inconsistencies.
+ List of inconsistencies is shown if there are any of type-1 or type-2.

### Fourth demo:
+ Script is checking what is percentage utilization of specifed folder/space on multiple switches.
+ There can be "border value" specifice (utlization will be printed out if it is above specified number).
