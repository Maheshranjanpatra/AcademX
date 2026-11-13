# SUBJECTS (Grouped by Category = Department)
# Keys match the display names in VALID_DEPARTMENTS (app/forms/auth.py)

SUBJECT_CATEGORIES = {
    # ── Verified (originals) ──
    "Mathematics": [
        "Calculus", "Algebra", "Linear Algebra", "Differential Equations",
        "Real Analysis", "Complex Analysis", "Topology", "Number Theory",
        "Combinatorics", "Graph Theory", "Probability Theory", "Statistics",
        "Mathematical Physics", "Differential Geometry", "Functional Analysis",
        "Applied Mathematics", "Mathematical Logic",
    ],
    "Physics": [
        "Classical Mechanics", "Quantum Mechanics", "Electromagnetism",
        "Thermodynamics", "Statistical Mechanics", "Optics",
        "Solid State Physics", "Nuclear Physics", "Particle Physics",
        "Astrophysics", "Condensed Matter Physics", "Plasma Physics",
        "Fluid Dynamics", "Mathematical Physics",
    ],
    "Statistics": [
        "Probability", "Statistical Inference", "Regression Analysis",
        "Time Series", "Bayesian Statistics", "Machine Learning",
        "Data Science", "Biostatistics", "Econometrics",
        "Nonparametric Statistics", "Multivariate Analysis",
        "Experimental Design", "Sampling Theory",
    ],

    # ── School of Management ──
    "Banking Technology": [
        "Banking Operations", "Financial Technology", "Risk Management",
        "Digital Payments", "Credit Analysis",
    ],
    "Economics": [
        "Microeconomics", "Macroeconomics", "Development Economics",
        "Econometrics", "Public Finance", "International Economics",
        "Indian Economy",
    ],
    "International Business": [
        "International Trade", "Global Marketing", "Cross-Cultural Management",
        "Foreign Exchange", "Export-Import Management",
    ],
    "Management Studies": [
        "Organizational Behaviour", "Marketing Management", "Financial Management",
        "Human Resource Management", "Operations Management", "Business Strategy",
    ],
    "Management Studies (Karaikal)": [
        "Organizational Behaviour", "Marketing Management",
        "Financial Management", "Business Strategy",
    ],
    "Management Studies (Port Blair)": [
        "Organizational Behaviour", "Marketing Management",
        "Financial Management", "Business Strategy",
    ],
    "Tourism Studies": [
        "Tourism Management", "Hospitality Management",
        "Travel Agency Operations", "Tourism Marketing", "Sustainable Tourism",
    ],

    # ── Tamil ──
    "Tamil": [
        "Tamil Language", "Tamil Literature", "Sangam Literature",
        "Modern Tamil Literature", "Tamil Grammar",
    ],

    # ── Physical, Chemical and Applied Sciences ──
    "Applied Psychology": [
        "Cognitive Psychology", "Social Psychology", "Clinical Psychology",
        "Organizational Psychology", "Research Methods",
    ],
    "Chemistry": [
        "Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry",
        "Analytical Chemistry", "Biochemistry", "Spectroscopy",
    ],
    "Coastal Disaster Management": [
        "Disaster Management", "Coastal Zone Management",
        "Climate Change Adaptation", "Risk Assessment", "Emergency Response",
    ],
    "Earth Sciences": [
        "Geology", "Geophysics", "Hydrology", "Mineralogy", "Geochemistry",
    ],

    # ── Life Sciences ──
    "Biochemistry & Molecular Biology": [
        "Cell Biology", "Molecular Biology", "Enzymology",
        "Metabolism", "Genetics",
    ],
    "Bioinformatics": [
        "Computational Biology", "Sequence Analysis",
        "Structural Bioinformatics", "Systems Biology", "Genomics",
    ],
    "Biotechnology": [
        "Genetic Engineering", "Cell Culture", "Industrial Biotechnology",
        "Immunology", "Plant Biotechnology",
    ],
    "Ecology & Environmental Sciences": [
        "Ecology", "Environmental Science", "Biodiversity",
        "Conservation Biology", "Environmental Impact Assessment",
    ],
    "Food Science & Technology": [
        "Food Chemistry", "Food Microbiology", "Food Processing",
        "Nutrition", "Food Safety",
    ],
    "Microbiology": [
        "General Microbiology", "Medical Microbiology",
        "Industrial Microbiology", "Immunology", "Virology",
    ],
    "Ocean Studies & Marine Biology (Port Blair)": [
        "Marine Biology", "Oceanography", "Fisheries Science",
        "Marine Ecology", "Marine Biotechnology",
    ],

    # ── Humanities ──
    "Foreign Languages": [
        "German", "Japanese", "Spanish", "Russian", "Chinese",
    ],
    "English": [
        "English Literature", "British Literature", "American Literature",
        "Postcolonial Literature", "Literary Criticism", "Linguistics",
    ],
    "French": [
        "French Language", "French Literature",
        "Francophone Studies", "French Culture",
    ],
    "Hindi": [
        "Hindi Language", "Hindi Literature", "Hindi Grammar",
        "Modern Hindi Prose",
    ],
    "Philosophy": [
        "Logic", "Ethics", "Metaphysics", "Epistemology",
        "Indian Philosophy", "Western Philosophy",
    ],
    "Physical Education & Sports": [
        "Physical Education", "Sports Science", "Exercise Physiology",
        "Sports Management", "Kinesiology",
    ],
    "Asian Christian Studies": [
        "Christian Theology", "Asian Christianity",
        "Biblical Studies", "Church History",
    ],

    # ── Social Sciences and International Studies ──
    "European Studies": [
        "European History", "European Union Studies",
        "European Politics", "European Culture",
    ],
    "Maritime Studies": [
        "Maritime History", "Maritime Law",
        "Ocean Governance", "Maritime Security",
    ],
    "Study of Social Inclusion": [
        "Social Inclusion", "Marginalized Communities",
        "Social Justice", "Inclusive Policy",
    ],
    "Anthropology": [
        "Physical Anthropology", "Social Anthropology",
        "Cultural Anthropology", "Ethnography", "Archaeological Anthropology",
    ],
    "History": [
        "Ancient India", "Medieval India", "Modern India",
        "World History", "Indian National Movement",
    ],
    "Politics & International Studies": [
        "Political Theory", "Indian Politics", "International Relations",
        "Comparative Politics", "Public Administration",
    ],
    "Social Work": [
        "Social Work Practice", "Community Development",
        "Social Case Work", "Social Policy", "Counselling",
    ],
    "South Asian Studies": [
        "South Asian History", "SAARC Studies",
        "South Asian Politics", "Regional Cooperation",
    ],

    # ── Engineering and Technology ──
    "Pollution Control & Environmental Engineering": [
        "Air Pollution Control", "Water Treatment", "Solid Waste Management",
        "Environmental Engineering", "Environmental Impact",
    ],
    "Computer Science": [
        "Data Structures", "Algorithms", "Operating Systems", "DBMS",
        "Computer Networks", "AI/ML", "Software Engineering",
    ],
    "Computer Science (Karaikal)": [
        "Data Structures", "Algorithms", "Operating Systems", "DBMS",
        "Computer Networks", "Software Engineering",
    ],
    "Electronics Engineering": [
        "Digital Electronics", "Analog Electronics", "VLSI Design",
        "Signal Processing", "Communication Systems", "Embedded Systems",
    ],

    # ── Education ──
    "Adult & Continuing Education": [
        "Adult Education", "Lifelong Learning",
        "Continuing Education", "Non-formal Education",
    ],
    "Education": [
        "Educational Psychology", "Pedagogy", "Curriculum Design",
        "Educational Technology", "Assessment",
    ],

    # ── Performing Arts / Law / Media ──
    "Performing Arts": [
        "Music", "Dance", "Theatre Arts",
        "Performing Arts Theory", "Stagecraft",
    ],
    "Law": [
        "Constitutional Law", "Criminal Law", "Civil Law",
        "Corporate Law", "International Law", "Jurisprudence",
    ],
    "Electronic Media & Mass Communication": [
        "Journalism", "Mass Communication", "Broadcasting",
        "Digital Media", "Media Ethics",
    ],
    "Library & Information Science": [
        "Library Science", "Information Science", "Digital Libraries",
        "Cataloguing", "Information Retrieval",
    ],

    # ── Green Energy ──
    "Nano Sciences & Technology": [
        "Nanomaterials", "Nanotechnology", "Nanomedicine",
        "Nanoelectronics", "Nanofabrication",
    ],
    "Green Energy Technology": [
        "Solar Energy", "Wind Energy", "Bioenergy",
        "Energy Storage", "Sustainable Energy",
    ],

    # ── Legacy (kept for backward compatibility) ──
    "Biology [legacy]": [
        "General Biology", "Cell Biology", "Genetics",
        "Ecology", "Evolution", "Botany", "Zoology",
    ],
    "ITEP [legacy]": [
        "Pedagogical Subjects", "Foundation Courses",
        "Curriculum Studies", "Educational Psychology", "Teaching Practicum",
    ],

    # ── Catch-all ──
    "Other": ["Other"],
}

