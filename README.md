# Octopus Use Odor Plumes 🐙

## Tracking chemosensory plume navigation in *Octopus rubescens*

This repository contains the code and processed data for the paper:

**"Octopus track chemosensory plumes to find food"**  
Willem Lee Weertman¹²³, Venkatesh Gopal⁴, Dominic M. Sivitilli¹², David Scheel³, David H. Gire²

¹University of Washington Friday Harbor Laboratories  
²Department of Psychology, University of Washington  
³Institute of Culture and Environment, Alaska Pacific University  
⁴Department of Physics, Elmhurst University

### Abstract
This study presents the first laboratory observations of octopuses performing chemosensory-plume-guided navigation to locate food sources. Using a custom-built octopus-safe flume and infrared imaging, we demonstrate that *Octopus rubescens* employs odor-gated rheotaxis and exhibits characteristic fast arm-aligned motions (FAAM) during chemosensory tracking. Our findings suggest that octopus arms and suckers serve as the primary chemosensory organs driving this behavior.

### Working with the 1T videos

*Written by gpt-6-astra (via Hermes Agent), at Willem Weertman's request.*

For collaborators: **[Download and use the octopus-centered, rotated videos](docs/1T-video-quickstart.md)**. The guide explains which existing Dropbox MP4s to choose, how to preserve animal/condition/trial identities, how to verify and read the videos in Python, and the processing and frame-alignment caveats. No DeepLabCut setup is needed to use the already-processed videos.

[![Real-video comparison of full-frame, background-subtracted, centered, and centered-rotated representations.](docs/assets/1T-video-examples/representations.png)](docs/1T-video-quickstart.md#visual-examples-what-the-representations-look-like)

The guide includes a labeled comparison and an animated example from the same trial.

### Key Features
- 🎥 DeepLabCut pose estimation models for octopus eye tracking
- 🌊 Analysis of chemosensory tracking behaviors in turbulent flow
- 📊 Quantification of fast arm-aligned motions (FAAM)
- 🗺️ Trajectory analysis and visualization tools

---

<p align="center">
  <img src="assets/octopus_tracking_demo.gif" alt="Octopus chemosensory tracking demonstration" width="600">
  <br>
  <em>Octopus rubescens performing chemosensory-plume-guided navigation in the experimental flume</em>
</p>
