[![](https://img.shields.io/badge/Visit-our%20project%20page-ff69b4)](https://school.brainhackmtl.org/project/template)

# MethNet

By Kendra Oudyk (she/her)

![](images/visualization__example.gif)

## Summary
For this project, I worked on Python package that creates a citation network for a given field that evolves over time, colored by methods used by papers in that field.

## Project definition

### Background
Methods can influence results in fMRI research (e.g., Carp, 2012; Eklund et al., 2016; Glatard et al., 2015). If methods influence results, then methodological trends may stystematically influence results. In order to explore this problem space, I thought it might be helpful to visualize methodological trends in fMRI research.

### Purpose
The purpose of this project was to make a Python package that could create a citation network for a given field, colored by methods used by papers in that field. Such a figure would be created for each year in a range, so that one can see the development of the network and the use of methods over time. Using this package to look at research using fMRI, I hope to observe whether methods correspond to groupings of papers in the citation network.

### Data
This package uses the [PubMed Central Open-Access Subset](https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/)\*, which is a set of papers on PubMed Central that are available under an open licence. I chose this dataset because the package need access to the full text of journal articles in order to search for methods-related keywords.

## Results
### Progress overview
I was able to create the type of figure that I had envisioned, and I practiced using almost all of tools and skills that I'd hoped to practice. However, the figure has some glitches and was not as informative as I'd hoped, and I did not get as far as I'd planned in terms of packaging and testing.

### Deliverables
- [Package](https://github.com/brainhack-school2020/koudyk_bhs_project) in progress,
- [Workflow diagram](https://github.com/brainhack-school2020/koudyk_bhs_project/blob/master/images/workflow_diagrams/diagram_entire_workflow.gv.png) illustrating how the package works,
- [Example notebook](https://github.com/brainhack-school2020/koudyk_bhs_project/blob/master/methnet/example.ipynb) showing how to use the package, and
- [Example gif](https://github.com/brainhack-school2020/koudyk_bhs_project/blob/master/images/visualization__example.gif), which is the output of the example notebook.

### Tools and skills practiced
In this project, I practiced (more or less)
- [x] Packaging
- [x] GitHub issues & projects
- [x] API interaction
- [x] XML
- [x] Jupytext
- [x] Python
- [x] Data visualization

## Conclusion and acknowledgement
Although the project did not end up exactly where I'd hoped, I learned a lot along the way. I appreciate all the effort that was put in by the BHS instructors and organizers, particularly Sam, Agah, Alexa, and Loic. I'm also especially thankful to Jérôme, who helped me even though he wasn't part of the BHS.


***

#### References
- Carp, J. (2012). On the plurality of (methodological) worlds: Estimating the analytic flexibility of fMRI experiments. *Frontiers in Neuroscience, 6*, 149.
- Eklund, A., Nichols, T. E., & Knutsson, H. (2016). Cluster failure: Why fMRI inferences for spatial extent have inflated false-positive rates. *Proceedings of the National Academy of Sciences, 113*(28), 7900-7905.
- Glatard, T., Lewis, L. B., Ferreira da Silva, R., Adalat, R., Beck, N., Lepage, C., ... & Khalili-Mahani, N. (2015). Reproducibility of neuroimaging analyses across operating systems. *Frontiers in Neuroinformatics, 9*, 12.

#### \*NCBI's Disclaimer and Copyright notice
The National Center for Biotechnology Information (NCBI), who own the PubMed data and E-utilities that we will be using, requests that we make this [Disclaimer and Copyright notice](https://www.ncbi.nlm.nih.gov/home/about/policies/) evident to users.
