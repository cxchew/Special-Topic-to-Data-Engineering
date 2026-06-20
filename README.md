# SECP3843: Special Topic in Data Engineering 🚀

Welcome to my GitHub E-Portfolio for the **SECP3843 - Special Topic in Data Engineering** course (Semester II, 2025/2026), Faculty of Computing, Universiti Teknologi Malaysia (UTM). 

This repository serves as a comprehensive digital collection of my academic data engineering coursework. It showcases my learning progression, technical achievements, and hands-on experience in design patterns, data workflows, and distributed computing. The projects contained herein demonstrate a wide spectrum of modern data engineering disciplines, from enterprise cloud Lakehouses and big data analytics to artificial intelligence pipelines and multidimensional warehouse architectures.

---

## 👨‍💻 About the Author & Team
While this E-Portfolio is an individual submission showcasing my personal contributions and growth, the core systems within were collaboratively engineered alongside my teammates in **Group 9** under the expert supervision of **Dr. Aryati Binti Bakri**.
* **Chew Chiu Xian** (A23CS0061)
* **Brendan Chia Yan Fei** (A23CS0211)
* **Ng Yu Hin** (A23CS0148)

---

## 📁 Repository Contents (Assignments & Tutorials)

Below is an overview of the tutorials and academic assignments contained in this repository. Navigate to their respective folders to view the full source code, deployment steps, and detailed implementation reports.

### ☁️ Tutorial 1: Microsoft Azure End-to-End Lakehouse
* **Topic:** Cloud Data Engineering, Data Lakes, and Delta Lakehouse Pipeline.
* **Summary:** Built a fully automated, cloud-native ETL data pipeline using the `AdventureWorks` dataset to securely move on-premises business records into an optimized, query-ready cloud analytics environment.
* **Key Skills:** Implementation of a strict **Medallion Architecture** (Bronze, Silver, Gold zones) inside Azure Data Lake Storage (ADLS) Gen2, Azure Data Factory (ADF) orchestration via Self-Hosted Integration Runtimes, big data cleansing using PySpark on Azure Databricks, Serverless Synapse SQL pool views, secure parameter management via Azure Key Vault, and interactive KPI dashboarding in Power BI.

### 🐘 Tutorial 2: Apache Spark Distributed Data Warehousing
* **Topic:** Big Data Scaling, Columnar Storage, and Star Schema Warehouses.
* **Summary:** Processed and analyzed a decade-plus timeline of Brazil's massive national school census dataset (**Censo Escolar**, 2010–2021) using distributed processing engines to bypass traditional relational hardware memory limits.
* **Key Skills:** Spark engine optimization, PySpark DataFrame manipulations, handling schema shifts across historical horizons, null-safe data imputation via `coalesce`, integer surrogate key generation with `monotonically_increasing_id()`, columnar write serialization using the **SNAPPY Parquet compression codec**, Java Database Connectivity (JDBC) streaming, and Star Schema physical layer design inside a PostgreSQL 17 database instance.

### 🧠 Tutorial 3: AI Algorithm (Image Classification Pipeline)
* **Topic:** Deep Learning Features & Advanced Regularization Defenses.
* **Summary:** Engineered a robust computer vision pipeline utilizing **TensorFlow and Keras** to accurately categorize multi-dimensional color pixel matrices from the classic CIFAR-10 image dataset into discrete label classes.
* **Key Skills:** Deep convolutional network architecture engineering, transitioning from flat ANNs to deep CNNs (**New_CNN**), spatial transformation via on-the-fly Data Augmentation (`RandomFlip`, `RandomRotation`, `RandomZoom`), Batch Normalization for gradient landscape smoothing, severe multi-tiered Dropout regularizations (25% to 50% barriers) to eliminate model overfitting variance, and statistical pipeline verification using Confusion Matrices.

### 📊 Academic Writing (Tutorial Article)
* **Topic:** Enterprise Multi-Fact Warehouse & Galaxy Schema Platform for PT. MPM.
* **Summary:** Designed a comprehensive 5-layer Business Intelligence solution to dismantle fragmented department silos for an Indonesian regional packaging manufacturer, establishing an analytical playground for executive decision-making.
* **Key Skills:** System boundary mapping (Use Case Diagrams), relational OLTP database design (ERD UML Notation), advanced **Galaxy Schema (Fact-Constellation)** multidimensional modeling, managing conformed shared dimensions (`Dim_Product`, `Dim_Date`), and tracking industrial KPIs such as **Overall Equipment Effectiveness (OEE)**.

### 🤖 Tutorial 4: Generative AI-Assisted ETL Automation
* **Topic:** Autonomous AI Agents & AI-Driven Pipeline Diagnostics.
* **Summary:** Leveraged advanced prompt engineering and autonomous AI software agents within `express.dev` to rapidly spin up an automated live data streaming engine that ingests real-time forecast parameters from the Malaysia Weather API into an enterprise data warehouse.
* **Key Skills:** Prompt engineering for operational data design, automated Cron Job trigger synchronization (2-minute cadence execution blocks), Snowflake cloud data warehouse integration, interactive AI debugging for account identifier authentication mismatches, and parsing complex data types by building AI-generated transformation mapping layers to flatten nested JSON array payloads into clean database tables.

---

## 💡 Overall Subject Reflection

Completing this course in Special Topic in Data Engineering has redefined my technical worldview. Moving past basic, static relational queries, I now understand that data engineering functions as the core nervous system of modern industry, which is the essential foundation that feeds analytics engines and keeps advanced machine learning models fueled with high-integrity data.

### 🏛️ 1. Architectural Evolution & Big Data Mastery
My journey across these projects demonstrated that raw data is a liability until structured intentionally. Developing the multi-tier **Medallion Architecture** in Azure and designing the **Galaxy Schema** for PT. MPM taught me how to take chaotic business records and mature them into authoritative, clean reporting layers using conformed dimensions. Furthermore, working with the 12-year *Censo Escolar* big data footprint in Apache Spark shifted my approach to scaling; witnessing massive datasets compress efficiently via **SNAPPY Parquet** columns while boosting retrieval speeds proved the absolute necessity of distributed computing layouts over traditional hardware.

### 🤖 2. The AI & Data Infrastructure Intersect
This curriculum illustrated the close, cyclical relationship between AI algorithms and data pipelines. In the computer vision pipeline (CIFAR-10), data engineering principles acted as a prerequisite for deep learning; without strict spatial augmentation and regularization layers, complex convolutional networks overfit to background noise. On the other hand, in the Snowflake automation pipeline, generative AI transformed from a product into a development tool. Utilizing autonomous agent loops inside `express.dev` proved how prompt engineering can abstract complex API infrastructure configurations and accelerate traditional development cycles.

### 🔍 3. Diagnostic Problem-Solving Maturity
True data engineering proficiency is built directly within system error logs. Overcoming unpredictable difficulties such as flattening multi-layered nested JSON structures from live weather payloads, mapping complex syntax layers in Keras, and debugging Snowflake account identifier authentication mismatches have strengthened my analytical resilience. These engineering bottlenecks taught me how to approach architectural system design with a rigorous, investigative mindset, ensuring that downstream business intelligence platforms remain accurate, scalable, and resilient against data drift.
