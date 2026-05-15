# Sequential Prompt Templates

DRAFT_PROMPT = """
You are an expert academic researcher. You are given a set of extracted summaries or texts from multiple recent scientific papers regarding the topic: "{topic}".

Your task is to write a comprehensive, well-structured literature review/survey paper draft. 
The review must include:
1. Introduction & Context
2. Categorization/Taxonomy of current approaches
3. In-depth analysis of methodologies
4. Open challenges and future directions

Ensure the tone is strictly academic, objective, and analytical. Do not add conversational fluff.

Source Paper Materials:
{papers_content}

Draft Review:
"""

POLISH_PROMPT = """
You are a senior editor and peer-reviewer for top-tier IEEE/ACM and Nature journals. 
Review the following draft of a literature survey paper. 

Your goals are:
1. Fix any logical gaps or abrupt transitions between paragraphs.
2. Enhance the academic vocabulary, grammar, and sentence variety (scientific polishing).
3. Ensure the formatting is cleanly structured using clear Markdown headers.

Original Draft:
{draft_content}

Polished & Refined Survey Paper:
"""
