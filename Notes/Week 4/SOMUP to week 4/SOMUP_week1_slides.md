---
title: Introduction to *Sound and Music Programming*
subtitle: Sound and Music Programming week 1
author: Dr. Matt Bellingham -- <matt.bellingham@port.ac.uk>
institute: University of Portsmouth
date: 1 October 2025
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

## Today's session

* **Part 1**: Introductions, software setup, combinatorial creativity
- **Break:** 10:30--10:45
- **Part 2:** Module overview & AI collaboration strategies

### Tasks to complete before next week
- Install **SuperCollider** on your own computer
- Install **Obsidian** on your own computer
- Create a **GitHub account** ready for week 2
- Make sure you have access to **Copilot Chat**

## Introductions
- What led you to choosing this module?
- What audio work have you done in the past?
- What audio programming environments have you had the opportunity to use before?
- What audio/music or other creative tools do you find inspiring or interesting?

## GitHub
> GitHub is a cloud-based platform where you can store, share, and work together with others to write code. Storing your code in a "repository" on GitHub allows you to:
> 
> - Showcase or share your work.
> - Track and manage changes to your code over time.
> - Let others review your code, and make suggestions to improve it.
> - Collaborate on a shared project, without worrying that your changes will impact the work of your collaborators before you're ready to integrate them.
> 
> Collaborative working, one of GitHub's fundamental features, is made possible by the open-source software, Git, upon which GitHub is built.


