# RFM-Based Customer Segmentation and Decision-Support Dashboard

## MSc Big Data Analytics Dissertation

This repository contains the analytical pipeline and interactive decision-support artefact developed for my MSc dissertation.

The project investigates customer segmentation using an extended RFM-based feature set and K-Means clustering on the UCI Online Retail dataset. A Gaussian Mixture Model (GMM) is also evaluated as a supporting probabilistic model to provide additional evidence about membership confidence and assignment uncertainty.

The final analytical artefact is implemented as an interactive web application using **Streamlit and Plotly**.

---

## Research Aim

The aim of this project is to develop and evaluate an interpretable customer segmentation framework based on RFM and additional behavioural features, and to translate the resulting customer groups into actionable business strategies through an interactive decision-support dashboard.

---

## Dataset

The project uses the **UCI Online Retail dataset**.

The raw dataset contains transaction-level records including:

- Invoice number
- Product code
- Product description
- Quantity
- Invoice date
- Unit price
- Customer ID
- Country

Following cleaning and customer-level feature engineering, the final modelling dataset contains:

- **4,338 unique customers**
- **7 clustering features**

---

## Data Cleaning

The data-cleaning pipeline includes:

- removal of records with missing Customer IDs;
- removal of cancelled invoices;
- removal of adjustment invoices where applicable;
- removal of zero or negative quantities;
- removal of zero or negative unit prices;
- duplicate removal;
- datetime conversion;
- creation of transaction-level total amount;
- validation of missing, invalid and infinite values.

The final cleaned transaction dataset is subsequently aggregated to customer level.

---

## Customer-Level Feature Engineering

The final clustering framework uses seven behavioural customer features.

### Core RFM Features

| Feature | Description |
|---|---|
| Recency | Number of days since the customer's most recent purchase |
| Frequency | Number of completed purchase invoices |
| Monetary | Total observed customer spending |

### Extended Behavioural Features

| Feature | Description |
|---|---|
| Average Order Value | Average financial value per purchase occasion |
| Basket Size | Average quantity purchased per transaction |
| Product Diversity | Number of unique products purchased |
| Total Quantity | Total quantity purchased across the analysis period |

`CustomerID` is retained only as an identifier and is not used as a clustering feature.

TransactionCount was investigated during feature engineering but excluded from the final clustering matrix because of its overlap with Frequency.

---

## Advanced Preprocessing

The final preprocessing pipeline includes:

1. validation of the customer-level feature dataset;
2. analysis of skewness and feature distributions;
3. `log1p` transformation of strongly skewed behavioural variables;
4. retention of genuine high-value and large-volume customers;
5. RobustScaler transformation using median and interquartile range.

Outliers were retained because extreme customer behaviour may represent commercially important customers rather than invalid observations.

The final modelling matrix contains:

**4,338 customers × 7 clustering features**

---

## K-Means Clustering

K-Means models were evaluated across multiple values of K.

The model-selection process considered:

- Elbow / within-cluster sum of squares;
- Silhouette Score;
- Davies-Bouldin Index;
- Calinski-Harabasz Index;
- random-seed stability;
- repeated subsampling stability;
- customer-profile interpretability;
- business usefulness.

K=2 provided a strong broad statistical benchmark, while **K-Means K=5** was retained as the final operational segmentation because it produced five stable and commercially interpretable customer groups.

---

## Final K-Means Customer Segments

| Segment | Customers | Customer Share | Monetary Contribution |
|---|---:|---:|---:|
| Dormant Occasional Customers | 661 | 15.24% | 2.69% |
| Active Regular Customers | 1,454 | 33.52% | 10.18% |
| High-Value Loyal Customers | 993 | 22.89% | 69.68% |
| Low-Value Infrequent Customers | 520 | 11.99% | 0.97% |
| High-Value Large-Order Buyers | 710 | 16.37% | 16.48% |

A key commercial finding is that the two high-value K-Means groups:

- High-Value Loyal Customers
- High-Value Large-Order Buyers

represent approximately **39.26% of customers** while generating approximately **86.16% of total observed Monetary value**.

---

## K-Means Assignment Confidence

Because clustering has no ground-truth customer labels, the project does not interpret uncertainty as classification error.

K-Means assignment confidence is examined using:

- individual Silhouette values;
- relative centroid margins;
- alternative nearest cluster;
- combined boundary criteria.

The final K-Means review group contains:

**541 customers — 12.47% of the customer population**

These customers are treated as boundary/review cases rather than misclassified customers.

---

## Gaussian Mixture Model

