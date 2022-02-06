import subprocess
import argparse
from libretranslator import decode_data, translate_data
from datetime import datetime
import logging 

LOG_FILE = 'payload_analyzer.log'

def parse_output(results):
    for res in list(results.split(b'\n')):

        if len(res) == 0:
            continue
        logging.info("-------------------------------------------")
        
        data = res.lstrip().split(b' ')
        logging.info(f"Number of similar payload flows: {int(data[0])}")

        data_len, hexa_payload = data[1].split(b',')
        logging.info(f"Size of payload: {int(data_len)}")
        logging.info(f"Hexa payload: {hexa_payload}")
        decoded_data = decode_data(hexa_payload.decode('utf-8'))

        if decoded_data is not None:
            logging.info(f"Decoded payload: {decoded_data}")
            trans_data = translate_data(decoded_data)
            logging.info(f"Translated payload: {trans_data}")


if __name__ == '__main__':

    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s :: %(message)s')

    prog = " Hexadecimal decoder and translator for network analysis."
    parser = argparse.ArgumentParser(prog=prog)
    group1 = parser.add_mutually_exclusive_group()
    group1.add_argument("-d", "--decode", required=False, type=str, help="Decode and translate the given string.")
    group1.add_argument("-c", "--clean", required=False, action='store_true', help="Clean the contents of the log file.")
    
    group2 = parser.add_argument_group("Analysis")
    group2.add_argument("-r", "--read", type=str, required=False, help="Name of the pcap file that is analyzed.")
    group2.add_argument("-p", "--port", type=int, required=False, help="Analyze traffic for a specific port only.")
    group2.add_argument("-l", "--length", type=int, required=False, help="Analyze data streams longer than the given length.")

    args = parser.parse_args()

    if args.decode is not None:
        print(decode_data(args.decode))
        exit()

    if args.clean:
        open(LOG_FILE, 'w').close()
        exit()

    if args.read is not None:
        pcap_file = args.read
        logging.info(".-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-.")
        # print("Date", datetime.now())
        # print("Pcap file:", pcap_file)
        logging.info(f"Starting analysis of {pcap_file}")
    else:
        print("You need to specify a pcap file to analyze. Exiting...")
        exit()

    if args.port is not None:
        port_num = args.port
        # print("Port:", port_num)
        logging.info(f"Port number: {port_num}")
        if args.length is not None:
            # print("Minimum payload length:", args.length)
            logging.info(f"Minimum payload lengthr: {args.length}")
            results = subprocess.check_output(f'tshark -r {pcap_file} -T fields -E separator=, -e data.len -e data "(data.len>{args.length})&&(tcp.srcport=={port_num})" | sort -n | uniq -c', shell=True)
        else:
            results = subprocess.check_output(f"tshark -r {pcap_file} -T fields -E separator=, -e data.len -e data '(tcp.srcport=={port_num})' | sort -n | uniq -c", shell=True)
    else:
        if args.length is not None:
            logging.info(f"Minimum payload lengthr: {args.length}")
            results = subprocess.check_output(f"tshark -r {pcap_file} -T fields -E separator=, -e data.len -e data '(data.len>{args.length})' | sort -n | uniq -c", shell=True)
        else:
            results = subprocess.check_output(f"tshark -r {pcap_file} -T fields -E separator=, -e data.len -e data | sort -n | uniq -c", shell=True)

    if len(results) > 0:
        parse_output(results)
    else:
        logging.warning("No results with these parameters")

    logging.info(f"Finished analysis of file: {pcap_file}")
    logging.info(".-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-.")