
# Hexa Payload Decoder 

![Arcane|Transmutation](https://i.imgur.com/hbsbZnt.png)

### Problem Statement
When analyzing malware traffic on the network sometimes we find ourselves spending several minutes decoding the data from the hexadecimal streams. In the best case scenario we can use some tools (like Wireshark) to see this hexadecimal streams already decoded, but sometimes the decoded characters are not supported by most of the networking analyzers.

### The Solution
The idea is to develop a tool aimed to extract the TCP hexadecimal data from netwrok captures filtering by a specific port provided by the user, decode it from hexadecimal and translate it from any language to english.

The workflow of the tool is the following:
  - User runs the bash script with two parameters, the pcap file to analyze and some port.
  - The bash script extracts the hexadecimal data from the TCP flows filtering by the user provided port using Tshark command.
  - The extracted hexadecimal data is passed to CyberChef decoder which uses multiple decoding techniques to get the raw data in the language it had been written.
  - The decoded data is finally passed to Google Translate python library which automatically detects the language and translate it to english.
  - The decoded and translated data is written to an output file to see the results.
  - This flow repeats for every TCP flow found in the pcap.
  
#### Help:
- Hexadecimal decoder and translator for network analysis. 
usage: payload_analyzer.sh [-h] [-d hexacode] [-p pcap] [-pp pcap port] 
where:
	 - h - show this help text 
	 - d hexacode - to decode and translate given hexadecimal code and print the results in standard output 
	 - p pcap - to decode and translate all TCP data in given pcap file and write the results in logfile payload_analyzer.log 
	 - t pcap port - to decode and translate all TCP data in given pcap file filtering by giving port and write the results in logfile payload_analyzer.log 
	 -l pcap port datalength - to decode and translate all TCP data in given pcap file filtering by giving port and data length and writes the results in logfile payload_analyzer.log 
	 - c - clean all results in logfile payload_analyzer.log


---

Here is the script working with some example pcap:

![Imgur](https://i.imgur.com/HI5xseO.png)

---

### References:

- CyberChef Decoder https://gchq.github.io/CyberChef/.
- Google Translaty Python Library https://py-googletrans.readthedocs.io/en/latest/.

