# Jupyter Notebook Setup

## Notebook Roles

Start here before editing or citing notebooks:

`docs/notebook_roles.md`

Short version:

- Frozen filed Exhibit A notebook: `legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb`
- Living wearable research notebook: `legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb`
- Legacy/supporting public notebook: `HandicapSkater-Public.ipynb`

The frozen filed notebook and filed PDF are locked court-record artifacts. Ongoing wearable research belongs in the living wearable notebook and generated research outputs, not in the filed-record path.

## Filed Exhibit A Verification Commands

Run these commands from the repository root.

### Canonical filed PDF

```sh
make verify-filed-exhibit-a
```

Verifies the canonical court-filed PDF:

`legal/cases/25-7526/filed/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf`

The check confirms the recorded SHA-256, 15-page count, and required Exhibit A title text on page 1.

```sh
make update-filed-exhibit-a-hash
```

Updates the filed PDF hash only after intentionally replacing the filed court artifact.

```sh
make reproduce-filed-exhibit-a-candidate
```

Generates a candidate PDF under:

`legal/cases/25-7526/reproduced_candidate/`

It does not overwrite the canonical filed PDF.

```sh
make compare-filed-exhibit-a
```

Compares the generated candidate PDF to the canonical filed PDF by byte hash, page count, and extracted text.

### Court-safe hash checks

```sh
make check-filed-input-data-hash
```

Verifies that:

`legal/cases/25-7526/data/2026-06-03_fsicss_legal_corpus_categorized.jsonl`

matches the SHA-256 recorded in:

`legal/cases/25-7526/data/SHA256SUMS.txt`

```sh
make check-filed-notebook-lock
```

Verifies that:

`legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb`

matches the frozen notebook SHA-256 recorded in:

`legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/NonTraditional_notebook.sha256`

```sh
make check-filed-artifact-locks
```

Runs the filed input data hash check, the frozen notebook lock check, and the `legal.src` import smoke test. This is the main court-safety verification command before reproducing Exhibit A.

### Reproduction and import checks

```sh
make smoke-test-legal-imports
```

Verifies that `legal.src` imports work from the repository root and that the filed Exhibit A output path resolves correctly.

```sh
make reproduce-filed-exhibit-a
```

Reproduces the filed Exhibit A PDF from the frozen notebook and writes:

`legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf`

It also writes:

`legal/cases/25-7526/outputs/exhibit_a_filed_2026-06-04/Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf.sha256`

### Normalized notebook integrity

```sh
make hash-nontraditional-notebook
```

Verifies the normalized integrity hash for:

`legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb`

The normalized hash ignores execution counts, outputs, and selected volatile metadata. It is not a byte-for-byte notebook hash.

```sh
make update-nontraditional-notebook-hash
```

Updates the normalized notebook hash after an intentional filed-record notebook correction.

### Intentional filed-record correction

```sh
make update-filed-exhibit-a-lock
```

Updates the frozen notebook hash lock after an intentional filed-record correction. Do not use this for ongoing research changes. Use:

`legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb`

for living wearable biomechanics and ParaTransit research.

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
