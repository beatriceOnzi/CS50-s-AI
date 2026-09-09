import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    damping_prob = (1 - damping_factor) / len(corpus)
    page_prob = {}

    if not corpus[page]:
        page_prob = {key: damping_prob for key in corpus}
        return page_prob

    for p in corpus:
        if (p in corpus[page]):
            page_prob[p] = damping_prob + (damping_factor / len(corpus[page]))
        else:
            page_prob[p] = damping_prob

    return page_prob
        

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page = random.choice(list(corpus.keys()))
    pages = [page]
    page_rank = {}

    for _ in range(n):
        page_prob = transition_model(corpus, page, damping_factor)
        page = get_next_page(page_prob)
        pages.append(page)

    for p in corpus:
        prob = pages.count(p) / n
        page_rank[p] = prob

    return page_rank


def get_next_page(page_prob):
    pages = list(page_prob)
    weights = list(page_prob.values())

    next_page = random.choices(pages, weights = weights, k=1)

    return next_page[0]


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    {
        "1.html": {"2.html", "3.html"}, 
        "2.html": {"3.html"}, 
        "3.html": {"2.html"}}

        to do:
        Simultaneous vs. sequential updates: Inside your loop, when you update pages_rank[p], 
        the calculation for the next page uses this already-updated value. Should all pages in one 
        round be based on the previous round's values? Think about whether you need a separate 
        copy to read from while writing new values.

    """
    damping_prob = (1 - damping_factor) / len(corpus)
    pages_rank = dict.fromkeys(corpus, (1 / len(corpus)))

    pages = list(pages_rank)

    while True:
        rank_values = list(pages_rank.values())
        copy_pages_rank = pages_rank.copy()

        for p in pages:
            sum = 0
            for i in pages:
                if not corpus[i]:
                    num_links_i = len(corpus)
                    sum = sum + (copy_pages_rank[i] / num_links_i)

                elif p in corpus[i]:
                    num_links_i = len(corpus[i])
                    sum = sum + (copy_pages_rank[i] / num_links_i)

            pages_rank[p] = damping_prob + (damping_factor * sum)

        new_rank_values = list(pages_rank.values())

        if not there_was_pagerank_change(rank_values, new_rank_values):
            break

    return pages_rank

def there_was_pagerank_change(rank_values, new_rank_values):
    for i in range(len(rank_values)):
        difference = abs(rank_values[i] - new_rank_values[i])
        if (difference > 0.001):
            return True
        
    return False


if __name__ == "__main__":
    main()
