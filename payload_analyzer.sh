#!/bin/bash

#This script goal is to decode any hex data and translate it to english.
#To do so it uses javascript CyberChef script and Googletrans python library.
#Javascript: It's necessary to have node and npm installed and  CyberChef Node-Api installed found at: https://github.com/gchq/CyberChef/wiki/Node-API
#Python3: It's also necessary to have Googletrans python3 library installed found at: https://py-googletrans.readthedocs.io/en/latest/

#Example:
#"d0 a2 d0 b0 d0 ba 20 d0 b4 d0 be d0 bb d0 b3 d0 be 20 d0 b8 20 d1 81 d0 bf d0 b0 d1 81 d0 b8 d0 b1 d0 be 20 d0 b7 d0 b0 20 d0 b2 d1 81 d0 b5 20 d1 80 d1 8b d0 b1 d1 8b 2e"

##########################################

if [ $# -ne 2 ]; then
    echo "Needs 2 arguments: Pcap File and Port"
    exit 1
fi

pcap_file=$1
port=$2
logfile="/var/log/payload_analyzer.log"
decoded=""
translated=""

echo "############################################" >> $logfile
echo "Date: $(date)" >> $logfile
echo "Pcap: $pcap_file" >> $logfile
echo "Port: $port" >> $logfile

function decoder {
    hex_data=$1
    #echo "Decoding $hex_data . . ."
    decoded_hex=$(echo "$hex_data" | node cyberchef-decode.js)
    #echo "Decoded hex: $decoded_hex"
    decoded=$decoded_hex
    #echo "Translating $decoded_hex... "
    translated_hex=$(python3 googletranslator.py "$decoded_hex")
    #echo $translated_hex
    translated=$translated_hex

    return 0
}

function parser {
    arr=("$@")
    #echo "Parsing: $arr"
    flows=$(echo $arr | cut -d" " -f1)
    size=$(echo $arr | cut -d" " -f2 | cut -d"," -f1)
    payload=$(echo $arr | cut -d" " -f2 | cut -d"," -f2)
    #echo "flows $flows"
    #echo "size $size"
    #echo "size2 ${#size}"
    #echo "payload $payload"
        tcpflowobj+="$flows"
    if [ ${#size} -gt 0 ]; then
        decoder $payload    
    else
        #echo "NO PAYLOAD"
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


echo "Reading pcap $pcap_file. . ."
echo "Filtering port $port. . ."
results=($(tshark -r $pcap_file -T fields -E separator=, -e data.len -e data tcp.srcport==$port | sort -n | uniq -c))
#results=("${results[@]:1}")
aux=("${results[@]}")

s=0

len=${#aux[@]}
i=0

while [ $i -lt $len ] ; do
    tcpflow="${results[@]:$s:2}"
    #echo "${tcpflow[@]}"
    parser "${tcpflow[@]}"
    s=$((s+2))
    i=$((i+2))
done

exit 0
