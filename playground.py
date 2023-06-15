import pyparsing as pp
import datetime

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

text = R"""------------------------------------------------------------------------------
------------------------------------------------------------------------------
Send any comments regarding submissions directly to submitter.
------------------------------------------------------------------------------
Archives at http://arxiv.org/
To unsubscribe, e-mail To: cs@arXiv.org, Subject: cancel
------------------------------------------------------------------------------
Submissions to:
Artificial Intelligence
Computer Vision and Pattern Recognition
Distributed, Parallel, and Cluster Computing
Computer Science and Game Theory
Machine Learning
Multiagent Systems
Robotics
Systems and Control
received from  Mon 12 Jun 23 18:00:00 GMT  to  Tue 13 Jun 23 18:00:00 GMT
------------------------------------------------------------------------------
------------------------------------------------------------------------------
\\
arXiv:2306.07353
Date: Mon, 12 Jun 2023 18:21:23 GMT   (27kb)

Title: HDDL 2.1: Towards Defining a Formalism and a Semantics for Temporal HTN
 Planning
Authors: Damien Pellier, Alexandre Albore, Humbert Fiorino, Rafael Bailon-Ruiz
Categories: cs.AI
Comments: 5 pages, International Workshop of Hierarchical Planning (ICAPS),
 2023
Journal-ref: International Workshop of Hierarchical Planning (ICAPS), 2023
\\
 Real world applications as in industry and robotics need modelling rich and
diverse automated planning problems. Their resolution usually requires
coordinated and concurrent action execution. In several cases, these problems
are naturally decomposed in a hierarchical way and expressed by a Hierarchical
Task Network (HTN) formalism.
 HDDL, a hierarchical extension of the Planning Domain Definition Language
(PDDL), unlike PDDL 2.1 does not allow to represent planning problems with
numerical and temporal constraints, which are essential for real world
applications. We propose to fill the gap between HDDL and these operational
needs and to extend HDDL by taking inspiration from PDDL 2.1 in order to
express numerical and temporal expressions. This paper opens discussions on the
semantics and the syntax needed for a future HDDL 2.1 extension.
\\ ( https://arxiv.org/abs/2306.07353 ,  27kb)
------------------------------------------------------------------------------
\\
arXiv:2306.07429
Date: Mon, 12 Jun 2023 21:15:25 GMT   (15219kb,D)

Title: Explaining CLIP through Co-Creative Drawings and Interaction
Authors: Varvara Guljajeva and Mar Canet Sol\`a and Isaac Joseph Clarke
Categories: cs.AI cs.CV cs.CY
ACM-class: I.2.0; I.2.m
\\
 This paper analyses a visual archive of drawings produced by an interactive
robotic art installation where audience members narrated their dreams into a
system powered by CLIPdraw deep learning (DL) model that interpreted and
transformed their dreams into images. The resulting archive of prompt-image
pairs were examined and clustered based on concept representation accuracy. As
a result of the analysis, the paper proposes four groupings for describing and
explaining CLIP-generated results: clear concept, text-to-text as image,
indeterminacy and confusion, and lost in translation. This article offers a
glimpse into a collection of dreams interpreted, mediated and given form by
Artificial Intelligence (AI), showcasing oftentimes unexpected, visually
compelling or, indeed, the dream-like output of the system, with the emphasis
on processes and results of translations between languages, sign-systems and
various modules of the installation. In the end, the paper argues that proposed
clusters support better understanding of the neural model.
\\ ( https://arxiv.org/abs/2306.07429 ,  15219kb)
------------------------------------------------------------------------------
\\
arXiv:2306.07464
Date: Mon, 12 Jun 2023 23:42:08 GMT   (1839kb,D)

Title: Unlocking Sales Growth: Account Prioritization Engine with Explainable
 AI
Authors: Suvendu Jena, Jilei Yang, Fangfang Tan
Categories: cs.AI cs.LG stat.ML
Comments: 9 pages, 11 figures, 2 tables
\\
 B2B sales requires effective prediction of customer growth, identification of
upsell potential, and mitigation of churn risks. LinkedIn sales representatives
traditionally relied on intuition and fragmented data signals to assess
customer performance. This resulted in significant time investment in data
understanding as well as strategy formulation and under-investment in active
selling. To overcome this challenge, we developed a data product called Account
Prioritizer, an intelligent sales account prioritization engine. It uses
machine learning recommendation models and integrated account-level explanation
algorithms within the sales CRM to automate the manual process of sales book
prioritization. A successful A/B test demonstrated that the Account Prioritizer
generated a substantial +8.08% increase in renewal bookings for the LinkedIn
Business.
\\ ( https://arxiv.org/abs/2306.07464 ,  1839kb)
------------------------------------------------------------------------------
\\"""

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
    # if 'Title' in paper['metadata']:
    #     paper['metadata']['Title'] = ' '.join(paper['metadata']['Title'].strip())
    if 'Authors' in paper['metadata']:
        paper['metadata']['Authors'] = paper['metadata']['Authors'].strip().split(', ')

    papers.append(paper)
