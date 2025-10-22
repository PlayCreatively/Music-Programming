---
title: Possible approaches to music and HCI
subtitle: Sound and Music Programming week 3
author: Dr. Matt Bellingham -- <matt.bellingham@port.ac.uk>
institute: University of Portsmouth
date: Wednesday 15th October 2025
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

## Recap of week 2
- We explored the concept of **interfaces** in musical contexts, from traditional instruments to novel digital systems.
- We introduced the field of **Music and Human-Computer Interaction (HCI)**, with reference to the **NIME** community and taxonomy of new musical interfaces.
- We discussed **Digital Musical Instruments (DMIs)** and their potential for creative expression and technical innovation.

## Recap of week 2
- **Assessment preparation:**
	- We talked about the expectations for the **technical artefact**, **AI collaboration portfolio**, and **viva voce,** including the **strategic use of AI tools** (e.g. LLMs) for ideation, coding, and reflection, with transparent documentation of AI contributions.
- **Inspirational examples:**
	- Augmented instruments (e.g. TouchKeys, T-VOKS)
	- Instrument-like and alternative controllers (e.g. ROLI Seaboard, ReacTable, Tenori-On)
	- Collaborative instruments (e.g. PLOrk, Dirty Electronics Ensemble)
- **Tools and resources:**
	- Recommended using **Obsidian** for documentation and **GitHub** for version control.
	- Considered the **NIME archives**, **PPIG**, **ICMC**, and **Computer Music Journal** for further research.

## In today's session

- **Design strategies**
	- Including **convergent** and **divergent** design methods, linked to bundling/unbundling in systems design.
	- Frameworks for **systematic innovation** and **design thinking** in musical HCI.
- **Theoretical foundations** and **critical perspectives**
	- The **three waves of HCI**:
		- **First wave**---Human factors and cognitive science (efficiency, usability).
		- **Second wave**---Social systems and ethnography (contextual enquiry, participatory design).
		- **Third wave**---Culture and experience (aesthetics, affect, speculative design).
- **Next steps**
	- Identifying an **area of interest** and undertaking early research


## Convergence and divergence
### Convergence
* Merge features from two candidate designs to produce a better one
* Discard ideas that poorly fit the desired outcome

### Divergence
* Generate new designs from existing one
* Use any creative technique, e.g. reduction to absurdity, exploring metaphors

Linked to *bundling* and *unbundling* in systems design.

--------

![Design convergence](images/course-fine.png){height=80%}

----

![Framework for innovation](images/Framework_for_Innovation_transparent.png){height=90%}

----

![Systematic design](images/Systemic_Design_Framework_transparent.png){height=90%}


## Why theory in HCI?
We want to make interactions with computers faster, more productive, more creative, more social, more fun — put simply, to make them better.

It is very hard to stumble into a good design without some structure.

Theories give us ways to criticise proposed designs, and toolkits for inventing new ones.

## Three waves of HCI [@Cooper:2007aa]
First wave (1980s) — Theory from human factors, ergonomics, and cognitive science

Second wave (1990s) — Theory from anthropology, sociology, and work psychology [@Blackwell:2003aa]

Third wave (2000s) — Theory from art, philosophy, and design [@Sengers:2010aa]

## First wave: HCI as engineering 'human factors’
* The 'user interface’ (or MMI — man-machine interface — note the dated gender specificity used at the time) is a separate module, designed independently of the main system.
* Design goal is efficiency (speed and accuracy) for a human operator to achieve well-defined functions.
* Use methods from cognitive science to model user’s perception, decision and action process, and predict usability.

There is also some clear messaging in some of these designs; what are they telling us?

--------

![Apollo-Soyuz controls (1975)](images/control.png){height=80%}

----------

![EMS VCS3 (1969)](images/synth.png){height=80%}

------

![The *DB33* Hammond synth in Pro Tools.](images/DB-33_Organ_01.jpeg){height=80%}

------

![The *Vacuum* synth in Pro Tools.](images/Vacuum_01.jpeg){height=80%}


## Theories give a critical perspective
Let’s look at a VCV Rack example and consider the Gestalt theory of perceptual organisation [@Todorovic:2008um]---for example ...

