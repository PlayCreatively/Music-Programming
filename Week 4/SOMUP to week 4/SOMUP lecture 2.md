---
title: An Introduction to Music and Human-Computer Interaction
subtitle: Sound and Music Programming week 2
author: Dr. Matt Bellingham -- <matt.bellingham@port.ac.uk>
institute: University of Portsmouth
date: Wednesday 8th October 2025
header-includes:
  - \usetheme[progressbar = frametitle]{metropolis}
  - \usecolortheme[snowy]{owl}
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

![EA Games sessions](/Users/mattb/Library/CloudStorage/OneDrive-UniversityofPortsmouth/0\ Inbox/EA.png){height=80%}

## Aims of the module
The module aims to foster dialogue on, and develop skills in, the design and creation of tools for sound and/or music. You will see and critique a variety of existing approaches, then develop your own original design. This may take the form of a novel digital musical instrument, interface/controller, interactive software, installation or sound toy. You will also make an initial evaluation of your design, and consider possibilities for subsequent deeper evaluation. You will also work in strategic partnership with AI tools, including large language models (LLMs), to support ideation, development, and debugging, while maintaining deep conceptual and technical understanding.

## Plan for today
* Start to focus on the possibilities for the module assessment
* Introduce the research area of Music and Human–Computer Interaction
* Provide some inspiration that you might carry over into your project ideas
* Discuss how large language models (LLMs) can support your coding and design process

## Learning outcomes
- LO1: Draw upon current research to conceive and design an original audio software\* artefact.
- LO2: Justify and evaluate decisions in the implementation of an original audio software\* artefact.
- LO3: Apply advanced knowledge and techniques of computational sound to the creation of audio software\*.
- LO4: Critically evaluate the success of their work against the stated aims and current research.

\*: Software, or software with hardware input and/or output.


## What is an interface?
![Rotary pots](images/knobs.jpeg){height=70%}

## What is an interface?
![Ableton *Launchpad*](images/launchpad.jpeg){height=70%}

## What is an interface?
![Guitar game controllers](images/guitar-game.jpeg){height=70%}

## What is an interface?
![Guitar MIDI controller](images/starr-guitar.jpeg){height=70%}

## What is an interface?
![Another angle of the Starr controller](images/starr-guitar2.jpeg){height=70%}

## What is an interface?
![Fender Telecaster](images/telecaster.jpeg){height=70%}

## What is an interface?
![Mapping inputs to outputs](images/mapping.png){height=70%}

## What is an interface?
![The action-reaction cycle [@lemanEmbodiedMusicCognition2008]](images/action-reaction.png){height=70%}

## What is an interface?
![Human-machine interaction [@Bongers:2006aa]](images/bongers-human-machine-interaction.png){height=70%}

## What is an interface?
![Various general inputs and outputs](images/inputs-outputs.png){height=70%}

## What is an interface?
![Trackpad gestures](images/windows-10-touch-gestures.jpg){height=70%}

## What is an interface?
![A Wiimote being used as an instrument.](images/wiimote-midi-osc.png){height=70%}

## What is an interface?
![OSC output controlled by a Kinect camera.](images/kinect-osc.png){height=70%}

## What is an interface?
![A phone being used in conjunction with an acoustic guitar.](images/guitar-phone.jpg){height=70%}

## What is an interface?
![A chat interface - the new GUI?](images/chattyg.png){height=70%}

## Which contexts might you work in?

- Musical instrument/performance tool
- Studio tool
- Learning aid
- Composition/production aid to support the creative act
- Sound installation
- Virtual environment


## Assessment
The assessment for *Sound and Music Programming* consists of three components:

1 -**Technical artefact**: A standalone piece of audio software or a bespoke system combining hardware and software. You must document which portions of code were generated with AI assistance versus written entirely by you. Use comments to indicate AI contributions and your modifications. A README file should summarise the aims and usage of your software. A video demonstration must be provided. All code must be version-controlled using Git, and a tagged GitHub repository link must be submitted.

## Assessment

2 - **AI collaboration portfolio**: A Markdown document (approx. 2000–2500 words) demonstrating your strategic partnership with AI tools. It should include:

   - Strategic AI briefing documentation
   - Example prompts and AI outputs
   - Critical filtering and decision making
   - Collaboration strategy reflection
   - Reflective annotation on aims, influences, implementation, evaluation, and references

## Assessment

3 - **Viva voce**: A 30-minute oral examination where you demonstrate your software, explain technical concepts, justify design decisions, and discuss your AI collaboration process. You must be able to modify code live and respond to technical questions. The session will be recorded and submitted with your portfolio.

All AI contributions must be transparently documented. You are expected to maintain conceptual ownership and verify AI-generated information. Strategic use of AI is a core part of the assessment.


## NIME---New Interfaces for Musical Expression

> Musical interface construction proceeds as **more art than science**, and possibly this is the only way that it can be done (Cook, 2001)

NIME = Art + Science

NIME = Music + Engineering + HCI

