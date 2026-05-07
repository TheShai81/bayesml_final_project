# README
## Bayesian Machine Learning (ADSP 32014) Final Project
### Latent Space Warriors - Bayesian Modeling of Market Volatility Following Political Communication Events

## Description

### Overview

We will investigate how political communication events influence short-term market volatility. The focus will be on modeling how markets respond to new political information such as speeches, interviews, or social media posts.

The project will analyze whether sentiment, emotional intensity, or potentially even the topics of each political communication are associated with changes in market volatility. Uncertainty will be measured using the VIX volatility index, which reflects expected volatility in the U.S. stock market (CBOE).

### Bayesian Framework

The objective is not to estimate a single fixed relationship between political communication and market volatility, but rather to estimate the posterior distribution of that relationship. For example, let xi be the sentiment score or linguistic features of political communication i and yi be the observed change in VIX following event i. A simple Bayesian model may be expressed as yi=+xi+𝜸zi+i for residual noise epsilon, sensitivity of market volatility to political communication features beta, control variable gamma, and baseline market behavior alpha. Bayesian inference treats beta as a distribution and observed data (political communications) is then used to update beliefs and obtain the posterior: P(|D) for observed communication features D (and potentially other market data, too).

### Methodology

- Event Collection
  - Collect time stamped political communication events such as speeches, interviews, and Truth Social/X posts
- Financial Data Collection
  - Collect financial time series data such as VIX index values and/or S&P 500 returns
- Text Processing and Feature Extraction
  - Apply NLP techniques to calculate sentiment scores, emotion, and/or topics (if we’re feeling ambitious)
  - These are our main explanatory variables
- Bayesian Modeling
  - Posterior distributions over model parameters can be estimated using maybe markov chain monte carlo methods as is usually the case with stock market data. I don’t think it’s taught in this class, but I’ve also read that variational inference is a common Bayesian approach.
  - We start with a hypothesis that beta (the effect of political communications on volatility) is normally distributed with mean 0 and standard deviation 1, meaning with no data we are starting with the belief that communications have NO effect on volatility. Then, as more data is observed, we updated that belief as to how beta is distributed. So, as an example, maybe we end up observing that |D ~ N(.8, .3), suggesting a positive effect on volatility and lower uncertainty.
- Features
  - Target variable: ΔVIX
  - Sentiment Scores(FinBERT): equals to the probability of positive minus the probability of negative
  - Uncertainty Score: How much the speech expresses uncertainty
  - Specific keywords: hawkish or dovish
  - Source: speech by trump or other politicians
  - Control variable: SPY return, CPI etc. 
- Evaluation and Analysis
  - Analyze posterior distributions over market sensitivity parameters, credible intervals for estimated effects, probability that certain features actually affect volatility.

---

## Trump Transcript Scraper

This script scrapes all transcript pages from the Senate Democrats Trump Transcript Archive.

- Iterates through all 22 archive pages
- Extracts every transcript link
- Visits each transcript page
- Extracts:
  - Transcript title
  - All <p> elements inside:
  - div.js-press-release.RawHTML.mb-5
  - Saves each transcript as a .txt file

### Output Format

Files are saved into:

`transcripts/`

Each filename follows:

`MMDDYYYY-#.txt`

Example:

```
04282026-0.txt
04282026-1.txt
```

Where:

MMDDYYYY = transcript date
`#` = transcript index for that date

### TXT File Structure

Each file contains:

```
<title_placeholder>

===== TRANSCRIPT BEGIN =====

<transcript-placeholder>
```

This delimiter (```===== TRANSCRIPT BEGIN =====```) makes later preprocessing easier.

### Requirements

Install dependencies:

`pip install requests beautifulsoup4`

### Running the Script

Place the Python script in a folder and run:

`python transcript_scraper.py`

The script will automatically create `transcripts/` in the same directory.

### Notes
- The scraper includes a 0.5-second delay between requests to avoid overloading the server.
- If a page fails, the scraper logs the error and continues.
- UTF-8 encoding is used for all transcript files.
- The script assumes the website structure remains consistent.