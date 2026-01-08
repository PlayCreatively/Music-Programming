---
title: MIDI and Open Sound Control
subtitle: Sound and Music Programming week 3
author: Dr. Matt Bellingham -- <matt.bellingham@port.ac.uk>
institute: University of Portsmouth
date: Wednesday 15th October 2025
header-includes:
  - \usetheme[progressbar = frametitle]{metropolis}
  - \usecolortheme[barn]{owl}
  - \titlegraphic{\includegraphics[width=2.5cm]{"/Users/mattb/Library/CloudStorage/OneDrive-UniversityofPortsmouth/3 Resources/Images/UOP_Faculty_Logo_LockUp_CCI_Linear_RGB-N-A.png"}}
mainfont: Inter
monofont: SF Mono
incremental: no
highlight-style: breezedark
aspectratio: 1610
lang: en-GB
urlcolor: red
section-titles: true
bibliography: /Users/mattb/Documents/scripts/bib/zotero.bib
csl: '/Users/mattb/Library/CloudStorage/OneDrive-UniversityofPortsmouth/3 Resources/scripts/bib/apa.csl'
---

## Protocols
* In computer science, a protocol is a set of rules for transmitting data between devices.
	* Example: MIDI
	* Other protocols: HTTP (HyperText Transfer Protocol), FTP (File Transfer Protocol), etc.
* All data is stored/transferred as bytes. A protocol establishes how to interpret those bytes
	* Sidebar: File extensions describe the encoding of bytes in files and how to interpret them as data
* MIDI encodes musical data as bytes. OSC (Open Sound Control) is another, more flexible, way of encoding musical data. 

## MIDI protocol
A Note On message indicates the beginning of a MIDI note

The message consists of three bytes of information: MIDI note number; MIDI channel number; MIDI velocity value

In general, MIDI note 60 is assigned to middle C key, and notes 21-108 correspond to the 88 keys of an extended keyboard controller


## MIDI protocol
The final byte indicates the velocity at which the key was pressed

Higher velocities lead to louder notes

A `Note Off` message indicates the end of a MIDI note

If the instrument being played has a release (or decay) phase, it will begin that phase when the message is received

## MIDI messages
A MIDI message typically comprises of two/three bytes.

There are two types of MIDI bytes, a status byte and a data byte.

The first bit of every byte indicates whether it is a status or a data byte which results in 7 available bits (leaving us 128 possible values).

## MIDI status byte

The status byte contains 4 bits to indicate the type of message and 3 bits to indicate the channel number that the message is sent on.

## Open Sound Control
> The basic unit of OSC data is a message, consisting of an address pattern, a type tag string, and arguments. The address pattern is a string that specifies the entity or entities within the OSC server to which the message is directed (within the “Addressing Scheme” described below) as well as what kind of message it is. The type tag string gives the datatype type of each argument. The arguments are the data contained in the message. For example, a message’s address pattern might be `/voice/3/freq`, it's type string might indicate that there is a single floating-point argument, and the argument might be `261.62558` [@wrightOpenSoundControl2005].

