from scapy.all import rdpcap, ICMP

MORSE_DICT = {
    '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E',
    '..-.': 'F', '--.': 'G', '....': 'H', '..': 'I', '.---': 'J',
    '-.-': 'K', '.-..': 'L', '--': 'M', '-.': 'N', '---': 'O',
    '.--.': 'P', '--.-': 'Q', '.-.': 'R', '...': 'S', '-': 'T',
    '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X', '-.--': 'Y',
    '--..': 'Z', '.----': '1', '..---': '2', '...--': '3',
    '....-': '4', '.....': '5', '-....': '6', '--...': '7',
    '---..': '8', '----.': '9', '-----': '0', '--..--': ',', '.-.-.-': '.',
    '..--..': '?', '-..-.':'/', '-....-': '-', '-.--.':'(', '-.--.-':')'
}

def extract_morse_from_pcap(pcap_file):
    print(f"[opening file] : {pcap_file}")
    packets = rdpcap(pcap_file)
    morse_code = ""
    previous_timestamp = 0.0

    for packet in packets:
        #Filter only the ICMP packets and type 8 (icmp)
        if packet.haslayer(ICMP) and packet[ICMP].type == 8:

            raw_time = float(packet.time)
            seconds = int(raw_time) % 60
            
            # If timestamp is big enough, that means its a marker between two words
            if previous_timestamp != 0.0 and raw_time - previous_timestamp >= 1.5:
                morse_code += "/"

            if seconds % 2 == 0:
                morse_code += "."  # even second = .
            elif seconds % 2 == 1:
                morse_code += "-"  # odd second = -

            previous_timestamp = raw_time        

    return morse_code

def decode_morse(morse_str):
    words = morse_str.split('/')
    decoded_text = ""
    for word in words:
        # Ignore empty spaces
        if word == "":
            continue
        if word in MORSE_DICT:
            decoded_text += MORSE_DICT[word]
        else:
            decoded_text += "?"
    return decoded_text


if __name__ == "__main__":
    
    # Configuration
    pcap_filename = "capture.pcapng"
    
    try:
        # 1. Extraction
        extracted_morse = extract_morse_from_pcap(pcap_filename)
        print("\n[+] EXTRACTION OK !")
        print(f"[*] MORSE CODE : {extracted_morse}")
        
        # 2. Decode
        final_text = decode_morse(extracted_morse)
        print(f"\n[+] Flag : {final_text}")
        
    except FileNotFoundError:
        print(f"[!] Error : '{pcap_filename}' cannot be found.")