# *Sound and Music Programming* assessment handbook 2025-26

# Module information

- Module title: Sound and Music Programming
- Module Code: M23952
- Level: 6
- Module leader: Dr. Matt Bellingham
- Email: <matt.bellingham@port.ac.uk>
- Telephone: 023 9284 5494

## General assessment information and key dates

There is one assessment for this module, which is a portfolio containing a main artefact, an AI collaboration portfolio, and a viva voce[^1]. The deadline for the portfolio is 3pm on Wednesday 14th January 2026.

## Module abstract and learning outcomes

### Abstract

This unit develops the principles and skills that underpin the application of sound and software programming for the creation of interactive audio applications and interfaces. Students will work in strategic partnership with AI tools to support ideation, development, and debugging, while maintaining deep conceptual and technical understanding. The unit places particular emphasis on creative application development using object-oriented design and coding techniques, and encourages the integration of multiple software environments to achieve complex interactivity and functionality.

### Learning outcomes

On successful completion of this unit, students should be able to:

- LO1: Draw upon current research to conceive and design an original audio software artefact.
- LO2: Justify and evaluate decisions in the implementation of an original audio software artefact.
- LO3: Apply advanced knowledge and techniques of computational sound to the creation of audio software.
- LO4: Critically evaluate the success of their work against the stated aims and current research.

# Assessment

## Portfolio

Your submission should consist of three separate components: a technical artefact, an AI collaboration portfolio, and a viva voce. All parts are explained below.

### Artefact (50%)

The main submission for Sound and Music Programming is either a standalone piece of audio software or a bespoke system which combines both hardware and software. You will need to submit a proposal which needs to be agreed before starting substantive work on your artefact; see below for more details.

**AI Attribution Requirements:** You must clearly document which portions of code were generated with AI assistance versus written entirely by you. Use clear comments to indicate AI contributions and your modifications. If you would like to draw the assessor's attention to particularly sophisticated examples of AI collaboration or human oversight, document this via comments in your code.

The submission should contain a basic README file summarising its aims and your vision for how it should be used in creative practice. The README file should directly indicate to the assessor how the software should be used. It is not required that you provide input audio files for the software, but you may choose to do so if you feel a certain sound or set of sounds highlight aspects of your submission. If sounds are provided they should use an open licence or have been created by yourself. You should not use any materials that are covered by copyright. A video demonstration of the artefact must be provided highlighting the core features and setup of the application. Guidance on how to do this can be found below.

Your submission to the submission portal linked via Moodle must include all code. If you would like to draw the assessor's attention to portions of the source code, you should document this via code comments. The submission should be version controlled using Git and a link to a GitHub repository should be provided. The submitted version should be tagged as `UPXXX_SOMUP_Submission` in the Git repository. It is advisable that you download and submit the zip folder that is created on GitHub when a tagged code commit is uploaded.

## AI collaboration portfolio (25%)

Your AI collaboration portfolio must be submitted as a single **Markdown document** (.md file) that demonstrates your strategic partnership with AI tools throughout the development process. The document should be approximately **2000---2500 words** and structured as follows:

### Required Structure

1. **Strategic AI Briefing Documentation (500---600 words)**
 Document how you provided context to AI tools, including your initial project brief, technical constraints, and creative goals. Include:
	 1. Your initial project brief given to AI tools
	 2. Examples of how you provided SuperCollider/DSP context
	 3. Evidence of how you refined your prompting approach

2. **Example Prompts and AI Outputs (800---1000 words)**
 Provide 4---5 detailed examples of AI interactions that were significant to your project development. For each example include:
 	1. The exact prompt you used (in code blocks)
 	2. The AI's response/output (in code blocks)
 	3. Your reflective commentary on the quality and usefulness of the response
 	4. How you modified or used the AI's suggestion

3. **Critical Filtering and Decision Making (400---500 words)**
 Document specific instances where you rejected or significantly modified AI suggestions. Include:
	1.  At least 2 examples of AI outputs you rejected with your reasoning
	2. Examples of code you modified or improved from AI suggestions
	3. Your criteria for evaluating AI suggestions in audio programming contexts

4. **Collaboration Strategy Reflection (300---400 words)**
 Reflect critically on your overall AI collaboration approach:
	1. How your AI collaboration strategy evolved during the project
	2. What you learned about effective human---AI partnership in audio programming
	3. How AI collaboration affected your learning and creative process
	4. Professional implications for audio programming practice

### Annotation Integration

Your AI collaboration portfolio must also include a reflective annotation that addresses the following:

