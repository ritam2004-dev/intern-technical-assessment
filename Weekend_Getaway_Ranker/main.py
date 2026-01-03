import pandas as pd
import math
from datetime import datetime
import os


# Dataset Path
DATA_PATH = "data/Top Indian Places to Visit.csv"


# City Coordinates (Latitude, Longitude)
CITY_COORDS = {
    # Major Metropolitan Cities
    "Delhi":           (28.6139, 77.2090),
    "Mumbai":          (19.0760, 72.8777),
    "Bangalore":       (12.9716, 77.5946),
    "Hyderabad":       (17.3850, 78.4867),
    "Chennai":         (13.0827, 80.2707),
    "Kolkata":         (22.5726, 88.3639),
    "Pune":            (18.5204, 73.8567),
    "Ahmedabad":       (23.0225, 72.5714),
    
    # North India - Delhi NCR & Nearby
    "Jaipur":          (26.9124, 75.7873),
    "Agra":            (27.1767, 78.0081),
    "Amritsar":        (31.6340, 74.8723),
    "Varanasi":        (25.3176, 82.9739),
    "Lucknow":         (26.8467, 80.9462),
    "Bhopal":          (23.2599, 77.4126),
    "Indore":          (22.7196, 75.8577),
    "Patna":           (25.5941, 85.1376),
    "Udaipur":         (24.5854, 73.7125),
    
    # Himalayan Region
    "Rishikesh":       (30.0869, 78.2676),
    "Haridwar":        (29.9457, 78.1642),
    "Dehradun":        (30.3165, 78.0322),
    "Mussoorie":       (30.4598, 78.0660),
    "Nainital":        (29.3803, 79.4636),
    "Manali":          (32.2396, 77.1887),
    "Shimla":          (31.1048, 77.1734),
    
    # Maharashtra Region
    "Lonavala":        (18.7537, 73.4076),
    "Alibaug":         (18.6514, 72.8720),
    "Mahabaleshwar":   (17.9244, 73.6577),
    "Matheran":        (18.9844, 73.2637),
    "Lavasa":          (18.4036, 73.5085),
    "Bhimashankar":    (19.0716, 73.5356),
    "Goa":             (15.2993, 74.1240),
    
    # East India - Bengal & Sikkim
    "Darjeeling":      (27.0410, 88.2663),
    "Siliguri":        (26.7271, 88.3953),
    "Gangtok":         (27.3331, 88.6083),
    "Pelling":         (27.2920, 88.3294),
    "Digha":           (21.6253, 87.5094),
    "Sundarbans":      (21.9497, 88.8831),
    "Bolpur":          (23.6840, 87.6847),
    "Jalpaiguri":      (26.5276, 88.7196),
    "Cooch Behar":     (26.3294, 89.4496),
    
    # South India
    "Bhubaneswar":     (20.2961, 85.8245),
    "Visakhapatnam":   (17.6868, 83.2185),
    "Kochi":           (9.9312, 76.2673),
    "Trivandrum":      (8.5241, 76.9366),
    "Mysore":          (12.2958, 76.6394),
}


# Haversine Distance Calculation
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))


# Recommendation Function
def recommend_places(source_city, top_n=5, max_distance=300, min_rating=4.3):
    try:
        df = pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        print(f"Error: Could not find dataset at {DATA_PATH}")
        return None
    except Exception as e:
        print(f"Error reading dataset: {e}")
        return None

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()

    # Rename columns
    df = df.rename(columns={
        "google review rating": "rating",
        "number of google review in lakhs": "popularity"
    })

    source_city = source_city.strip()

    if source_city not in CITY_COORDS:
        print(f"Coordinates not available for {source_city}")
        return None

    src_lat, src_lon = CITY_COORDS[source_city]

    # Remove same city
    df = df[df["city"].str.lower() != source_city.lower()]

    # Distance calculation
    def calculate_distance(city):
        city = city.strip()
        if city in CITY_COORDS:
            lat, lon = CITY_COORDS[city]
            return round(haversine(src_lat, src_lon, lat, lon), 2)
        return None

    df["distance_km"] = df["city"].apply(calculate_distance)

    # Remove places without distance
    df = df.dropna(subset=["distance_km"])

    # Apply distance and rating filters
    df = df[
        (df["distance_km"] <= max_distance) &
        (df["rating"] >= min_rating)
    ]

    if len(df) == 0:
        print(f"No destinations found matching your criteria")
        return None

    # Normalization
    df["rating_norm"] = df["rating"] / df["rating"].max()
    df["popularity_norm"] = df["popularity"] / df["popularity"].max()
    df["distance_norm"] = 1 - (df["distance_km"] / df["distance_km"].max())

    # Calculate Final Score (40% rating, 30% popularity, 30% distance)
    df["score"] = (
        0.4 * df["rating_norm"] +
        0.3 * df["popularity_norm"] +
        0.3 * df["distance_norm"]
    )

    # Return top N results
    return df.sort_values("score", ascending=False).head(top_n)[
        ["city", "state", "name", "distance_km", "rating", "popularity", "score"]
    ]


