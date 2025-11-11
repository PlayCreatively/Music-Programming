- Your name: Alexander Freyr Þorgeirsson
- Your project title: Parameter Playground: a playful act of exploration within a high-dimensional parameter space
- Planned AI collaboration tools: ChatGPT (GPT-5), GitHub Copilot
# Describe the theme or key idea behind your project
The key idea is to make it quicker and easier to explore the sound space of a synthesizer using only an X–Y pad and linear algebra.
# Project research and AI collaboration strategy
*Discuss examples of current or historic related projects and explain how*
*you plan to strategically collaborate with AI tools during development.*
*How will you maintain creative control while leveraging AI capabilities?*

I don't think there are any related projects
https://projector.tensorflow.org/
## Proposed sources
Note: please use APA referencing as standard. Include sources on both
technical audio programming concepts and AI collaboration approaches where relevant.

https://en.wikipedia.org/wiki/Dimensionality_reduction
https://en.wikipedia.org/wiki/Principal_component_analysis
# Project development plan
Explain how your project will work from a user's perspective and outline
your approach to balancing independent work with AI collaboration.
## What do you anticipate users to hear?
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
- Almost exhaustively explore high dimensional parameter-space using intuitive 2D exploration.
- Explore and capture the sound of changing parameters, through B-Splines.
- Discovering and exploring presets.
- Explore parameters around and between saved presets.
- Play different notes using the keyboard.
## How will you approach AI collaboration during development?
Describe your planned strategy for using AI tools while ensuring you
maintain deep understanding of the technical concepts.
# Technical specifications
## Input sources you will be using
- Synthetic sources
## Output sources you will be using
- Real-time audio output
- Parameter presets in text form
- Audio file output, if time allows
## Real-time control methods
- Python - DearPyGUI
- Open Sound Control (OSC)
- Keyboard
# Assessment preparation
Briefly outline:
- How you will document your AI collaboration process

- What aspects of your project you expect to demonstrate in the viva voce
- Any potential challenges you anticipate in explaining your technical
implementation