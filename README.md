# rtl_433_autosec

This program will caputure signals from car keyfob, convert it into bits and log it to a python program over dbus for storage.

## How to add support for unsupported vehicles
1. Create a function that checks if binary packet in bitbuffer matches packet structure. You can do this in the following ways:
	* First row of bitbuffer contains the preamble - creat a preable check
	* Second row of bitbuffer contains the static and encrypted code, create a check on static code, length of code, etc/
	* Return 1 if all checks on bitbuffer is successful
	* Example code is written in src/cars/maruti_nippon.c. The function is check_for_maruti_nippon
2. Create a function that converts the bits into a binary string. Append the name of the car or something unique for python program to distinguish between packets.
	* Convert first row of bitbuffer into bits
	* Convert second row of bitbuffer into bits
	* Append first row and second row
	* Append name of car
	* Example function is written in src/cars/maruti_nippon.c. The function is create_maruti_nippon_bit_pk.
3. Add function reference in file src/find_car.c
	* Add the find_car function reference for unsupported vehicle in check_for_car array.
	* Add the bit string conversion function reference to create_car_bit_pk array.

## Running

    rtl_433 -h

```
		= General options =
  [-V] Output the version string and exit
  [-v] Increase verbosity (can be used multiple times).
       -v : verbose, -vv : verbose decoders, -vvv : debug decoders, -vvvv : trace decoding).
  [-c <path>] Read config options from a file
		= Tuner options =
  [-d <RTL-SDR USB device index> | :<RTL-SDR USB device serial> | <SoapySDR device query> | rtl_tcp | help]
  [-g <gain> | help] (default: auto)
  [-t <settings>] apply a list of keyword=value settings for SoapySDR devices
       e.g. -t "antenna=A,bandwidth=4.5M,rfnotch_ctrl=false"
  [-f <frequency>] Receive frequency(s) (default: 433920000 Hz)
  [-H <seconds>] Hop interval for polling of multiple frequencies (default: 600 seconds)
  [-p <ppm_error>] Correct rtl-sdr tuner frequency offset error (default: 0)
  [-s <sample rate>] Set sample rate (default: 250000 Hz)
		= Demodulator options =
  [-R <device> | help] Enable only the specified device decoding protocol (can be used multiple times)
       Specify a negative number to disable a device decoding protocol (can be used multiple times)
  [-X <spec> | help] Add a general purpose decoder (prepend -R 0 to disable all decoders)
  [-Y auto | classic | minmax] FSK pulse detector mode.
  [-Y level=<dB level>] Manual detection level used to determine pulses (-1.0 to -30.0) (0=auto).
  [-Y minlevel=<dB level>] Manual minimum detection level used to determine pulses (-1.0 to -99.0).
  [-Y minsnr=<dB level>] Minimum SNR to determine pulses (1.0 to 99.0).
  [-Y autolevel] Set minlevel automatically based on average estimated noise.
  [-Y squelch] Skip frames below estimated noise level to reduce cpu load.
  [-Y ampest | magest] Choose amplitude or magnitude level estimator.
		= Analyze/Debug options =
  [-a] Analyze mode. Print a textual description of the signal.
  [-A] Pulse Analyzer. Enable pulse analysis and decode attempt.
       Disable all decoders with -R 0 if you want analyzer output only.
  [-y <code>] Verify decoding of demodulated test data (e.g. "{25}fb2dd58") with enabled devices
		= File I/O options =
  [-S none | all | unknown | known] Signal auto save. Creates one file per signal.
       Note: Saves raw I/Q samples (uint8 pcm, 2 channel). Preferred mode for generating test files.
  [-r <filename> | help] Read data from input file instead of a receiver
  [-w <filename> | help] Save data stream to output file (a '-' dumps samples to stdout)
  [-W <filename> | help] Save data stream to output file, overwrite existing file
		= Data output options =
  [-F kv | json | csv | mqtt | influx | syslog | trigger | null | help] Produce decoded output in given format.
       Append output to file with :<filename> (e.g. -F csv:log.csv), defaults to stdout.
       Specify host/port for syslog with e.g. -F syslog:127.0.0.1:1514
  [-M time[:<options>] | protocol | level | noise[:secs] | stats | bits | help] Add various meta data to each output.
  [-K FILE | PATH | <tag> | <key>=<tag>] Add an expanded token or fixed tag to every output line.
  [-C native | si | customary] Convert units in decoded output.
  [-n <value>] Specify number of samples to take (each sample is an I/Q pair)
  [-T <seconds>] Specify number of seconds to run, also 12:34 or 1h23m45s
  [-E hop | quit] Hop/Quit after outputting successful event(s)
  [-h] Output this usage help and exit
       Use -d, -g, -R, -X, -F, -M, -r, -w, or -W without argument for more help



		= Supported device protocols =
    [01]  Maruti Nippon (key received from maker space)
    [02]  Toyota Innova 2015

* Disabled by default, use -R n or a conf file to enable


		= Input device selection =
	RTL-SDR device driver is available.
  [-d <RTL-SDR USB device index>] (default: 0)
  [-d :<RTL-SDR USB device serial (can be set with rtl_eeprom -s)>]
	To set gain for RTL-SDR use -g <gain> to set an overall gain in dB.
	SoapySDR device driver is available.
  [-d ""] Open default SoapySDR device
  [-d driver=rtlsdr] Open e.g. specific SoapySDR device
	To set gain for SoapySDR use -g ELEM=val,ELEM=val,... e.g. -g LNA=20,TIA=8,PGA=2 (for LimeSDR).
  [-d rtl_tcp[:[//]host[:port]] (default: localhost:1234)
	Specify host/port to connect to with e.g. -d rtl_tcp:127.0.0.1:1234


		= Gain option =
  [-g <gain>] (default: auto)
	For RTL-SDR: gain in dB ("0" is auto).
	For SoapySDR: gain in dB for automatic distribution ("" is auto), or string of gain elements.
	E.g. "LNA=20,TIA=8,PGA=2" for LimeSDR.
```

## Troubleshooting

If you see this error:

    Kernel driver is active, or device is claimed by second instance of librtlsdr.
    In the first case, please either detach or blacklist the kernel module
    (dvb_usb_rtl28xxu), or enable automatic detaching at compile time.

then

    sudo rmmod rtl2832_sdr dvb_usb_rtl28xxu rtl2832

or add

    blacklist dvb_usb_rtl28xxu

to /etc/modprobe.d/blacklist.conf

