# cloacked-pixel-python3
As **NOBODY** is using python2, so. A python3 version of [cloacked-pixel](https://github.com/livz/cloacked-pixel.git).

# Install
Follow these shell commands:

```shell
# clone this repo to local
git clone https://github.com/Grazee/cloacked-pixel-python3.git

# install python3 dependencies
pip3 install -r requirements.txt
```

# Usage
## Hide
To hide data or file into an image:

```shell
python3 lsb.py hide -i [img_file] -s [payload_file] -o [out_file] -p [password]
```

**For example**, hide `secret.png` into `origin.jpg` with password `1234567`.

```shell
python3 lsb.py hide -i images/origin.jpg -s images/secret.png -o stego.png -p 1234567
```

The command above will generate a new file named `stego.png`.

## Extract
To extract data or file from an stego image:

```shell
python3 lsb.py extract -i [stego_file] -o [out_file] -p [password]
```

**For example**, extract secret data from `stego.jpg` with password `1234567`, and save those data as file `secret.png`:

```shell
python3 lsb.py extract -i images/stego.png -o secret.png -p 1234567
```
