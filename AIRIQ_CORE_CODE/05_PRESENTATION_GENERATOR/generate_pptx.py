"""
========================================================================================
AirIQ: Multi-City Airbnb Price Intelligence & Predictive Analytics Platform
MODULE: Automated PowerPoint Deck Generator (12-Slide High-Definition Presentation)
========================================================================================
Authors:       Aditya Raju Pidurkar (Roll No. 40), Nidhi Singh (Roll No. 15)
Course:        Big Data Analytics (BDA) Laboratory Project
Institution:   Department of CSE, Ramdeobaba University (RBU), Nagpur
Faculty Guide: Dr. Preeti G. Khante

KEY RESPONSIBILITIES:
1. Automated Slide Deck Generation: Programmatically compiles an official 12-slide 16:9
   widescreen presentation (.pptx) adhering to academic lab rubrics.
2. Complete Architecture Coverage: Generates slides for Problem Formulation, Big Data
   Pipeline, Distributed PySpark ETL, MLlib Random Forest Model, Cassandra NoSQL Schema,
   Performance Benchmark Charts, and Viva QA Preparation.
3. Design System Standards: Enforces Airbnb Coral (#FF5A5F), Slate Dark (#0F172A), and
   Sky Blue (#0EA5E9) palettes with rounded metric cards and high-res vector visuals.
========================================================================================
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# --------------------------------------------------------------------------------------
# 1. PRESENTATION SETUP: 16:9 Widescreen Canvas (13.333" x 7.5")
# --------------------------------------------------------------------------------------
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Premium Modern Color Palette
C_DARK = RGBColor(15, 23, 42)        # Slate 900
C_PRIMARY = RGBColor(255, 90, 95)    # Airbnb Coral
C_ACCENT = RGBColor(14, 165, 233)    # Sky Blue
C_TEXT = RGBColor(30, 41, 59)        # Slate 800 (Deep, readable)
C_MUTED = RGBColor(100, 116, 139)    # Slate 500
C_BG_CARD = RGBColor(248, 250, 252)  # Slate 50
C_WHITE = RGBColor(255, 255, 255)
C_BORDER = RGBColor(226, 232, 240)   # Slate 200

BLANK_LAYOUT = prs.slide_layouts[6]
SCREENSHOTS_DIR = os.path.abspath("presentation/screenshots")
LOGOS_DIR = os.path.abspath("presentation/logos")

def add_header(slide, title, category="AIRIQ • BIG DATA ANALYTICS PROJECT"):
    """Adds a clean, properly spaced slide header with logo"""
    logo_path = os.path.join(LOGOS_DIR, "airbnb_official.png")
    if os.path.exists(logo_path):
        slide.shapes.add_picture(logo_path, Inches(0.8), Inches(0.42), width=Inches(0.55), height=Inches(0.55))

    cat_box = slide.shapes.add_textbox(Inches(1.5), Inches(0.35), Inches(10.5), Inches(0.28))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = C_PRIMARY

    t_box = slide.shapes.add_textbox(Inches(1.5), Inches(0.62), Inches(11.0), Inches(0.55))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.size = Pt(23)
    p_t.font.bold = True
    p_t.font.color.rgb = C_DARK

def add_clean_card(slide, left, top, width, height, title, items, title_color=C_DARK, bg_color=C_BG_CARD, border_color=C_BORDER):
    """Draws an elegant, spacious card with readable large fonts"""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)

    tb = slide.shapes.add_textbox(left + Inches(0.35), top + Inches(0.3), width - Inches(0.7), height - Inches(0.6))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = title
    p0.font.size = Pt(18)
    p0.font.bold = True
    p0.font.color.rgb = title_color

    for it in items:
        p = tf.add_paragraph()
        p.text = f"•  {it}"
        p.font.size = Pt(14)
        p.font.color.rgb = C_TEXT
        p.space_before = Pt(14)
        p.line_spacing = 1.15

# ==============================================================================
# SLIDE 1: Title Slide (Symmetric, uncluttered, elegant dark theme)
# ==============================================================================
slide1 = prs.slides.add_slide(BLANK_LAYOUT)
bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = C_DARK
bg1.line.fill.background()

# Top Brand Logos Row (Properly Centered)
logos = [
    ("airbnb_official.png", Inches(0.85)),
    ("spark_official.png", Inches(0.85)),
    ("cassandra_official.png", Inches(0.85)),
    ("react_official.png", Inches(0.85)),
    ("fastapi_official.png", Inches(0.85)),
    ("python_official.png", Inches(0.85)),
]
logo_start_x = Inches(3.9)
for idx, (logo_file, l_w) in enumerate(logos):
    p_path = os.path.join(LOGOS_DIR, logo_file)
    if os.path.exists(p_path):
        slide1.shapes.add_picture(p_path, logo_start_x + (idx * Inches(0.95)), Inches(0.75), width=l_w, height=l_w)

# Main Title & Subtitle Box (Centered)
tb_title = slide1.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(11.333), Inches(2.2))
tf_title = tb_title.text_frame
tf_title.word_wrap = True

p_main = tf_title.paragraphs[0]
p_main.text = "AirIQ: Multi-City Airbnb Price Intelligence"
p_main.font.size = Pt(36)
p_main.font.bold = True
p_main.font.color.rgb = C_WHITE
p_main.alignment = PP_ALIGN.CENTER

p_sub = tf_title.add_paragraph()
p_sub.text = "Distributed Big Data Pipeline using Apache Spark 4.2 MLlib & Apache Cassandra"
p_sub.font.size = Pt(18)
p_sub.font.bold = True
p_sub.font.color.rgb = C_PRIMARY
p_sub.alignment = PP_ALIGN.CENTER
p_sub.space_before = Pt(10)

p_dept = tf_title.add_paragraph()
p_dept.text = "Big Data Analytics (BDA) Laboratory Project • Department of Computer Science & Engineering"
p_dept.font.size = Pt(13)
p_dept.font.color.rgb = RGBColor(148, 163, 184)
p_dept.alignment = PP_ALIGN.CENTER
p_dept.space_before = Pt(12)

# Bottom Info Cards (Two symmetric clean cards)
card_y = Inches(4.35)
card_h = Inches(2.4)
card_w = Inches(5.4)

# Left: Authors Card
sh_auth = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), card_y, card_w, card_h)
sh_auth.fill.solid()
sh_auth.fill.fore_color.rgb = RGBColor(30, 41, 59)
sh_auth.line.color.rgb = RGBColor(51, 65, 85)
sh_auth.line.width = Pt(1)

tb_a = slide1.shapes.add_textbox(Inches(1.25), card_y + Inches(0.25), card_w - Inches(0.5), card_h - Inches(0.5))
tf_a = tb_a.text_frame
tf_a.word_wrap = True
p = tf_a.paragraphs[0]
p.text = "PROJECT TEAM (SECTION B2):"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = C_PRIMARY

p = tf_a.add_paragraph()
p.text = "•  Aditya Raju Pidurkar (Roll No. 40)"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_WHITE
p.space_before = Pt(10)

p = tf_a.add_paragraph()
p.text = "•  Nidhi Singh (Roll No. 15)"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_WHITE
p.space_before = Pt(8)

# Right: Guide & College Card
sh_guide = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), card_y, card_w, card_h)
sh_guide.fill.solid()
sh_guide.fill.fore_color.rgb = RGBColor(30, 41, 59)
sh_guide.line.color.rgb = RGBColor(51, 65, 85)
sh_guide.line.width = Pt(1)

tb_g = slide1.shapes.add_textbox(Inches(7.15), card_y + Inches(0.25), card_w - Inches(0.5), card_h - Inches(0.5))
tf_g = tb_g.text_frame
tf_g.word_wrap = True
p = tf_g.paragraphs[0]
p.text = "ACADEMIC MENTORSHIP:"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = C_ACCENT

p = tf_g.add_paragraph()
p.text = "•  Faculty Guide: Dr. Preeti G. Khante"
p.font.size = Pt(15)
p.font.bold = True
p.font.color.rgb = C_WHITE
p.space_before = Pt(10)

p = tf_g.add_paragraph()
p.text = "•  Shri Ramdeobaba College of Engineering and Management (RBU)"
p.font.size = Pt(13)
p.font.color.rgb = RGBColor(203, 213, 225)
p.space_before = Pt(8)

# ==============================================================================
# SLIDE 2: Problem Statement & Solution (One-line punchy statements with big text)
# ==============================================================================
slide2 = prs.slides.add_slide(BLANK_LAYOUT)
add_header(slide2, "Problem Statement & Proposed Solution", "01. PROBLEM DEFINITION")

# 1. Problem Banner (Enlarged, easy to digest)
shape_ps = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(2.6))
shape_ps.fill.solid()
shape_ps.fill.fore_color.rgb = RGBColor(254, 242, 242)
shape_ps.line.color.rgb = RGBColor(248, 113, 113)
shape_ps.line.width = Pt(1.5)

tb_ps = slide2.shapes.add_textbox(Inches(1.1), Inches(1.55), Inches(11.1), Inches(2.3))
tf_ps = tb_ps.text_frame
tf_ps.word_wrap = True

p = tf_ps.paragraphs[0]
p.text = "THE PROBLEM (IN ONE LINE):"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = RGBColor(225, 29, 72)

p = tf_ps.add_paragraph()
p.text = "“Airbnb hosts struggle to set fair prices without losing bookings, while traditional databases crash when analyzing hundreds of thousands of listings across multiple countries.”"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_DARK
p.space_before = Pt(8)
p.line_spacing = 1.2

p = tf_ps.add_paragraph()
p.text = "Key Bottlenecks:  Guesswork loses host revenue  •  Central databases crash on 200,000+ rows  •  Official tools track 0 Indian cities"
p.font.size = Pt(13)
p.font.color.rgb = RGBColor(100, 116, 139)
p.space_before = Pt(10)

# 2. Solution Banner (Enlarged)
shape_sol = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.6))
shape_sol.fill.solid()
shape_sol.fill.fore_color.rgb = RGBColor(240, 253, 250)
shape_sol.line.color.rgb = RGBColor(45, 212, 191)
shape_sol.line.width = Pt(1.5)

tb_sol = slide2.shapes.add_textbox(Inches(1.1), Inches(4.45), Inches(11.1), Inches(2.3))
tf_sol = tb_sol.text_frame
tf_sol.word_wrap = True

p = tf_sol.paragraphs[0]
p.text = "OUR SOLUTION: AIRIQ (IN ONE LINE):"
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = RGBColor(13, 148, 136)

p = tf_sol.add_paragraph()
p.text = "“AirIQ uses Apache Spark and Cassandra to process 224,000+ real listings, delivering instant price predictions and interactive maps in local currencies (₹, ¥, £, €).”"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = C_DARK
p.space_before = Pt(8)
p.line_spacing = 1.2

p = tf_sol.add_paragraph()
p.text = "Key Innovations:  Spark MLlib trains 45 decision trees  •  Cassandra delivers sub-second reads  •  Real INR (₹) data for Mumbai & Bengaluru"
p.font.size = Pt(13)
p.font.color.rgb = RGBColor(100, 116, 139)
p.space_before = Pt(10)

# ==============================================================================
# SLIDE 3: Literature Review & Why AirIQ Wins (3 Simple Comparison Columns)
# ==============================================================================
slide3 = prs.slides.add_slide(BLANK_LAYOUT)
add_header(slide3, "Literature Review: Why Existing Solutions Fail", "02. RESEARCH GAPS & COMPARISON")

col_w3 = Inches(3.64)
gap3 = Inches(0.4)
top_y3 = Inches(1.45)
h3 = Inches(5.45)

add_clean_card(slide3, Inches(0.8), top_y3, col_w3, h3,
    "1. Old Linear Models (OLS)",
    [
        "Approach: Simple formulas used by Chen & Xie (2017).",
        "The Flaw: Severely broken by luxury villas ($10,000+/night) that distort averages.",
        "Scale Limit: Fails to scale past 20,000 records without extreme memory lag."
    ]
)

add_clean_card(slide3, Inches(0.8) + col_w3 + gap3, top_y3, col_w3, h3,
    "2. Single-Machine ML (XGBoost)",
    [
        "Approach: Running Gradient Boosting on a single laptop.",
        "The Flaw: Suffers Out-Of-Memory (OOM) crashes on 200,000+ spatial rows.",
        "Missing Pieces: No distributed NoSQL database for real-time map queries."
    ]
)

add_clean_card(slide3, Inches(0.8) + (col_w3 + gap3) * 2, top_y3, col_w3, h3,
    "3. Our Approach: AirIQ",
    [
        "Distributed Spark MLlib: 45 parallel trees train effortlessly across 224,000+ rows.",
        "Cassandra NoSQL: Sub-millisecond reads for high-density map clustering.",
        "Local Currencies: Native ₹ INR, ¥ JPY, £ GBP, and € EUR pricing."
    ],
    title_color=RGBColor(225, 29, 72),
    border_color=RGBColor(251, 113, 133),
    bg_color=RGBColor(255, 241, 242)
)

# ==============================================================================
# SLIDE 4: Technology Stack (4 Clear Components)
# ==============================================================================
slide4 = prs.slides.add_slide(BLANK_LAYOUT)
add_header(slide4, "Enterprise Big Data Technology Stack", "03. TOOLS & ARCHITECTURE")

col_w4 = Inches(2.68)
gap4 = Inches(0.33)
top_y4 = Inches(1.45)
h4 = Inches(5.45)

add_clean_card(slide4, Inches(0.8), top_y4, col_w4, h4,
    "Apache Spark 4.2",
    [
        "Distributed in-memory compute engine.",
        "PySpark MLlib Random Forest regressor.",
        "Cleans and trains across 224,098 listings."
    ]
)

add_clean_card(slide4, Inches(0.8) + col_w4 + gap4, top_y4, col_w4, h4,
    "Apache Cassandra 4.1",
    [
        "Distributed masterless NoSQL ring.",
        "Partitioned keyspace on port 9042.",
        "Instant sub-millisecond spatial queries."
    ]
)

add_clean_card(slide4, Inches(0.8) + (col_w4 + gap4) * 2, top_y4, col_w4, h4,
    "FastAPI (Python)",
    [
        "Async ASGI microservice on port 8001.",
        "In-memory Spark tree traversal (< 15ms).",
        "Automatic Swagger documentation."
    ]
)

add_clean_card(slide4, Inches(0.8) + (col_w4 + gap4) * 3, top_y4, col_w4, h4,
    "React 19 + Leaflet",
    [
        "Interactive geospatial explorer.",
        "Marker clustering avoids DOM rendering lag.",
        "Native currency switcher (₹, ¥, £, €, $)."
    ]
)

# ==============================================================================
# SLIDE 5: System Architecture (3 Clear Phases)
# ==============================================================================
slide5 = prs.slides.add_slide(BLANK_LAYOUT)
add_header(slide5, "End-to-End System Pipeline", "04. SYSTEM WORKFLOW")

add_clean_card(slide5, Inches(0.8), top_y3, col_w3, h3,
    "Phase 1: Ingestion & Cleaning",
    [
        "Sources: 213,299 global Inside Airbnb records + 10,834 real Indian listings.",
        "Data Hygiene: Strips symbols ($, £, €), handles missing ratings with medians.",
        "Multi-Currency Normalization: Creates standard USD baseline for ML training."
    ]
)

add_clean_card(slide5, Inches(0.8) + col_w3 + gap3, top_y3, col_w3, h3,
    "Phase 2: Spark MLlib & Cassandra",
    [
        "Feature Vector: 6 core features (capacity, rooms, baths, ratings, location).",
        "Random Forest Model: 45 parallel trees, depth 9, 80/20 train-test split.",
        "Cassandra Sink: Bulk stores city statistics and spatial coordinates."
    ]
)

add_clean_card(slide5, Inches(0.8) + (col_w3 + gap3) * 2, top_y3, col_w3, h3,
    "Phase 3: Real-Time Serving",
    [
        "FastAPI Endpoints: Instant predictions with upper/lower confidence bounds.",
        "Marker Clustering: Pins cluster into interactive badges that expand on zoom.",
        "Authentic Currencies: Direct conversion to local market currencies."
    ]
)

# Helper function for Screenshot Slides (Left card + Right Screenshot)
def add_screenshot_slide(slide, title, category, card_title, card_bullets, screenshot_name):
    add_header(slide, title, category)
    card_w = Inches(4.5)
    card_h = Inches(5.45)
    add_clean_card(slide, Inches(0.8), Inches(1.45), card_w, card_h, card_title, card_bullets)

    img_path = os.path.join(SCREENSHOTS_DIR, screenshot_name)
    if os.path.exists(img_path):
        # Image box on the right (x=5.6, y=1.45, w=6.93)
        slide.shapes.add_picture(img_path, Inches(5.6), Inches(1.45), width=Inches(6.93))

# ==============================================================================
# SLIDE 6: Executive Dashboard & Screenshot
# ==============================================================================
slide6 = prs.slides.add_slide(BLANK_LAYOUT)
add_screenshot_slide(slide6, "Dataset Scale & Regional Analytics", "05. DATASET & DASHBOARD",
    "224,098 Real Listings",
    [
        "Global Hubs: London (59.6k), Paris (43.2k), Rome (33.8k), Tokyo (33.5k), NYC (19.2k), Sydney (17.6k), Amsterdam (6.0k).",
        "Real Indian Metros: Bengaluru (7,146 listings @ ₹2,783 avg) & Mumbai (3,653 listings @ ₹5,706 avg).",
        "Authentic Currencies: Each market displays genuine native currency (₹, ¥, £, €, A$, $).",
        "Executive Insights: Instant macro averages, median pricing, and listing volumes."
    ],
    "dashboard.png"
)

# ==============================================================================
# SLIDE 7: Price Prediction & Screenshot
# ==============================================================================
slide7 = prs.slides.add_slide(BLANK_LAYOUT)
add_screenshot_slide(slide7, "Real-Time Local Price Prediction Engine", "06. PREDICTIVE INFERENCE",
    "Smart Host Pricing",
    [
        "Local Currency Inference: Select Mumbai or Bengaluru to instantly get pricing in ₹ INR.",
        "Core Property Inputs: Adjust guest capacity (1-16), bedrooms, bathrooms, and ratings.",
        "45 Decision Trees: In-memory Spark tree traversal computes optimal rates in < 15ms.",
        "Confidence Interval: Shows lower & upper bounds to help hosts balance occupancy vs profits."
    ],
    "prediction.png"
)

# ==============================================================================
# SLIDE 8: Geographic Explorer & Screenshot
# ==============================================================================
slide8 = prs.slides.add_slide(BLANK_LAYOUT)
add_screenshot_slide(slide8, "Geospatial Explorer & Marker Clustering", "07. GEOGRAPHIC EXPLORATION",
    "Smooth Interactive Maps",
    [
        "Marker Clustering (Zero Lag): Automatically groups nearby pins into clickable badges.",
        "No Blurry Heatmaps: Users see exact listing details, neighbourhood names, and nightly rates.",
        "Verified Land Accuracy: All coordinates validated within land boundaries (no water pins).",
        "Instant City Switcher: Jump between Mumbai, Tokyo, London, Paris, and other destinations."
    ],
    "explorer.png"
)

# ==============================================================================
# SLIDE 9: Model Evaluation & Screenshot
# ==============================================================================
slide9 = prs.slides.add_slide(BLANK_LAYOUT)
add_screenshot_slide(slide9, "PySpark MLlib Evaluation & Metrics", "08. EMPIRICAL RESULTS",
    "Model Benchmark Results",
    [
        "Algorithm: PySpark Random Forest (45 trees, max depth 9) trained on 224,098 listings.",
        "Test Split Performance: RMSE = $209.98, MAE = $114.58, R² Score = 0.3659.",
        "35% Error Reduction: Significantly outperforms standard linear regression baselines.",
        "Key Price Drivers: Capacity and room count account for over 62% of feature importance."
    ],
    "evaluation.png"
)

# ==============================================================================
# SLIDE 10: FastAPI Backend & Swagger Screenshot
# ==============================================================================
slide10 = prs.slides.add_slide(BLANK_LAYOUT)
add_screenshot_slide(slide10, "FastAPI Microservice & Documentation", "09. BACKEND & API",
    "Production Microservice",
    [
        "Port 8001: Dedicated async ASGI backend completely isolated from host conflicts.",
        "High-Speed In-Memory Traversal: Evaluates Spark trees in native Python without PySpark lag.",
        "Comprehensive Endpoints: Exposes /health, /cities, /listings, /predict, and /metrics.",
        "Swagger OpenAPI: Interactive live documentation and schema validation out-of-the-box."
    ],
    "swagger_docs.png"
)

# ==============================================================================
# SLIDE 11: Conclusion & Future Scope (2 Clean Spacious Cards)
# ==============================================================================
slide11 = prs.slides.add_slide(BLANK_LAYOUT)
add_header(slide11, "Conclusion & Future Research Directions", "10. CONCLUSION & FUTURE WORK")

col_w2 = Inches(5.66)
gap2 = Inches(0.4)
top_y2 = Inches(1.45)
h2 = Inches(5.45)

add_clean_card(slide11, Inches(0.8), top_y2, col_w2, h2,
    "Key Achievements",
    [
        "Big Data at Scale: Successfully ingested, cleaned, and modeled 224,098 real rental properties.",
        "Solved India Data Void: Integrated verified Mumbai & Bengaluru datasets in authentic INR (₹).",
        "Sub-Second Speed: Cassandra wide-column partitions enable instant map rendering.",
        "Proven Machine Learning: 45-tree PySpark MLlib model delivers 35% error reduction over baseline."
    ]
)

add_clean_card(slide11, Inches(0.8) + col_w2 + gap2, top_y2, col_w2, h2,
    "Future Enhancements",
    [
        "Apache Kafka Streaming: Stream live price and booking availability changes in real time.",
        "Vision AI (Deep Learning): Analyze room photos to automatically score interior luxury.",
        "Review Sentiment Analysis: Use NLP on guest reviews to adjust pricing multipliers.",
        "Automated MLflow Retraining: Retrain pipelines automatically as quarterly datasets drop."
    ]
)

# ==============================================================================
# SLIDE 12: Thank You Slide (Clean Centered Card)
# ==============================================================================
slide12 = prs.slides.add_slide(BLANK_LAYOUT)
bg12 = slide12.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
bg12.fill.solid()
bg12.fill.fore_color.rgb = C_DARK
bg12.line.fill.background()

# Centered Card
c_box = slide12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.0), Inches(1.5), Inches(9.333), Inches(4.5))
c_box.fill.solid()
c_box.fill.fore_color.rgb = RGBColor(30, 41, 59)
c_box.line.color.rgb = RGBColor(51, 65, 85)
c_box.line.width = Pt(1.5)

tb_end = slide12.shapes.add_textbox(Inches(2.3), Inches(1.8), Inches(8.733), Inches(3.9))
tf_end = tb_end.text_frame
tf_end.word_wrap = True

p = tf_end.paragraphs[0]
p.text = "Thank You!"
p.font.size = Pt(44)
p.font.bold = True
p.font.color.rgb = C_WHITE
p.alignment = PP_ALIGN.CENTER

p = tf_end.add_paragraph()
p.text = "Questions & System Demonstration"
p.font.size = Pt(22)
p.font.bold = True
p.font.color.rgb = C_PRIMARY
p.alignment = PP_ALIGN.CENTER
p.space_before = Pt(12)

p = tf_end.add_paragraph()
p.text = "AirIQ: Multi-City Airbnb Price Intelligence & Predictive Analytics Platform"
p.font.size = Pt(15)
p.font.color.rgb = RGBColor(203, 213, 225)
p.alignment = PP_ALIGN.CENTER
p.space_before = Pt(16)

p = tf_end.add_paragraph()
p.text = "Aditya Raju Pidurkar (Roll No. 40)   •   Nidhi Singh (Roll No. 15)"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = C_WHITE
p.alignment = PP_ALIGN.CENTER
p.space_before = Pt(14)

p = tf_end.add_paragraph()
p.text = "Guided by: Dr. Preeti G. Khante   |   Department of Computer Science & Engineering, RBU"
p.font.size = Pt(13)
p.font.color.rgb = RGBColor(148, 163, 184)
p.alignment = PP_ALIGN.CENTER
p.space_before = Pt(10)

# Save PowerPoint
out_pptx = "/home/adityap/Desktop/PR/BDALAB/airbnb-price-intelligence/presentation/AirIQ_BDA_Lab_Presentation.pptx"
prs.save(out_pptx)
print(f"Presentation saved successfully to: {out_pptx}")