1. **Original Aims**: What were your original aims for your artefact? Who is it for and/or what is it designed to do? You may refer to a persona or a "Jobs To Be Done" (JTBD) framework. Heuristics can be useful in specifying the desired behaviour of your artefact.
2. **Influences**: What existing tools influenced your thinking and implementation (e.g. NIME tools, commercial software)? What did you learn from them, and how have they shaped your work?
3. **Implementation Process**: How did you approach the implementation phase? What decisions did you make? Were any viability tests required to select hardware/software? What problems did you encounter, and how did you overcome or work around them?
4. **Evaluation**: Evaluate your finished artefact against your original aims and/or heuristics. Which elements are you most proud of? What would you change if you had more time, and how?
5. **References**: Compile an APA-formatted reference list that includes well-chosen technical sources and details of the tools that influenced your work.

All code examples should be properly formatted using Markdown code blocks with appropriate syntax highlighting.

### Viva Voce (25%)

You will participate in a **viva voce** with the module leader lasting **30 minutes**, conducted either in-person or via Teams. It must be scheduled during the final week before the deadline (**week commencing Monday 5th January 2026**). All vivas must be arranged before Christmas.

During the viva, you will be assessed on both your technical understanding and the functionality of your artefact. You should be prepared to:

- Demonstrate your software live and highlight its core features
- Explain key technical concepts used in your implementation, especially DSP principles and relevant architecture
- Justify design decisions made during development, including technical and creative choices
- Modify code in real-time to show your understanding extends beyond what you've submitted
- Discuss your AI collaboration process with specific examples from your development experience
- Handle technical questions about audio programming concepts relevant to your project

This is not a test of memory; you may consult your code and notes during the viva. The session will be recorded and must be submitted with your portfolio.

## Proposal

A proposal form detailing your intentions must be completed on GitHub. This requires you to create a repo for your project ([guidance here][repo]), add `mattbport` as a collaborator ([guidance here][collaborator]), and make a new [Markdown][markdown] file (with a `.md` extension) named with your name, student number, and 'SOMUP proposal'. The Markdown file should be populated with the template provided at the end of this handbook which you can then complete. Your proposal must be approved by the module leader before you begin working on the main artefact. The proposal is not graded.

[repo]: https://docs.github.com/en/repositories/creating-and-managing-repositories/quickstart-for-repositories
[collaborator]: https://docs.github.com/en/account-and-profile/how-tos/setting-up-and-managing-your-personal-account-on-github/managing-access-to-your-personal-repositories/inviting-collaborators-to-a-personal-repository
[markdown]: https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax

## Criteria

| Criterion | Learning outcomes covered | Weighting |
|---|---|---|
| **Creative concept and technical artefact**: originality, creativity, and technical competence in the design and implementation of an interactive audio software artefact. Includes strategic use of AI tools and integration of multiple software environments. | 1, 2, and 3 | 50% |
| **AI collaboration portfolio**: evidence of strategic AI partnership, including prompt refinement, critical filtering, and reflective insight. Demonstrates how AI was used to support ideation, development, and problem-solving while maintaining conceptual ownership. | 1, 2, and 4 | 25% |
| **Viva voce performance**: technical understanding and conceptual mastery through live demonstration, explanation, and modification of the artefact. Includes discussion of AI collaboration and design decisions. | 2, 3, and 4 | 25% |

## Referral (second attempt)

If you fail the module with a grade under 40% you may be allowed to submit for a second attempt if you fulfil the criteria to be eligible. In this case, you will have to resubmit your complete portfolio and participate in a new viva voce.

## Eligibility for an Automatic Extension

This assessment is eligible for an Automatic Extension of up to 48 hours. You may wish to use the Automatic Extension due to unforeseen circumstances preventing you from submitting the assessment by the published assessment deadline. You do not have to do anything to use an Automatic Extension. The 48-hour period starts from the time and date of the original deadline. For example, given the original deadline is at 3pm on a Wednesday, the end of the Automatic Extension deadline will be 3pm on the Friday. If you submit the assessment by the original deadline, or within the 48-hour extension, you cannot re-submit it again during the Automatic Extension period. No academic support will be available in relation to the completion of the assessment during the 48-hour extension period.

Note: All vivas must be completed and recorded before the original submission deadline. The automatic extension does not apply to viva voce scheduling or participation. You must confirm your viva date with the module leader before Christmas.

## Submission checklist

You must submit the following evidence via the Wiseflow submission portal, linked from Moodle:

