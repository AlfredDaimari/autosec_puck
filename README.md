# rtl_433_autosec

This program will caputure signals from car keyfob, convert it into bits and log it to a python program over dbus for storage.

## Building / Installation

rtl_433 is written in portable C (C99 standard) and known to compile on Linux (also embedded), MacOS, and Windows systems.
Older compilers and toolchains are supported as a key-goal.
Low resource consumption and very few dependencies allow rtl_433 to run on embedded hardware like (repurposed) routers.
Systems with 32-bit i686 and 64-bit x86-64 as well as (embedded) ARM, like the Raspberry Pi and PlutoSDR are well supported.

See [BUILDING.md](docs/BUILDING.md)

On Debian (sid) or Ubuntu (19.10+), `apt-get install rtl-433` for other distros check https://repology.org/project/rtl-433/versions

On FreeBSD, `pkg install rtl-433`.

On MacOS, `brew install rtl_433`.

Docker images with rtl_433 are available [on the github page of hertzg](https://github.com/hertzg/rtl_433_docker).

## How to add support for unsupported sensors

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
    [02]  Ashoka Garage Toyota

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


		= Flex decoder spec =
Use -X <spec> to add a flexible general purpose decoder.

<spec> is "key=value[,key=value...]"
Common keys are:
	name=<name> (or: n=<name>)
	modulation=<modulation> (or: m=<modulation>)
	short=<short> (or: s=<short>)
	long=<long> (or: l=<long>)
	sync=<sync> (or: y=<sync>)
	reset=<reset> (or: r=<reset>)
	gap=<gap> (or: g=<gap>)
	tolerance=<tolerance> (or: t=<tolerance>)
	priority=<n> : run decoder only as fallback
where:
<name> can be any descriptive name tag you need in the output
<modulation> is one of:
	OOK_MC_ZEROBIT :  Manchester Code with fixed leading zero bit
	OOK_PCM :         Non Return to Zero coding (Pulse Code)
	OOK_RZ :          Return to Zero coding (Pulse Code)
	OOK_PPM :         Pulse Position Modulation
	OOK_PWM :         Pulse Width Modulation
	OOK_DMC :         Differential Manchester Code
	OOK_PIWM_RAW :    Raw Pulse Interval and Width Modulation
	OOK_PIWM_DC :     Differential Pulse Interval and Width Modulation
	OOK_MC_OSV1 :     Manchester Code for OSv1 devices
	FSK_PCM :         FSK Pulse Code Modulation
	FSK_PWM :         FSK Pulse Width Modulation
	FSK_MC_ZEROBIT :  Manchester Code with fixed leading zero bit
<short>, <long>, <sync> are nominal modulation timings in us,
<reset>, <gap>, <tolerance> are maximum modulation timings in us:
PCM/RZ  short: Nominal width of pulse [us]
         long: Nominal width of bit period [us]
PPM     short: Nominal width of '0' gap [us]
         long: Nominal width of '1' gap [us]
PWM     short: Nominal width of '1' pulse [us]
         long: Nominal width of '0' pulse [us]
         sync: Nominal width of sync pulse [us] (optional)
common    gap: Maximum gap size before new row of bits [us]
        reset: Maximum gap size before End Of Message [us]
    tolerance: Maximum pulse deviation [us] (optional).
Available options are:
	bits=<n> : only match if at least one row has <n> bits
	rows=<n> : only match if there are <n> rows
	repeats=<n> : only match if some row is repeated <n> times
		use opt>=n to match at least <n> and opt<=n to match at most <n>
	invert : invert all bits
	reflect : reflect each byte (MSB first to MSB last)
	match=<bits> : only match if the <bits> are found
	preamble=<bits> : match and align at the <bits> preamble
		<bits> is a row spec of {<bit count>}<bits as hex number>
	unique : suppress duplicate row output

	countonly : suppress detailed row output

E.g. -X "n=doorbell,m=OOK_PWM,s=400,l=800,r=7000,g=1000,match={24}0xa9878c,repeats>=3"



		= Output format option =
  [-F kv|json|csv|mqtt|influx|syslog|trigger|null] Produce decoded output in given format.
	Without this option the default is KV output. Use "-F null" to remove the default.
	Append output to file with :<filename> (e.g. -F csv:log.csv), defaults to stdout.
	Specify MQTT server with e.g. -F mqtt://localhost:1883
	Add MQTT options with e.g. -F "mqtt://host:1883,opt=arg"
	MQTT options are: user=foo, pass=bar, retain[=0|1], <format>[=topic]
	Supported MQTT formats: (default is all)
	  events: posts JSON event data
	  states: posts JSON state data
	  devices: posts device and sensor info in nested topics
	The topic string will expand keys like [/model]
	E.g. -F "mqtt://localhost:1883,user=USERNAME,pass=PASSWORD,retain=0,devices=rtl_433[/id]"
	With MQTT each rtl_433 instance needs a distinct driver selection. The MQTT Client-ID is computed from the driver string.
	If you use multiple RTL-SDR, perhaps set a serial and select by that (helps not to get the wrong antenna).
	Specify InfluxDB 2.0 server with e.g. -F "influx://localhost:9999/api/v2/write?org=<org>&bucket=<bucket>,token=<authtoken>"
	Specify InfluxDB 1.x server with e.g. -F "influx://localhost:8086/write?db=<db>&p=<password>&u=<user>"
	  Additional parameter -M time:unix:usec:utc for correct timestamps in InfluxDB recommended
	Specify host/port for syslog with e.g. -F syslog:127.0.0.1:1514


		= Meta information option =
  [-M time[:<options>]|protocol|level|noise[:<secs>]|stats|bits] Add various metadata to every output line.
	Use "time" to add current date and time meta data (preset for live inputs).
	Use "time:rel" to add sample position meta data (preset for read-file and stdin).
	Use "time:unix" to show the seconds since unix epoch as time meta data.
	Use "time:iso" to show the time with ISO-8601 format (YYYY-MM-DD"T"hh:mm:ss).
	Use "time:off" to remove time meta data.
	Use "time:usec" to add microseconds to date time meta data.
	Use "time:tz" to output time with timezone offset.
	Use "time:utc" to output time in UTC.
		(this may also be accomplished by invocation with TZ environment variable set).
		"usec" and "utc" can be combined with other options, eg. "time:unix:utc:usec".
	Use "replay[:N]" to replay file inputs at (N-times) realtime.
	Use "protocol" / "noprotocol" to output the decoder protocol number meta data.
	Use "level" to add Modulation, Frequency, RSSI, SNR, and Noise meta data.
	Use "noise[:secs]" to report estimated noise level at intervals (default: 10 seconds).
	Use "stats[:[<level>][:<interval>]]" to report statistics (default: 600 seconds).
	  level 0: no report, 1: report successful devices, 2: report active devices, 3: report all
	Use "bits" to add bit representation to code outputs (for debug).


		= Read file option =
  [-r <filename>] Read data from input file instead of a receiver
	Parameters are detected from the full path, file name, and extension.

	A center frequency is detected as (fractional) number suffixed with 'M',
	'Hz', 'kHz', 'MHz', or 'GHz'.

	A sample rate is detected as (fractional) number suffixed with 'k',
	'sps', 'ksps', 'Msps', or 'Gsps'.

	File content and format are detected as parameters, possible options are:
	'cu8', 'cs16', 'cf32' ('IQ' implied), and 'am.s16'.

	Parameters must be separated by non-alphanumeric chars and are case-insensitive.
	Overrides can be prefixed, separated by colon (':')

	E.g. default detection by extension: path/filename.am.s16
	forced overrides: am:s16:path/filename.ext

	Reading from pipes also support format options.
	E.g reading complex 32-bit float: CU32:-


		= Write file option =
  [-w <filename>] Save data stream to output file (a '-' dumps samples to stdout)
  [-W <filename>] Save data stream to output file, overwrite existing file
	Parameters are detected from the full path, file name, and extension.

	File content and format are detected as parameters, possible options are:
	'cu8', 'cs8', 'cs16', 'cf32' ('IQ' implied),
	'am.s16', 'am.f32', 'fm.s16', 'fm.f32',
	'i.f32', 'q.f32', 'logic.u8', 'ook', and 'vcd'.

	Parameters must be separated by non-alphanumeric chars and are case-insensitive.
	Overrides can be prefixed, separated by colon (':')

	E.g. default detection by extension: path/filename.am.s16
	forced overrides: am:s16:path/filename.ext

```


Some examples:

| Command | Description
|---------|------------
| `rtl_433` | Default receive mode, use the first device found, listen at 433.92 MHz at 250k sample rate.
| `rtl_433 -C si` | Default receive mode, also convert units to metric system.
| `rtl_433 -f 868M -s 1024k` | Listen at 868 MHz and 1024k sample rate.
| `rtl_433 -M hires -M level` | Report microsecond accurate timestamps and add reception levels (depending on gain).
| `rtl_433 -R 1 -R 8 -R 43` | Enable only specific decoders for desired devices.
| `rtl_433 -A` | Enable pulse analyzer. Summarizes the timings of pulses, gaps, and periods. Can be used with `-R 0` to disable decoders.
| `rtl_433 -S all -T 120` | Save all detected signals (`g###_###M_###k.cu8`). Run for 2 minutes.
| `rtl_433 -K FILE -r file_name` | Read a saved data file instead of receiving live data. Tag output with filenames.
| `rtl_433 -F json -M utc \| mosquitto_pub -t home/rtl_433 -l` | Will pipe the output to network as JSON formatted MQTT messages. A test MQTT client can be found in `examples/mqtt_rtl_433_test_client.py`.
| `rtl_433 -f 433.53M -f 434.02M -H 15` | Will poll two frequencies with 15 seconds hop interval.

## Google Group

Join the Google group, rtl_433, for more information about rtl_433:
https://groups.google.com/forum/#!forum/rtl_433


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

## Releases

Version numbering scheme used is year.month. We try to keep the API compatible between releases but focus is on maintainablity.
