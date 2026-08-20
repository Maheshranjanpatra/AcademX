# SUBJECTS (Grouped by Category)

SUBJECT_CATEGORIES = {
    "Mathematics": [
        "Calculus",
        "Algebra",
        "Linear Algebra",
        "Differential Equations",
        "Real Analysis",
        "Complex Analysis",
        "Topology",
        "Number Theory",
        "Combinatorics",
        "Graph Theory",
        "Probability Theory",
        "Statistics",
        "Mathematical Physics",
        "Differential Geometry",
        "Functional Analysis",
        "Applied Mathematics",
        "Mathematical Logic",
    ],
    "Physics": [
        "Classical Mechanics",
        "Quantum Mechanics",
        "Electromagnetism",
        "Thermodynamics",
        "Statistical Mechanics",
        "Optics",
        "Solid State Physics",
        "Nuclear Physics",
        "Particle Physics",
        "Astrophysics",
        "Condensed Matter Physics",
        "Plasma Physics",
        "Fluid Dynamics",
        "Mathematical Physics",
    ],
    "Statistics": [
        "Probability",
        "Statistical Inference",
        "Regression Analysis",
        "Time Series",
        "Bayesian Statistics",
        "Machine Learning",
        "Data Science",
        "Biostatistics",
        "Econometrics",
        "Nonparametric Statistics",
        "Multivariate Analysis",
        "Experimental Design",
        "Sampling Theory",
    ],
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
