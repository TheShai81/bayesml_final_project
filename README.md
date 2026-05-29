# Bayesian Machine Learning Final Project

## Latent Space Warriors: Political Communication and Market Volatility

This project studies whether political communication events are associated with short-term market volatility. The core dataset combines local transcript text features with market variables such as VIX changes and S&P 500 returns. The modeling workflow identifies latent volatility regimes, studies transitions between those regimes, and compares NLP-only predictors against models with financial controls.

The final report frames the project around a central question: can topics in Donald J. Trump political communications help explain short-term shifts in market volatility, beyond the persistence already present in financial markets? The project uses the VIX as the main uncertainty measure and treats volatility as a regime-switching process rather than a single linear response.

Raw transcript files live in `transcripts/`, which is ignored by Git. The tracked files are derived datasets, notebooks, and aggregate visual outputs.

## Research Design

The project combines three pieces:

- Political communication data: transcripts of speeches, interviews, press events, and public statements.
- Market data: VIX levels and changes, S&P 500 returns, lagged returns, and rolling volatility controls.
- Regime modeling: a latent-state approach that treats market volatility as moving between low-, medium-, and high-volatility states.

The report emphasizes that the goal is not only to estimate one fixed coefficient for the effect of political communication. Instead, the project asks how communication topics relate to uncertainty over market-regime transitions. This motivates the Bayesian extension, where transition effects are represented as posterior distributions rather than only point estimates.

## Workflow

```mermaid
flowchart TD
    A[Scrape Trump transcript archive] --> B[Clean transcript text]
    B --> C[Build transcript aggregate features]
    B --> D[Extract topic-mixture scores]
    E[Collect VIX and S&P 500 market data] --> F[Create finance controls]
    C --> G[Merge text and market data by date]
    D --> G
    F --> G
    G --> H[Model-ready dataset]
    H --> I[Gaussian HMM on absolute VIX changes]
    I --> J[Low, medium, high volatility regimes]
    J --> K[Transition model: current state plus NLP topics]
    K --> L[NLP-only logistic model]
    K --> M[NLP plus financial controls]
    L --> N[Coefficient and performance comparison]
    M --> N
    K --> O[Bayesian multinomial transition model]
    O --> P[Posterior intervals and probability effects]
    N --> Q[Visualizations and final interpretation]
    P --> Q
```

## Data and Methodology

### Transcript Data

