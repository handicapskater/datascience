# Filed Exhibit A Reproducible Artifact

This directory is reserved for the filed Exhibit A PDF and its reproducibility metadata.

Filed PDF:

Exhibit_A_Wearable_Biomechanical_ParaTransit.pdf

Frozen source notebook:

legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb

Original filed-generation command:

    jupyter nbconvert --to pdf legal/notebooks/NonTraditional_Mobility_Aid_Biomechanics_ParaTransit_Burden.ipynb --TemplateExporter.exclude_input=True

Preferred reproduction command:

    make reproduce-filed-exhibit-a

or:

    bash legal/scripts/reproduce_filed_exhibit_a.sh

If using Google Colab, clone the repo and change to repo root before running the notebook:

    !git clone https://github.com/handicapskater/datascience.git /content/datascience
    %cd /content/datascience

Do not use the NonTraditional notebook for ongoing research. Use:

legal/notebooks/Wearable_Biomechanical_ParaTransit_Reproducible.ipynb

for continuing wearable biomechanics, ParaTransit burden, and Supreme Court-level record development.
