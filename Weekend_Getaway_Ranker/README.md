# 🏖️ Weekend Getaway Ranker

A Python-based recommendation engine that suggests and ranks the **best weekend travel destinations in India** based on **distance, rating, and popularity**, using the _India's Must-See Places_ travel dataset.

---

## Project Objective

The goal of this project is to build a **local travel recommendation system** that:

- Takes a **source city** as interactive user input
- Identifies nearby tourist destinations within realistic weekend travel distance
- Filters destinations
- Ranks them using a **composite scoring algorithm**
- Produces **human-readable ranked outputs** in both console and timestamped text files

This project demonstrates practical **data engineering concepts**, including data preprocessing, feature engineering, distance calculation using the Haversine formula, normalization, weighted scoring logic, and ranking.

---

The dataset includes:

- **Name** – Destination name
- **City** – City location
- **State** – State location
- **Type** – Category of attraction (Historical, Religious, Nature, etc.)
- **Establishment Year** – Year the place was established
- **Google Review Rating** – Average rating out of 5
- **Number of Google Reviews (in lakhs)** – Review count in lakhs
- **Time Needed to Visit (hrs)** – Recommended visit duration
- **Entrance Fee (INR)** – Entry fee in Indian Rupees
- **Airport within 50 km** – Nearest airport availability
- **Weekly Off** – Closed days
- **Best Time to Visit** – Ideal visiting season
- **Significance** – Cultural, historical, or religious importance

### Data Enrichment

- Manually added **latitude–longitude coordinates** for **47 major Indian cities**
- Cities span multiple regions:
  - Major Metropolitan Cities
  - North India
  - Himalayan Region
  - Maharashtra Region
  - East India
  - South India
- Distances are calculated using the **Haversine formula** for accurate great-circle distance measurement

---

## 📂 Dataset Used

**Dataset Name:** Top Indian Places to Visit  
**Source:** Kaggle – Travel Dataset: Guide to India’s Must-See Places  
**Format:** CSV

---

## 📁 Project Structure

```
Weekend-Getaway-Ranker/
│
├── data/
│   └── Top Indian Places to Visit.csv
│
├── output/
│   ├── Kolkata_weekend_getaways_20260103_132644.txt
│   ├── Pune_weekend_getaways_20260103_132647.txt
│   └── Siliguri_weekend_getaways_20260103_132638.txt
│
├── weekend_getaway_ranker.py
├── requirements.txt
└── README.md
```

---

The dataset includes:

- **Name** – Destination name
- **City** – City location
- **State** – State location
- **Type** – Category of attraction (Historical, Religious, Nature, etc.)
- **Establishment Year** – Year the place was established
- **Google Review Rating** – Average rating out of 5
- **Number of Google Reviews (in lakhs)** – Review count in lakhs
- **Time Needed to Visit (hrs)** – Recommended visit duration
- **Entrance Fee (INR)** – Entry fee in Indian Rupees
- **Airport within 50 km** – Nearest airport availability
- **Weekly Off** – Closed days
- **Best Time to Visit** – Ideal visiting season
- **Significance** – Cultural, historical, or religious importance

### Data Enrichment

- Manually added **latitude–longitude coordinates** for **47 major Indian cities**
- Cities span multiple regions:
  - Major Metropolitan Cities
  - North India
  - Himalayan Region
  - Maharashtra Region
  - East India
  - South India
- Distances are calculated using the **Haversine formula** for accurate great-circle distance measurement

---

## Technologies Used

- Python
- Pandas

---

## Recommendation Algorithm

Each destination is ranked using a **composite score** based on three normalized factors:

### Rating Score (40%)

- Based on Google review ratings (0–5 scale)
- Normalized using min-max scaling: `rating_norm = rating / max_rating`
- Higher-rated destinations receive higher scores
- **Why 40%?** Quality of experience is the most important factor for recommendations

### Popularity Score (30%)

- Based on number of Google reviews (in lakhs)
- Normalized: `popularity_norm = reviews / max_reviews`
- More popular destinations (crowd-validated) receive higher scores

### Distance Score (30%)

- Calculated using **Haversine formula** for accurate spherical distance
- Inverted normalization: `distance_norm = 1 - (distance / max_distance)`
- Closer destinations receive higher scores

### Final Composite Score Formula

Final Score formula:
Final Score = (0.4 × Rating Score) + (0.3 × Popularity Score) + (0.3 × Distance Score)

---

### Filtering Criteria

Destinations are filtered by:

- **Maximum Distance:** 300 km
- **Minimum Rating:** 4.3/5.0
- **Same City Exclusion:** Removes destinations in the source city

---

## Features

- Interactive console-based city input
- Case-Insensitive Input
- Distance-based filtering (≤300 km)
- Rating threshold filtering (≥4.3)
- Timestamped output reports
- Multi-city support across India

---

## How to Run the Project

### Clone the Repository

```bash
git clone https://github.com/ritam2004-dev/Intern-Technical-Assessment.git
cd Weekend-Getaway-Ranker
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Script

```bash
python main.py
```

### Enter Your City

```plaintext
🌄 WEEKEND GETAWAY RECOMMENDATION SYSTEM 🌄

Available Cities:

   Agra            Ahmedabad       Alibaug         Amritsar        Bangalore
   Bhopal          Bhimashankar    Bolpur          Bhubaneswar     Chennai
   ...

────────────────────────────────────────────────────────────────────────────────

Enter your source city: Kolkata
```

---

## Future Enhancements

- Dynamic Distance API - Integrate external API for real road distances
- Web Interface - Build Flask/FastAPI dashboard with interactive maps
- Personalization - Add user preference filters (budget, attraction type, travel time)
- Multi-Day Trips - Extend to 3-day or week-long trips

## 👨‍💻 Author

**Ritam Khatua**
