ServerOptions.inDevices
ServerOptions.outDevices

s.options.numInputBusChannels = 0;   // disable input
s.options.sampleRate = 44100;        // or 44100; match Audio MIDI Setup
s.boot;

iMac Microphone
iMac Speakers

// command + space => write "audio MIDI Setup"

ServerOptions.inDevices[1]

Server.default.options.inDevice_(ServerOptions.inDevices[1]);
Server.default.options.outDevice_(ServerOptions.outDevices[1]);
s.reboot;

(
{
	SinOsc.ar([200,300] !2)
}.play
)

// [command+/] => comment shortcut



(


var w, slider, amp;

w = Window("Slider Demo", Rect(200, 200, 300, 60)).front;

slider = Slider(w, Rect(20, 20, 260, 20))
.action_{ |sl| amp = sl.value};

{

	var freq = 200;

	Saw.ar(freq !2, amp)
}.scope
)

(
{

	var freq = 80;
	var detune = 0.99;
	var width = Line.kr(0.1, 0.9, 10);

	Pulse.ar([freq, freq * detune], width)
}.scope
)

( // low pass pink noise (rumble)
{
	var cutoff = MouseX.kr(20, 10000, 1);
	var noise = PinkNoise.ar !2;

	LPF.ar(noise, cutoff)
}.play
)


( // low pass pulse
{
	var cutoff = MouseX.kr(20, 10000, 1);
	var freq = 80;
	var detune = 0.99;
	var width = Line.kr(0.1, 0.9, 10);

	var pulse = Pulse.ar([freq, freq * detune], width);

	LPF.ar(pulse, cutoff)
}.play
)



( // resonance low pass pulse
{
	var cutoff = MouseX.kr(20, 10000, 1);
	var freq = 80;
	var detune = 0.99;
	var width = Line.kr(0.1, 0.9, 10);

	var pulse = Pulse.ar([freq, freq * detune], width);
	var res = MouseY.kr;

	RLPF.ar(pulse, cutoff, res)
}.play
)

(
{
	var freq = 60;
	var sound = SinOsc.ar(freq);
	var speed = 4;
	var pulse = Impulse.kr(speed);
	var env = EnvGen.kr(Env.perc(releaseTime: 1/speed), pulse);

	sound * env
}.scope
)