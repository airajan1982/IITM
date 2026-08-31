"""Keyword frequency extractor: reads .txt files from a folder, counts word
frequencies (excluding stopwords), and writes the results to CSV."""

import os
import string
import time
import csv
from collections import Counter

FOLDER_NAME = "sample_texts"
STOPWORDS = {
    'the', 'is', 'at', 'on', 'of', 'a', 'and', 'to', 'in', 'it', 'for',
    'that', 'as', 'with', 'was', 'were', 'be', 'this', 'by', 'an',
}
TOP_N = 50
ALL_COUNTS_FILE = "keyword_counts.csv"
TOP_KEYWORDS_FILE = "top_keywords.csv"

# Built once (not per file/char) - a single-pass replacement for the
# original's nested "for p in string.punctuation: text.replace(p, ' ')".
PUNCTUATION_TABLE = str.maketrans(string.punctuation, " " * len(string.punctuation))


def find_txt_files(folder):
    """Return the list of .txt filenames directly inside `folder`."""
    if not os.path.exists(folder):
        print("folder not found")
        return []
    print("reading folder:", folder)
    return [name for name in os.listdir(folder) if name.endswith('.txt')]


def tokenize_file(path, stopwords):
    """Read a text file and return its cleaned, stopword-filtered words."""
    with open(path, 'r', encoding='utf-8') as f:
        text = " ".join(line.strip() for line in f)
    text = text.lower().translate(PUNCTUATION_TABLE)
    return [w for w in text.split(" ") if w and w not in stopwords]


def collect_words(folder, txt_files, stopwords):
    """Tokenize every file in `txt_files` and return the combined word list."""
    allwords = []
    for filename in txt_files:
        path = os.path.join(folder, filename)
        allwords.extend(tokenize_file(path, stopwords))
    return allwords


def write_keyword_csv(filename, rows):
    """Write (word, count) rows to a CSV file with a header."""
    with open(filename, 'w', newline='', encoding='utf-8') as fout:
        writer = csv.writer(fout)
        writer.writerow(['Word', 'Count'])
        writer.writerows(rows)


def print_top_keywords(sorted_counts, n):
    print(f"Top {n} keywords:")
    for word, count in sorted_counts[:n]:
        print(word, ":", count)


def print_stats(total_words, unique_words):
    print("Total words:", total_words)
    print("Unique words:", unique_words)
    print("Average frequency:", round(total_words / unique_words, 2))


def print_duplicate_stats(total_words, unique_words):
    # Kept as a separate call (mirrors the original's intentional duplicate
    # print) but reuses the already-computed totals instead of recomputing.
    print("Recomputing stats again (unnecessary):")
    avg = total_words / unique_words
    print("Words:", total_words, " Unique:", unique_words, " Avg:", avg)


def report_timing(start_time):
    elapsed = time.time() - start_time
    print("Time taken to execute the script:", elapsed, "seconds")
    if elapsed > 5:
        print("This script is very slow! You might want to optimize it...")
    else:
        print("Good speed but still can be optimized.")


def confirm_outputs(*filenames):
    if all(os.path.exists(name) for name in filenames):
        print("Output files generated successfully.")
    else:
        print("Something went wrong in writing files.")


def main():
    start_time = time.time()

    txt_files = find_txt_files(FOLDER_NAME)
    print("Found", len(txt_files), "text files")

    allwords = collect_words(FOLDER_NAME, txt_files, STOPWORDS)
    wordcounts = Counter(allwords)
    sorted_counts = sorted(wordcounts.items(), key=lambda kv: kv[1], reverse=True)

    print_top_keywords(sorted_counts, TOP_N)

    write_keyword_csv(ALL_COUNTS_FILE, sorted_counts)
    write_keyword_csv(TOP_KEYWORDS_FILE, sorted_counts[:TOP_N])

    total_words = sum(wordcounts.values())
    unique_words = len(wordcounts)
    print_stats(total_words, unique_words)
    print_duplicate_stats(total_words, unique_words)

    report_timing(start_time)
    confirm_outputs(ALL_COUNTS_FILE, TOP_KEYWORDS_FILE)

    print("---- END OF SCRIPT ----")


if __name__ == "__main__":
    main()
