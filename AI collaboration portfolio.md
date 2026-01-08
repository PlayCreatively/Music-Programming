# AI collaboration portfolio
## Foreword

As my use of LLMs are heavily dialogue driven and due to them preferring lengthy replies, I don’t just trim the output; I go as far as to actively cherry-pick select sentences that capture the overall gist or match my immediate focus, based on my reply. So when reading the responds, keep in mind the major asterisk that they're heavily trimmed down.
## 1. Strategic AI Briefing Documentation

### 1.1 AI Incorporation 

For this project, AI took the role of an informant, a teacher, as well as an assistant programmer; therefore there was no one single project brief, but instead, more of a continual dialogue.

The actual implementation of the project began with me providing the LLM a visual mock-up of exactly how I envisioned the interface. I started with a mock-up so that I was not restricting my vision, which tends to happen when working at the implementation level. I provided it to ChatGPT 5.1, including what interactions it allows for. I asked explicitly for python libraries as I knew it would make the linear algebra part of the project, trivial.

<img src="attachments/Desktop%20-%201.jpg" width="600">

**Prompt**

```
Does python have libraries that allow me to make custom GUI?
What I want is to explore high dimensional space through a 2D slice. I will be able to: 
- add a dimension and name it, as well as specify the range domain 
- add vectors to this space which get displayed as a floating knob on the 2D pad 
- multi-select vectors and get context sensitive options on right click 
- keyboard control 
- etc, I made a figma mockup of how it could be
```

The LLM recommends a fitting stack for the task.

**LLM output** *(ChatGPT 5.1)*

```
For that kind of “explore N-D via a 2-D slice” tool, Python can absolutely do it. The combo I recommend:

- **PySide6 (Qt)** for app chrome: docks, lists, context menus, keyboard focus, shortcuts.
- **pyqtgraph** for the fast, interactive 2D pad (pan/zoom, grid, scatter, hit-testing).
- **python-osc** later, if you want to stream values to SC/Faust.

Why this stack? Qt makes the sidebars/tree + right-click menus trivial, and pyqtgraph is GPU-accelerated and happy with hundreds of moving points. It’s a good fit for “friendly toy but snappy”.
```

It also provides me with a running code to kick off with. I ran it and gave feedback.
I ask the LLM to take a more thoughtful look at the mock-up as it overcomplicated it with multiple windows.

**Prompt**

```
Nice, but you overcomplicated it a bit. I only need two windows like my mockup shows. Analise my mockup and see how I do it
```

**LLM output** *(ChatGPT 5.1)*

```
Got it — your mockup is really just two views with tight, minimal state:

1. the 2D pad (big playground)
2. the side inspector (Selected + Vectors)

Here’s the lean interpretation and how to wire it without extra scaffolding.

When you’re ready, I can drop a trimmed Dear PyGui version that matches this two-window spec line-for-line, no extra scaffolding, and the exact selection/slider behavior your mock implies.
```

After further inspecting the application and the underlying code I added some needed clarifications.

**Prompt**

```
Do that. But first let me clarify two things: 
1. the 0 and 1 numbers surrounding the sliders are the min and max, and you can double click on it to change it. 
2. the 2D pad is not necessarily aligned with any dimension. Later on I will add the feature to select 3 points and align the camera to a plane they form; so the 2D pad needs to have a dynamic alignment.
```
### 1.2 Prompt refinement
- **Provide options:** as a global command, I instructed the LLM to provide at least two potential approaches to any implementation and provide arguments as to why one works best for the project.
- **Human formality and curtesy**: speaking to it in a thought out and polite manner not only makes you more thoughtful than you might be if talking to a machine, it itself is also more likely to be helpful — the logic being based on prior research, suggesting that politeness increases the quality of LLMs, as well as the commonly held intuition that since LLMs are a autocomplete prediction machines, deviating from the training data might impact the quality of the answer.
---
## 2. Example Prompts and AI Outputs
### 2.1 Space Filling Curves

Although the project did not end up including this feature, it was a part of my journey of learning about dimension reduction, as it is the entire project's Unique Selling Point (USP).

