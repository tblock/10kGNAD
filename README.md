# Ten Thousand German News Articles Dataset

For more information visit the detailed [project page](https://tblock.github.io/10kGNAD/).

1. Install the required python packages `pip install -r requirements.txt`.
2. Download and decompress the `corpus.sqlite3` file into the project root from [compressed from here](https://github.com/OFAI/million-post-corpus/releases/download/v1.0.0/million_post_corpus.tar.bz2) or directly from [here](https://github.com/tblock/10kGNAD/releases/download/v1.0/corpus.sqlite3).
3. Run `python code/extract_dataset_from_sqlite.py corpus.sqlite3 articles.csv` to extract the articles.
4. Run `python code/split_articles_into_train_test.py` to split the dataset.

## License

All code in this repository is licensed under a MIT License.

The dataset is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