<https://www.verywellmind.com/gestalt-laws-of-perceptual-organization-2795835>

<https://en.wikipedia.org/wiki/Principles_of_grouping>

-------

![VCV Rack](images/vcv.png){height=80%}

-------


![Continuity - do we 'read’ lines as continuous?](images/continuity.png){height=80%}

------

![Similarity - are similar things grouped together?](images/similarity.png){height=80%}

--------

![Pragnanz - do we perceive the image in the simplest possible way?](images/pragnanz.png){height=80%}

---------


## Second wave: HCI as social system
* The design of complex systems is a socio-technical experiment — needs to take account of other information factors including conversations, paper, physical settings.
* Study the context where people work — use ethnography and contextual enquiry to understand other ways of seeing the world.
* Other stakeholders are integrated into the design process — prototyping and participatory workshops aim to empower users and acknowledge other value systems.

------

![An information system](images/office.png){height=80%}

--------

![An information system](images/orchestra.png){height=80%}

--------

![An information system](images/laptop.png){height=80%}


## Second wave: HCI as social system
Some relevant social systems about which we can think ethnographically; how do people work? How can the system fit into this model?

[Google Wave](https://en.wikipedia.org/wiki/Google_Wave) --> [Google Docs](https://en.wikipedia.org/wiki/Google_Docs)

[BandLab](https://www.bandlab.com)

[Figma](https://www.figma.com)

[Open Sound Control](https://en.wikipedia.org/wiki/Open_Sound_Control) as interstitial tissue; we will come back to this protocol to allow us to network multiple devices in real-time.


## Third wave: HCI as culture and experience
* Ubiquitous computing affects every part of our lives — it mixes public (offices, lectures) and private (bedrooms, bathrooms).
* Outside the workplace, efficiency is not a priority — usage is discretionary; user experience (UX) includes aesthetics, affect.
* Design experiments are speculative and interpretive — critical assessment of how this is meaningful.

-------

![Dunne and Raby - Teddy blood bag radio [-@Dunne:2009aa; see also @dunneDesignDebate2008]](images/blood.png){height=70%}

-------

![Dunne and Raby - Faraday chair [-@Dunne:1995aa]](images/dunne.png){height=70%}

<https://collections.vam.ac.uk/item/O63805/faraday-chair-chair-dunne-raby/>

-------

![Ring Drone (2020)](images/drone.png){height=80%}

## Mark McKeague — City Symphonies

![Mark McKeague — City Symphonies](images/traffic.png){height=50%}

<https://markmckeague.com/work/city-symphonies>

<https://player.vimeo.com/video/44197369>

<https://markmckeague.com/work/ototo>


## Third wave: HCI as culture and experience
- Culture and experience
- Not focussed on speed and accuracy, but on aesthetics
- Making music or art for pure pleasure---autotelic practice
- Treating users as co-creators and participants, rather than as subjects
- Playful; consider Steven Johnson's book *Wonderland* [-@johnsonWonderland2017]

<https://www.ted.com/talks/steven_johnson_the_playful_wonderland_behind_great_inventions>


------

![The often-used *cone of possibilities*](images/futures.png){height=80%}

--------

![An updated cone of possibilities, taken from @gallHowVisualiseFutures2022](images/gallcone.png){height=80%}

----

![Design types](images/design-research.png){height=80%}

## Alternative approaches you may wish to consider

* Positive computing — e.g. @calvoPositiveComputingTechnology2014 — wellbeing, flow, empathy, mindfulness, altruism.
* Inclusion and accessibility — physical and sensory capabilities, ageing, low income, human rights.
* Feminist utopianism — e.g. @bardzellFeministHCITaking2010 — amplifying marginalised voices.

-------

![Prototyping continuum [@Lepore:2010aa]](images/prototyping.jpg){height=80%}

----------

## For the next session ...
* Think about the rough area you are interested in exploring.
* What other tools/interfaces/formalisms are there in this area?
* Find at least two existing solutions or implementations in the same or a similar area.




## References {.allowframebreaks}