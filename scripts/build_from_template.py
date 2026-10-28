import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

TEMPLATE_PATH = "/home/adityap/Downloads/final ppt.pptx"
OUT_PATHS = [
    "/home/adityap/Desktop/PR/BDALAB/airbnb-price-intelligence/presentation/AirIQ_BDA_Lab_Presentation.pptx",
    "/home/adityap/Desktop/AirIQ_BDA_Lab_Presentation.pptx",
    "/home/adityap/Desktop/AIRIQ_CORE_CODE/05_PRESENTATION_GENERATOR/AirIQ_BDA_Lab_Presentation.pptx"
]

def set_text(shape, text, font_size=None, bold=None, color=None):
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    if not tf.paragraphs:
        p = tf.add_paragraph()
    else:
        p = tf.paragraphs[0]
        # clear remaining paragraphs
        for extra_p in tf.paragraphs[1:]:
            extra_p.text = ""
    p.text = text
    if font_size is not None:
        p.font.size = Pt(font_size)
    if bold is not None:
        p.font.bold = bold
    if color is not None:
        p.font.color.rgb = color

def set_paragraphs(shape, paragraphs_list, font_size=None, color=None):
    if not shape.has_text_frame:
        return
    tf = shape.text_frame
    # Clear existing
    for i, p in enumerate(tf.paragraphs):
        p.text = ""
    
    for i, text in enumerate(paragraphs_list):
        if i < len(tf.paragraphs):
            p = tf.paragraphs[i]
        else:
            p = tf.add_paragraph()
        p.text = text
        if font_size is not None:
            p.font.size = Pt(font_size)
        if color is not None:
            p.font.color.rgb = color

