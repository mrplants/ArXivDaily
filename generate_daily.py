import pyparsing as pp
import re
import json
import datetime

# Get current date
now = datetime.datetime.now()

# Format date as four-digit year, two-digit month, and two-digit day
year = now.strftime("%Y")
month = now.strftime("%m")
day = 14#now.strftime("%d")

# Open the arXiv file in read mode
with open(f'/Users/grinch/Developer/Software/ArXiv/ArXivDaily/data/{year}-{month}-{day}.txt', 'r') as f:
    # Read the entire file content
    text = f.read().split(r'%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%')[0]

def parse_arxiv_text(text):
    """
    Parse the ArXiv text to extract the metadata, abstract, and URL of each paper.

    This function uses the pyparsing library to define a grammar for parsing the 
    ArXiv text, which includes metadata categories (like title, authors, date, etc.), 
    the abstract, and the URL for each paper.

    Args:
        text (str): The ArXiv text to parse.

    Returns:
        list of dict: A list of dictionaries, where each dictionary represents a paper
                      and contains the keys 'metadata', 'abstract', and 'url'.
                      The 'metadata' is a dictionary itself with keys like 'Title',
                      'Authors', 'Date', etc. The 'abstract' is a string and 'url' is
                      the URL of the paper.
    """
    separator = pp.Suppress('\\\\'+pp.line_end())
    continued_line = pp.LineEnd().suppress() + pp.LineStart() + pp.Literal('\u00A0').suppress() + pp.restOfLine
    category = pp.Group(pp.LineStart() +
                        pp.Word(pp.alphas + ".-") +
                        pp.Suppress(":") +
                        pp.Group(pp.rest_of_line +
                                pp.ZeroOrMore(continued_line)) + 
                        pp.LineEnd().suppress())
    metadata = separator + pp.OneOrMore(category)('metadata')
    abstract = pp.SkipTo(pp.Suppress('\\\\'), include=True) + pp.SkipTo('\\\\')('abstract')
    url = pp.Suppress(pp.SkipTo('( ')) + pp.Suppress('( ') + pp.SkipTo(' ,')('url')
    # Define the overall grammar
    grammar = pp.OneOrMore(pp.Group(pp.Suppress(pp.SkipTo(separator)) + metadata + abstract + url))

    papers = []

    for results in grammar.parse_string(text):
        results.as_dict()
        paper = {
            'metadata' : {key:' '.join(values).strip() for key, values in results.as_dict()['metadata']},
            'abstract' : ' '.join([line.strip() for line in results.as_dict()['abstract'].split()]),
            'url' : results.as_dict()['url']
        }
        if 'Comments' in paper['metadata']:
            paper['metadata']['Comments'] = paper['metadata']['Comments'].strip().split(', ')
        if 'Date' in paper['metadata']:
            paper['metadata']['Date'] = datetime.datetime.strptime(paper['metadata']['Date'].split('\xa0', 1)[0].strip(), "%a, %d %b %Y %H:%M:%S %Z")
        if 'Authors' in paper['metadata']:
            paper['metadata']['Authors'] = paper['metadata']['Authors'].strip().split(', ')

        papers.append(paper)

    return papers

papers = parse_arxiv_text(text)

ML_papers = [paper for paper in papers if ('cs.AI' not in paper['metadata']['Categories'] and 'cs.LG' in paper['metadata']['Categories'])]
AI_papers = [paper for paper in papers if ('cs.AI' in paper['metadata']['Categories'] and 'cs.LG' not in paper['metadata']['Categories'])]
ML_AI_papers = [paper for paper in papers if ('cs.AI' in paper['metadata']['Categories'] and 'cs.LG' in paper['metadata']['Categories'])]

combined_papers = ML_papers + AI_papers + ML_AI_papers
for paper in combined_papers:
    paper['metadata']['Date'] = paper['metadata']['Date'].strftime("%a, %d %b %Y %H:%M:%S %Z")

website = r'''<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        #papers {
            width: 50%;
            margin: auto;
        }
        .paper {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .dropdown {
            cursor: pointer;
            font-weight: bold;
            color: #0056b3;
            text-decoration: underline;
        }
        .dropdown:hover {
            color: #007bff;
        }
        .abstract, .link {
            display: none;
            margin-left: 20px;
            margin-top: 10px;
        }
        .link a {
            color: #0056b3;
        }
        .link a:hover {
            color: #007bff;
        }
    </style>
</head>
<body>
    <div id="papers"></div>

    <script>
        var papers = PAPERS;

        var papersDiv = document.getElementById("papers");

        papers.forEach(function(paper, index) {
            var paperDiv = document.createElement("div");
            paperDiv.className = "paper";

            var titleDiv = document.createElement("div");
            titleDiv.innerText = (index + 1) + ". " + paper.metadata.Title;
            titleDiv.className = "dropdown";

            var abstractDiv = document.createElement("div");
            abstractDiv.innerText = paper.abstract;
            abstractDiv.className = "abstract";

            var linkDiv = document.createElement("div");
            linkDiv.innerHTML = '<a href="' + paper.url + '" target="_blank">Link to paper</a>';
            linkDiv.className = "link";

            titleDiv.addEventListener("click", function() {
                var display = abstractDiv.style.display;
                abstractDiv.style.display = display === "block" ? "none" : "block";
                linkDiv.style.display = abstractDiv.style.display;
            });

            paperDiv.appendChild(titleDiv);
            paperDiv.appendChild(abstractDiv);
            paperDiv.appendChild(linkDiv);
            papersDiv.appendChild(paperDiv);
        });
    </script>
</body>
</html>
'''

website = website.replace('PAPERS', json.dumps(combined_papers))

with open(f'/Users/grinch/Documents/Research/arXiv dailies/{year}-{month}-{day}.html', 'w') as f:
    f.write(website)