Gaussian Mixture Models were evaluated as a probabilistic alternative to K-Means.

The final supporting model is:

**GMM C5 Spherical**

GMM provides additional customer-level information including:

- maximum membership probability;
- second-highest membership probability;
- probability margin;
- normalised entropy;
- alternative component;
- membership confidence category.

The final GMM ambiguity criteria identify:

**259 customers — 5.97% of the customer population**

These represent ambiguous probabilistic memberships rather than classification errors.

---

## K-Means and GMM Comparison

### Common Validation Metrics

| Metric | K-Means K=5 | GMM C5 Spherical |
|---|---:|---:|
| Silhouette Score | 0.2512 | 0.2299 |
| Davies-Bouldin Index | 1.2230 | 1.3749 |
| Calinski-Harabasz Index | 1755.97 | 1587.50 |
| Mean Random-Seed ARI | 0.9999 | 0.9985 |
| Minimum Random-Seed ARI | 0.9996 | 0.9918 |
| Mean 80% Subsampling ARI | 0.9541 | 0.9610 |
| Minimum 80% Subsampling ARI | 0.9011 | 0.8898 |

### Cross-Model Assignment Similarity

- **Adjusted Rand Index:** 0.6289
- **Normalised Mutual Information:** 0.6512
- **Aligned customer agreement:** 81.40%

These values measure similarity between two unsupervised partitions and are not classification accuracy measures.

K-Means K=5 remains the **primary operational model**.

GMM C5 Spherical is retained as a **supporting probabilistic and uncertainty-analysis model**.

---

## Business Strategy Mapping

| Segment | Objective | Recommended Action | Target KPI | Priority |
|---|---|---|---|---|
| Dormant Occasional Customers | Reactivation | Low-cost win-back communication with time-limited personalised incentives | Reactivation rate | Medium |
| Active Regular Customers | Develop customer value | Cross-sell relevant products and encourage the next purchase through loyalty milestones | Purchase frequency | High |
| High-Value Loyal Customers | Retention | VIP recognition, priority service and early-access retention benefits | Revenue retention | Very High |
| Low-Value Infrequent Customers | Efficient nurture | Automated low-cost offers and product recommendations with controlled campaign spend | Conversion rate | Low |
| High-Value Large-Order Buyers | Protect order value | Order-value incentives, replenishment reminders and priority support for large purchases | Average order value | Very High |

The Large-Order segment represents observed large-order purchasing behaviour. The project does not assume that these customers are verified wholesale or B2B buyers.

---

# Interactive Decision-Support Dashboard

The final artefact is implemented using:

- Python
- Streamlit
- Plotly
- Pandas
- NumPy
- scikit-learn

The application consumes the final customer-level segmentation outputs generated by the analytical pipeline.

## Dashboard Pages

### 1. Executive Overview

Provides the main segmentation and commercial findings, including:

- total customers;
- total Monetary value;
- customer segments;
- high-value customer share;
- high-value Monetary contribution;
- K-Means review percentage;
- GMM ambiguity percentage;
- aligned model agreement;
- segment size and Monetary contribution;
- customer share versus Monetary share.

---

### 2. Customer Segment Profiles

Provides behavioural interpretation of the five K-Means segments using:

- segment size;
- customer share;
- Monetary contribution;
- operational priority;
- median behavioural features;
- selected-segment versus overall median comparison;
- all-segment behavioural heatmap;
- strategy and KPI information.

---

### 3. Customer Value & Revenue

Examines commercial importance using:

- Monetary contribution by segment;
- customer share versus Monetary share;
- Frequency versus Monetary customer scatter;
- Average Order Value versus Basket Size;
- high-value customer analysis;
- customer ranking;
- value-concentration analysis.

---

### 4. Customer Confidence & Explorer

Provides customer-level assignment evidence using:

#### K-Means

- confidence category;
- individual Silhouette;
- relative centroid margin;
- alternative K-Means segment.

#### GMM

- maximum probability;
- second probability;
- probability margin;
- entropy;
- alternative component;
- membership-confidence category.

The page also provides a searchable customer explorer and cross-model agreement evidence.

---

### 5. Model Comparison

Compares K-Means K=5 and GMM C5 Spherical using:

- Silhouette;
- Davies-Bouldin Index;
- Calinski-Harabasz Index;
- random-seed stability;
- subsampling stability;
- Adjusted Rand Index;
- Normalised Mutual Information;
- aligned customer agreement;
- K-Means versus aligned GMM overlap matrix;
- agreement by segment;
- uncertainty overlap.

