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
lsb.py hide [img_file] [payload_file] [password]
```

For example, hide `secret.png` into `origin.jpg` with password `1234567`.

```shell
python3 lsb.py hide images/origin.jpg images/secret.png 1234567
```

The command above will generate a new file named `origin-stego.png`.

## Extract
To extract data or file from an stego image:

```shell
python3 lsb.py extract [stego_file] [out_file] [password]
```

For example, extract secret data from `stego.jpg` with password `1234567`, and save those data as file `secret.png`:

```shell
python3 lsb.py extract images/stego.png secret.png 1234567
```
