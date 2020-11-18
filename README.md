# routines

***************************************************************************************************
Formal Definition of a "routine" -> a python function with the following properties:
- short memorable name
- computes a commonly used Variable from a raw dataset directory.
- when called, looks for the Variable in dir/routinesMemory where dir is the directory of 
  the dataset. If not found, the routine saves the variable after having computed it.
***************************************************************************************************

Python version has to be >=3.7 ot there will be imports issues!

Useful link to [create a python package from a git repository](https://towardsdatascience.com/build-your-first-open-source-python-project-53471c9942a7)

## Installation:
Using a conda environment is very much advised. Instructions here: [manage conda environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- from a local repository (recommended if plans to work on it/regularly pull upgrades)

```
$ conda activate env_name
$ cd path/to/save_dir # any directory where your code will be accessible by your editor and safe. NOT downloads folder.
$ git clone https://github.com/Npix-routines/NeuroPyxels
$ cd NeuroPyxels
$ python setup.py develop # this will create an egg link to save_dir, which means that you do not need to reinstall the package each time you pull an udpate from github.

```
- from the remote repository (recommended for easy passive install)
```
$ conda activate env_name
$ pip install git+https://github.com/Npix-routines/NeuroPyxels@master

```
- Now test that the installation works.
If it doesn't, figure out which packages are missing from the error log.
```
$ conda activate env_name
$ python
>>> import npix # NO ERROR OMG THIS PACKAGE IS SO AWESOME

```

### Pull remote updates (after Maxime's updates :)):
```
$ conda activate env_name
$ cd path/to/save_dir/NeuroPyxels
$ git pull
# And that's it, thanks to the egg link no need to reinstall the package!
```

### Push local updates:
```
# DO NOT DO THAT WITHOUT CHECKING WITH MAXIME FIRST
# ONLY ON DEDICATED BRANCH CREATED WITH THE GITHUB BROWSER INTERFACE

$ cd path/to/save_dir/NeuroPyxels
$ git checkout DEDICATED_BRANCH_NAME # ++++++ IMPORTANT
$ git add.
$ git commit -m "commit details - try to be specific"
$ git push origin DEDICATED_BRANCH_NAME # ++++++ IMPORTANT

# Then pull request to master branch using the online github green button! Do not forget this last step, to allow the others repo to sync.
```


