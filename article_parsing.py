import os
import webbrowser
from newspaper import Article
from collections import Counter
import re
from googlesearch import search
import time
import requests

def load_wordlist(file_path):
    """Loads a word list from a given text file."""
    with open(file_path, 'r') as file:
        return {word.strip().lower() for word in file if word.strip()}

def fetch_article_content(url):
    """Fetches the content of an article from a given URL, opening in browser on CAPTCHA errors."""
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 429:  # Too Many Requests
            print(f"CAPTCHA or too many requests error for {url}. Opening in browser.")
            webbrowser.open(url)  # Open the link in the default web browser
            return None
        else:
            print(f"Error fetching article from {url}: {e}")
            return None

def count_word_frequencies(article_text, word_list):
    """Counts word frequencies in the article text."""
    words = re.findall(r'\b\w+\b', article_text.lower())
    return Counter(word for word in words if word in word_list)

def save_to_txt(url, pos_count, pos_percent, neg_count, neg_percent, word_freq_pos, word_freq_neg, output_file, debug=False):
    """Writes the URL and word frequency data to a text file."""
    with open(output_file, 'a') as f:
        f.write(f"URL: {url}\n")
        f.write(f"[[[\t\tPercent Positive :\t{pos_percent}%\t|\tPercent Negative :\t{neg_percent}%\t]]]\n\n")
        f.write(f"Total Positive Word Count: {pos_count}\nTotal Negative Word Count: {neg_count}\n")
        
        if debug:
            for label, word_freq in [('Positive', word_freq_pos), ('Negative', word_freq_neg)]:
                f.write(f"Word Frequencies {label}:\n")
                f.writelines(f"{word}: {freq}\n" for word, freq in word_freq.items() if freq > 0)

        f.write("\n" + "-" * 50 + "\n")
    time.sleep(2)

def normalize_data(pos_count, neg_count):
    total_count = pos_count + neg_count
    return (round(pos_count / total_count, 4), round(neg_count / total_count, 4)) if total_count else (0, 0)

def process_article(url, positive_word_list, negative_word_list, output_file):
    """Fetches the article, counts word frequencies, and writes the result to a text file."""
    article_content = fetch_article_content(url)
    if article_content:
        word_frequencies_pos = count_word_frequencies(article_content, positive_word_list)
        word_frequencies_neg = count_word_frequencies(article_content, negative_word_list)

        pos_count = sum(word_frequencies_pos.values())
        neg_count = sum(word_frequencies_neg.values())
        pos_percent, neg_percent = normalize_data(pos_count, neg_count)

        save_to_txt(url, pos_count, pos_percent, neg_count, neg_percent, word_frequencies_pos, word_frequencies_neg, output_file)

def find_articles(keyword, num_results=20):
    """Searches for articles containing the specified keyword."""
    keywordAdditions = [" financial articles", " recent changes", " predictions"]
    search_results = []

    for addition in keywordAdditions:
        search_query = f"{keyword}{addition}"
        print(f"Searching for articles containing: '{search_query}'")
        for attempt in range(3):  # Retry up to 3 times
            try:
                results = search(search_query, num_results)
                search_results.extend(results)
                time.sleep(1)  # Wait for 1 second between searches
                break  # Break out of retry loop if successful
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:  # Too Many Requests
                    print(f"Received 429 error. Waiting for 5 minutes before retrying...")
                    time.sleep(300)  # Wait for 5 minutes before retrying
                else:
                    print(f"Error during search: {e}")
                    break  # Exit retry loop on other errors
    
    return search_results

def article_processor_function(url_list):
    """Processes the articles in the given URL list."""
    negative_word_list = load_wordlist('/Users/adam/Documents/GitHub/Linear_Regression/Keywords/Negative.txt')
    positive_word_list = load_wordlist('/Users/adam/Documents/GitHub/Linear_Regression/Keywords/Positive.txt')

    output_file = 'article_word_frequencies.txt'
    for url in url_list:
        process_article(url, positive_word_list, negative_word_list, output_file)
        print(f"Word frequencies for the article at {url} saved to {output_file}.")

# Example usage
url_list = find_articles('GOOGL')
article_processor_function(url_list)
