# How to use the scripts

First demo script execution for TX power:
```
 /Library/Cisco/RADKit/env/bin/python first_demo.py --service <service-id> --tx-pwr --product-id "<transceiver type>" --border-value "<float>"
```

Arguments:

```
`--rx_pwr` - RX power is verified
`--tx_pwr` - TX power is verified
`--product_id` - transceiver type ("cisco product id" from "show interface transceiver details")
`--border_value` - values of RX/TX power below that value are shown in results
```

Example of running script for TX power readings:
```
WKOZIOL-M-21JH:sfp wkoziol$/Library/Cisco/RADKit/env/bin/python first_demo.py --service "cg73-rqm1-896c" --tx-pwr --product-id "QSFP-40G-LR4-S" --border-value "0.1"
19:20:12.602Z INFO  | Connecting to forwarder [uri='wss://ecs.radkit.net/forwarder-1/websocket/']
19:20:13.134Z INFO  | Connection to forwarder successful [uri='wss://ecs.radkit.net/forwarder-1/websocket/']
19:20:15.295Z INFO  | Connecting to forwarder [uri='wss://ecs.radkit.net/forwarder-3/websocket/']
19:20:15.522Z INFO  | Connection to forwarder successful [uri='wss://ecs.radkit.net/forwarder-3/websocket/']
19:20:24.173Z INFO  | Gathering all needed commands for TX power check.
19:20:24.174Z INFO  | Devices where checks are done: ['SFP-9236-1', 'FX3-11', 'SFP-SL', 'FX3-10', 'SFP-93180-1', 'SFP-93180-2']
19:20:25.011Z INFO  | ################################################################
19:20:25.011Z INFO  | Device: SFP-9236-1
19:20:25.447Z INFO  | ################################################################
19:20:25.448Z INFO  | Device: FX3-11
19:20:26.222Z INFO  | ################################################################
19:20:26.222Z INFO  | Device: SFP-SL
19:20:26.662Z INFO  | ################################################################
19:20:26.662Z INFO  | Device: FX3-10
19:20:27.443Z INFO  | ################################################################
19:20:27.443Z INFO  | Device: SFP-93180-1
19:20:28.224Z INFO  | ################################################################
19:20:28.224Z INFO  | Device: SFP-93180-2
19:20:28.224Z INFO  | Ethernet1/53 = AVM2249M1W3
19:20:28.224Z INFO  | Lane 1 -1.36
19:20:28.225Z INFO  | Ethernet1/53 = AVM2249M1W3
19:20:28.225Z INFO  | Lane 2 -1.01
19:20:28.225Z INFO  | Ethernet1/53 = AVM2249M1W3
19:20:28.225Z INFO  | Lane 3 -0.92
19:20:28.225Z INFO  | Ethernet1/53 = AVM2249M1W3
19:20:28.225Z INFO  | Lane 4 -0.85
19:20:28.225Z INFO  | Ethernet1/54 = FNS24130XK1
19:20:28.225Z INFO  | Lane 2 0.00
19:20:28.226Z INFO  | terminating client [identity='wkoziol@cisco.com' reason='shutting down']
```