SUBJECT_CHOICES = [(subject, subject) for category, subjects in SUBJECT_CATEGORIES.items() for subject in subjects]

ALL_SUBJECTS = sorted([subject for subjects in SUBJECT_CATEGORIES.values() for subject in subjects])

POPULAR_TAGS = [
    # Mathematics
    "calculus", "algebra", "differential-equations", "linear-algebra",
    "real-analysis", "complex-analysis", "topology", "number-theory",
    "combinatorics", "graph-theory", "probability", "statistics",
    "mathematical-physics", "differential-geometry", "functional-analysis",
    "applied-mathematics", "mathematical-logic",
    # Physics
    "classical-mechanics", "quantum-mechanics", "electromagnetism",
    "thermodynamics", "statistical-mechanics", "optics", "solid-state-physics",
    "nuclear-physics", "particle-physics", "astrophysics", "condensed-matter",
    "plasma-physics", "fluid-dynamics",
    # Statistics
    "statistical-inference", "regression-analysis", "time-series",
    "bayesian", "machine-learning", "data-science", "biostatistics",
    "econometrics", "nonparametric", "multivariate-analysis",
    "experimental-design", "sampling-theory",
    # General
    "gk", "competitive-exams", "study-materials", "exam-papers",
    "notes", "seminar", "project",
]
