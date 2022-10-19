# General description


+ Script is checking all devices in the service and is looking for VPC pairs
+ Once VPC pairs are found there is check done on those devices in order to verify if there are any VPC inconsistencies present there.

Example script execution:
```
WKOZIOL-M-21JH:partner_workshops wkoziol$ /Library/Cisco/RADKit/env/bin/python third_demo.py  --service "cg73-rqm1-896c"
23:21:41.529Z INFO  | Logging configured [root_level='ERROR' level='INFO' con_level='TRACE' con_json=False file_level='TRACE' file_json=False file_name=None file_rotate=True with_rate_limiting=True]
Cisco email: wkoziol@cisco.com
23:21:55.941Z INFO  | Connecting to forwarder [uri='wss://ecs.radkit.net/forwarder-2/websocket/']
23:21:56.168Z INFO  | Connection to forwarder successful [uri='wss://ecs.radkit.net/forwarder-2/websocket/']
23:21:57.957Z INFO  | Connecting to forwarder [uri='wss://ecs.radkit.net/forwarder-4/websocket/']
23:21:58.172Z INFO  | Connection to forwarder successful [uri='wss://ecs.radkit.net/forwarder-4/websocket/']
[('FX3-11', 'FX3-12'), ('FX3-07', 'FX3-08')]
23:22:05.286Z INFO  | ======================================================
23:22:05.286Z INFO  | +++++++ VPC pair: ('FX3-11', 'FX3-12')+++++++
23:22:05.286Z INFO  | ------------------------------------------------------
23:22:05.286Z INFO  | Inconsistency was found: STP Mode
23:22:05.286Z INFO  | FX3-11 value: MST
23:22:05.286Z INFO  | FX3-12 value: Rapid-PVST
23:22:05.286Z INFO  | ------------------------------------------------------
23:22:05.286Z INFO  | Inconsistency was found: STP Loopguard
23:22:05.287Z INFO  | FX3-11 value: Enabled
23:22:05.287Z INFO  | FX3-12 value: Disabled
23:22:05.287Z INFO  | ------------------------------------------------------
23:22:05.287Z INFO  | Inconsistency was found: Allowed VLANs
23:22:05.287Z INFO  | FX3-11 value: 10
23:22:05.287Z INFO  | FX3-12 value: 10,20
23:22:05.736Z INFO  | ======================================================
23:22:05.736Z INFO  | +++++++ VPC pair: ('FX3-07', 'FX3-08')+++++++
23:22:05.737Z INFO  | ------------------------------------------------------
23:22:05.737Z INFO  | Inconsistency was found: Allowed VLANs
23:22:05.737Z INFO  | FX3-07 value: 10,20,30,40,50,60,70,90,100
23:22:05.737Z INFO  | FX3-08 value: 10,20,30,40,50,60,70,80,90,100
23:22:05.737Z INFO  | terminating client [identity='wkoziol@cisco.com' reason='shutting down']
```
