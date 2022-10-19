from radkit_client import Device, run_on_device_dict, helpers
from radkit_common import nglog
from pyvis.network import Network
from deepdiff import DeepDiff
import os
import re
import json


IC = nglog.LazyTag("NXOS Neighbor Discovery", desc="Tag for Neighbor Discovery IC")
nglog.basicConfig()

class scrubber():
    FLAT = 0
    PER_LINE = 1
    FIRST_MATCH = 2

    def __init__(self):
        self.success = False
        self.data = []

    def scrub(self, output, rex, mode = 0, debug = 0):
        matches = []
        if type(output) == str:
            output = [output]
        for line in output:
            line_matches = []
            for match in re.findall(rex, line):
                if debug:
                    print('scrub_line:', line)
                    print('scrub_match:', match)
                if type(match) == tuple:
                    line_matches += list(match)
                else:
                    line_matches += [match]
                if mode == self.FIRST_MATCH:
                    self.data = match
                    self.success = True
                    return 1

            if line_matches:
                if mode == scrubber.FLAT:
                    matches += line_matches
                elif mode == scrubber.PER_LINE:
                    matches += [line_matches]

        if debug:
            print('scrub_total:', len(matches))
        self.data = matches
        self.success = bool(matches)
        return len(matches)

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

def cmd_parser(commands,devices):
    if type(commands) == str:
        commands = [commands]
    request = devices.exec(commands).wait()
    parsed_cmd_tmp = {}
    #print(request.result.data)
    for dev in request.result:
        parsed_cmd_tmp[dev] = {}
        for cmd in request.result[dev]:
            if cmd_decoder(request.result[dev][cmd].data) is not None:
                #print(request.result[dev][cmd].data)
                tmp_cmd = cmd_decoder(request.result[dev][cmd].data)
                parsed_cmd_tmp[dev][cmd] = {}
                parsed_cmd_tmp[dev][cmd] = tmp_cmd
                #nglog.info( "[" + dev + "] - " + "`" + cmd + "` was parsed")
            else:
                nglog.info("This command `" + cmd + "` has encountered error on device " + dev)
                #nglog.info("Vis diagram has been generated.")
                parsed_cmd_tmp[dev][cmd] = {}
                parsed_cmd_tmp[dev][cmd] = None
    return parsed_cmd_tmp

def cmd_decoder(output):
    output = output.split('\n')
    output = output[1:-1]
    return output

def vpc_finder(commands, device):
	vpc_list = []
	vpc_pairs = []
	for dev in device:
		sc.scrub(commands[dev]["show run | inc peer-keepalive"], r'peer-keepalive destination\s((?:\d{1,3}\.){3}\d{1,3})\ssource\s((?:\d{1,3}\.){3}\d{1,3})', mode=sc.FIRST_MATCH)
		if sc.data:
			tmp_dict = {}
			vpc_brief = json_parser(["show vpc brief"], device.filter("name",dev))
			vpc_domain = vpc_brief[dev]["show vpc brief"]["vpc-domain-id"]
			tmp_dict={
				"dev_name" : dev,
				"vpc_domain" : vpc_domain,
				"local_ip" : sc.data[1],
				"remote_ip" :  sc.data[0]
			}
			for item in vpc_list:
				if sc.data[1] == item["remote_ip"] and sc.data[0] == item["local_ip"] and vpc_domain == item["vpc_domain"]:
					vpc_tmp = (dev,item["dev_name"])
					vpc_pairs.append(vpc_tmp)
			vpc_list.append(tmp_dict)
	return vpc_pairs

def get_commands(device: Device) -> None:
	vpc_keepalive = cmd_parser("show run | inc peer-keepalive", device)
	vpc_pairs = vpc_finder(vpc_keepalive, device)
	for dev_pair in vpc_pairs:
		vpc_consistency = json_parser(["show vpc consistency-parameters global"], device.filter("name", dev_pair[0]))
		nglog.info("======================================================")
		nglog.info("+++++++ VPC pair: " + str(dev_pair) + "+++++++")
		for param in vpc_consistency[dev_pair[0]]["show vpc consistency-parameters global"]["TABLE_vpc_consistency"]["ROW_vpc_consistency"]:
			if param["vpc-param-local-val"] != param["vpc-param-peer-val"]:
				nglog.info("------------------------------------------------------")
				nglog.info("Inconsistency was found: " + str(param["vpc-param-name"]))
				nglog.info(dev_pair[0] + " value: " + str(param["vpc-param-local-val"]))
				nglog.info(dev_pair[1] + " value: " + str(param["vpc-param-peer-val"]))

if __name__ == "__main__":
	sc = scrubber()
	run_on_device_dict(get_commands)