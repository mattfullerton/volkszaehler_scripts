# Read a heat meter's current reading and send it to Volkszähler using the Optical MBUS interface on a Linux system, e.g. Raspberry PI

This is a VERY rough and ready and hacky approach to getting the data out of the meter and uploading to Volkszähler.
For getting the data out, I am currently working around the mbus-test program which is on GitHub here:

https://github.com/geronet1/mbus-test

I am using a version modified from the original, posted on the mikrocontroller.net forum thread here:

https://www.mikrocontroller.net/topic/438972#6103099

I removed the decoding testing code within the main function, and modified some of the defines to match what seemed to work well for the meter in our flat, the Engelmann Sensostar E, as follows:

```
int init_size = 536; // 532 x 0x55 bei 2400 baud 8N1 = 2,2 sek.
int init_pause = 240; // ms
unsigned char prim_adr = 0x00;
```

I have further changed the first serial device to be changed to be the Raspberry PI's (1st generation) UART - `/dev/ttyAMA0`. Previously I was using a USB version of the IR transceiver.

I have not yet looked to see what improvements the GitHub version has brought.

To build the source code:
```
gcc main.c mbus-decode.c mbus.c -o main -lm
```

The `run.sh` script (`chmod 700 run.sh` to make executable) is the clunky part: it pipes commands into the mbus-test program and redirects the output to text files. The main text output is parsed and the data used to send to Volkszaehler, by a Python script.