**Prompt**

```
can you project a finite 3d space onto a 2d space?
```

**LLM output** *(ChatGPT 5.1)*

```
Yes — absolutely. In fact, we do this constantly. Every time you render a 3D scene to your screen in a video game, you're projecting a finite 3D space onto a 2D surface (your monitor).
```

**Prompt**

```
I guess I don't mean project, then, but to fully translate the domain
```

The LLM picks up on what I mean and explains that dimension reduction can't be done faithfully but there are a few ways with different pros and cons.

**LLM output** *(ChatGPT 5.1)*

```
Ah, I see what you’re getting at — you don’t just mean _visual projection_, you mean _can a 3D space be fully, faithfully translated into 2D_ — where nothing is lost, every point in 3D maps uniquely into 2D, and can be recovered without ambiguity.

In that sense: **no**, not in the continuous, geometric sense. You can’t embed a three-dimensional Euclidean space into two dimensions without losing information.

However, if you relax some rules, you _can_ do interesting cheats:

- **Non-continuous encodings:** You can encode 3D coordinates in 2D by packing data. For example, store `z` in color channels or in binary digits. It’s not geometrically faithful, but it’s _informationally_ faithful.
    
- **Fractals or space-filling curves:** These can map 3D space to 2D in a way that’s technically bijective, but they break locality — points close in 3D may be far apart in 2D.
    
- **Topological projections with distortion:** Like world maps — Earth’s surface (a 3D sphere) can be mapped onto 2D with distortion in area or shape.
```

Being familiar with two of the suggestions but not with space-filling curves, it peaked my interest.

**Prompt**

```
okay tell me about Fractals or space-filling curves
```

**LLM output** *(ChatGPT 5.1)*

```
**Fractals** and **space-filling curves** are examples of mappings that _defy our geometric intuitions_. They let you take a line (1D) or plane (2D) and “fill” a higher-dimensional space (like a cube) in a way that is technically bijective — every point in one corresponds to a unique point in the other.

### Space-filling curves: the dimensional cheats

A **space-filling curve** is a continuous curve that passes through every point in a region of space.  
The most famous examples are:

- **Peano curve** (1890)
    
- **Hilbert curve** (1891)
    
- **Z-order (Morton) curve** — used in computer graphics and data indexing
```

