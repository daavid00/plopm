---
title: 'plopm: A lightweight and flexible tool for visualization and postprocessing of OPM Flow geological models'
tags:
  - Corner-point grids
  - GIF
  - OPM Flow
  - PNG
  - VTK
authors:
  - name: David Landa-Marbán
    orcid: 0000-0002-3343-1005
    affiliation: 1
    corresponding: true
affiliations:
 - name: NORCE Research AS, Bergen, Norway
   index: 1
date: 16 February 2026
bibliography: paper.bib
---

# Summary

Reservoir simulations help the energy industry understand how underground pressure affects the movement of fluids such as water, oil, or gas and how it influences the stability of the surrounding rocks. These insights support better decisions in areas like energy production, carbon storage, and geothermal development. An important step in working with simulation results is postprocessing, which involves visualizing and analyzing the data. `plopm` is a tool designed to make this step faster, easier, and more consistent. `plopm` is operated through the command line, where users specify their postprocessing tasks using simple flags. This approach supports reproducibility and encourages efficient workflows. `plopm` is highly efficient, able to postprocess models containing hundreds of millions of cells in only a few tens of seconds. The tool offers several ways to visualize geological models. For example, users can generate 2D maps and choose how values are projected along a particular dimension, such as taking the maximum, minimum, or a pore‑volume‑weighted average. These options make it easier to compare scenarios and understand key patterns in the subsurface. Although `plopm` was originally intended to produce PNGs, GIFs, and VTK files from OPM Flow simulations, it has since grown more flexible. It can now also process results stored in CSV files, broadening its usefulness beyond the standard OPM Flow output format.

