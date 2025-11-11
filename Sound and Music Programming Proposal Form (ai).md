* **Your name:** Alexander Freyr Þorgeirsson
* **Your project title:** Parameter Playground: a playful act of exploration within a high-dimensional parameter space
* **Planned AI collaboration tools:** ChatGPT (GPT-5), GitHub Copilot

## Describe the theme or key idea behind your project

The project explores sound generation as a *playful act of exploration* within a high-dimensional parameter space. Instead of presenting synthesis as a technical interface full of knobs and sliders, it treats sound as something to *navigate visually* — a landscape shaped by mathematical relationships.

Users will interact with a 2D “slice” of a higher-dimensional synth parameter space. Each axis can represent different synthesizer parameters or module relationships. Moving across the plane morphs the sound in complex, continuous ways.  ~~The aim is to build intuition for how synthesis parameters interact and to make sound design feel more like *drawing* or *playing* than programming.~~

The project draws from NIME and DMI traditions of speculative and experiential interface design. It aims to sit firmly in the “third wave” of HCI — valuing aesthetics, exploration, and affect over efficiency.

---

## Project research and AI collaboration strategy

Historically, visual and modular synth systems such as the **ReacTable**, **VCV Rack**, and **T-VOKS** have reimagined electronic music interfaces by mapping complex synthesis into accessible, embodied experiences. The proposed project extends these ideas by adding *mathematical exploration* and *AI-assisted mapping* — using AI to help generate and tune parameter relationships between modules.

The project will be developed using **SuperCollider** for synthesis, with **Processing or Python (Raylib / Faust experiments)** for the visual layer. OSC (Open Sound Control) will connect the systems in real time.

AI tools will be used as:

* **Collaborators for ideation:** generating code prototypes and suggesting DSP structures.
* **Debugging assistants:** helping refine OSC communication and synthesis logic.
* **Reflective partners:** offering explanations of DSP and interaction design concepts for documentation.

Creative control will remain fully human-led. AI will not decide mappings or sonic goals but will support faster prototyping and conceptual breadth — consistent with the “strategic AI partnership” model encouraged in the module.

---

### Proposed sources (APA style)

* Boulanger, R., & Lazzarini, V. (2010). *The Audio Programming Book.* MIT Press.
* Wilson, S., Cottle, D., & Collins, N. (2011). *The SuperCollider Book.* MIT Press.
* Puckette, M. (2006). *The Theory and Technique of Electronic Music.* World Scientific.
* Jensenius, A. R. (2017). *A NIME taxonomy.* In *Proceedings of the New Interfaces for Musical Expression Conference.*
* Rogers, Y., Sharp, H., & Preece, J. (2011). *Interaction Design: Beyond Human-Computer Interaction.* Wiley.
* Wright, M., & Freed, A. (2005). *Open Sound Control: A new protocol for communicating with sound synthesizers.* *Computer Music Journal, 29*(4).
* Orchard, D. (2025). *Baby Steps in Semi-Automatic Coding.* *LM Orchard Blog.*
* Spiess, F. (2025). *How to Use Claude for Coding.* *Claude.ai Blog.*

---

## Project development plan

The user experience revolves around *direct manipulation of sound through motion and shape*. Users will interact with a canvas that visually represents a 2D plane of interconnected synthesis parameters. The system will interpolate between parameter presets in real time and allow playful exploration through touch, mouse, or external control (OSC or MIDI).

### What do you anticipate users to hear?

A continuously morphing electronic soundscape that changes fluidly as the user moves through the plane — between percussive, tonal, and textural timbres. The goal is not precision but curiosity: each small motion yields perceptible yet smooth change, teaching the ear how parameters interact.

### How will users interact with your software?

Through a **graphical interface** displaying a coordinate plane. Users can:


### What unique features does your software offer them?

* navigating a parameter space instead of tweaking controls.

---

### How will you approach AI collaboration during development?

I will use **ChatGPT** and **Copilot** to support:

* Generating and refining Python code.

---

## Technical specifications

### Input sources

* Synthetic sources (oscillators, noise, FM, wavetable)
* Real-time control input via OSC or MIDI
* Optional text input for generative curves (function-based modulation)

### Output sources

* Real-time audio output

### Real-time control methods

* OSC (primary)
* MIDI (secondary for simple control mapping)
* Mouse/keyboard interaction within the GUI

---

## Assessment preparation

* **AI documentation:** All AI prompts, outputs, and reflections will be logged in Markdown (for portfolio inclusion).
* **Viva demonstration:** The final demo will show live sound exploration and OSC interaction, explaining synthesis mapping and AI’s role in development.
* **Challenges:** Explaining high-dimensional interpolation and OSC synchronization clearly in the viva may be complex; diagrams and annotated code will be prepared to assist.

---

Would you like me to adapt this draft for **SuperCollider as the main environment** (with Processing or TouchOSC for visuals), or would you prefer to lean into your newer **Python + Raylib + Faust** direction for this version of the proposal? The structure of the text can stay the same, but the technical section and AI collaboration focus would shift accordingly.
