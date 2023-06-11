import re
import json
import datetime

# Get current date
now = datetime.datetime.now()

# Format date as four-digit year, two-digit month, and two-digit day
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")

# Open the arXiv file in read mode
with open(f'/Users/grinch/Developer/Software/ArXiv/ArXivDaily/data/{year}-{month}-{day}.txt', 'r') as f:
    # Read the entire file content
    text = f.read().split(r'%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%--%%')[0]

def parse_arxiv_text(text):
    papers = []

    # Regular expression pattern for a paper entry
    pattern = re.compile(r"arXiv:(?P<id>[\d\.]+).*?Date: (?P<date>.*?GMT).*?Title: (?P<title>.*?)(?=Authors:).*?Authors: (?P<authors>.*?)(?=Categories:).*?Categories: (?P<categories>.*?)(?=\\\\).*?\\\\(?P<abstract>.*?)(?=\\\\ \(.*?\))", re.S)

    for match in pattern.finditer(text):
        paper_dict = match.groupdict()
        # Clean up the fields
        paper_dict['abstract'] = re.sub("\s+", " ", paper_dict['abstract'].strip())
        paper_dict['authors'] = paper_dict['authors'].split(', ')
        paper_dict['categories'] = paper_dict['categories'].split(' ')
        papers.append(paper_dict)

    return papers

papers = parse_arxiv_text(text)

ML_papers = [paper for paper in papers if ('cs.AI' not in paper['categories'] and 'cs.LG' in paper['categories'])]
AI_papers = [paper for paper in papers if ('cs.AI' in paper['categories'] and 'cs.LG' not in paper['categories'])]
ML_AI_papers = [paper for paper in papers if ('cs.AI' in paper['categories'] and 'cs.LG' in paper['categories'])]

combined_papers = ML_papers + AI_papers + ML_AI_papers
for i, paper in enumerate(combined_papers):
    paper['link'] = f'https://arxiv.org/abs/{paper["id"]}'

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
            titleDiv.innerText = (index + 1) + ". " + paper.title;
            titleDiv.className = "dropdown";

            var abstractDiv = document.createElement("div");
            abstractDiv.innerText = paper.abstract;
            abstractDiv.className = "abstract";

            var linkDiv = document.createElement("div");
            linkDiv.innerHTML = '<a href="' + paper.link + '" target="_blank">Link to paper</a>';
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

with open(f'/Users/grinch/Developer/Software/ArXiv/ArXivDaily/dailies/{year}-{month}-{day}.html', 'w') as f:
    f.write(website)