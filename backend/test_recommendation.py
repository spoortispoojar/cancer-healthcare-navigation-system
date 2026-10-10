
from app.recommendation import find_facilities


results = find_facilities(
    city="Bengaluru",
    cancer_type="Breast",
    current_treatment="Chemotherapy",
)

print("Matching facilities:")

if results:
    for facility in results:
        print(facility)
else:
    print("No matching facilities found.")