[NIME archives](https://www.nime.org/archives/)

* Instrument designers have tended to quickly explore new interaction technologies and subsequently contributed to HCI more broadly;
* Musical instruments demand nuanced interaction - a great test of new technologies.

## Digital Musical Instrument (DMI)

![DMI layout](images/DMI.png){width=80%}

* Any controller can be combined with any kind of sound generation.
* DMIs can be almost any shape and size, from handheld DMIs for one user to architectural scale for many users.

## A NIME Taxonomy [@Jensenius:2017aa]

Lots of new instruments/interfaces/controllers (etc.) presented at NIME over 20 years, but a few broad types [@Jensenius:2017aa]:

* extended/augmented instruments
* instrument-like controllers
* instrument-inspired controllers
* alternative controllers
* collaborative instruments

## A NIME Taxonomy [@Jensenius:2017aa]

* AUGMENTED instruments: traditional instruments augmented with sensor technology.
* INSTRUMENT-LIKE controllers: new designs strongly based on traditional instruments.
* INSTRUMENT-INSPIRED controllers: new instruments inspired by, but not based on, traditional instruments.
* ALTERNATIVE controllers: new instruments which are not based on any traditional instrument.
* COLLABORATIVE instruments: those played/can be played by more than one person.


## Extended/Augmented Instruments
* Extensions or ‘add ons’ to more tried and tested instruments.
* Typically involve adding sensors and/or signal processing to traditional instrument designs.
* Why might someone build an augmented instrument?
* What might the advantages and disadvantages be?

## Extended/Augmented Instruments - some examples

[Augmented Guitar](https://www.youtube.com/watch?v=5LtYwuTcWdY)

[TouchKeys](https://www.youtube.com/watch?v=qwTv8JPH5cQ) - reminiscent of [Roli's hardware](https://roli.com/uk)

[Augmented violin](https://www.youtube.com/watch?v=UKRrEdS_SMI)

[T-VOKS](https://www.youtube.com/watch?v=jJdVsv_-WIo)

## Instrument-Like and Instrument-Inspired Controllers

Interface is closely or more loosely based on traditional musical instrument designs, but (because a controller rather than an instrument) sound generation and mapping can be completely different.

[New Toy (2019)](https://www.youtube.com/watch?v=qlPNhG-vMsY)

[Haken Continuum](https://www.youtube.com/watch?v=vKky73-9yOU) - see the [Haken Audio site](https://www.hakenaudio.com/)

[ROLI Seaboard Rise](https://www.youtube.com/watch?v=E14aKskrIgs) and the new [ROLI Piano and Airwave](https://youtu.be/bxYfWekmx-A?si=yHJ8TIFlGbU7PBIy)


## Alternate Controllers
Not based on and/or actively avoid the language of old designs.
Many are one-offs/for designer use only, but a few have been released commercially.

## ReacTable

![ReacTable](images/Reactable_Multitouch.jpg){height=70%}

## ReacTable

![ReacTable](images/reactable1.jpg){height=60%}

<https://www.youtube.com/watch?v=vm_FzLya8y4>

## Yamaha Tenori-On

![The Yamaha TENORI-ON](images/tenori-on.jpg){height=60%}

<https://www.yamaha.com/en/about/design/synapses/id_005/>

<https://www.youtube.com/watch?v=hzcpTMO0CrI>

## E-textiles

From the great @IntelligentInstrumentsLab2025, an interesting piece of work by @skachEtextiles2020.

<https://youtu.be/VT8Ht0lf_F4?si=1LMKMBy_TUVl6Vcz>

Intelligent Instruments Lab: <https://iil.is/>


## Collaborative Instruments
Intended for use by more than one player.

Because few traditional instruments are for more than one player, they tend also to come under the alternate controller category.

[Stanford Mobile Phone Orchestra](https://www.youtube.com/watch?v=ADEHmkL3HBg)

[Princeton Laptop Orchestra (PLOrk)](https://www.youtube.com/watch?v=gOsaANAfZcw)

[Dirty Electronics Ensemble](https://www.youtube.com/watch?v=ZpBxL4WExWc) - see [Dirty Electronics](https://www.dirtyelectronics.org/) and [the DMU ensemble](https://www.dmu.ac.uk/jukebox/dirty-electronics-ensemble.aspx)

[Symphony for 100 car radios](https://cdm.link/theres-a-synth-symphony-for-100-cars-coming-based-on-tuning/)


## Useful resources
* The [NIME conferences over the last ~10 years](https://nime.org/past-nimes/) offer a huge range of inspirational work
* [PPIG](https://www.ppig.org) - wide range of creative applications of technology [@Blackwell:2019ab]
* [ICMC](https://quod.lib.umich.edu/i/icmc/) - some musical interfaces amongst other kinds of computer music
* [Computer Music Journal](https://direct.mit.edu/comj) - as above
* [TEI](https://tei.acm.org/) - some music/audio-related works [e.g. @wilkieWhatCanLanguage2010] amongst more general HCI.
* Sound art/sonic art, e.g. in [Leonardo Music Journal](https://direct.mit.edu/lmj)

## Obsidian
A good local Markdown editor which pairs well with GitHub. Very widely used by programmers for notes and as a 'second brain'.

<https://obsidian.md/>


## References {.allowframebreaks}