## Version control
GitHub is an example of a [Version control system (Wikipedia)](https://en.wikipedia.org/wiki/Version_control)

![A version control system](https://qph.cf2.quoracdn.net/main-qimg-8451a3ecbca8820d36328d27bb19eed4-pjlq){height=70%}

## Markdown
<https://www.markdownguide.org/basic-syntax/>

> **Markdown** is a [lightweight markup language](https://en.wikipedia.org/wiki/Lightweight_markup_language "Lightweight markup language") for creating [formatted text](https://en.wikipedia.org/wiki/Formatted_text "Formatted text") using a [plain-text editor](https://en.wikipedia.org/wiki/Text_editor "Text editor"). [John Gruber](https://en.wikipedia.org/wiki/John_Gruber "John Gruber") created Markdown in 2004 as a [markup language](https://en.wikipedia.org/wiki/Markup_language "Markup language") that is easy to read in its source code form. Markdown is widely used for [blogging](https://en.wikipedia.org/wiki/Blog "Blog") and [instant messaging](https://en.wikipedia.org/wiki/Instant_messaging "Instant messaging"), and also used elsewhere in [online forums](https://en.wikipedia.org/wiki/Online_forums "Online forums"), [collaborative software](https://en.wikipedia.org/wiki/Collaborative_software "Collaborative software"), [documentation](https://en.wikipedia.org/wiki/Documentation "Documentation") pages, and [readme files](https://en.wikipedia.org/wiki/README "README").

## Bricolage
[Bricolage](https://en.wikipedia.org/wiki/Bricolage)

> In art, bricolage is a technique or creative mode, where **works are constructed from various materials available or on hand**, and is often seen as a characteristic of postmodern art practice. It has been likened to the concept of curating and has also been described as the **remixture, reconstruction, and reuse** of separate materials or artifacts **to produce new meanings and insights**.

## Knowledge management
Paul, A. M. (2021). [The Extended Mind: The power of thinking outside the brain](https://anniemurphypaul.com/books/the-extended-mind/). Eamon Dolan Books.

[Commonplace book](https://en.wikipedia.org/wiki/Commonplace_book)

[Memex](https://en.wikipedia.org/wiki/Memex), a precursor to hypertext by [Vannevar Bush](https://en.wikipedia.org/wiki/Vannevar_Bush)

[Zettelkasten](https://en.wikipedia.org/wiki/Zettelkasten)

[Building a Second Brain](https://www.buildingasecondbrain.com)

Ideas and thinking have a compound interest that accretes over time. See Andy Matuschak's work in this area, e.g. [Evergreen note-writing as fundamental unit of knowledge work](https://notes.andymatuschak.org/zR6RRbCfY5rFkiimFnaJZKB)

## Obsidian
> But most importantly, without a permanent reservoir of ideas, you will not be able to develop any major ideas over a longer period of time because you are restricting yourself either to the length of a single project or the capacity of your memory. Exceptional ideas need much more than that.
>
> The things you are supposed to find in your head by brainstorming usually don't have their origins in there. Rather, they come from the outside: through reading, having discussions and listening to others, through all the things that could have been accompanied and often even would have been improved by writing.

We will make use of Obsidian as an example of a modern PKM app that uses Markdown: <https://obsidian.md/>

## Specific knowledge
<https://nav.al/specific-knowledge>

We can start to develop new areas and new insights by bringing together two or more domains.

> ... **specific knowledge is found ... by pursuing your innate talents, your genuine curiosity, and your passion**.

- Specific knowledge can't be trained
- Specific knowledge is found by pursuing your curiosity
- Building specific knowledge will feel like play to you

## SuperCollider
### What is it?
An incredibly powerful language for synthesis and musical composition.

### Why use it?
Uses all of the core programming concepts found in lower level languages such as C++ in a fashion streamlined for rapid prototyping.

### What differentiates itself from other tools or languages?
Speed of development, comprehensive GUI tools, can run comfortably over a network, easily embeddable in other systems.

Install SuperCollider on your own PC/Mac: [https://supercollider.github.io/downloads](https://supercollider.github.io/downloads)

## SC140
Each track is constructed from a single Tweet less than 140 characters in length - see [https://supercollider.github.io/sc-140.html](https://supercollider.github.io/sc-140.html)

```js
play{LeakDC.ar(BRF.ar(Saw.ar(8,Decay2.kr(x=Duty.kr(1/8,0,Drand([0,Drand((0.4,0.5..1))],inf)),0.01,0.3))**1.5,x*20+[45.1,45],0.1)).tanh}//#sc
```

```js
play{AllpassC.ar(SinOsc.ar(55).tanh,0.4,TExpRand.ar(2e-4, 0.4,Impulse.ar(8)).round([2e-3,4e-3]),2)};// #supercollider with bass please...
```

---

![The usability expressivity continuum](images/continuum.png){height=80%}

---


## Audio programming languages
A programming language designed for audio and/or music work.
The language contains relevant abstractions for the user’s convenience.

The language 'understands' the tools and protocols that the user will need - oscillators, filters, envelopes, MIDI, OSC, etc. The user does not need to build these from scratch.

Most audio programming languages differentiate between audio signals and control signals.

## Audio programming languages

### Graphical languages
* Examples---Max [@cycling74Max2024], Pure Data [@puckettePureData2024]
* Typically use a unidirectional patch-cable metaphor for output/input---quick to learn
* Visual, and therefore easier to 'read' signal flow
* Large projects can become hard to read, manage, and change

## Audio programming languages

### Text-oriented languages
* Examples---SuperCollider [@mccarthySuperCollider2024], Csound [@Vercoe:2014aa], ChucK [@Wang:2008aa]
* Not visual, making them initially harder to 'read'
* Basic syntax needs to be learned up-front
* Highly expressive, and allows for significant efficiencies



## Module structure

All our sessions will run from 9am to 12pm on Wednesday mornings in TB1. The first six weeks will blend lecture content with workshops. The remaining sessions will consist of a two-hour workshop with drop-in time as you develop your artefact.

- Lectures **define**
- Workshops **implement**
- Drop-ins **support**

## Module topics at a glance

- Music and HCI
- Version control
- Synth design
- Patterns
- Control mechanisms
- Temperament and MIDI
- Modulation control
- Routing and signal flow
- Envelope generators
- Sample playback
- Digital filter theory
- Phase shifting
- FIR and IIR filters
- Algorithmic composition
- Evolutionary Algorithms (EA) and Genetic Algorithms (GA)



## Terminology check

*Don't worry if most or all of these topics are unfamiliar!*

- Sound propagation
- Wavelength, frequency, amplitude
- Harmonic content and the harmonic series
- Envelopes
- Localisation
- Decibels
- Equal loudness contours
- Logarithms
- Metering, including reference levels
- Synchronisation (e.g. SMPTE, word clock)
- MIDI


## Module topics at a glance
* Audio theory
* Digital audio
* Digital synthesis
* Object-oriented design
* Delay-based effects
* Spectral audio processing
* Software project management and version control
* OSC
* Processing audio dynamics
* Generative audio

## Your AI use up to now

What LLMs do you use? How often? For what?

## AI in programming - paradigm shift

The role of the programmer is changing fundamentally. Instead of focusing solely on writing code, the modern developer is becoming an orchestrator of AI tools.

* You will be a supervisor, not a simple typist [@orchardBabyStepsSemiautomatic2025; @spiessHowUseClaude2025].
* Your job is to provide clear direction, manage the process, and ensure quality [@orchardBabyStepsSemiautomatic2025; @reedWaterfall15Minutes2025; @spiessHowUseClaude2025].
* The AI handles the repetitive, tedious parts of the work, leaving you to focus on design and architecture [@grebenyukkeanClaudeCodeExperience2025].

## The Plan/Execute Cycle

A common theme amongst experienced AI-augmented programmers is the use of a structured workflow.

* **Plan:** Start by writing a detailed specification or plan.md file [@ledbetterUsingPlanExecute2025; @orchardBabyStepsSemiautomatic2025; @reedMyLLMCodegen2025].
* **Execute:** Use the AI to implement the plan, with you in the loop, supervising and providing feedback [@reedLLMCodegenHeros2025].
* **Trust and Tools:** The more you trust the AI, the more you can automate. Some even use the AI as a universal computer interface, trusting it with full filesystem access [@steinbergerClaudeCodeMy2025].

## Test, document, communicate

As code generation becomes cheap and fast, the tiebreaker for successful products is shifting from code elegance to user experience [@reedMyLLMCodegen2025]. This means new skills are paramount.

* **Defensive Coding:** You need to catch errors introduced by AI agents [@ronacherAIChangesEverything2025].
* **Strategic Thinking:** The focus moves to architectural decisions and problem-solving [@ballAmpNowAvailable2025]. The AI can handle the 'paint-by-numbers' work.
* **Effective Prompting:** Strong writing skills are critical. Your ability to craft clear, concise, and detailed prompts is a key factor in the AI's success [@reedWaterfall15Minutes2025].

## The spectrum of AI use

Not everyone approaches AI use in the same way. These articles show a few interesting philosophies.

* Some developers, like Geoffrey Litt, use AI for 'vibe coding', prioritising fun and personal utility over production-level techniques [@littStevensHackableAI2025].
* Others, like Max Woolf, are more pragmatic, viewing LLMs as a powerful but not universal tool to be used via API for specific problem-solving tasks, dismissing 'vibe coding' as unprofessional [@woolfExperiencedLLMUser2025].
* Ultimately, AI in coding is not a fundamental shift in abstraction, but a change in 'velocity,' allowing you to spend more time on design and less on the implementation grind [@grebenyukkeanClaudeCodeExperience2025; @orchardBabyStepsSemiautomatic2025].

## AI in programming - examples

* <https://harper.blog/2025/04/17/an-llm-codegen-heros-journey/>
* <https://lucumr.pocoo.org/2025/6/4/changes/>
* <https://maryrosecook.com/blog/post/become-an-ai-augmented-engineer>
* <https://me.micahrl.com/blog/llm-plan-execute-cycle/>
* <https://blog.lmorchard.com/2025/06/07/semi-automatic-coding/>
* <https://harper.blog/2025/02/16/my-llm-codegen-workflow-atm/>


# Module assessment

## Learning outcomes

LO1: Draw upon current research to conceive and design an original audio software artefact.

LO2: Justify and evaluate decisions in the implementation of an original audio software artefact.

LO3: Apply advanced knowledge and techniques of computational sound to the creation of audio software.

LO4: Critically evaluate the success of their work against the stated aims and current research.



## Assessment overview
### Technical Artefact
The technical artefact comprises 50% of the assessment and includes audio software with README, video demo, and codebase.

### AI Collaboration Portfolio
The AI portfolio accounts for 25% and documents AI tool use with prompts, outputs, reflections, and critical filtering.

### Viva Voce Examination
The viva voce is a 30-minute oral exam worth 25%, involving artefact demonstration and discussion of technical decisions and AI collaboration.

Submission deadline: Wednesday 14th January 2026 at 3pm. The brief is available via Moodle.


## Key texts with library links

[The Audio Programming Book](https://search.ebscohost.com/login.aspx?direct=true&db=nlebk&AN=324701&site=eds-live) [@Boulanger:2010aa]

[The SuperCollider Book](https://search.ebscohost.com/login.aspx?direct=true&db=edswah&AN=000316916500011&site=eds-live) [@Wilson:2011aa]

[The Theory and Technique of Electronic Music](https://msp.ucsd.edu/techniques.htm) [@Puckette:2006aa]

[Microsound](https://search.ebscohost.com/login.aspx?direct=true&db=cat01619a&AN=up.1075347&site=eds-live) [@Curtis:2004aa]

[The Computer Music Tutorial](https://search.ebscohost.com/login.aspx?direct=true&db=cat01619a&AN=up.1515278&site=eds-live) [@Roads:1996aa]

## Tasks for next week

* Install **SuperCollider** and explore the patches made today. If you are new to SuperCollider, try running through a few pages of [Getting Started With SuperCollider by Scott Wilson and James Harkins](https://doc.sccode.org/Tutorials/Getting-Started/00-Getting-Started-With-SC.html). This tutorial ships with SuperCollider; look for 'Getting started' in the help browser on the right of the IDE: <https://supercollider.github.io/>
* Install **Obsidian** for documentation: <https://obsidian.md/>
* Create a **GitHub account:** <https://docs.github.com/en/get-started/start-your-journey/creating-an-account-on-github>
* Check your access to **Copilot Chat**: <https://m365.cloud.microsoft/>

## GitHub setup
Install all the software we have looked at today on your own computer and explore it.

If you haven't yet done so, get a GitHub account and upgrade it to a free Pro account.

1. [Make a personal GitHub account here](https://github.com/signup). Use any email address that you wish.
2. Email <matt.bellingham@port.ac.uk> with your GitHub username. I will then add you as a collaborator to the module repo.
3. Using your personal GitHub account, [join GitHub Education here](https://github.com/education/students). This will give you a free _GitHub Pro_ account while you are a student.

If you have any questions please let me know at <matt.bellingham@port.ac.uk>


## References {.allowframebreaks}