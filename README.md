# Finetuning GPT-2 XL on song lyrics in Google Colab using TPUs
- Finetuning: GPT-2_Training_(TPU).ipynb
    - Finetune the pre-trained 1558M parameter GPT-2 on any dataset using Google Colab's TPU-Cluster
    - Model snapshots can be written to Google Drive to preserve the training progress 

- In order to clean lyrics data for model training, use data_preperation.py.
- After finetuning use Google Colab GPUs for generating output text (GPT_2_Generation_(GPU).ipynb)

@ Credits to [Shawn Presser](https://github.com/shawwn/gpt-2) and [Max Woolf](https://github.com/minimaxir/gpt-2-simple) for their contributions