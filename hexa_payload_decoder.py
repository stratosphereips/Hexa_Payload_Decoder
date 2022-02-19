import subprocess
import argparse
from libretranslator import decode_data, translate_data
from datetime import datetime
import logging
import json

def parse_json(results):
    # Create a set that holds the unique payloads
    hexa_set = set()
    for res in results:
        hexa_payload = res["_source"]["layers"]["data"][0]

        # Do not attempt to translate something that is already been attempted
        if hexa_payload in hexa_set:
            continue
        else:
            hexa_set.add(hexa_payload)

        decoded_data = decode_data(hexa_payload)
        if decoded_data is not None:
            # Log inforamtion only about strings that can be decoded to reduce the log file
            logging.info(f"Hexa payload: {hexa_payload}, size: {res['_source']['layers']['data.len'][0]}")
            logging.info(f"Decoded payload: {decoded_data}")
            trans_data = translate_data(decoded_data)
            logging.info(f"Translated payload: {trans_data}")
        else:
            logging.debug(f"Hexa payload: {hexa_payload}, size: {res['_source']['layers']['data.len'][0]}")

if __name__ == '__main__':

    prog = " Hexadecimal decoder and translator for network analysis."
    parser = argparse.ArgumentParser(prog=prog)
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument("-d", "--decode", required=False, type=str, help="Decode and translate the given string.")
    group1.add_argument("-c", "--clean", required=False, action='store_true', help="Clean the contents of the log file.")

    group2 = parser.add_argument_group("Analysis")
    group2.add_argument("-r", "--read", type=str, required=False, help="Name of the pcap file that is analyzed.")
    group2.add_argument("-p", "--port", type=int, required=False, help="Analyze traffic for a specific port only.")
    group2.add_argument("-l", "--length", type=int, required=False, default=2, help="Analyze data streams longer than the given length.")
    group2.add_argument("-w", "--write", type=str, required=False, default='payload_analyzer.log', help="Store output in log file. Default payload_analyzer.log")

    args = parser.parse_args()

    max_len = args.length

    logging.basicConfig(filename=args.write, level=logging.INFO, format='%(asctime)s :: %(message)s')

    if args.decode is not None:
        print(decode_data(args.decode))
        exit()

    if args.clean:
        open(args.write, 'w').close()
        exit()

    if args.read is not None:
        pcap_file = args.read
        logging.info(".-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-.")
        logging.info(f"Starting analysis of {pcap_file}")
    else:
        print("You need to specify a pcap file to analyze. Exiting...")
        exit()

    logging.info(f"Minimum payload length: {args.length}")

    if args.port is not None:
        port_num = args.port
        logging.info(f"Port number: {port_num}")
        results = subprocess.check_output(f"tshark -r {pcap_file} -T fields -T json -E separator=, -e data.len -e data '(data.len>{max_len})&&(tcp.srcport=={port_num})'", shell=True)
    else:
        results = subprocess.check_output(f"tshark -r {pcap_file} -T fields -T json -E separator=, -e data.len -e data '(data.len>{max_len})'", shell=True)

    if len(results) > 0:
        res_json = json.loads(results.lstrip())
        parse_json(res_json)
    else:
        logging.warning("No results with these parameters")

    logging.info(f"Finished analysis of file: {pcap_file}")
    logging.info(".-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-.")