from datetime import datetime
import os

def write_output_to_file(source_city, recommendations, output_dir="output"):
    # Make sure the folder exists
    os.makedirs(output_dir, exist_ok=True)

    # Make file name with city and time
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{source_city.replace(' ', '_')}_weekend_getaways_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        # Header
        f.write("=" * 78 + "\n")
        f.write(f"WEEKEND GETAWAY RECOMMENDATIONS FROM {source_city.upper()}\n")
        f.write("=" * 78 + "\n")
        f.write("Generated on: "
                f"{datetime.now().strftime('%A, %B %d, %Y at %I:%M:%S %p')}\n")
        f.write(f"Total Destinations Found: {len(recommendations)}\n")
        f.write("=" * 78 + "\n\n")

        # Body
        if recommendations is not None and not recommendations.empty:
            for index, row in enumerate(recommendations.itertuples(index=False), start=1):
                f.write(f"#{index} {row.name.upper()}\n")
                f.write("-" * 78 + "\n")
                f.write(f"  Location   : {row.city}, {row.state}\n")
                f.write(f"  Distance   : {row.distance_km:.2f} km\n")
                f.write(f"  Rating     : {row.rating:.1f} / 5.0\n")
                f.write(f"  Popularity : {row.popularity:.2f} lakhs reviews\n")
                f.write(f"  Score      : {row.score:.4f}\n\n")
        else:
            f.write("No recommendations available\n\n")

        # Footer
        f.write("=" * 78 + "\n")
        f.write("END OF REPORT\n")
        f.write("=" * 78 + "\n")

    print("Recommendation saved in output file:", filepath)



def display_recommendations(source_city, recommendations):
    title = f"TOP WEEKEND GETAWAYS FROM {source_city.upper()}"
    print(title)
    print("=" * len(title))

    # If there is nothing to show
    if recommendations is None or recommendations.empty:
        print("No recommendations available")
        return

    # Table header
    print(f"{'#':<3} {'DESTINATION':<30} {'CITY':<15} "
          f"{'DIST(km)':<10} {'RATING':<8} {'POPULARITY':<12} {'SCORE':<8}")
    print("-" * 90)

    # Table rows
    for idx, row in enumerate(recommendations.itertuples(index=False), start=1):
        name = row.name
        if len(name) > 30:
            name = name[:28] + ".."

        city = row.city
        if len(city) > 15:
            city = city[:13] + ".."

        print(f"{idx:<3} {name:<30} {city:<15} "
              f"{row.distance_km:>7.2f}   "
              f"{row.rating:>7.1f}   "
              f"{row.popularity:>8.2f}   "
              f"{row.score:>7.2f}")

    print("-" * 90)



# Main Execution
if __name__ == "__main__":
    print("\n" + "=" * 78)
    print("🌄 WEEKEND GETAWAY RECOMMENDATION SYSTEM 🌄")
    print("=" * 78)
    
    # Display available cities in organized format
    print("\nAvailable Cities:\n")
    cities_list = sorted(CITY_COORDS.keys())
    
    # Display cities in 5 columns
    for i in range(0, len(cities_list), 5):
        row_cities = cities_list[i:i+5]
        print("   " + "".join(f"{city:<15}" for city in row_cities))
    
    print("\n" + "─" * 78)
    
    # Interactive user input
    source_city = input("\nEnter your source city: ").strip()
    
    # Case-insensitive city matching
    matched_city = None
    for city in CITY_COORDS:
        if city.lower() == source_city.lower():
            matched_city = city
            break
    
    if matched_city is None:
        print("\n" + "=" * 78)
        print(f"Error: '{source_city}' is not available in our database.")
        print(f"\nPlease choose from the available cities listed above.")
        print("=" * 78 + "\n")
    else:
        # Get recommendations
        recommendations = recommend_places(
            source_city=matched_city,
            top_n=5,
            max_distance=300,
            min_rating=4.3
        )
        
        # Display on console
        display_recommendations(matched_city, recommendations)
        
        # Save to timestamped file
        if recommendations is not None and not recommendations.empty:
            write_output_to_file(matched_city, recommendations)
            print()