1. **Technical artefact package** - All source code, related files (e.g. audio files), and a README file with usage instructions and creative vision, compressed into a single zip file;
2. **AI collaboration portfolio** - Markdown document (.md file) as specified above, submitted as a separate file (not in zip file);
3. **Viva voce recording** - Recording of your viva session as a separate `.mp4` file (not in zip file).
4. **Mandatory AI Acknowledgement** - An additional page or separate document confirming and detailing the use of AI in your submission (see 'AI Collaboration Guidelines and Academic Integrity' section).

Optionally, you may choose to also submit presets/templates/example settings for your software, and/or example input audio files.

## Viva Voce Guidelines

All vivas will be conducted via Teams or in-person in our normal lab in the Eldon building during the final week before submission. Vivas will be scheduled in advance and you must contact the module leader before Christmas to arrange your session.

### Viva Format

- **Duration:** 30 minutes total
- **Structure:** Demonstration (5---10 minutes) + technical discussion (20---25 minutes)
- **Materials:** You may consult your code, notes, and documentation
- **Recording:** All vivas will be recorded for assessment purposes and you must submit this recording as part of your portfolio

### Technical Setup Requirements

- **Working software installation** with your project ready to run
- **Stable internet connection** (for Teams vivas)
- **Screen sharing capability** to show your code and software
- **Audio setup** that allows clear demonstration of your audio software

### What to Expect

The examiner will ask you to:

1. Give a brief demonstration of your software's core features
2. Explain specific technical implementations and design choices
3. Modify or extend code to demonstrate understanding
4. Discuss how AI collaboration influenced your development process
5. Answer questions about relevant DSP concepts and SuperCollider techniques

### Assessment Focus

- **Technical Competence:** Understanding of sound and music programming concepts and implementation across a range of software and hardware (as appropriate)
- **Conceptual Understanding:** Ability to explain and justify technical decisions
- **AI Collaboration Insights:** Thoughtful reflection on human-AI partnership benefits and limitations
- **Problem-Solving Skills:** Ability to adapt and modify solutions in real-time
- **Communication:** Clear explanation of technical concepts and project rationale

## AI Collaboration Guidelines and Academic Integrity

### Mandatory AI Acknowledgement

You must clearly state if and how you have used artificial intelligence (AI) in the preparation of this submission. This acknowledgement is a **mandatory part of the submission**. It can be an additional page at the start of your submission (after the cover page), or it can be a separate document, but it must be submitted.

Work submitted without the acknowledgement is considered to be **incomplete**. Every submission must include the required acknowledgement, which must be consistent with the content of the items being submitted. If there is no acknowledgement contained in the submission, or if the acknowledgement is inconsistent with the work being submitted, then the Universitys **academic misconduct regulations apply**. Academic tutors may need to discuss with you any aspect of your submission, including the content of your acknowledgement.

#### Required Acknowledgement Form

Students must complete the following form and include it with their submission. If you did not use AI in this assessment all points below will be 'N'.

## I acknowledge that I used AI in this assessment

| Use of AI | Yes (Y) / No (N) |
| :--- | :--- |
| I used AI for developing ideas. | Y/N |
| I used AI for research and/or information gathering. | Y/N |
| I used AI to identify themes. | Y/N |
| I used AI for data analysis. | Y/N |
| I used AI to structure my assessment. | Y/N |
| I used AI to get feedback on my work. | Y/N |
| I used AI tools to generate images, tables, figures or diagrams: | Y/N |
| I used AI tools for proofreading, grammar check, etc: | Y/N |
| I used AI tools to improve flow and legibility: | Y/N |
| Other [Please specify]: | Y/N |

### Expected AI Tool Usage

This assessment **requires and evaluates** your strategic collaboration with AI tools. You are expected to:

1. **Use AI as a strategic development partner** to accelerate coding, explore creative possibilities, and solve technical challenges, while maintaining creative control and deep conceptual understanding.
2. **Document all AI collaboration transparently** in your code comments and README file. You must indicate clearly where and how you used AI-generated material.
3. **Demonstrate critical evaluation skills** by being prepared to discuss AI suggestions you rejected or modified during your viva voce.
4. **Maintain conceptual ownership** by ensuring you understand all code in your submission and can explain, modify, and extend it during the viva voce.
5. **Verify all AI-generated information** about SuperCollider syntax, DSP concepts, and audio programming practices against reliable sources and your own testing.

### Examples of Strategic vs Basic AI Collaboration

#### Strategic AI Collaboration Examples

