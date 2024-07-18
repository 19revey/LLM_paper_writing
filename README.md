# LLM paper writing

[![Demo Page](https://img.shields.io/badge/Project-Demo-FF4B4B?logo=streamlit)](https://llmpaperwriting.streamlit.app/)
[![GitHub issues open](https://img.shields.io/github/issues/19revey/LLM_paper_writing.svg?color=orange&label=Issues&logo=github)](https://github.com/19revey/LLM_paper_writing/issues) [![License: MIT](https://img.shields.io/badge/License-MIT-success.svg?logo)](https://github.com/19revey/LLM_paper_writing/blob/main/LICENSE)

<!-- [![arxiv paper](https://img.shields.io/badge/arXiv-Paper-B31B1B?logo=arxiv)](https://arxiv.org/abs/2402.06221) -->
<!-- [![PyPI Latest Release](https://img.shields.io/pypi/v/zlm.svg?label=PyPI&color=3775A9&logo=pypi)](https://pypi.org/project/zlm/) -->
<!-- [![PyPI Downloads](https://img.shields.io/pypi/dm/zlm.svg?label=PyPI%20downloads&color=blueviolet&target=blank)](https://pypi.org/project/zlm/) -->


This AI model is designed to assist in generating scholarly content for academic papers in the area of granular segregation. It embeds queries to retrieve highly similar text chunks from relevant papers, using these documents to craft responses.

**Warning:** References might not be included in the response. Ensure all content is properly cited for publication purposes.

<img src="demo.png" alt="Description of Image" width="500" height="400">



## Features
- **Paragraph Generation**: Automatically generates text for academic papers based on given prompts.
- **Customization**: Ability to fine-tune the model on specific topics or styles.
- **Free to use**: Powered by the latest Gemini 1.5 pro. While there is a limit on request frequency, it is currently free.
- **Secure**: The code is open source, and uploaded PDF files are stored on Astra DB for persistence.

<img src="https://i0.wp.com/gradientflow.com/wp-content/uploads/2023/10/newsletter87-RAG-simple.png?w=1464&ssl=1" alt="Description of Image" width="500" height="300">


## Getting Started

- The app is hosted on streamlit cloud: [https://llmpaperwriting.streamlit.app/](https://llmpaperwriting.streamlit.app/)

- To run it locally, start by configuring the necessary environmental variables:
```bash
  - GOOGLE_API_KEY
  - ASTRA_DB_ID
  - ASTRA_DB_APPLICATION_TOKEN=
```
- Next, clone this repository and launch the container:
```bash
    docker compose up
```