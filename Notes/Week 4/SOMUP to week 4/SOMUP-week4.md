---
title: 'Interaction design for sound and music'
subtitle: Sound and Music Programming week 4
author: Dr. Matt Bellingham -- <matt.bellingham@port.ac.uk>
institute: University of Portsmouth
date: Wednesday 22nd October 2025
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

## Session overview

- Interaction design principles
- Assessment briefing and past work
- Using LLMs for SuperCollider
- Proposal planning
- OSC apps for exploration

## Interaction design for sound and music
### Why it matters
- Interfaces shape creative possibilities
- Usability vs expressivity continuum
- Design heuristics for musical tools

----

![Form vs. function, or artists vs. designers](images/artistdesigner.png){height=80%}

------

## Form vs. Function, or Artists vs. Designers
> ... artists are seen as creative, solution oriented, divergent and non-rational thinkers. Their preferred style of work is supposed to reflect the non-orderly manner of these thought processes and a regard for aesthetics over mathematics. Scientists however, are seen as more methods-oriented, quantitatively skilled and rigidly objective. [@Dillon:1995aa]

## Interaction Design
> A central concern of interaction design is to develop interactive products that are usable. Usable generally means easy to learn, effective to use, and provide an enjoyable user experience. [@Rogers:2011aa]

-------

![The usability-expressivity continuum [@Repenning:1997aa].](images/continuum.png){height=80%}

-------

![An audio programming language continuum [@bellinghamChoosersVisualProgramming2022]](images/continuum2.png){height=80%}

------

## Gillian Crampton Smith, in @Moggridge:2006aa
> Good interaction design should maximise the following:
> 
> * Clear mental model (e.g. Apple’s Hypercard)
> * Reassuring feedback (tactile keyboard, clicking)
> * Navigability
> * Consistency
> * Intuitive interaction

-----

![Hypercard](images/hypercard.png){height=80%}

------

![The desktop metaphor; this example shows the original Macintosh OS](images/mac.gif){height=80%}


## Sonic Finder

Bill Gaver’s Sonic Finder used sound to reinforce OS actions. Some sounds were adopted into the MacOS we still use.

Sonic Finder demo: <https://vimeo.com/158610127>

----

