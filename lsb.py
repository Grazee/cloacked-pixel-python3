import sys
import struct
import numpy
import argparse
import matplotlib.pyplot as plt
from Crypto.Util.number import long_to_bytes

from PIL import Image

from crypt import AESCipher

# Decompose a binary file into an array of bits
def decompose(data):
    v = []
    
    # Pack file len in 4 bytes
    fSize = len(data)
    bs = b''
    size_byte = struct.pack('i', fSize)
    bs += size_byte
    bs += data
	
    # bs += [ord(b) for b in data]

    for b in bs:
        for i in range(7, -1, -1):
            v.append((b >> i) & 0x1)

    return v

# Assemble an array of bits into a binary file
def assemble(v):
    bs = b""

    length = len(v)
    for idx in range(0, len(v), 8):
        b = 0
        for i in range(0, 8):
            if (idx + i < length):
                b = (b << 1) + v[idx + i]
        b = long_to_bytes(b)
        bs = bs + b

    # print("debug:", len(bs[:4]))
    payload_size = struct.unpack("i", bs[:4])[0]

    return bs[4: payload_size + 4]

# Set the i-th bit of v to x
def set_bit(n, i, x):
    mask = 1 << i
    n &= ~mask
    if x:
        n |= mask
    return n

# Embed payload file into LSB bits of an image
def embed(imgFile, payload, outFile, password):
    # Process source image
    img = Image.open(imgFile)
    (width, height) = img.size
    conv = img.convert("RGBA").getdata()
    print("[*] Input image size: %dx%d pixels." % (width, height))
    max_size = width*height*3.0/8/1024		# max payload size
    print("[*] Usable payload size: %.2f KB." % (max_size))

    f = open(payload, "rb")
    data = f.read()
    f.close()
    print("[+] Payload size: %.3f KB " % (len(data)/1024.0))

    # Encypt
    cipher = AESCipher(password)
    data_enc = cipher.encrypt(data)

    # Process data from payload file
    v = decompose(data_enc)

    # Add until multiple of 3
    while(len(v)%3):
        v.append(0)
    payload_size = len(v)/8/1024.0
    print("[+] Encrypted payload size: %.3f KB " % (payload_size))
    if (payload_size > max_size - 4):
        print("[-] Cannot embed. File too large")
        sys.exit()

    # Create output image
    steg_img = Image.new('RGBA',(width, height))
    data_img = steg_img.getdata()
    idx = 0
    for h in range(height):
        for w in range(width):
            (r, g, b, a) = conv.getpixel((w, h))
            if idx < len(v):
                r = set_bit(r, 0, v[idx])
                g = set_bit(g, 0, v[idx+1])
                b = set_bit(b, 0, v[idx+2])
            data_img.putpixel((w,h), (r, g, b, a))
            idx = idx + 3

    steg_img.save(outFile, "PNG")
    print("[+] %s embedded successfully!" % payload)

# Extract data embedded into LSB of the input file
def extract(in_file, out_file, password):
    # Process source image
    img = Image.open(in_file)
    (width, height) = img.size
    conv = img.convert("RGBA").getdata()
    print("[+] Image size: %dx%d pixels." % (width, height))

    # Extract LSBs
    v = []
    for h in range(height):
        for w in range(width):
            (r, g, b, a) = conv.getpixel((w, h))
            v.append(r & 1)
            v.append(g & 1)
            v.append(b & 1)

    data_out = assemble(v)

    # Decrypt
    cipher = AESCipher(password)
    data_dec = cipher.decrypt(data_out)

    # Write decrypted data
    out_f = open(out_file, "wb")
    out_f.write(data_dec)
    out_f.close()

    print("[+] Written extracted data to %s." % out_file)

# Statistical analysis of an image to detect LSB steganography
def analyse(in_file):
    '''
    - Split the image into blocks.
    - Compute the average value of the LSBs for each block.
    - The plot of the averages should be around 0.5 for zones that contain
    hidden encrypted messages (random data).
    '''
    BS = 100	# Block size 
    img = Image.open(in_file)
    (width, height) = img.size
    print("[+] Image size: %dx%d pixels." % (width, height))
    conv = img.convert("RGBA").getdata()

    # Extract LSBs
    vr = []	# Red LSBs
    vg = []	# Green LSBs
    vb = []	# LSBs
    for h in range(height):
        for w in range(width):
            (r, g, b, a) = conv.getpixel((w, h))
            vr.append(r & 1)
            vg.append(g & 1)
            vb.append(b & 1)

    # Average colours' LSB per each block
    avgR = []
    avgG = []
    avgB = []
    for i in range(0, len(vr), BS):
        avgR.append(numpy.mean(vr[i:i + BS]))
        avgG.append(numpy.mean(vg[i:i + BS]))
        avgB.append(numpy.mean(vb[i:i + BS]))

    # Nice plot 
    numBlocks = len(avgR)
    blocks = [i for i in range(0, numBlocks)]
    plt.axis([0, len(avgR), 0, 1])
    plt.ylabel('Average LSB per block')
    plt.xlabel('Block number')

    #   plt.plot(blocks, avgR, 'r.')
    # plt.plot(blocks, avgG, 'g')
    plt.plot(blocks, avgB, 'bo')

    plt.show()

# def show_usage():
#     sys.exit()

if __name__ == "__main__":
    usage_text = """
    LSB steganogprahy. Hide files within least significant bits of images.

example:
    python3 lsb.py hide -i [img_file] -s [payload_file] -o [out_file] -p [password]
    python3 lsb.py extract -i [stego_file] -o [out_file] -p [password]
    python3 lsb.py analyse -i [stego_file]
    """
        
    parser = argparse.ArgumentParser(usage_text)
    parser.add_argument('-i', help='file input', type=str, dest='in_file')
    parser.add_argument('-o', help='file output', type=str, dest='out_file', default='out.png')
    parser.add_argument('-s', help='file to hide as secret', type=str, dest='secret_file')
    parser.add_argument('-p', help='passcode for hide/extract secret', type=str, dest='password')    

    if len(sys.argv) <= 1:
        parser.print_help()
        exit()
        
    u = sys.argv.pop(1)

    args = parser.parse_args()
    
    if u == "hide":
        if args.in_file and args.secret_file and args.out_file and args.password:
            embed(args.in_file,
                  args.secret_file,
                  args.out_file,
                  args.password)
        else:
            parser.print_help()
    elif u == "extract":
        if args.in_file and args.out_file and args.password:
            extract(args.in_file,
                    args.out_file,
                    args.password)
        else:
            parser.print_help()
    elif u == "analyse":
        if args.in_file:
            analyse(args.in_file)
        else:
            parser.print_help()
    else:
        parser.print_help()
