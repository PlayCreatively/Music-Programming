- Name: Alexander Freyr Þorgeirsson
- Project title: Parameter Playground: a playful act of exploration within a high-dimensional parameter space
- Planned AI collaboration tools: ChatGPT (GPT-5), GitHub Copilot
# Describe the theme or key idea behind your project
---
The key idea is to make it quicker and easier to explore the sound space of a synthesizer using only an X–Y pad and linear algebra.
# Project research and AI collaboration strategy

## **Traditional XY-Pad**

| Traditional XY-Pads simply map the X and Y plane to two parameters. Those parameters are either customizable by the user or hardwired by the designer company. | ![[Pasted image 20251112191436.png\|300]] |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------- |

## **Vector synthesis**

| Vector Synthesis is more or less the same as a XY-Pad but it's interpolating between, in this case, C → D and A → B. | [Wikipedia](https://en.wikipedia.org/wiki/Vector_synthesis)<br>![[Pasted image 20251112191128.png]] |
| -------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------: |

## **Distance/Venn-Diagram Synthesis**

|     | Multimapper32MIDI<br>![[download.png]]<br>XY Send Nodes Circlepan<br>![[Pasted image 20251112193704.png]]![[Pasted image 20251112190456.jpg]] |
| --- | :-------------------------------------------------------------------------------------------------------------------------------------------: |


https://projector.tensorflow.org/
## Proposed sources

https://en.wikipedia.org/wiki/Dimensionality_reduction
https://en.wikipedia.org/wiki/Principal_component_analysis
## What do you anticipate users to hear?
---
I anticipate users to hear some nice presets for DX7 Yamaha and then any and every sound in between them. Although, I anticipate the majority of the sound-space to be nonsense 
## How will users interact with your software?

Below are mockup snapshots made with Figma showcasing various states of the app.
What's missing is the transparency of the presets depending on their Euclidian distance from the 2D plane that the user sees.

| The preset *Piano* is selected which gives you a view of its parameter values, arbitrarily named *freq1..freq3*. You can see their values range from 0 to 1, which is customizable.                                                                                                      | ![[Desktop - 1.jpg]] |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| - Selected *Piano*, *Terminator* and *Home*.<br><br>- The 2D plane button is being hovered, letting you preview the plane that you're about to focus on.                                                                                                                                 | ![[Desktop - 2.jpg]] |
| - Selected *808*, *Speak Out*, *Jam*.<br><br>- The Spline button is being hovered, showcasing the B-Spline that flows through each preset.                                                                                                                                               | ![[Desktop - 4.jpg]] |
| - Selected the B-Spline.<br><br>- Spline named *Tractor*.<br><br>- Min/Max sliders<br><br>- Position of colored presets on spline<br><br>- Current position on spline<br><br>- No key set for triggering spline interpolation.<br><br>⚠️ Missing ADSR settings for spline interpolation. | ![[Desktop - 3.jpg]] |

## What unique features does your software offer them?
---
- Almost exhaustively explore high dimensional parameter-space using intuitive 2D exploration.
- Explore and capture the sound of changing parameters, through B-Splines.
- Discovering and exploring presets.
- Explore parameters around and between saved presets.
- Play different notes using the keyboard.
## How will you approach AI collaboration during development?
---
I will use AI as a research partner, as an API assistant and coding partner.
# Technical specifications
## Input sources you will be using
---
- Synthetic sources
## Output sources you will be using
---
- Real-time audio output
- Parameter presets in text form
- Audio file output, if time allows
## Real-time control methods
---
- Python - DearPyGUI
- Open Sound Control (OSC)
- Keyboard (as opposed to MIDI)
# Assessment preparation
---
I will document my AI collaboration in markdown format, documenting learning outcomes and notable changes in direction.
I will directly demonstrate my digital artifact in person, showcasing all of its features and potential.
As with any code, there are different layers of abstraction and depending on which layer I need to explain some are bound to be understood in a general sense but not to the point of being able to teach someone else to write it from scratch.