![Microsoft's Bob; see [here](https://youtu.be/ZegWedG-jk4) for a demo.](images/bob.jpg){height=80%}

----

![Minesweeper](images/minesweeper.jpg){height=80%}

----

![The early iPhone operating system](images/iphone1.jpg){height=80%}

------

![The shift from a skeuomorphic design to a flatter design language](images/calculator.jpg){height=80%}

----

![Google's *material design* language](images/material.jpg){height=80%}

------

![Apple's watchOS widget design](images/watchos.jpg){height=80%}

----

![AR navigation early design](images/navigation.png){height=80%}

-----

![Google Maps AR navigation](images/arnavigation.png){height=80%}

------

![Nintendo Game and Watch](images/gamewatch.png){height=80%}

-------

![Nintendo DS](images/ds.png){height=80%}

-----

![Nintendo Wii U](images/wii-u.png){height=80%}

------

![Flip phone](images/oldflip.png){height=80%}

-----

![Old laptop design, complete with trackball and monochrome display](images/oldlaptop.png){height=80%}

-------

![Prototype folding phone](images/folding.png){height=80%}

------

![Microsoft's [Courier design](https://en.wikipedia.org/wiki/Microsoft_Courier) has been worked on for years; see the new [patent from 2024](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12108620)](images/microsoft-patent.png){height=80%}

------

![Microsoft's Duo and Neo](images/duo-neo.png){height=80%}


## Types of user work
@Cooper:2007aa suggests that a product should minimise the work that the user needs to do;

* Cognitive work;
* Memory work;
* Visual work;
* Physical work.

## Alan Cooper [-@Cooper:2004aa]

Computer | Human
--|--
Fast | Slow
Error-free | Error-prone
Deterministic | Irrational
Apathetic | Emotional
Literal | Inferential
Sequential | Random
Predictable | Unpredictable
Amoral | Ethical
Stupid | Intelligent

Cooper, A. (2004) *The Inmates are Running the Asylum: Why High-tech Products Drive Us Crazy and How to Restore the Sanity*, 2nd ed, Sams Publishing.

## Four basic activities of interaction design

@Rogers:2011aa outline the four basic activities of interaction design. They can be considered as a cyclical model;

* Establishing requirements
* Designing alternatives
* Prototyping
* Evaluating

-------

![Research community overlap [@Blackwell:2019ab].](images/hci-blackwell.png){height=80%}

------

![Empirical techniques presented at PPIG [@Blackwell:2019ab].](images/ppig.png){height=80%}


## Designing interfaces
The component activities of interaction design, as outlined by Gillian Crampton-Smith [in @Moggridge:2006aa] and Philip Tabor [in @Cooper:2007aa]:

* Understand - what is going on;
* Abstract - what are the main parts;
* Structure - how do the parts connect;
* Represent - how can the structure be represented;
* Detail - what attributes to use.

All of these activities are connected with iterative feedback loops. We can see that they situate the (explicit) design of the interface *after* the initial sketching and wireframing stages.

## Personas and composite archetypes
Personas are composite archetypes; they are not real people, but are based on the observed behaviours and motivations of real people. Importantly, personas are based on observed behaviour from the research phase and help the designer choose the right individuals to design for.

@Cooper:2008aa (see Moodle for the PDF)

@Pruitt:2003aa: <https://www.microsoft.com/en-us/research/wp-content/uploads/2017/03/pruitt-grudinold.pdf>

<http://www.measuringu.com/blog/personas-ux.php>

<https://www.interaction-design.org/literature/book/the-encyclopedia-of-human-computer-interaction-2nd-ed/personas> 

Alan Cooper video: <https://vimeo.com/38811794> 

-------

![Personas created for Dolby by @BoltPeters:2012uc; see <https://boltpeters.com/clients/dolby/>](images/dolby-chart-01.jpeg){height=80%}


## Personas
The use of personas avoids the problems of:

* the elastic user [@Cooper:2007aa], which is a situation where the development team unconsciously change the idealised user’s skills to fit the project;
* self-referential design - designing for yourself - where the designer uses their own goals, skills, motivations and mental models [@Cooper:2007aa];
* concentrating too much on edge cases [@Pruitt:2003aa].



## An alternative approach---'Jobs To Be Done' (JTBD) [@Christensen:2016aa]

<https://hbr.org/2016/09/know-your-customers-jobs-to-be-done>

* 'Job' is shorthand for what an individual really seeks to accomplish in a given circumstance.
* The circumstances are more important than customer characteristics, product attributes, new technologies, or trends.
* Good innovations solve problems that formerly had only inadequate solutions---or no solution.
* Jobs are never simply about function—they have powerful social and emotional dimensions.

<https://youtu.be/Stc0beAxavY>

## Discussion - applying either approach to your area of interest

Personas - who are your target users? What are their behaviours and motivations? How can we know?

... or ... 

What job(s) do your target users need to do? What are the social and emotional dimensions? What characteristics might help them ‘hire’ your solution to the given problem?

## Assessment
### Portfolio components
- **Artefact** (50%) – interactive audio software
- **AI collaboration portfolio** (25%) – 2000–2500 words
- **Viva voce** (25%) – 30-minute technical discussion

## Possible topics of interest
* Instrument interface
* Cooperative work
* Educational interfaces
* Composition/installation
* Sound toys/games
* Other?


## Three interaction design approaches

### Rogers
> ... easy to learn, effective to use, and provide an enjoyable user experience [@Rogers:2011aa]

### Crampton Smith
> Clear mental model, reassuring feedback, navigability, consistency, and intuitive interaction [Crampton Smith in @Moggridge:2006aa]

### Cooper
> Minimise the work that the user needs to do: cognitive work, memory work, visual work, and physical work [@Cooper:2007aa]



## AI collaboration requirements
### What to include in your portfolio

- **Prompt + output**: Show the exact input you gave the LLM and the result.
- **Critical filtering**: Explain what you kept, changed, or discarded—and why.
- **Reflection**: What did the AI help you understand or achieve?
- **Conceptual ownership**: You must remain the author of the idea and design.
- **Verification**: Test and validate all AI-generated code or claims.


## Past student examples

- **Example 1**: OSC-controlled granular synth using TouchOSC + SuperCollider
  - Clear design rationale, responsive interface, well-documented AI use
- **Example 2**: Generative ambient system with MIDI input
  - Strong conceptual framing, iterative prototyping with LLMs
- **Example 3**: Live-coded performance tool for improvisation
  - Emphasis on expressivity and minimal UI

**Discussion prompt**: What makes these projects effective from a design and technical perspective?

## Feeding context to an LLM
### Why context matters
- LLMs perform better when given **specific, structured information**.
- Context helps generate **relevant, accurate, and creative outputs**.

### Sources of context
- **Your research notes** (e.g., Obsidian vault)
- **Lecture materials** (slides, etc.)
- **Assessment handbook** (requirements, marking criteria)

## How to provide context
- Summarise key points in your prompt:
    - Project aim and constraints
    - Technical environment (e.g., SuperCollider, OSC)
    - Design principles (e.g., usability, JTBD)
- Use **structured prompts**
- Include **specific questions**:
    - “How can I minimise cognitive load in this design?”
    - “Suggest OSC mappings for these controls.”


## Tip
- Keep prompts concise but **rich in context**.
- Iteratively refine: add details from research as you go.


## Using LLMs for SuperCollider

- **Prompt engineering**:
  - Be specific: “Write a SynthDef with 3 sine oscillators and amplitude envelopes”
  - Include constraints: “Use OSC input to control frequency”
- **Iterative refinement**:
  - Ask follow-up questions to improve or adapt the code
- **Debugging**:
  - Use LLMs to explain errors or suggest fixes
- **Ethical use**:
  - Always attribute AI contributions
  - Reflect on what you learned or changed



## Tasks for after consolidation week — early drafts, scene-setting, exploring

### 1. Define your area of interest and the problem space
- Write a short outline of your chosen area of interest.
- Explain what problem(s) your project aims to solve and why this matters.

### 2. Undertake initial research into existing solutions
- Find at least **three existing solutions** in the same general problem space.
- Ask: How have others tackled similar issues?
- Collect **citations, URLs, and brief notes** for your report.
- Summarise your findings in Obsidian or another note-taking tool.

## Tasks for after consolidation week — early drafts, scene-setting, exploring

### 3. Establish requirements
- Sketch out the requirements of your solution using **personas** or **Jobs To Be Done (JTBD)** frameworks.
- Consider usability heuristics and interaction design principles.



## References {.allowframebreaks}
