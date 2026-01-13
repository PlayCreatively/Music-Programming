# Parameter Playground: 
*a playful act of exploration within a high-dimensional parameter space*

## Overview
- ### [Project Proposal](Alexander%20Þorgeirsson%202544706%20SOMUP%20proposal.md)

This project is an interactive application that allows users to explore a high-dimensional parameter space of a DX7 synthesizer through a 2D slice interface. Users can navigate, select, and manipulate DX7 presets represented as nodes within this space, and hear the corresponding audio output generated via OSC messages to a SuperCollider DX7 synthesis engine.

The goal of this project is to provide an intuitive, frictionless and entry level way for users to explore the complex parameter space of FM synthesis, fostering better flow and creativity in sound design.

## Setup
### Prerequisites
> [!IMPORTANT]
> This project was built and tested on Windows 11. While it should work on other operating systems, some adjustments may be necessary.

1.  **Python Installed**: Ensure you have [Python 3.10 or later](https://www.python.org/downloads/) installed on your system.
2.  **Python Environment**: Ensure you have the following packages installed:
```bash
pip install "imgui[glfw]" "PyOpenGL" "numpy" "python-osc"
```
3.  **SuperCollider**: This project uses SuperCollider for sound synthesis. Follow the setup instructions on the [Audio-Programming](https://github.com/PlayCreatively/Audio-Programming#setup) repo.
### How to run
1. Navigate to the project directory in your terminal.
2. Run:
```bash
cd Project
python main.py
```

*or*

if you're running on a windows computer, you can simply double-click `run.bat` to start the program.

## How to use

### Interface Controls
-   **Pan**: Right-click or Middle-click + Drag to move around the parameter space.
-   **Zoom**: Use the Mouse Wheel to zoom in and out.
-   **Select Preset**: Left-click on a node (circle) to select it.
-   **Preview Sound**: Left-click and hold either on a preset to play it or anywhere one the 2D slice to play a preset at that point.
-   **Move Preset**: Left-click + Drag a node to move it within the 2D slice.
-   **Multi-Select**: Hold `Ctrl` while clicking to select multiple presets.
-   **Create Slice**: Multi-select 3 presets and press the `define plane from these 3 presets` button to create a new slice view.

### Audio & Synthesis
The application sends OSC messages to `127.0.0.1:57120` with the address `/update_synth`. The parameters control a DX7-style FM synthesis engine found [here](https://github.com/PlayCreatively/Audio-Programming).

## Documentation
- ### [AI Collaboration Portfolio](Alexander%20Þorgeirsson%202544706%20SOMUP%20AI%20collaboration%20portfolio.md)
