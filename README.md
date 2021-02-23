# M&C 2021 paper on hybrid transport-depletion sequence

| | |
|-|-|
|Paper| ![Status: Submitted](https://img.shields.io/badge/Status-Submitted-yellow)|
|Data| [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4554319.svg)](https://doi.org/10.5281/zenodo.4554319)|
|License| [![BSD 3-Clause](https://img.shields.io/github/license/CORE-GATECH-GROUP/mc21-depletion)](https://github.com/CORE-GATECH-GROUP/mc21-depletion/blob/main/LICENSE.txt)|

This repository contains analysis and build scripts to produce the paper 
"Towards an Efficient and Stable Hybrid Transport-depletion Sequence
Using Reduced-order Solutions at Substeps" written by Andrew Johnson and
Dan Kotlyar of Georgia Institute of Technology, Computational and Reactor
Engineering (CoRE) lab. The conference paper was submitted to the 2021
ANS M&C conference.

## Building

The paper can be build using `make`. The data set can be downloaded
from [Zenodo](https://zenodo.org/record/4554319) and should be stored
as `data.h5`. The `make` script will fetch the data file if it
does not exist. 

The style and other conference-specific LaTeX files can be obtained from
the [M&C author section](http://mc.ans.org/info-for-authors/) and manually
extracted. Alternatively, the command `make ans` will extract the necessary
files for you with `curl`. The paper requires the following files:
`mc2021.bst`, `mc2021.cls`, `cites.sty`, and `citesort.sty`

The command `make prereqs` will fetch the data file and LaTeX files without
building the the source document nor running any analysis scripts. This can
be used to determine if you need to manually download the prerequisites.