The transcript corpus is collected from the Senate Democrats Trump Transcript Archive. Each file includes a title and transcript body separated by a delimiter, which makes downstream parsing easier. The current local corpus contains 423 transcript files, with 403 having known dates. For GitHub hygiene, the raw `transcripts/` folder is ignored, while aggregate transcript features are exported to `final_data/transcript_aggregate_features.csv`. The broader text preprocessing and topic-modeling workspace is available in the [Text Data Preprocessing & Topic Modeling Google Drive folder](https://drive.google.com/drive/folders/1f6mUv6malpXvKc_uSYXvjHuDcNSRH-77?dmr=1&ec=wgc-drive-%5Bmodule%5D-goto).

The transcript analysis uses cleaned aggregate text features, keyword themes, and topic-mixture scores. The report describes these text features as the political communication inputs that condition downstream volatility-transition models. In the current modeling notebooks, the main predictors are the topic score columns, represented as `nmf_topic_*_score` features and mapped to interpretable political themes such as economy/taxes/tariffs, media attacks, foreign policy, and patriotism.

### Financial Data

The financial side of the project uses daily VIX observations as the main proxy for market uncertainty and S&P 500 returns as market controls. The raw market-data workspace is available in the [S&P 500 and VIX Data Google Drive folder](https://drive.google.com/drive/folders/1_K4H14WJYbNM5v2hkNpHWIKP8EeOJlyG?dmr=1&ec=wgc-drive-%5Bmodule%5D-goto). The modeling target is based on absolute daily VIX changes, because the project is interested in volatility intensity rather than only the direction of the VIX move.

The finance notebook also derives market-style fields such as forward S&P 500 returns, drawdowns, realized volatility, risk-off day indicators, and VIX shock flags. These features support interpretation and provide additional context for the volatility-regime results. The original finance preprocessing Colab is linked here: [Finance Data Preprocessing](https://colab.research.google.com/drive/17MHytI5UC-8EwQ7GNwxKkvX2HS3CQCEg).

### HMM Regime Discovery

The first modeling step fits a Gaussian Hidden Markov Model to absolute VIX changes. The HMM assumes that observed volatility behavior is generated by an unobserved market state. The transition matrix workflow is also documented in the [Volatility Transition Matrix Colab](https://colab.research.google.com/drive/1MeFJkOG4JfWSrf5Axli-SrKsnv5XRS34). After fitting, the states are reordered by their learned emission means so that:

- State 0 corresponds to low volatility.
- State 1 corresponds to medium volatility.
- State 2 corresponds to high volatility.

This allows the model to discover volatility regimes probabilistically rather than relying on manually chosen VIX thresholds.

### Transition Modeling

After inferring the latent volatility states, the project models next-state transitions using multinomial logistic regression. The transition model predicts the next volatility state from:

- the current inferred volatility state,
- NLP topic scores from the political communication corpus,
- and, in the full model, financial controls such as lagged VIX, S&P 500 returns, and rolling volatility.

This setup tests whether political communication features provide explanatory value beyond the strong persistence already present in financial volatility.

Before fitting the transition models, predictor columns are imputed and standardized so coefficient comparisons are more meaningful. The feature scaling workflow is documented in the [Feature Scaling & Standardizing Colab](https://colab.research.google.com/drive/1WqfTmfDI324nrgu74EDrwTE4gIRZfpev).

### Bayesian Extension

The Bayesian extension replaces point-estimated transition coefficients with posterior distributions estimated in PyMC. This gives a more honest uncertainty story: the model can report posterior means, highest-density credible intervals, and probabilities that a topic effect is positive.

The report's main interpretation is that topic effects are directionally suggestive in the NLP-only models, but uncertainty is substantial and the effects shrink when financial controls are added.

## Repository Structure

```text
.
├── final_data/
│   ├── model_ready_dataset.csv
│   ├── finance_enriched_dataset.csv
│   └── transcript_aggregate_features.csv
├── notebooks/
│   ├── baseline_model.ipynb
│   ├── extension_model.ipynb
│   ├── transcript_visualizations.ipynb
│   ├── finance_results.ipynb
│   ├── visualization_results.ipynb
│   ├── prob_effect_comparison.csv
│   └── assets/
├── src/
│   └── transcript_scraper.py
└── transcripts/        # ignored by Git
```

## Data Outputs

- `final_data/model_ready_dataset.csv`: main modeling dataset with NLP topic features, VIX variables, S&P 500 controls, and standardized model inputs from the [feature scaling workflow](https://colab.research.google.com/drive/1WqfTmfDI324nrgu74EDrwTE4gIRZfpev).
- `final_data/finance_enriched_dataset.csv`: finance-style derived fields, including forward returns, drawdowns, realized volatility, VIX shock flags, and risk-off indicators from the [finance preprocessing workflow](https://colab.research.google.com/drive/17MHytI5UC-8EwQ7GNwxKkvX2HS3CQCEg).
- `final_data/transcript_aggregate_features.csv`: transcript-level aggregate features only. This file does not include raw transcript bodies or token lists.

## Transcript Visualizations

Notebook: `notebooks/transcript_visualizations.ipynb`  
Figures: `notebooks/assets/transcript_visualizations/`

This notebook visualizes the transcript corpus using aggregate statistics. It avoids printing raw transcript bodies and exports only aggregate features.

Current transcript summary:

- 423 transcript files.
- 403 transcripts with known dates.
- Date range: 2025-05-24 to 2026-04-29.
- 825,492 cleaned words.
- Median transcript length: 1,431 cleaned words.

Generated figures:

**Transcript count and total words by month**

![Transcript volume by month](notebooks/assets/transcript_visualizations/monthly_transcript_volume.png)

**Broad keyword themes and share of transcripts mentioning each theme**

![Transcript theme keyword prevalence](notebooks/assets/transcript_visualizations/theme_keyword_prevalence.png)

**Theme mentions per 1,000 words over time**

![Monthly transcript theme intensity](notebooks/assets/transcript_visualizations/monthly_theme_intensity.png)

**Finance-related keyword counts**

![Finance keyword mentions in transcripts](notebooks/assets/transcript_visualizations/finance_keyword_mentions.png)

**Theme co-occurrence across transcripts**

![Transcript theme co-occurrence heatmap](notebooks/assets/transcript_visualizations/theme_cooccurrence_heatmap.png)

## Finance Visualizations

Notebook: `notebooks/finance_results.ipynb`  
Figures: `notebooks/assets/finance_results/`

This notebook derives market-style results from the model-ready data. It adds forward S&P 500 returns, VIX forward changes, drawdowns, realized volatility, VIX shock flags, and risk-off day indicators.

Current finance summary:

- 183 market observations.
- S&P 500 total return over the sample: about 20.5%.
- Maximum S&P 500 drawdown: about -9.1%.
- Average VIX: 18.40.
- Maximum VIX: 31.05.

Generated figures:

**S&P 500 level, VIX level, and S&P 500 drawdown**

![S&P 500, VIX, and drawdown](notebooks/assets/finance_results/price_vix_drawdown_view.png)

**Average forward S&P 500 returns after low-, medium-, and high-VIX-move days**

![Forward returns by VIX-move regime](notebooks/assets/finance_results/forward_returns_by_regime.png)

**Event-study view around top-decile absolute VIX moves**

![VIX shock event study](notebooks/assets/finance_results/vix_shock_event_study.png)

**Relationship between S&P 500 daily returns and daily VIX changes**

![S&P 500 returns versus VIX changes](notebooks/assets/finance_results/sp500_vix_leverage_scatter.png)

## Model Result Visualizations

Primary notebooks:

- `notebooks/baseline_model.ipynb`
- `notebooks/extension_model.ipynb`
- `notebooks/visualization_results.ipynb`

Figures:

- `notebooks/assets/`
- `notebooks/assets/additional_visualizations/`

The baseline notebook fits a three-state volatility-regime model and then uses transition classifiers to test whether NLP topic features help predict next-period volatility states. The extension notebook fits a Bayesian multinomial transition model to quantify uncertainty in those effects. The visualization notebook creates presentation-ready plots from the model outputs.

Generated model-result figures:

**VIX over time colored by inferred volatility state**

![VIX over time with inferred volatility state](notebooks/assets/vix_over_time_w_state.png)

**Compact timeline of inferred volatility regimes**

![Regime timeline ribbon](notebooks/assets/additional_visualizations/regime_timeline_ribbon.png)

**Strongest NLP predictors of high-volatility transitions**

![High-volatility NLP predictors](notebooks/assets/high_volatility_predictors.png)

**Strongest NLP predictors of low-volatility transitions**

![Low-volatility NLP predictors](notebooks/assets/low_volatility_predictors.png)

**Coefficient stability after adding financial controls**

![NLP coefficient stability after controls](notebooks/assets/nlp_after_controls_stability_plot.png)

**HMM transition probability heatmap**

![Transition matrix heatmap](notebooks/assets/additional_visualizations/transition_matrix_heatmap.png)

**NLP topic coefficients for high-volatility transitions**

![Topic coefficient lollipop plot](notebooks/assets/additional_visualizations/topic_coefficient_lollipop.png)

**Topic effects before and after financial controls**

![Controls dumbbell plot](notebooks/assets/additional_visualizations/controls_dumbbell_plot.png)

**Bayesian probability-effect intervals**

![Bayesian uncertainty intervals](notebooks/assets/additional_visualizations/bayesian_uncertainty_intervals.png)

**Probability changes with and without financial controls**

![Probability change comparison](notebooks/assets/additional_visualizations/probability_change_comparison.png)

**Average topic score by volatility regime**

![Topic state composition heatmap](notebooks/assets/additional_visualizations/topic_state_composition_heatmap.png)

**NLP-only versus full-model confusion matrices**

![Confusion matrix comparison](notebooks/assets/additional_visualizations/confusion_matrix_comparison.png)

**Largest VIX-move days annotated on the VIX series**

![Annotated high VIX events](notebooks/assets/additional_visualizations/annotated_high_vix_events.png)

**Accuracy, macro F1, high-state precision, and high-state recall**

![Model performance comparison](notebooks/assets/additional_visualizations/model_performance_comparison.png)

### Key model findings:

- The regime model separates low-, medium-, and high-volatility movement days.
- High volatility is persistent once entered.
- NLP-only transition models show suggestive topic effects for high-volatility transitions.
- Adding financial controls improves classification performance and shrinks many NLP topic effects.
- The Bayesian extension shows substantial uncertainty around most topic effects.

## Results Interpretation

The report's overall finding is that volatility-regime persistence is the dominant force in the models. Current volatility state is consistently the strongest predictor of next-period volatility state, which matches the financial intuition that volatility clusters over time.

Political communication topics still appear to contain some information. In the NLP-only transition models, topics such as patriotism, media attacks, economy/taxes/tariffs, and environment show positive associations with transitions into the high-volatility state. However, these effects are modest compared with the effect of the current volatility regime.

When financial controls are added, many NLP coefficients shrink toward zero. This suggests that part of the topic signal overlaps with broader market conditions, especially lagged VIX behavior and S&P 500 movements. The Bayesian extension reinforces this interpretation: posterior means for some topic effects remain positive, but credible intervals often include zero.

In short, the project supports a cautious conclusion: political communication may provide incremental information about short-term volatility-regime dynamics, but market persistence and broader financial conditions remain the stronger drivers.

## Transcript Scraper

Script: `src/transcript_scraper.py`

The scraper collects transcript pages from the Senate Democrats Trump Transcript Archive and saves each transcript as a `.txt` file under `transcripts/`.

Each transcript file follows this structure:

```text
<title>

===== TRANSCRIPT BEGIN =====

<transcript body>
```

The `transcripts/` directory is listed in `.gitignore`, so raw transcript files are not tracked by default.

## Requirements

The notebooks use common Python data-science packages:

```bash
pip install pandas numpy matplotlib scikit-learn jupyter
```

The baseline model notebook also uses:

```bash
pip install hmmlearn
```

The Bayesian extension notebook uses:

```bash
pip install pymc arviz pytensor
```

The scraper uses:

```bash
pip install requests beautifulsoup4
```

## References Mentioned in the Report

- Marinč, Massoud, Ichev, and Valentinčič, "Presidential candidates linguistic tone: The impact on the financial markets," *Economics Letters*, 2021.
- Cboe VIX volatility products and VIX reference material.
- Senate Democratic Caucus Trump Transcript Archive.
- Yahoo Finance historical S&P 500 data.
- `hmmlearn` documentation for Gaussian HMM estimation.
- PyMC documentation and PyMC probabilistic programming framework reference.

## Reproducing the Current Outputs

Run notebooks from the `notebooks/` directory:

```bash
jupyter nbconvert --to notebook --execute transcript_visualizations.ipynb --inplace
jupyter nbconvert --to notebook --execute finance_results.ipynb --inplace
jupyter nbconvert --to notebook --execute visualization_results.ipynb --inplace
```

The Bayesian extension can take much longer because it samples posterior distributions with PyMC.