- Using AI to brainstorm multiple algorithmic approaches to a synthesis problem, then evaluating and combining the best elements
- Providing AI with detailed project context and constraints to get more relevant code suggestions
- Iteratively refining prompts based on AI outputs to achieve more sophisticated solutions
- Using AI to explain complex DSP concepts and then testing understanding by implementing variations

#### Basic AI Collaboration Examples

- Simply copying and pasting AI-generated code without modification or understanding
- Using AI only for syntax corrections without engaging with design decisions
- Accepting first AI suggestion without evaluation or testing alternatives
- Relying on AI for explanations without verifying against authoritative sources

### Recommended AI Tools

- **Free Access Options:** We all get access to the underlying ChatGPT model via [Microsoft Copilot](https://m365.cloud.microsoft/chat). In addition we will make use of the free tiers of [Gemini](https://gemini.google.com/), [Claude](https://claude.ai/), and [ChatGPT](https://chatgpt.com/). You are welcome to use your own paid or local model (e.g. via [Ollama](https://ollama.com/)) if you wish, but note that we cannot install local models on University-owned computers.
- **SuperCollider-Specific Support:** Use AI for syntax help, UGen explanations, DSP algorithm implementation, and debugging assistance
- **Accessibility:** If you have limited access to AI tools, contact the module leader for alternative arrangements and support

### Academic Integrity Requirements

- **Attribution Standard:** All AI contributions must be clearly attributed in code comments and `README` documentation
- **Collaboration Boundary:** AI should enhance your capabilities, not replace your understanding or creative decision-making
- **Verification Mechanism:** You must be prepared to demonstrate understanding through live code explanation and modification in your viva voce
- **Honest Documentation:** AI collaboration portfolio must represent authentic experiences with AI collaboration

### Assessment Support

- **Weekly workshops:** Attend the weekly workshops which will introduce DSP using SuperCollider and effective AI collaboration techniques for sound and music programming (Wednesdays 9am to 12pm in the first six weeks, then Wednesdays 11am to 1pm)
- **Weekly drop-ins in the second half of the module:** Once you started your assessment work we will run drop-in sessions on Fridays from 3pm to 4pm (starting Monday 21<sup>st</sup> November) for guidance on DSP, SuperCollider, strategic AI partnership, and troubleshooting software/hardware combinations.
- **Viva Preparation:** Practice sessions available from Week 10 in the drop-in sessions for students who want feedback on their demonstration approach
- **Technical Support:** Contact Matt if you encounter issues with AI tool access or collaboration strategies

# Categorical marking

When your assessment is marked, it will receive a percentage score. We use a method called &lsquo;categorical marking' to ensure consistency and fairness across all markers, which associates each grade with a description, as follows. See the [understanding your results](https://myport.port.ac.uk/my-course/exams/understanding-your-results) page for more information.

## University of Portsmouth Categorical Marking Criteria

| Classification | Mark | Description |
|---|---|---|
| Publishable / Professional standard | 100 | Exceptional in most/all aspects, substantially exceeding expectations. |
| Near publishable / Professional | 95 | |
| Exceptional 1st | 88 | |
| Outstanding 1st | 85 | |
| Excellent 1st | 82 | Excellent quality, exceeding expectations in many aspects. |
| Very good 1st | 78 | |
| Clear 1st | 75 | |
| Just about a 1st | 72 | |
| Very good 2:1 | 68 | Meets all intended learning outcomes; exceeds threshold in several. |
| Clear 2:1 | 65 | |
| Just about a 2:1 | 62 | |
| Very good 2:2 | 58 | Meets all intended learning outcomes; exceeds threshold in some. |
| Clear 2:2 | 55 | |
| Just about a 2:2 | 52 | |
| Very good 3rd | 48 | Meets all intended learning outcomes; rarely exceeds threshold. |
| Clear 3rd | 45 | |
| Just about a pass | 42 | |
| Not quite a pass / Marginal fail | 38 | Fails to meet all intended learning outcomes; inadequate for this level. |
| Marginal fail | 35 | |
| Mid-range fail | 32 | |
| Mid-range fail | 28 | |
| Fail | 22 | |
| Fail | 15 | |
| Non-submission or no adequate attempt | 0 | No submission |


# Mark scheme

| Criterion | Absolute Fail (0--29%) | Marginal Fail (30--39%) | Adequate (40--49%) | Good (50--59%) | Very Good (60--69%) | Excellent (70--79%) | Outstanding (80%+) |
|---|---|---|---|---|---|---|---|
| **Creative concept and technical artefact (50%).** | No functional software. No evidence of programming competence or creative direction. No integration of AI or multiple tools. Conceptual understanding is absent. | Limited functionality and poor code structure. Minimal creativity. AI use is unclear or superficial. Conceptual understanding is weak and lacks coherence. | Basic functionality and programming competence. Limited creativity and superficial use of AI or tool integration. Conceptual understanding is present but underdeveloped. | Functional and creative artefact with clear technical structure. AI and tool use are evident but may lack optimisation. Conceptual understanding is sound but may lack depth or clarity in places. | Well-designed and imaginative artefact with strong technical execution. AI and tool use are effective and clearly documented. Demonstrates good understanding of core concepts and thoughtful implementation. | Highly creative and technically sophisticated artefact. Strategic use of AI and effective integration of software tools. Demonstrates strong conceptual understanding and well-justified design decisions. Minor issues may exist but do not detract from overall quality. | Exhibits exceptional creativity and technical mastery. The artefact demonstrates innovative use of AI tools and seamless integration of multiple software environments. Functionality is robust and professionally presented, with clear evidence of deep conceptual understanding and original thinking. |
| **AI collaboration portfolio (25%)** | No meaningful documentation. No strategic AI use. No reflection or critical filtering. No evidence of understanding. | Minimal documentation. Basic AI use. Limited reflection or evaluation. Lacks strategic direction. | Meets basic requirements. Some strategic AI use. Basic reflection and filtering. Limited insight into collaboration process. | Clear documentation and thoughtful AI use. Evidence of critical filtering and strategic decisions. Reflection is present but may lack depth. | Strong documentation and sophisticated AI strategy. Clear evaluation and iterative refinement. Demonstrates thoughtful engagement with AI tools. | Expert-level AI collaboration. Nuanced reflection and strategic integration. Clear evidence of prompt refinement, critical filtering, and conceptual ownership. | Exemplary documentation of AI collaboration. Demonstrates innovative strategy, critical insight, and professional-level reflection. Offers new perspectives on human---AI partnership in audio programming. |
| **Viva voce performance (25%)** | Unable to demonstrate software or explain technical concepts. No understanding of AI use. Fails to engage with viva requirements. | Limited demonstration. Struggles with technical explanation. Minimal AI discussion. Unable to respond effectively to questions. | Basic demonstration and explanation. Some understanding of technical and AI aspects. Limited ability to modify or extend code live. | Competent demonstration. Clear technical discussion. AI collaboration explained with examples. Handles most questions effectively. | Strong technical presentation. Detailed explanation and live modification. Strategic AI use discussed with clarity. | Exceptional technical and conceptual mastery. Sophisticated AI discussion and real-time problem-solving. Demonstrates full understanding of artefact and underlying principles. | Professional-level presentation. Deep insight into technical and AI aspects. Demonstrates ability to teach and extend concepts live. Handles all questions with confidence and clarity. |

# Proposal Template

```markdown
---
title: Your Sound and Music Programming project title
author: Your name
date: The date you complete the proposal
---

# Describe the theme or key idea behind your project
Explain your creative vision and technical goals here.

# Project research and AI collaboration strategy
Discuss examples of current or historic related projects and explain how you plan to strategically collaborate with AI tools during development. How will you maintain creative control while leveraging AI capabilities?

## Proposed sources
Note: please use APA referencing as standard. Include sources on both technical audio programming concepts and AI collaboration approaches where relevant.

# Project development plan
Explain how your project will work from a user's perspective and outline your approach to balancing independent work with AI collaboration.

## What do you anticipate users to hear?
Your text here

## How will users interact with your software?
Your text here

## What unique features does your software offer them?
Your text here

## Planned AI collaboration tools (e.g. ChatGPT, GitHub Copilot, etc.)
Which tool(s) are you planning to use?

## How will you approach AI collaboration during development?
Describe your planned strategy for using AI tools while ensuring you maintain deep understanding of the technical concepts.

# Technical specifications

## Input sources you will be using
For example:

- Audio file input
- Real-time input
- Synthetic sources
- Other (specify here)

## Output sources you will be using
For example:

- Audio file output
- Real-time audio output
- Other (e.g the software emits control data)

## Real-time control methods
For example:

- SuperCollider GUI
- Open Sound Control (OSC)
- MIDI
- Other (please specify)

# Assessment preparation
Briefly outline:

- How you will document your AI collaboration process
- What aspects of your project you expect to demonstrate in the viva voce
- Any potential challenges you anticipate in explaining your technical implementation
```

[^1]: A viva voce (Latin for &ldquo;with the living voice&rdquo;) is an oral examination where students demonstrate their knowledge and understanding through spoken discussion with an examiner.