def build_presentation():
    prs = Presentation(TEMPLATE_PATH)
    
    # =========================================================================
    # SLIDE 1: Title Slide
    # =========================================================================
    s1 = prs.slides[0]
    for s in s1.shapes:
        if s.name == "Course label":
            set_text(s, "BIG DATA ANALYTICS  |  PROJECT PRESENTATION")
        elif s.name == "Text 0":
            set_text(s, "AirIQ: Airbnb Price Intelligence", font_size=32, bold=True)
        elif s.name == "Subtitle":
            set_text(s, "Multi-city rental price prediction & spatial analytics using Apache Spark MLlib and Apache Cassandra", font_size=15)
        elif s.name == "Presenter details":
            set_paragraphs(s, [
                "Ramdeobaba University, Nagpur",
                "Course: Big Data Analytics",
                "Presented by: Aditya Raju Pidurkar-40",
                "                          Nidhi Singh-15"
            ])
        elif s.name == "Motif caption":
            set_text(s, "MARKET COVERAGE")
        elif s.name == "Title motif label 1":
            set_text(s, "London")
        elif s.name == "Title motif label 2":
            set_text(s, "Paris")
        elif s.name == "Title motif label 3":
            set_text(s, "Tokyo")
        elif s.name == "Title motif label 4":
            set_text(s, "Mumbai")
        elif s.name == "Title motif label 5":
            set_text(s, "Bengaluru")

    # =========================================================================
    # SLIDE 2: Problem Statement (01 INTRODUCTION)
    # =========================================================================
    s2 = prs.slides[1]
    for s in s2.shapes:
        if s.name == "Section tag":
            set_text(s, "01  INTRODUCTION")
        elif s.name == "Text 0":
            set_text(s, "Problem statement")
        elif s.name == "Heading Background":
            set_text(s, "Background")
        elif s.name == "Text Background":
            set_text(s, "Short-term rental platforms such as Airbnb accumulate hundreds of thousands of listings with volatile, hyper-local nightly rates.")
        elif s.name == "Heading Problem":
            set_text(s, "Problem")
        elif s.name == "Text Problem":
            set_text(s, "Setting fair prices manually causes empty rooms or lost revenue, single-machine tools crash on 200,000+ spatial rows, and official portals cover 0 Indian cities.")
        elif s.name == "Heading Approach":
            set_text(s, "Approach")
        elif s.name == "Text Approach":
            set_text(s, "Use Apache Spark MLlib and Cassandra to process 224,098 listings in parallel, predicting fair rates in native local currencies (₹, ¥, £, €).")

    # =========================================================================
    # SLIDE 3: Objectives and Scope (01 INTRODUCTION)
    # =========================================================================
    s3 = prs.slides[2]
    for s in s3.shapes:
        if s.name == "Section tag":
            set_text(s, "01  INTRODUCTION")
        elif s.name == "Text 0":
            set_text(s, "Objectives and scope")
        elif s.name == "Objective 1":
            set_text(s, "Ingest 224,098 listings across 7 global hubs and 2 real Indian metros (Mumbai, Bengaluru).")
        elif s.name == "Objective 2":
            set_text(s, "Clean currency symbols and standardize a USD baseline for homoscedastic regression.")
        elif s.name == "Objective 3":
            set_text(s, "Train a 45-tree PySpark MLlib Random Forest Regressor across 6 core physical features.")
        elif s.name == "Objective 4":
            set_text(s, "Store partitioned spatial records and macro statistics in Apache Cassandra (port 9042).")
        elif s.name == "Objective 5":
            set_text(s, "Provide interactive price predictions and zero-lag Leaflet marker clustering in native currencies.")
        elif s.name == "Scope heading 1":
            set_text(s, "Within scope")
        elif s.name == "Scope list 1":
            set_paragraphs(s, [
                "Multi-market pricing in native local currencies (₹, ¥, £, €)",
                "Interactive marker clustering without browser DOM lag",
                "Sub-millisecond NoSQL reads via partitioned Cassandra keys"
            ])
        elif s.name == "Scope heading 2":
            set_text(s, "Outside scope")
        elif s.name == "Scope list 2":
            set_paragraphs(s, [
                "In-app booking payment and transaction processing",
                "Host identity and guest ID verification",
                "Surge pricing adjustments based on real-time live weather"
            ])

    # =========================================================================
    # SLIDE 4: Technology Stack (02 METHODOLOGY)
    # =========================================================================
    s4 = prs.slides[3]
    for s in s4.shapes:
        if s.name == "Section tag":
            set_text(s, "02  METHODOLOGY")
        elif s.name == "Text 0":
            set_text(s, "Technology stack")
        elif s.name == "Name Apache Hadoop 3.2.4":
            set_text(s, "Apache Spark 4.2")
        elif s.name == "Role Apache Hadoop 3.2.4":
            set_text(s, "Distributed in-memory compute engine for parallel DataFrame transformations and MLlib regression.")
        elif s.name == "Name HDFS":
            set_text(s, "Apache Cassandra 4.1")
        elif s.name == "Role HDFS":
            set_text(s, "Distributed masterless NoSQL database providing sub-millisecond queries via partitioned keyspaces.")
        elif s.name == "Name MapReduce":
            set_text(s, "PySpark MLlib")
        elif s.name == "Role MapReduce":
            set_text(s, "Parallel Random Forest regressor with VectorAssembler trained on 224,098 listings.")
        elif s.name == "Name Hadoop Streaming":
            set_text(s, "FastAPI (Python)")
        elif s.name == "Role Hadoop Streaming":
            set_text(s, "Asynchronous ASGI microservice on port 8001 executing in-memory Spark tree traversal in < 15ms.")
        elif s.name == "Name YARN":
            set_text(s, "React 19 + Vite")
        elif s.name == "Role YARN":
            set_text(s, "Modern reactive frontend with React-Leaflet and Leaflet MarkerCluster for zero DOM lag.")
        elif s.name == "Name Python":
            set_text(s, "Python 3.14")
        elif s.name == "Role Python":
            set_text(s, "Core programming language powering data pipelines, CQL drivers, and automated evaluation.")

    # =========================================================================
    # SLIDE 5: System Architecture and Workflow (02 METHODOLOGY)
    # =========================================================================
    s5 = prs.slides[4]
    for s in s5.shapes:
        if s.name == "Section tag":
            set_text(s, "02  METHODOLOGY")
        elif s.name == "Text 0":
            set_text(s, "System architecture and workflow")
        elif s.name == "Stage 1 name":
            set_text(s, "Raw Datasets")
        elif s.name == "Stage 1 detail":
            set_text(s, "224,098 listings")
        elif s.name == "Stage 2 name":
            set_text(s, "PySpark ETL")
        elif s.name == "Stage 2 detail":
            set_text(s, "Clean & normalize")
        elif s.name == "Stage 3 name":
            set_text(s, "MLlib Pipeline")
        elif s.name == "Stage 3 detail":
            set_text(s, "Random Forest")
        elif s.name == "Stage 4 name":
            set_text(s, "Cassandra Sink")
        elif s.name == "Stage 4 detail":
            set_text(s, "NoSQL partitions")
        elif s.name == "Stage 5 name":
            set_text(s, "FastAPI Engine")
        elif s.name == "Stage 5 detail":
            set_text(s, "In-memory trees")
        elif s.name == "Stage 6 name":
            set_text(s, "React Frontend")
        elif s.name == "Stage 6 detail":
            set_text(s, "Maps & pricing")
        elif s.name == "Lane input label":
            set_text(s, "Storage: Local FS / HDFS")
        elif s.name == "Lane execution label":
            set_text(s, "Execution: PySpark 4.2 MLlib & Uvicorn ASGI")
        elif s.name == "Lane output label":
            set_text(s, "Storage: Apache Cassandra (Port 9042)")
        elif s.name == "Flow text":
            set_paragraphs(s, [
                "Conceptual flow",
                "input CSVs → PySpark ETL → MLlib Random Forest → Cassandra sink → FastAPI & React"
            ])
        elif s.name == "Export text":
            set_paragraphs(s, [
                "Output serving",
                "Trained 45-tree model and Cassandra partitioned tables serve real-time predictions in < 15ms."
            ])

    # =========================================================================
    # SLIDE 6: Implementation and Execution (02 METHODOLOGY)
    # =========================================================================
    s6 = prs.slides[5]
    for s in s6.shapes:
        if s.name == "Section tag":
            set_text(s, "02  METHODOLOGY")
        elif s.name == "Text 0":
            set_text(s, "Implementation and execution")
        elif s.name == "Environment table" and s.has_table:
            tbl = s.table
            rows_data = [
                ("Platform", "Linux (x86_64)"),
                ("Framework", "Apache Spark 4.2 + Apache Cassandra 4.1"),
                ("Language", "Python 3.14 + React 19 (JavaScript)"),
                ("Execution", "Distributed Spark Worker & FastAPI ASGI (Uvicorn)"),
                ("Datasets Input", "Inside Airbnb (7 hubs) + DoorstepAnalytics (India)"),
                ("Storage Sink", "Cassandra keyspace airbnb_intelligence (port 9042)")
            ]
            for r_idx, (col0, col1) in enumerate(rows_data):
                tbl.rows[r_idx].cells[0].text = col0
                tbl.rows[r_idx].cells[1].text = col1
        elif s.name == "Step 1":
            set_text(s, "Load 213,299 Inside Airbnb & 10,834 DoorstepAnalytics CSVs into PySpark")
        elif s.name == "Step 2":
            set_text(s, "Clean prices, impute null ratings with medians, and derive price_usd")
        elif s.name == "Step 3":
            set_text(s, "Train 45-tree Random Forest Regressor (max depth 9) on 80% train split")
        elif s.name == "Step 4":
            set_text(s, "Batch-insert city summaries and spatial listings into Apache Cassandra")
        elif s.name == "Step 5":
            set_text(s, "Launch FastAPI backend on port 8001 with pre-loaded in-memory Spark trees")

    # =========================================================================
    # SLIDE 7: Dataset Distribution Across Markets (03 RESULTS)
    # =========================================================================
    s7 = prs.slides[6]
    for s in s7.shapes:
        if s.name == "Section tag":
            set_text(s, "03  RESULTS")
        elif s.name == "Text 0":
            set_text(s, "Observed dataset distribution across markets")
        elif s.name == "Rating counts table" and s.has_table:
            tbl = s.table
            rows_data = [
                ("Market Destination", "Listings", "Average Rate (Local Currency)"),
                ("London (United Kingdom)", "59,690", "£227.95 GBP"),
                ("Paris (France)", "43,286", "€299.30 EUR"),
                ("Rome (Italy)", "33,846", "€237.18 EUR"),
                ("Tokyo (Japan)", "33,535", "¥27,207.16 JPY"),
                ("New York City (USA)", "19,299", "$280.60 USD"),
                ("Bengaluru & Mumbai (India)", "10,834", "₹2,783 / ₹5,706 INR")
            ]
            for r_idx, (c0, c1, c2) in enumerate(rows_data):
                tbl.rows[r_idx].cells[0].text = c0
                tbl.rows[r_idx].cells[1].text = c1
                tbl.rows[r_idx].cells[2].text = c2
        elif s.name == "Table note":
            set_text(s, "Total = 224,098 verified listings across 7 official Inside Airbnb global hubs and 2 real Indian metros.")

    # =========================================================================
    # SLIDE 8: Analysis of the Results (03 RESULTS)
    # =========================================================================
    s8 = prs.slides[7]
    for s in s8.shapes:
        if s.name == "Section tag":
            set_text(s, "03  RESULTS")
        elif s.name == "Text 0":
            set_text(s, "Analysis of the results")
        elif s.name == "Statistic 1":
            set_text(s, "224,098")
        elif s.name == "Statistic label 1":
            set_paragraphs(s, ["Total listings", "Ingested & modeled"])
        elif s.name == "Statistic 2":
            set_text(s, "35.1%")
        elif s.name == "Statistic label 2":
            set_paragraphs(s, ["Error reduction", "vs OLS baseline"])
        elif s.name == "Statistic 3":
            set_text(s, "$209.98")
        elif s.name == "Statistic label 3":
            set_paragraphs(s, ["Test RMSE", "44,272 test records"])
        elif s.name == "Statistic 4":
            set_text(s, "0.3659")
        elif s.name == "Statistic label 4":
            set_paragraphs(s, ["R² Score", "45 trees, depth 9"])
        elif s.name == "Interpretation heading":
            set_text(s, "Interpretation")
        elif s.name == "Interpretation list":
            set_paragraphs(s, [
                "The Random Forest model explains 36.6% of global price variance across 9 diverse cities, reducing RMSE by 35.1% over standard OLS baselines ($323.37).",
                "Accommodates (guest capacity) and bedrooms are the primary price drivers, accounting for 62.2% of total feature importance.",
                "Native currency calibration ensures domestic purchasing power (₹ INR in India, ¥ JPY in Japan) is preserved without exchange distortion."
            ])

    # =========================================================================
    # SLIDE 9: Validation and System Deployment (03 RESULTS)
    # =========================================================================
    s9 = prs.slides[8]
    for s in s9.shapes:
        if s.name == "Section tag":
            set_text(s, "03  RESULTS")
        elif s.name == "Text 0":
            set_text(s, "System validation and deployment metrics")
        elif s.name == "Job counters table" and s.has_table:
            tbl = s.table
            rows_data = [
                ("AirIQ Component Summary", "Status / Value"),
                ("FastAPI Backend Status", "Active (Port 8001)"),
                ("Apache Cassandra Cluster", "UN - Up/Normal (Port 9042)"),
                ("Spark MLlib Trees Loaded", "45 Trees (In-Memory)"),
                ("Prediction Latency", "< 15 ms per request"),
                ("Map Pin Clustering", "Zero DOM lag (react-leaflet-cluster)"),
                ("Indian Metros Covered", "Mumbai & Bengaluru (Real INR)"),
                ("Total Listings Ingested", "224,098 records")
            ]
            for r_idx, (col0, col1) in enumerate(rows_data):
                tbl.rows[r_idx].cells[0].text = col0
                tbl.rows[r_idx].cells[1].text = col1
        elif s.name == "Observations heading":
            set_text(s, "Key system validations")
        elif s.name == "Observation 1":
            set_text(s, "All 14,000 spatial coordinates were validated to fall within land boundaries (no water pins).")
        elif s.name == "Observation 2":
            set_text(s, "FastAPI pre-loads decision tree nodes into memory, avoiding PySpark JVM execution overhead during inference.")
        elif s.name == "Observation 3":
            set_text(s, "Leaflet marker clustering dynamically aggregates hundreds of dense pins into interactive badges.")
        elif s.name == "Verification text":
            set_paragraphs(s, [
                "Deployment verification",
                "The full stack (Cassandra + FastAPI + React) runs smoothly on Kali Linux with sub-second response times."
            ])

    # =========================================================================
    # SLIDE 10: Conclusion and Future Scope (04 CONCLUSION)
    # =========================================================================
    s10 = prs.slides[9]
    for s in s10.shapes:
        if s.name == "Section tag":
            set_text(s, "04  CONCLUSION")
        elif s.name == "Text 0":
            set_text(s, "Conclusion and future scope")
        elif s.name == "Conclusion heading":
            set_text(s, "Conclusion")
        elif s.name == "Conclusion text":
            set_text(s, "The project successfully demonstrates how 224,098 short-term rental listings can be harmonized, stored, and modeled using Apache Spark MLlib, Cassandra NoSQL, and React 19 to provide accurate, multi-currency price intelligence.")
        elif s.name == "Outcomes heading":
            set_text(s, "Learning outcomes")
        elif s.name == "Outcomes list":
            set_paragraphs(s, [
                "Distributed data engineering with PySpark DataFrames and Data Types",
                "PySpark MLlib Random Forest Regressor and VectorAssembler pipelines",
                "Apache Cassandra partitioned keyspaces and CQL query optimization",
                "Multi-currency normalization and de-normalization strategies",
                "Full-stack integration using async FastAPI and Leaflet marker clustering"
            ])
        elif s.name == "Future scope heading":
            set_text(s, "Future scope")
        elif s.name == "Future scope list":
            set_paragraphs(s, [
                "Integrate Apache Kafka for real-time streaming of calendar price changes.",
                "Add Deep Learning (CNNs / Vision Transformers) to score interior listing photos.",
                "Incorporate NLP sentiment analysis on guest reviews for pricing multipliers.",
                "Deploy automated CI/CD retraining using MLflow on quarterly Inside Airbnb releases."
            ])

    # =========================================================================
    # SLIDE 11: References (04 CONCLUSION)
    # =========================================================================
    s11 = prs.slides[10]
    for s in s11.shapes:
        if s.name == "Section tag":
            set_text(s, "04  CONCLUSION")
        elif s.name == "Text 0":
            set_text(s, "References")
        elif s.name == "Reference 1":
            set_text(s, "Apache Spark Documentation, \"MLlib: Main Guide - Random Forest Regression,\" spark.apache.org/docs/latest/ml-classification-regression.html, 2026.")
        elif s.name == "Reference 2":
            set_text(s, "Apache Cassandra Documentation, \"Architecture & Data Modeling with Partition Keys,\" cassandra.apache.org/doc/latest/, 2026.")
        elif s.name == "Reference 3":
            set_text(s, "Inside Airbnb, \"Adding data to the debate - Open Housing and Rental Data,\" insideairbnb.com/get-the-data/, 2026.")
        elif s.name == "Reference 4":
            set_text(s, "J. Chen and K. Xie, \"Consumer valuation of Airbnb listings: a hedonic pricing approach,\" International Journal of Contemporary Hospitality Management, vol. 29, no. 9, 2017.")

    # =========================================================================
    # SLIDE 12: Thank You Slide
    # =========================================================================
    s12 = prs.slides[11]
    for s in s12.shapes:
        if s.name == "Text 0":
            set_text(s, "Thank you", font_size=40, bold=True)
        elif s.name == "Closing subtitle":
            set_text(s, "Questions and discussion", font_size=18)
        elif s.name == "Project name":
            set_text(s, "AirIQ: Multi-City Airbnb Price Intelligence Platform", font_size=15, bold=True)
        elif s.name == "University":
            set_text(s, "Aditya Raju Pidurkar-40  |  Nidhi Singh-15\nRamdeobaba University, Nagpur", font_size=13)
        elif s.name == "Motif caption":
            set_text(s, "MARKET COVERAGE")
        elif s.name == "Closing motif label 1":
            set_text(s, "London")
        elif s.name == "Closing motif label 2":
            set_text(s, "Paris")
        elif s.name == "Closing motif label 3":
            set_text(s, "Tokyo")
        elif s.name == "Closing motif label 4":
            set_text(s, "Mumbai")
        elif s.name == "Closing motif label 5":
            set_text(s, "Bengaluru")

    for path in OUT_PATHS:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        prs.save(path)
        print(f"[+] Saved exact RBU template presentation to: {path}")

if __name__ == "__main__":
    build_presentation()
