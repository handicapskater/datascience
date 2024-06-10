# Jupyter Notebook Setup

### Ensure Homebrew is up-to-date
brew update
brew upgrade

### Install Python with pyenv
pyenv install 3.10

pipenv --python /opt/local/bin/python3.10

### Create a new project directory and navigate to it
mkdir my_notebook_project

cd my_notebook_project


conda create -n datascience python=3.10

conda activate datascience

conda install jupyter numpy pandas matplotlib seaborn scikit-learn

conda install ipykernel

conda update -n base -c conda-forge conda

python -m ipykernel install --user --name myenv --display-name "Python 3.10 (myenv)"

jupyter notebook

jupyter trust HandicapSkater-DataScience.ipynb


[//]: # (from notebook import trust)

[//]: # ()
[//]: # (notebook_path = 'DataScience.ipynb')

[//]: # ()
[//]: # (trust.mark_notebook_as_trusted&#40;notebook_path&#41;)

### Create a new pipenv environment with the Homebrew-installed Python

[//]: # (pipenv --python /usr/local/bin/python3)
pipenv --python /opt/local/bin/python3.10

pipenv --python `which python`

### Install Jupyter and other dependencies
pipenv install jupyter

pipenv install numpy pandas matplotlib seaborn scikit-learn

### Activate the pipenv shell
pipenv shell

### Install ipykernel
pipenv install ipykernel

### Add the pipenv environment to Jupyter
python -m ipykernel install --user --name=HandicapSkater --display-name "Python 3.10 (HandicapSkater)"

### Run Jupyter Notebook
jupyter notebook