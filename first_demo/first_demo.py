from radkit_client import Device, run_on_device_dict, helpers
from radkit_common import nglog
from pyvis.network import Network
import os
import re
import json


IC = nglog.LazyTag("NXOS Neighbor Discovery", desc="Tag for Neighbor Discovery IC")
nglog.basicConfig()

def json_parser(commands,devices):
    # Generating "<cmd> | json | no-more"
    pipes = " | json | no-more"
    cmds = [s + pipes for s in commands]
    # Requesting commands from radkit inventory
    request = devices.exec(cmds).wait()
    parsed_cmd_tmp = {}
    for dev in request.result:
        parsed_cmd_tmp[dev] = {}
        for cmd in request.result[dev]:
            if json_decoder(request.result[dev][cmd].data) is not None:
                tmp_json = json_decoder(request.result[dev][cmd].data)
                # Removing " | json | no-more" from show commands
                cmd = cmd.replace(" | json | no-more", "")
                parsed_cmd_tmp[dev][cmd] = {}
                parsed_cmd_tmp[dev][cmd] = tmp_json
                #nglog.info( "[" + dev + "] - " + "`" + cmd + "` was parsed")
            else:
                nglog.info("This command `" + cmd + "` has encountered error on device " + dev)
                #nglog.info("Vis diagram has been generated.")
                cmd = cmd.replace(" | json | no-more", "")
                parsed_cmd_tmp[dev][cmd] = {}
                parsed_cmd_tmp[dev][cmd] = None
    return parsed_cmd_tmp

def json_decoder(output):
    output = output[output.find('{'):]
    output = re.sub('([^}]*)$','',output)
    test_output = output.replace('\n','')
    try:
        output_json = json.loads(test_output)
    except ValueError:
        output_json = None
        # Eventually if we would like to finish execution of topology discovery here
        #sys.exit(1)
    return output_json

def hostname_check(dev, dev_dict):
	d = dev_dict.filter("name",dev)
	parsed_cmd = json_parser(["show hostname"],d)
	device = parsed_cmd[dev]["show hostname"]["hostname"]
	return device
	
def dom_check(device, parsed_cmd, product_id, pwr_type, border_value):
		devices = [item[0] for item in device.items()]
		nglog.info("Devices where checks are done: " + str(devices))
		for d in devices:
			hostname = hostname_check(d, device)
			nglog.info("################################################################")
			nglog.info("Device: " + d)
			if type(parsed_cmd[d]["show interface transceiver details"]["TABLE_interface"]["ROW_interface"]) is dict:
				parsed_cmd[d]["show interface transceiver details"]["TABLE_interface"]["ROW_interface"] = [(parsed_cmd[d]["show interface transceiver details"]["TABLE_interface"]["ROW_interface"])]
			for interface in parsed_cmd[d]["show interface transceiver details"]["TABLE_interface"]["ROW_interface"]:
				if "cisco_product_id" in interface and interface["cisco_product_id"] == product_id:
					if "TABLE_lane" in interface:
						if type(interface["TABLE_lane"]["ROW_lane"]) is dict:
							interface["TABLE_lane"]["ROW_lane"] = [(interface["TABLE_lane"]["ROW_lane"])]
						for lane in interface["TABLE_lane"]["ROW_lane"]:
							if pwr_type in lane:
								if float(lane[pwr_type]) <= float(border_value):
									nglog.info(interface["interface"] + " = " + interface["serialnum"])
									nglog.info("Lane " + lane["lane_number"] + " " + lane[pwr_type])
def get_commands(
	device: Device,
	*,
	rx_pwr: bool = False,
	tx_pwr: bool = False,
	product_id: str = "",
	border_value: str = "1000"
) -> None:
	rx_pwr_var = "rx_pwr"
	tx_pwr_var = "tx_pwr"
	parsed_cmd = json_parser(["show interface transceiver details"],device)
	if rx_pwr:
		nglog.info("Gathering all needed commands for RX power check.")
		dom_check(device, parsed_cmd, product_id, rx_pwr_var, border_value)
	if tx_pwr:
		nglog.info("Gathering all needed commands for TX power check.")
		dom_check(device, parsed_cmd, product_id, tx_pwr_var, border_value)	
if __name__ == "__main__":
	run_on_device_dict(get_commands)