WCSS, AIC and BIC are not presented as directly comparable metrics because they relate to different modelling objectives.

---

### 6. Strategy & Decision Support

The final management-focused page allows a user to select a segment and immediately view:

- customer size;
- customer share;
- Monetary contribution;
- value-concentration index;
- Monetary rank;
- behavioural profile;
- cross-model confidence evidence;
- management objective;
- recommended action;
- target KPI;
- operational priority;
- segment Value-Scale Matrix.

---

## Repository Structure

```text
RFM-Customer-Segmentation/
│
├── Data/
│   ├── Raw/
│   ├── Cleaned/
│   ├── Advance_Processed And Final/
│   └── dashboard data/
│
├── Notebooks/
│
├── dashboard/
│   ├── streamlit_app.py
│   ├── inspect_dashboard_data.py
│   ├── qa_dashboard.py
│   │
│   ├── components/
│   │   ├── data_loader.py
│   │   ├── metrics.py
│   │   ├── charts.py
│   │   └── styles.py
│   │
│   ├── pages/
│   │   ├── executive_overview.py
│   │   ├── segment_profiles.py
│   │   ├── customer_value.py
│   │   ├── confidence_explorer.py
│   │   ├── model_comparison.py
│   │   └── strategy_decision_support.py
│   │
│   └── assets/
│       └── screenshots/
│
├── .streamlit/
│   └── config.toml
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Running the Dashboard Locally

### 1. Clone the repository

```bash
git clone https://github.com/pushkarmopur/RFM-Customer-Segmentation.git
```

### 2. Enter the repository

```bash
cd RFM-Customer-Segmentation
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Start the dashboard

```bash
streamlit run dashboard/streamlit_app.py
```

The application will normally open locally at:

```text
http://localhost:8501
```

---

## Dashboard Quality Assurance

A reproducibility and QA script is provided:

```bash
python dashboard/qa_dashboard.py
```

The script verifies:

- final customer count;
- duplicate Customer IDs;
- missing Customer IDs;
- number of K-Means segments;
- high-value customer count;
- K-Means boundary/review count;
- GMM ambiguous count;
- aligned K-Means/GMM assignments;
- supporting-table dimensions;
- cross-model ARI;
- cross-model NMI.

The final validated dashboard dataset contains **4,338 unique customers with no duplicate or missing Customer IDs**.

---

## Reproducibility

The analytical workflow follows the sequence:

```text
UCI Online Retail Dataset
        ↓
Data Cleaning
        ↓
Customer-Level Feature Engineering
        ↓
Advanced Preprocessing
        ↓
K-Means Multi-K Evaluation
        ↓
K-Means K=5 Operational Segmentation
        ↓
K-Means Assignment Confidence
        ↓
GMM Model Evaluation
        ↓
GMM C5 Spherical
        ↓
Probabilistic Membership Analysis
        ↓
K-Means–GMM Comparison
        ↓
Business Profile Alignment
        ↓
Dashboard-Ready Customer Dataset
        ↓
Streamlit Decision-Support Dashboard
```

The repository contains the analytical notebooks, final data outputs and dashboard source code required to document and reproduce the main stages of the project.

---

## Key Findings

1. K-Means K=5 produces five stable and commercially interpretable customer groups.
2. High-Value Loyal Customers contribute the largest share of observed Monetary value.
3. The two high-value K-Means segments represent 39.26% of customers but generate 86.16% of observed Monetary value.
4. K-Means K=5 shows extremely high random-seed stability and strong subsampling stability.
5. GMM C5 Spherical also shows strong stability and provides additional probabilistic membership information.
6. K-Means and GMM achieve 81.40% aligned customer agreement.
7. The algorithms differ most strongly in their representation of large-order/high-value purchasing behaviour.
8. Assignment-confidence analysis provides a more cautious interpretation than treating all cluster assignments as equally certain.
9. The Streamlit application translates clustering outputs into customer profiles, commercial priorities and actionable management strategies.

---

## Important Interpretation Notes

- Clustering is unsupervised; there are no ground-truth customer segment labels.
- Model agreement is not classification accuracy.
- Boundary customers are not automatically misclassified customers.
- GMM membership probabilities describe model-based assignment confidence.
- Monetary represents observed customer spending across the dataset period and should not be interpreted as monthly revenue.
- Large-order behaviour does not establish wholesale or B2B status.
- K=2 remains an important broad statistical K-Means benchmark, while K=5 is used as the final operational segmentation.

---




---

## Author

**Pushkar Mopur**  
MSc Big Data Analytics  
Atlantic Technological University  
2026