Having seen the video by 3Blue1Brown on [Hilbert Curves](https://youtu.be/3s7h2MHQtxc) I had fortunately formed an intuition behind the concept. However, an obvious downfall to it was that now and then, at certain intersections, the locality majorly breaks down, as demonstrated in this image. 

<img src="attachments/hilbert%20curve%20colored.png" width="300">

and this is only in 2 dimensions, I can only imagine that it becomes way worse the higher the dimensions are. But the only thing I knew about Hilbert Curves was that they can map 2D data down to 1D while preserving some locality. But since it recommended Hilbert Curves I could only assume it was relevant to higher dimensions.

**Prompt**

```
can any n dimension be mapped onto 2d?
```

**LLM output** *(ChatGPT 5.1)*

```
Yes — beautifully so. The Hilbert curve generalizes cleanly to any number of dimensions.

The 2D Hilbert curve that fills a square is just the simplest member of a whole **family** of Hilbert curves that can fill cubes, hypercubes, and beyond. You can have a **3D Hilbert curve** that fills a cube, or a **4D Hilbert curve** that winds through a tesseract, and mathematically there’s no limit — you can define one for any finite dimension _n_.
```

**Prompt**

```
oh so a hilbert curve always maps down to 1d?
```

**LLM output** *(ChatGPT 5.1)*

```
Exactly — that’s the heart of it.

A **Hilbert curve** is fundamentally a _1D parameterization_ of a higher-dimensional space.

So yes — no matter how high you go in dimension, the Hilbert curve itself is always **1D**. It’s a _curve_, not a surface or volume. What changes is the **space it fills**.
```

Knowing I can at least reduce the dimensions down to 1D was very promising, but I had clearly stated that I wanted to go from nD to 2D, so I ask how to do that using Hilbert Curves.

**Prompt**

```
Alright so if I map n-dimension to a hilbert curve, how can I map that to a 2d plane which preserves Hilbert's locality?
```

**LLM output** *(ChatGPT 5.1)*

```
You can do this by letting the **Hilbert curve act as a middleman** between the dimensions.

nD space  →  1D Hilbert index  →  2D space

Because both legs use Hilbert ordering, you preserve Hilbert’s strong locality properties as much as a dimension-reducing map can.
```

As the LLM suggests, I can have a 1D Hilbert Curve exhaustively slither through any finite n-dimensional space, store the mapping from 1D to nD, then have it slither through 2D screen space and store that 1D to 2D mapping and with this I can do 2D → 1D → nD, which allows me to map an XY-pad to a somewhat locally coherent n-dimensional space. And to quickly finish the thought, the resolution of the nD space would be limited by the resolution of the 2D space, which would be at the pixel level of the screen (assuming you can't zoom into the XY-pad).

### 2.2 Matrix Transposition

I was struggling with understanding the code snippets since it was using NumPy's `ndarray` which doesn't have any inherent shape. Before I finally understood how to think about an array of vectors in terms of rows and columns, I asked why the syntax seemed reversed, since thinking about it in object oriented terms you'd first index the object (vector) and then the individual fields in the object (xyz); so understandably it seemed reversed to me.

**Prompt**

```
why does it feel like the shape syntax is reversed? Why (N, 2) and not (2, N)
```

**LLM output** *(ChatGPT 5.1)*

```
This is a _deeply_ common confusion — and the reason it feels “reversed” is because **you’re intuitively thinking in vector-major order**, but **NumPy is row-major**, inherited from C.

in NumPy:

### **rows = items**

### **columns = features**

So:
- **N rows** → N things (presets, points, samples)
- **2 columns** → each thing has 2 numbers (x and y)
```

The explanation reminded me of AoS and SoA, so I jumped to the conclusion that NumPy was simply reversed (SoA) to make the memory layout more friendly for SIMD operations. I ask if I was right.

**Prompt**

```
ooooooh ok. so what I'm starting to understand is that this is a structure of arrays vs arrays of structure problem. Is that right?
```

**LLM output** *(ChatGPT 5.1)*

```
You just hit the nail _dead center_.

It **is** a _Structure of Arrays (SoA) vs. Array of Structures (AoS)_ distinction.

And NumPy — like most numerical computing systems — is firmly SoA.

SoA is preferred because it:
- lines up with row-major memory
- vectorizes trivially
- works with BLAS/LAPACK
- broadcasts beautifully
- makes operations like `T @ B` natural
- is cache-friendly for numeric workloads
- matches ML frameworks like PyTorch, JAX, TensorFlow
  
**2D arrays**
- `(N, D)` – `X`  
    → all presets, each D-dimensional
- `(D, 2)` – `B`  
    → two basis vectors (u,v) in D-space
```

It went on to congratulate me for the great detective work, but in the same response, but not as obviously as portrayed above — remember these are only tiny curated snippets of the overall output — it was contradicting itself with `(N, D)` – `X`  and `(D, 2)` – `B`. I raise my confusion. I decided to be very explicit and thorough to get my point across to not feed it any of *my* own cocky 'hallucinations'.

But since I noticed the pattern more easily, seeing them side by side, I guessed it was for matrix operation reasons.

**Prompt**

```
alright, I guess I'm confused because you seem to be mixing SoA and AoS.
(N, D) is AoS - because each row is a vector 
(D, 2) is SoA - because each row is a dimension or better said, an index into a vector

I can only assume that you're forming them this way is because (D, 2) is for the basis which we want to be in a matrix format in order to do matrix operations on vectors easily. Am I right?
```

**LLM output** *(ChatGPT 5.1)*

```
Yeah, you’ve spotted a real thing here: we _are_ mixing perspectives a bit, and the SoA/AoS terminology is part of why it feels weird.

This is the subtle bit:  
SoA vs AoS **depends on what you call the “struct”.**

- `B` is **AoS over dimensions**, **SoA over axes**.
- `X` is **AoS over presets**, **SoA over dimensions** (if you think column-wise).

SoA vs AoS is _not absolute_; it’s relative to what you consider “the entity”.

But why specifically `(D, 2)` and not `(2, D)`? 
You are completely right.  
We pick `(D, 2)` so that the **projection equation** is natural

Otherwise, you’d have to constantly transpose:
`# if B is (2, D) 
Y = T @ B.T  # (N, D) @ (D, 2) -> (N, 2)`
```

**Prompt**

```
I think Y = T @ B.T might be fine, feels more consistent. When I assign new vectors for U and V won't I have to transpose the vectors to assign them to the transposed UV shape anyways?
```

The LLM agrees and I keep the `Basis` data layout consistent with the rest of the vectors.

---
## 3. Critical Filtering and Decision Making

Due to my dialogical approach of AI collaboration there wasn't much critical filtering as there were occasional pushbacks and very frequent querying.

### 3.1 From Retained Mode To Immediate Mode

The Qt start off template the LLM generated for me was using the python Qt framework it suggested but after reviewing the code in order to build on top of, it became clear to me that it was taking an immediate mode approach with the Qt framework and I asked why it did that. 

**Prompt**

```
explain to me why you're destroying and rebuilding the gui. Qt isn't immediate mode is it?
```

The LLM goes on to explain that it indeed was doing a hacky approach of emulating immediate mode with Qt. It suggests that I refactor the code to an appropriate retained mode.

**LLM output** *(ChatGPT 5.1)*

```
Exactly — Qt is **not** an immediate-mode GUI. It’s a retained-mode framework:  
each widget (button, slider, list item…) is an object that persists, and Qt automatically repaints only what needs it.

So yes — what I gave you (destroying and rebuilding sliders each refresh) is conceptually a _hacky_ “immediate-mode emulation*. It’s easy to reason about, but it isn’t the Qt way.

So, in Qt:
- You **don’t need** to rebuild the GUI each frame.
- You **should** update existing widgets instead.
  
In your current project, since you’re already using Qt, the next refactor should:
- keep `Inspector` persistent;
- connect each slider’s `valueChanged` once;
- update widget values directly when `NDStore` changes, not rebuild the layout.

That gives you better performance, no recursion, and keeps the architecture idiomatic to Qt.
```

Learning from trial and error, earlier in the project, I knew how error prone and complex it is to keep data up to date in retained mode, and my UI was gonna need at least two different interfaces to change the parameters, one being a long list of sliders to change individual parameters and the other the XY-pad; both had to update the other and if I ever were to change the data in the code I'd have to make sure they update as well. Therefore I suggested we go for an immediate mode library.

**Prompt**

```
ok. that makes a lot of sense and now I understand your approach. In that case I think it might be best to go for an immediate mode library.
```

### 3.2 Gram-Schmidt 

For the basis vector construction function, it wrote in the comments that it was using Gram-Schmidt, my assumption was that you'd normally use the cross-product on two axis to derive the 3rd which is orthogonal. So I inquired on it.

**Prompt**

```
why are you using Gram-Schmidt? Can't you just construct 2 basic vectors from the 3 and then create the 3rd with cross product?
```

As the LLM explains, the cross-product is predominantly a 3D exclusive operation. Therefore requiring us to use a dimension agnostic formula to derive the plane.

**LLM output** *(ChatGPT 5.1)*

```
Right, in 3D you’d totally just use a cross product — that’s the natural way to get a perpendicular vector.  
But the key is: you’re not guaranteed to live in 3D anymore.

It works _only_ in **three dimensions** (and in a special, exotic sense, also in 7D via octonions).

So in higher dimensions, the concept of “orthogonal complement” replaces the cross product, and Gram–Schmidt is the general way to compute that.
```

When it came to utilizing the function, I was having no luck. I asked if the code was truly correct.

**Prompt**

```
is this correct? 

def assign_basis_from_three_points(p1, p2, p3): 
	global Basis 
	# All are (D,) in unit space. 
	u = p2 - p1 
	u /= np.linalg.norm(u) + 1e-12 
	w = p3 - p1 
	# Gram–Schmidt: v = w - (u·w)u 
	v = w - np.dot(u, w) * u 
	v /= np.linalg.norm(v) + 1e-12 
	# Pack as columns 
	Basis = np.stack([u, v]) # (2,D)
```

The LLM responds with plausible issues, as well as suggesting a more robust formula, called QR. It was only a single line `np.linalg.qr()` which reduced the amount of code which meant less bugs.

**LLM output** *(ChatGPT 5.1)*

```
### Alternative: use QR instead of manual Gram–Schmidt

Another plausible way:

`def basis_qr_from_three_points(p1, p2, p3):     
	A = np.stack([p2 - p1, p3 - p1], axis=1)  # shape (D, 2)     
	# QR decomposition: A = Q R, with Q having orthonormal columns     
	Q, _ = np.linalg.qr(A)     
	# Take the first two columns as basis     
	return Q[:, :2]  # shape (D, 2)`
	
Comparison:
- **Your Gram–Schmidt version**
    - Pros: Conceptually direct, easy to read, minimal machinery.
    - Cons: Need to hand-roll degeneracy checks; slightly less numerically robust.
- **QR-based version**
    - Pros: Uses a stable, well-tested routine; easier to extend if you want more than 2 basis vectors later.
    - Cons: Less transparent if you’re thinking geometrically; a bit more “black box”.
```

---
## 4. Collaboration Strategy Reflection

> [!IMPORTANT]
> As agreed with my supervisor, Matt Bellingham, the following section will look the same for both Audio Programming and Sound and Music Programming as both projects were worked on in tandem and differentiating between my LLM collaboration approaches would be difficult and frankly disingenuous, as they were one in the same. 

The collaboration was at its best when I was able to abstract individual generic problems from the project and tackle it in isolation using an LLM as a thinking partner. Once that problem is solved, implementing it manually as a generic function guarantees that you retain ownership and full comprehension of the whole codebase.

What can sadly happen is that time constraints and anxieties will steer you towards taking shortcuts and working in a somewhat reverse order: getting the LLM to work on the whole solution until you get to the desired goal and then retroactively study and refactor the code base. This may take more time in the long run, but in the short term it can sooth your anxieties about going down a null route. 

I tried to get the LLM to work in a way that facilitated the former approach, however, their underlying incentive is predisposed to do the work for you and spit out working code. It is not yet capable of reprograming itself to slow down and have a human-like dialogue where its making sure you're following along as opposed to throwing a whole assay at you, hoping it's covering all potential future questions you might have.

Creatively, it affords you to stay more in the high level thinking than the implementation level, freeing you from the limitations of your own knowledge and capability as well as the tunnel vision that the implementation level traps you in.

For a long time, professions relating to programming have had the unavoidable affordance of shortcuts, be it writing solutions based on intuition alone or brute-forced debugging which leads to solutions you can't explain. Later on, since the introduction of the internet (and websites such as [stackoverflow.com](https://stackoverflow.com/)), outsourcing your solutions to fellow programmers have become easier, and now, at the dawn of LLMs, as they creep into our tools, it has become close to impossible to not make use of the speed boost.
However, this is only relevant to jobs for which not enough time has been allocated, and as long as jobs have fast approaching deadlines, shortcuts will be taken.

---
## Annotation Integration
### 5.1 Original aims

- **Creative goal:** Use linear algebra to turn an XY-pad into a slice of the full parameter space of a complex synth.
- **JTBD:** An approachable way of comprehensively exploring a powerful synth's sound space that abstracts away all the complexity.
- **Heuristics:** (H1) Usefulness; (H2) Intuitive understanding and clarity.

### 5.2 Influences

- **Software:** The Super Collider’s trick of reading the mouse’s X and Y coordinates to explore ranges of values inspired me to look for ways to explore a larger space while staying within the same interaction paradigm.
- **Concepts:** My initial research into LLM's semantic vector spaces and how they encoded meaning as a point in high dimensional space, allowing for elementary vector arithmetic to uncover hidden vector encodings, like so:

  $$\Large \textcolor{Apricot}{Queen} - \textcolor{thistle}{King} + \textcolor{thistle}{Man} ≈ \textcolor{Apricot}{Woman}$$
  
  From there I realized I could essentially encode a synthesizer's entire preset as a point in high dimensional parameter space.

### 5.3 Implementation process

- **Language choice:** Although python usually isn't my language of choice I knew it had a very strong basis in mathematics and would trivialize any math I'd throw at it. 
- **Stack choice:** Going with glfw and pyimgui came to be after realizing how important it was to use immediate mode for the UI in order to sidestep the complications of synchronizing states. I went from: 
  PySide6 (Qt) → DearPyGUI *(dear IMGUI inspired)* → PyIMGUI *(dear IMGUI port)*
### 5.4 Evaluation against aims and heuristics

- **H1 Usefulness:**
	
	**Pros:**
	- Make a slice/window through high dimensional parameter space that linearly intersects 3 selected points.
	- Effortlessly click and drag around to create a temporary preset that plays live, can tweak the individual parameters of and be saved and labelled with a single click.
	
	**Cons:** 
	- [Missing splines and presets-on-rails](attachments/Desktop%20-%203.jpg) (moving presets).
	- Missing Principal Component Analysis (PCA) and 'trait parameters' *([latent variable](https://en.wikipedia.org/wiki/Latent_and_observable_variables#Inferring_latent_variables)).*
	- Uniform Manifold Approximation (UMAP) or other general non-linear dimension reduction for a more complicated 'trait parameters' *([latent variable](https://en.wikipedia.org/wiki/Latent_and_observable_variables#Inferring_latent_variables))*.
	- Limited to my 'in-house' synth.

- **H2 Intuitive understanding and clarity:** 
	Ideally the interface reflects and hints at the whole slice through high dimensional space concept and makes it digestible and even allows for forming a kind of embodied intuition for traversing the space.
	
	**Pros:**
	- Visual bounds of the slice where it intersects the unit-hyper-square.
	- Lots of dot metaphors to drive home the point in high-D space.
	- When hovering individual parameters it shows the line it moves along.
	- Presets that don't land on the plane are scaled based on the Euclidian distance from the plane.
	
	**Cons:**
	- Missing transitional animation when changing slice/window as well as [grid preview](attachments/Desktop%20-%202.jpg).
	- Presets outside of the slice and in the back or forefront of it could feature more visuals to drive home the distance metaphor. 
	- Bounds of slice is visible but not of the unit-hyper-square itself.

### 5.5 Reference list

- Grant Sanderson. (24, December 24). _This open problem taught me what topology is_ [Video]. YouTube. [https://youtu.be/IQqtsm-bBRU?t=649](https://youtu.be/IQqtsm-bBRU?t=649)
- Immediate mode (computer graphics). (2025). In _Wikipedia_. [https://en.wikipedia.org/w/index.php?title=Immediate_mode_(computer_graphics)&oldid=1298908603](https://en.wikipedia.org/w/index.php?title=Immediate_mode_\(computer_graphics\)&oldid=1298908603)
- Latent and observable variables. (2025). In _Wikipedia_. [https://en.wikipedia.org/w/index.php?title=Latent_and_observable_variables&oldid=1291183159#Inferring_latent_variables](https://en.wikipedia.org/w/index.php?title=Latent_and_observable_variables&oldid=1291183159#Inferring_latent_variables)
- Latent space. (2025). In _Wikipedia_. [https://en.wikipedia.org/w/index.php?title=Latent_space&oldid=1322694913](https://en.wikipedia.org/w/index.php?title=Latent_space&oldid=1322694913)
- Vector synthesis. (2025). In _Wikipedia_. [https://en.wikipedia.org/w/index.php?title=Vector_synthesis&oldid=1302907156](https://en.wikipedia.org/w/index.php?title=Vector_synthesis&oldid=1302907156)