![Graphical representation of plopm's functionality ([here](https://cssr-tools.github.io/plopm/examples.html#graphical-abstract) are details to reproduce this).](paper.png){ width=100% }

# Statement of need

OPM Flow is an open-source simulator for subsurface applications such as CO$_2$ storage, hydrogen storage, and hydrocarbon production [@Rassmussen:2021]. There is growing demand for tools that make it easier to visualize and analyze simulation results, particularly for large‑scale models. `plopm` is a user‑friendly Python tool designed to support this need by providing efficient visualization and postprocessing of OPM Flow outputs. It is intended for researchers, engineers, and students who need to quickly interpret simulation results and compare scenarios. `plopm` offers flexible 2D visualization options, allowing users to choose among several projection methods depending on their analysis goals. This flexibility is especially relevant in current studies where rapid exploration of model behavior is essential. A key motivation behind `plopm` is to improve reproducibility, an increasingly important requirement in scientific research and technical reporting. Each generated figure can be reproduced by using a clear set of command‑line flags, ensuring that results can be regenerated, shared, and further processed in a consistent and transparent manner.

# State of the field

[ParaView](https://www.paraview.org) is a widely used open‑source post‑processing and visualization tool written in C++. It offers a comprehensive graphical user interface and excels at interactive 3D rendering, slicing, contouring, and animating simulation results. However, ParaView can have a steep learning curve, may experience performance and stability limitations, and is demanding in terms of memory and setup.


[ResInsight](https://resinsight.org) is an open‑source C++ tool designed specifically for postprocessing reservoir simulations, including Eclipse and OPM Flow models. It performs well when analyzing large datasets and visualizing grids, wells, and dynamic properties. Nevertheless, ResInsight can face performance issues with very large models, and importing models with extensive fault information may be time‑consuming. Users on macOS may also encounter installation challenges. In addition, the software struggles with models that have extremely small cell dimensions (below 1 mm) or very large cell counts (greater than 100 million).


While both ResInsight and ParaView are excellent tools for 3D visualization, lower‑dimensional tasks (2D and 1D) often carry unnecessary overhead when performed through full-featured visualization environments. In such cases, Python scripts can significantly streamline the postprocessing workflow. To the author’s knowledge, prior to the development of `plopm` there was no integrated, well‑documented Python‑based tool capable of generating PNGs, GIFs, and VTKs from OPM Flow output files using command‑line flags. Python provides a more accessible and flexible environment than C++, lowering the entry barrier for researchers, engineers, and students who require lightweight and customizable tools for model analysis.


The VTK functionality in `plopm` was originally implemented to enable 3D visualization of a SPE11C benchmark model, which contained more than 100 million cells. This capability made it possible to generate visualizations such as this [GIF](https://github.com/OPM/pyopmspe11/blob/main/docs/text/figs/pyopmspe11c100Mcells.gif). The motivation for developing this feature was the limited VTK support available in OPM Flow. In particular, several useful quantities are not exported (e.g., FIPNUM, FLORES), and the simulator writes the entire grid at every report step, leading to extremely large output files. In contrast, the VTK functionality in `plopm` allows users to efficiently extract selected data directly from OPM Flow output files (e.g., UNRST, INIT, EGRID) and convert them into lightweight VTK structures suitable for 3D visualization.


`plopm` offers a variety of options for visualizing simulation results, allowing users to compare methods and select the one that best fits their needs. For additional details about the capabilities included in plopm, see the [examples](https://cssr-tools.github.io/plopm/examples.html) in the project documentation.

# Software design

`plopm` leverages well‑established and widely used Python libraries. The Matplotlib package [@Hunter_Matplotlib_A_2D_2007] forms the core of the plotting routines. NumPy [@2020NumPy-Array] provides the foundational array operations used throughout the tool, and SciPy [@Virtanen:2020] supports interpolation tasks as well as the computation of normal and lognormal distributions used in ensemble visualizations. To display progress and estimate remaining runtime during postprocessing, the alive‑progress package [@aliveprogress] is employed. Parsing of OPM Flow binary output files is handled through the [opm](https://pypi.org/project/opm/) library.


The primary methods implemented in `plopm` include handling of corner‑point grids, parsing input decks (for example, to visualize wells and faults), enforcing homogenized colorbar limits to compare multiple models within a single figure, mapping OPM Flow output to VTK format, and stacking filter and cell‑value operations.


Interaction with the tool is performed via the terminal through an executable named `plopm`, which exposes a collection of command‑line flags (70 at the time of writing; see the online documentation for the current list at [current list](https://cssr-tools.github.io/plopm/introduction.html#overview)). These flags control key functionality such as specifying input models, defining the desired postprocessing operations, and selecting output file names. This design enables users to apply consistent postprocessing settings across different simulations. Advanced users familiar with Python can also access the underlying modules directly, allowing integration into more complex workflows and customization of model transformations to meet specific research or engineering needs.

# Research impact statement

`plopm` is already being adopted across several projects at NORCE Research AS. GitHub traffic insights also show a steady increase in repository clones, indicating broader interest and growing usage within the community.

The software has supported several research publications, including:

* @10.2118/218477-MS, where it was used to generate 2D maps of static properties and dynamic quantities such as pressure, salinity, and CO$_2$ saturation in synthetic 2D radial geometries.
* @10.1007/s11242-025-02275-0, for producing 2D maps of static properties and CO$_2$ mass for the FluidFlower/SPE11A models.
* @10.2118/231853-PA, for comparing 2D maps across different grid resolutions of the SPE11B benchmark model.
* @landamarban2025, for generating 2D maps of static properties and pore‑volume‑weighted average pressure for the Troll aquifer model.

The software also supports the online documentation of several open‑source tools, including:

* [expreccs](https://github.com/cssr-tools/expreccs): A Python framework using OPM Flow to simulate regional and site reservoirs for CO$_2$ storage. 
* [pofff](https://github.com/cssr-tools/pofff): An image-based history-matching framework for the FluidFlower Benchmark using OPM Flow.
* [pycopm](https://github.com/cssr-tools/pycopm): An open-source tool to tailor OPM Flow geological models.
* [pyopmnearwell](https://github.com/cssr-tools/pyopmnearwell): A Python framework to simulate near well dynamics using OPM Flow.
* [pyopmspe11](https://github.com/OPM/pyopmspe11): A Python framework using OPM Flow for the CSP SPE11 benchmark project.

Significant effort has been dedicated to developing comprehensive online documentation that enables users to reproduce figures, tables, and computational workflows from recent publications. This work is motivated by the FAIR principles (Findable, Accessible, Interoperable, Reusable) [@Wilkinson2016], which have not been consistently implemented in subsurface research in recent years [@liu2025]. For example, the [Publication](https://cssr-tools.github.io/pofff/publication.html), [TCCS-13](https://cssr-tools.github.io/expreccs/tccs-13.html#), and [Convergence](https://opm.github.io/pyopmspe11/convergence.html) documentation includes step‑by‑step terminal commands (such as `plopm`) required to generate the results published in @10.1007/s11242-025-02275-0, @landamarban2025, and @10.2118/231853-PA, respectively. These pages include the exact terminal commands (such as those invoking `plopm`) needed to regenerate the published outputs. This ensures that the scientific results are not only transparent but also directly reusable by other researchers, thereby enhancing methodological rigor and accelerating future developments.

# AI usage disclosure

No generative AI tools were used in the development of this software. Microsoft M365 Copilot (powered by a GPT‑5–class large language model developed by Microsoft) was used to check and improve the writing of this manuscript.

# Acknowledgements

The author acknowledges funding from the [Center for Sustainable Subsurface Resources (CSSR)](https://cssr.no), grant nr. 331841, supported by the Research Council of Norway, research partners NORCE Research AS and the University of Bergen, and user partners Equinor ASA, Harbour Energy, Sumitomo Corporation, Earth Science Analytics, GCE Ocean Technology, and SLB Scandinavia. The author also acknowledges funding from the [Expansion of Resources for CO2 Storage on the Horda Platform (ExpReCCS) project](https://www.norceresearch.no/en/projects/expansion-of-resources-for-co2-storage-on-the-horda-platform-expreccs), grant nr. 336294, supported by the Research Council of Norway, Equinor ASA, A/S Norske Shell, and Harbour Energy Norge AS.

# References
