# AirIQ Methodology & Analytical Framework
## AirIQ: Airbnb Pricing & Market Intelligence Using Apache PySpark

---

## 1. Data Hygiene, Invalid Records & Outlier Strategy

### A. Target Variable Normalization ($\text{log1p}(price)$)
Listing prices display strong right-skewness. To stabilize error variance and prevent numerical instability near zero, we apply the `log1p` transformation:
$$y_i = \text{log1p}(price_i) = \ln(1 + price_i)$$

Model training minimizes loss on $y_i$. For reporting metrics in original USD currency units, test set predictions $\hat{y}_i$ are transformed back via `expm1`:
$$\hat{price}_i = \text{expm1}(\hat{y}_i) = \exp(\hat{y}_i) - 1$$

### B. Segmentation: Invalid Records vs. Statistical Outliers

#### 1. Invalid Records (Removed from Processing)
- `price <= 0.0`
- `accommodates < 1`
- Malformed coordinates outside NYC geographic limits (`latitude < 40.4` or `latitude > 40.9`)

#### 2. Statistical Outliers (Retained & Flagged)
Rather than automatically dropping expensive listings or active properties:
- Calculate Interquartile Range per borough: $IQR = Q3 - Q1$.
- Add binary indicator flag: `is_high_price_outlier = when(price > Q3 + 1.5*IQR, 1).otherwise(0)`.
- Retain high-price listings in ML training and exploratory analysis to model luxury market segments.

### C. Conditional Imputation of Missing Rating Values
Missing ratings (`review_scores_rating = null`) are imputed using neighborhood medians computed strictly on the training set, accompanied by a binary flag (`rating_imputed_flag = 1`).

---

## 2. Demand Proxy Formalization (San Francisco Model)

Inside Airbnb datasets do not contain private transaction records. Demand indicators are computed using the academic **San Francisco Model**:

### A. Estimated Monthly Bookings Proxy ($B_m$)
Assuming guests submit reviews at an empirical review rate $R_{rate} \approx 0.50$ (50% review rate):
$$B_m = \frac{reviews\_per\_month}{0.50}$$

### B. Estimated Occupancy Rate Proxy ($Occ_{90}$)
$$Occ_{90} = \min\left(\frac{B_m \times 3}{90}, 1.0\right)$$

### C. Estimated Monthly Revenue Proxy ($Rev_m$)
$$Rev_m = B_m \times \max(minimum\_nights, 3) \times price$$

*Academic Requirement:* All UI components and reports visibly prefix these metrics with **[DEMAND PROXY]**.

---

## 3. PySpark MLlib Modeling Framework

```
                       +-----------------------------------+
                       |    Cleaned Spark DataFrame        |
                       +-----------------------------------+
                                         |
                                         v
                       +-----------------------------------+
                       | Train / Test Split (80% / 20%)    |
                       |        Seed = 42                  |
                       +-----------------------------------+
                                         |
                  +----------------------+----------------------+
                  | Fit Pipeline                                | Transform Only
                  v                                             v
+-----------------------------------+         +-----------------------------------+
|  Training Pipeline Fitting        |         |  Test Pipeline Execution          |
|  - StringIndexer (Train Vocab)    |         |  - Apply Indexer Metadata         |
|  - OneHotEncoder (Train Categories|         |  - Apply OneHotEncoder Vector     |
|  - VectorAssembler                |         |  - Apply VectorAssembler          |
|  - Fit Estimators (LR / RF / GBT) |         |  - Predict log1p(price)           |
+-----------------------------------+         +-----------------------------------+
                  |                                             |
                  v                                             v
+-----------------------------------+         +-----------------------------------+
|   Trained Pipeline Model          | -------->   Test Dataset Predictions        |
+-----------------------------------+         +-----------------------------------+
                                                                |
                                                                v
                                              +-----------------------------------+
                                              | Inverse expm1 Transformation      |
                                              | Compute USD Metrics (MAE, RMSE, R²|
                                              +-----------------------------------+
```

### A. Data Leakage Prevention Protocol
All transformations dependent on dataset statistics (category vocabulary indexing, median imputation values, vector scaling parameters) are fit **strictly on the 80% train split** inside a `pyspark.ml.Pipeline`. The test split is transformed passively via `PipelineModel.transform()`. Target-derived metrics are excluded from input feature vectors.

### B. Evaluated Models & Selection Strategy
1. **Simple Baseline Model:** Predicts target mean/median derived from training set ($R^2 = 0.0$ benchmark).
2. **Linear Regression (`LinearRegression`):** Ridge/Lasso regularized linear baseline.
3. **Random Forest Regressor (`RandomForestRegressor`):** Ensemble decision trees (`numTrees=100`, `maxDepth=8`).
4. **Gradient-Boosted Trees (`GBTRegressor`):** Iterative boosting model (`maxIter=50`, `maxDepth=6`).

Final model selection is strictly evidence-based, choosing the model with the highest test set $R^2$ and lowest test set USD RMSE and MAE.

---

## 4. Market Mispricing Intelligence Methodology

Using test set predictions inverse-transformed back to USD scale ($\hat{P}_i = \text{expm1}(\hat{y}_i)$):
$$\text{Residual } e_i = P_{actual, i} - \hat{P}_{predicted, i}$$
$$\text{Standardized Residual Z-Score } Z_i = \frac{e_i - \bar{e}}{\sigma_e}$$

- **Potentially Underpriced ($Z_i < -1.0$):**  
  Listing price is significantly below market expectation based on attributes.
- **Fair Market Value ($-1.0 \le Z_i \le 1.0$):**  
  Listing price aligns with market expectation.
- **Potentially Overpriced ($Z_i > 1.0$):**  
  Listing price is significantly above market expectation.
