# Simple Light Awesome Port Scanner (SLAPS)

Scans TCP ports on a host and just tells you whats open. Customizable threads and timeouts.

There are many port scanners but this one purposefully tries to do the bare minimum as simply as possible and without many (or any) requirements.

## Install

    git clone https://github.com/chm0dx/slaps.git

## Use

    usage: slaps.py [-h] [-p PORTS] [-t THREADS] [-w WAIT] [-j] hosts

    Simple Light Awesome Port Scanner: Because this thing SLAPS

    positional arguments:
      hosts                 A comma-separated list of hosts to be scanned

    optional arguments:
      -h, --help            show this help message and exit
      -p PORTS, --ports PORTS
                        A comma-separated list of ports to be scanned. Defaults to
                        21,22,25,53,80,139,443,445,3389,8000,8080,8443
      -t THREADS, --threads THREADS
                        The number of max threads. Defaults to 100
      -w WAIT, --wait WAIT  The number of seconds to wait for a response. Defaults to 1
      -j, --json            Print full JSON output

(because this thing slaps)

![slaps](https://thumbs.gfycat.com/DimImprobableCommongonolek-size_restricted.gif)
