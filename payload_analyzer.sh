#!/bin/bash

#This script goal is to decode any hex data and translate it to english.
#To do so it uses javascript CyberChef script and Googletrans python library.
#Javascript: It's necessary to have node and npm installed and  CyberChef Node-Api installed found at: https://github.com/gchq/CyberChef/wiki/Node-API
#Python3: It's also necessary to have Googletrans python3 library installed found at: https://py-googletrans.readthedocs.io/en/latest/

#Example:
#"d0 a2 d0 b0 d0 ba 20 d0 b4 d0 be d0 bb d0 b3 d0 be 20 d0 b8 20 d1 81 d0 bf d0 b0 d1 81 d0 b8 d0 b1 d0 be 20 d0 b7 d0 b0 20 d0 b2 d1 81 d0 b5 20 d1 80 d1 8b d0 b1 d1 8b 2e"

##########################################

logfile="$(pwd)/payload_analyzer.log"
decoded=""
translated=""

# Hexadecimal decoder function using CyberChef 
function decoder {
    hex_data=$1
    echo "Decoding $hex_data . . ."
    decoded_hex=$(echo "$hex_data" | node cyberchef-decode.js)
    decoded=$decoded_hex
    echo "Decoded hex data: $decoded_hex"
    translated_hex=$(python3 googletranslator.py "$decoded_hex")
    translated=$translated_hex

    return 0
}

# Parser function to achieve a clean write to logfile
function parser {
    arr=("$@")
    flows=$(echo $arr | cut -d" " -f1)
    size=$(echo $arr | cut -d" " -f2 | cut -d"," -f1)
    payload=$(echo $arr | cut -d" " -f2 | cut -d"," -f2)
        tcpflowobj+="$flows"
    if [ ${#size} -gt 0 ]; then
        decoder $payload    
    else
        size=0
        payload="No Payload"
        decoded="No Payload"
        translated="No Payload"
    fi

    echo "-------------------------------------------" >> $logfile
    echo "Number of Equal Payload Flows: $flows" >> $logfile
    echo "Size of Payload: $size" >> $logfile
    echo "Hexa Coded Payload: $payload" >> $logfile
    echo "Decoded Payload: $decoded" >> $logfile
    echo "Translated Payload: $translated" >> $logfile

    return 0
}

# Hexadecimal decode option
function hexa_decode_option {
    decoder $1
    echo "Decoded $1:"
    echo $decoded
    echo "Translating . . ."
    echo $translated
    return 0
}

# Pcap option will read the pcap and obtain the minimun parameters using Tshark
function pcap_decode_option {
    pcap_file=$(realpath $1)
    echo ".-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-." >> $logfile
    echo "Date: $(date)" >> $logfile
    echo "Pcap: $pcap_file" >> $logfile
    echo "Port: All ports" >> $logfile
    
    echo "Reading pcap $pcap_file . . . " 
    echo "Without port filter (this may take a while) . . ."
    results=($(tshark -r $pcap_file -T fields -E separator=, -e data.len -e data | sort -n | uniq -c))
    aux=("${results[@]}")

    s=0

    len=${#aux[@]}
    i=0

    while [ $i -lt $len ] ; do
        tcpflow="${results[@]:$s:2}"
        parser "${tcpflow[@]}"
        s=$((s+2))
        i=$((i+2))
    done
    
    echo ".-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-END-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-." >> $logfile

    echo "Done"
    echo  "See results at payload_analyzer.log"
    
    return 0
}

# Pcap and Port filtering option will read the pcap and obtain the minimun parameters filtering by port using Tshark
function port_decode_option {
    pcap_file=$(realpath $1)
    port=$2
    echo ".-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-." >> $logfile
    echo "Date: $(date)" >> $logfile
    echo "Pcap: $pcap_file" >> $logfile
    echo "Port: $port" >> $logfile
    
    echo "Reading pcap $pcap_file . . ."
    echo "Filtering port $port . . ."
    results=($(tshark -r $pcap_file -T fields -E separator=, -e data.len -e data tcp.srcport==$port | sort -n | uniq -c))
    aux=("${results[@]}")

    s=0

    len=${#aux[@]}
    i=0

    while [ $i -lt $len ] ; do
        tcpflow="${results[@]:$s:2}"
        parser "${tcpflow[@]}"
        s=$((s+2))
        i=$((i+2))
    done

    echo ".-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-END-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-." >> $logfile

    echo "Done"
    echo "See results at payload_analyzer.log"
    
    return 0
}

# Pcap, port and data length filtering option will read the pcap and obtain the minimun parameters filtering by port using Tshark
function datalen_decode_option {
    pcap_file=$(realpath $1)
    port=$2
    datalen=$3
    echo ".-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-." >> $logfile
    echo "Date: $(date)" >> $logfile
    echo "Pcap: $pcap_file" >> $logfile
    echo "Port: $port" >> $logfile
    echo "Data Len: $datalen" >> $logfile
    
    echo "Reading pcap $pcap_file . . ."
    echo "Filtering port $port . . ."
    echo "Filtering data length $datalen . . ."
    results=($(tshark -r $pcap_file -T fields -E separator=, -e data.len -e data "(data.len>$datalen)&&(tcp.srcport==$port)" | sort -n | uniq -c))
    aux=("${results[@]}")

    s=0

    len=${#aux[@]}
    i=0

    while [ $i -lt $len ] ; do
        tcpflow="${results[@]:$s:2}"
        parser "${tcpflow[@]}"
        s=$((s+2))
        i=$((i+2))
    done

    echo ".-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-END-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-." >> $logfile

    echo "Done"
    echo "See results at payload_analyzer.log"
    
    return 0
}


# Usage and Help section
usage="- Hexadecimal decoder and translator for network analysis. \nusage: $(basename "$0") [-h] [-d hexacode] [-p pcap] [-pp pcap port] 

\nwhere:
    \n\t  -h - show this help text
    \n\t  -d  hexacode - to decode and translate given hexadecimal code and prints the results in standard output
    \n\t  -p pcap - to decode and translate all TCP data in given pcap file and writes the results in logfile payload_analyzer.log 
    \n\t  -t pcap port - to decode and translate all TCP data in given pcap file filtering by giving port and writes the results in logfile payload_analyzer.log
    \n\t  -l pcap port datalength - to decode and translate all TCP data in given pcap file filtering by giving port and data length and writes the results in logfile payload_analyzer.log
    \n\t  -c - clean all results in logfile payload_analyzer.log"

if [ $# -lt 1 ]; then
    echo -e $usage
    exit 1  
fi

option=$1
case "$option" in
    -h) 
        echo -e "$usage"
        ;;
    -d) 
        hexa_decode_option $2
        ;;
    -p) 
        pcap_decode_option $2
        ;;
    -t) 
        port_decode_option $2 $3
        ;;
    -l) 
        datalen_decode_option $2 $3 $4
        ;;    
    -c) 
        echo "Cleaning logfile."
        echo "" > $logfile
        ;;   
    *) 
        echo "illegal option: \n"
        echo -e "$usage"
        ;;
esac

exit 0
