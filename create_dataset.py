import csv
from itertools import combinations
topics = [
    ("Artificial Intelligence",
     "Artificial intelligence enables computers to perform tasks that normally require human intelligence.",
     "AI allows computer systems to complete activities that usually need human thinking."),

    ("Machine Learning",
     "Machine learning systems identify patterns in data and use them to make predictions.",
     "ML models learn from data patterns to predict future outcomes."),

    ("Online Education",
     "Online education allows students to attend classes and access learning materials through the internet.",
     "Internet-based learning lets students join classes and study resources remotely."),

    ("Renewable Energy",
     "Solar energy converts sunlight into electricity using photovoltaic panels.",
     "Photovoltaic panels generate electrical power from sunlight."),

    ("Water Conservation",
     "Water conservation reduces unnecessary water use and protects freshwater resources.",
     "Saving water helps prevent waste and preserve available freshwater."),

    ("Environmental Pollution",
     "Air pollution occurs when harmful gases and particles enter the atmosphere.",
     "The presence of dangerous particles and gases in the air causes air pollution."),

    ("Cybersecurity",
     "Cybersecurity protects computer systems and networks from digital attacks.",
     "Digital security safeguards networks and computers against cyber threats."),

    ("Data Privacy",
     "Data privacy concerns how personal information is collected, stored, and shared.",
     "Personal data privacy involves the handling and sharing of people's information."),

    ("Public Health",
     "Public health initiatives aim to prevent disease and improve community well-being.",
     "Community health programs work to reduce illness and support healthier populations."),

    ("Nutrition",
     "A balanced diet provides essential nutrients required for normal body function.",
     "The body needs a variety of nutrients from a balanced diet to function properly."),

    ("Agriculture",
     "Crop rotation helps maintain soil fertility and can reduce pest problems.",
     "Growing different crops in sequence can improve soil health and limit pests."),

    ("Biodiversity",
     "Biodiversity refers to the variety of living organisms in an ecosystem.",
     "The range of different life forms within an ecosystem is called biodiversity."),

    ("Electric Vehicles",
     "Electric vehicles use electric motors powered by rechargeable batteries.",
     "Rechargeable batteries supply energy to the motors in electric cars."),

    ("Cloud Computing",
     "Cloud computing provides computing resources and storage over the internet.",
     "Internet services allow users to access remote computing power and data storage."),

    ("Social Media",
     "Social media platforms allow people to communicate and share information online.",
     "People use online social networks to exchange information and communicate."),

    ("Time Management",
     "Effective time management helps students organise tasks and meet deadlines.",
     "Students can complete work on time by planning and organising their activities."),

    ("Physical Exercise",
     "Regular physical activity can improve cardiovascular fitness and general health.",
     "Consistent exercise supports heart health and overall physical fitness."),

    ("Space Exploration",
     "Space exploration uses scientific instruments to study planets and other celestial objects.",
     "Scientists investigate planets and celestial bodies using space exploration technologies."),

    ("Database Systems",
     "A database organises information so it can be stored, retrieved, and updated efficiently.",
     "Database systems manage information for efficient storage, searching, and modification."),

    ("Research Methods",
     "Researchers collect and analyse evidence to answer specific research questions.",
     "Research involves gathering and examining evidence to investigate defined questions.")
]

rows = []

# 20 exact-copy pairs
for i, (topic, original, paraphrase) in enumerate(topics, 1):
    rows.append({
        "pair_id": f"P{i:03}",
        "document_1": original,
        "document_2": original,
        "similarity_type": "exact_copy",
        "label": 1,
        "source_id_1": f"SRC{i:03}",
        "source_id_2": f"SRC{i:03}",
        "matching_passage": original
    })

# 20 paraphrased pairs
for i, (topic, original, paraphrase) in enumerate(topics, 1):
    rows.append({
        "pair_id": f"P{i+20:03}",
        "document_1": original,
        "document_2": paraphrase,
        "similarity_type": "paraphrased",
        "label": 1,
        "source_id_1": f"SRC{i:03}",
        "source_id_2": f"PAR{i:03}",
        "matching_passage": f"Shared concept: {topic}"
    })

# 60 unrelated pairs, using different academic topics
for n, (i, j) in enumerate(list(combinations(range(20), 2))[:60], 41):
    topic1, text1, para1 = topics[i]
    topic2, text2, para2 = topics[j]

    rows.append({
        "pair_id": f"P{n:03}",
        "document_1": text1,
        "document_2": text2,
        "similarity_type": "unrelated",
        "label": 0,
        "source_id_1": f"SRC{i+1:03}",
        "source_id_2": f"SRC{j+1:03}",
        "matching_passage": ""
    })

# Write the CSV file
filename = "document_similarity_dataset.csv"

with open(filename, "w", newline="", encoding="utf-8-sig") as file:
    columns = [
        "pair_id",
        "document_1",
        "document_2",
        "similarity_type",
        "label",
        "source_id_1",
        "source_id_2",
        "matching_passage"
    ]
    writer = csv.DictWriter(file, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)

print("Dataset created:", filename)
print("Total pairs:", len(rows))
print("Similar pairs:", sum(r["label"] == 1 for r in rows))
print("Unrelated pairs:", sum(r["label"] == 0 for r in rows))
