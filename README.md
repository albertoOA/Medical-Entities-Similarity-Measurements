# Medical Entities Similarity Measurements

All the code implemented in this repository is the work done by **Alberto Olivares Alarcos** as part of his Master Thesis in the field of  Artificial Intelligence. The thesis is named as: 'Semantic Distances Between Medical Entities' and it was done during the course 2017-2018 and presented on April 2018. 


The Director of the thesis was **Horacio Rodríguez Hontoria**, professor and researcher at the School of Informatics of the University: **Universitat Politècnica de Catalunya (UPC)**, Spain.


## Instalation of necessary tools

In order to make use of this repository, it is necessary to install some specific Python tools and libraries. We have used Jupyter Notebooks in order to show our results in an elegant format. Thus, we need to install it. There are three main experiments devoted to the computation of similarity between drugs by means of three different sorts of techniques: 

- Similarity based on text mining
- Similarity based on taxonomy
- Similarity based on molecular structure

We explain the linux commands we need to run for the installation of the tools for each of those experiments. Note that there is not need for extra tools in the case of the Taxonomy experiment.

### Text mining
```
$ sudo pip3 install editdistance

$ sudo pip3 install -U nltk
$ sudo pip3 install pandas
```

### Molecular Structure
Downlowad miniconda from the next link:  https://conda.io/miniconda.html

```
$ cd ~/Downloads/
$ bash Miniconda3-latest-Linux-x86_64.sh
$ conda install conda-build
```

Restart the terminal to see the changes
```
$ conda create -c rdkit -n rdkit-env rdkit
$ source activate rdkit-env
```

Fixing some memory problems
```
$ pip3 install --upgrade jsonschema
```

Necessary libraries for some of the tasks done within this experiment.
```
$ conda install -c anaconda scikit-learn
$ conda install -c anaconda matplotlib
```

We need to create a kernel of the environment for jupyter notebook or else, we could not run this experiment. Please, note that once you opened jupyter notebook on your browser, you would need to choose this kernel to run the Molecular Structure notebook.
```
$ python -m ipykernel install --user --name rdkit-env-kernel
```

Now we can run jupyter.
```
$ jupyter notebook
```
