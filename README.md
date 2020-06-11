[![](https://img.shields.io/badge/Visit-our%20project%20page-ff69b4)](https://school.brainhackmtl.org/project/template)

# Methnet

By Kendra Oudyk (she/her)

![](images/visualization__example.gif)

### Background
Methods can influence results in fMRI. If methods influence results, then methodological trends may stystematically influence results. In order to explore this problem space, I wanted to visualize methodological trends in fMRI research.

### Purpose
The purpose of this project is to create a visualization of the fMRI citation network, colored by methods used. In this way, I'm hoping to observe whether methods correspond to groupings of papers in the citation network.

### Methods
#### Summary
There are 3 main stages in what this package does:
1. A user inputs a query to get papers and a list of keywords to search for;
2. The package gets papers matching the query and searches for the keywords; and
3. The the package creates a gif visualization of the data.

#### 1. User input
Someone who wants to use this package would input
  - **A PubMed query** to find papers for the field they're interested in. It might be helpful to build a query using the [PubMed website's advanced search function](https://pubmed.ncbi.nlm.nih.gov/advanced/) to get the syntax right. Note that there are additional filters used in this package, so you might see more results on the website than you'll get from this package.
  - **A list of methods keywords** to search for in the papers found (e.g., names of software). In this package, we just search for whether each keyword was mentioned anywhere in the text, and we do not search for synonyms. This means that the keyword should be specific.
    - Bad example: **"data"** (too generic)
    - Good example: **"SPSS"** (specific)


#### 2. Get data
We use the [PubMed Central Open-Access Subset](https://www.ncbi.nlm.nih.gov/pmc/tools/openftlist/), which is a set of papers on PubMed Central that are available under an open licence. We're using this set of papers because the open licence allows us to access the full text programmatically. We need the full text to search for methods-related keywords

We find papers that match the user's query using the [NCBI Entrez Programming E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25497/). These are a set of server-side programs that allow us to get information from the database at the National Center for Biotechnology Information (NCBI), which includes the PMC Open-Access Subset.

These programs allow us to find open-access articles that match our query and get their full texts so we can search for keywords. You can see the full workflow for getting the data [here](images/workflow_diagrams/diagram_pubmed.gv.png), and the code [here](methnet/pubmed.py).

#### 3. Visualize data
We couldn't find a package that could do what we wanted in a straightforward manner (though we didn't look/try for very long). So we decided to write our own code to do this.  

Essentially, this is how it works:
- For each year,
  - Create a circle with one point for each paper ID, including the search results and the references of the search results.
  - Draw a line between each search result and each of their references, colored by which method keyword was mentioned in the search-result paper.
- Then make a gif out of the yearly images.

You can ses the full workflow for getting the data [here](images/workflow_diagrams/diagram_vis.gv.png), and the code [here](methnet/visualizations.py).

## Deliverables
- [Package](https://github.com/brainhack-school2020/koudyk_bhs_project) in progress,
- [Workflow diagram](https://github.com/brainhack-school2020/koudyk_bhs_project/blob/master/images/workflow_diagrams/diagram_entire_workflow.gv.png) illustrating how the package works,
- [Example gif](https://github.com/brainhack-school2020/koudyk_bhs_project/blob/master/images/visualization__example.gif), and
- [Notebook](https://github.com/brainhack-school2020/koudyk_bhs_project/blob/master/methnet/example.ipynb) showing how to use the functions in the package.

## Goals met
In this project, I practiced (more or less)
- [ ] Software testing
- [x] Packaging
- [x] GitHub features
- [x] API interaction
- [x] XML
- [x] Text mining
- [x] Jupytext




### NCBI's Disclaimer and Copyright notice
The National Center for Biotechnology Information (NCBI), who own the PubMed data and E-utilities that we will be using, requests that we make this [Disclaimer and Copyright notice](https://www.ncbi.nlm.nih.gov/home/about/policies/) evident to users.