## Software used in our OSC workshop
### Proprietary
* [Max](https://cycling74.com/products/max)

### Open
* [Pure Data](http://msp.ucsd.edu/software.html)
* [Processing](https://processing.org)
* [Ardour](https://ardour.org) - see the [OSC pages](https://manual.ardour.org/using-control-surfaces/controlling-ardour-with-osc/) for full details of how to control Ardour via OSC
* [SuperCollider](https://supercollider.github.io)


## Open Sound Control
> Entities within a system are addressed individually by an open-ended URL-style symbolic naming scheme that includes a powerful pattern matching language to specify multiple recipients of a single message [@freedFeaturesFutureOpen2009].


## OSC
* OSC (Open Sound Control) is a protocol for digital music/multimedia devices developed at UC Berkeley at their Center for New Music and Audio Technology (CNMAT).
* Like MIDI, OSC is designed for real-time control of sound/media.
* Benefits [from @wrightOpenSoundControl2021]:
	* Open-ended, URL-style symbolic naming scheme
	* Symbolic and high-resolution numeric argument data
	* Remember with MIDI data many of the parameters were limited from 0-127
	* Pattern matching language to specify multiple recipients of a single message
	* Single messages can be routed to multiple procedures on an OSC server
	* High resolution time tags (64 bit values)
	* 'Bundles' of messages whose effects must occur simultaneously

## SC’s client-server model
SC’s client and server communicate with each other internally using OSC.

## OSC
OSC Address pattern is a `/` separated address encoding (similar to URL encoding) that specifies the address of a procedure/function to execute on the server

OSC type tag string defines the type of the arguments for the procedure at the specified address.

Earlier versions of the OSC protocol omitted type tag strings. The comma is used to distinguish that there is in fact an OSC type tag string.

All arguments are multiples of 4 bytes

## OSC messages

| Packet size | OSC address pattern | OSC tag type string | Arguments |       |     |     |     |
| ------ | -------- | ------- | --------- | ----- | --- | --- | 
| 48          | `/sounds/sine`        | `,ffff`               | 401.5     | 45.53 | 1.0 | 0.0 |   |


## Type tags

| OSC tag types | Type         |
| ------------- | ------------ |
| `i`             | 32-bit int   |
| `f`             | 32-bit float |
| `s`             | String       |
| `b`             | Blob         |


## OSC vs. MIDI
### Portability
The MIDI protocol is universally recognised by music hardware/software. Can essentially play MIDI file/data anywhere

OSC can be recognised by any OSC server. Client/Server need to agree on addressing space/methods. OSC provides a syntax for communicating but doesn’t agree on a 'language' to communicate musical data.

### Flexibility
MIDI is restrictive. Data is generally confined to one byte. Only can encode certain musical data though there are alternatives using system exclusive messages.

### Resolution
MIDI has poor resolution, especially for parameters like pitch. Restricted to a range of 0-127

OSC has up to 64-bit resolution for any datatype and the ability to send even higher, user-defined resolutions via OSC blobs

## Networking - localhost
* The term localhost in networking refers to the destination address to your own computer when using internet protocols.
	* Provides a loopback interface
	* IP address – `127.0.0.1` (so private IP address)
* When you run SuperCollider on your own computer, sclang communicates with `scsynth` via localhost
* `s.addr; posts` -> `NetAddr(127.0.0.1, 57110)`

## Ports
* A port is a communication endpoint on a device.
* Messages need to be directed to specific programs running on a device.
	* Ports are addresses for destination messages on a given device.
	* For example, `scsynth` generally uses port 57110 if it is available to receive communication
	* `sclang` generally uses port 57120 if it is available to receive communication
	* `scsynth` does need to send messages to `sclang` in certain instances. Think about the method .poll.
	* Messages sent via HTTP to a web server are received on port 80.
* Servers assign ports to running programs (i.e., processes) so that incoming messages get forwarded properly to the correct application.
	* `s.addr; posts` -> `NetAddr(127.0.0.1, 57110)`

## OSCdef
`sclang` can be configured to listen to incoming OSC messages and process them via the class `OSCDef`

Each `OSCDef` requires a function that will process the incoming message


## SC and Max via OSC
![Max sending OSC to SuperCollider](images/max.png){height=80%}

## SC and Processing via OSC
![Setting up OSC in Processing](images/oscP5.png){height=80%}

## SC and Processing via OSC
![Setting up SuperCollider control in Processing](images/SC_Processing.png){height=80%}

## OSC to Ardour
![Setting up OSC control in Ardour](images/ardour.png){height=80%}

## Ardour
<https://manual.ardour.org/using-control-surfaces/controlling-ardour-with-osc/osc-control/>

Only for interest today - there’s no need to get it unless it seems useful to you. [The demo is free, full version whatever you want to pay](https://community.ardour.org/download)


## Free OSC phone apps
## iOS

ZIG SIM for iOS: <https://apps.apple.com/us/app/zig-sim/id1112909974>

Mrmr OSC controller for iOS: <https://apps.apple.com/us/app/mrmr-osc-controller/id294296343>

## Android
ZIG SIM for Android via an APK: <https://apkpure.com/zig-sim/com.onetoten.app.zig_sim>

OSC Controller for Android: <https://play.google.com/store/apps/details?id=com.ffsmultimedia.osccontroller&hl=en_CA>

The most widely used paid OSC phone app is TouchOSC: <https://hexler.net/touchosc>

TouchOSC mark 1 is in maintenance mode but is still useful: <https://hexler.net/touchosc-mk1>
Around £5: <https://apps.apple.com/us/app/touchosc-mk1/id288120394> or <https://play.google.com/store/apps/details?id=net.hexler.touchosc_a>

The full TouchOSC is around £20: <https://hexler.net/touchosc>


## References {.allowframebreaks}


