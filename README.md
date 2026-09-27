# Nymora — Ask Doubts. Learn Fearlessly.

A free, anonymous study platform for university students. Built with Flask.

## Features

- **Anonymous Q&A** — Ask doubts without fear of judgment
- **Quizzes** — Topic-wise and PYQ practice with explanations
- **Video Playlists** — Ad-free curated YouTube courses with progress tracking
- **Study Materials** — Notes, PDFs, and handouts (admin-verified)
- **Past Papers** — Previous year exam papers
- **Gamified Streaks** — Daily consistency tracker
- **Admin Panel** — Full moderation: users, content, materials, papers

## Tech Stack

- **Backend:** Flask 3.0, SQLAlchemy, Flask-Login, Authlib (Google OAuth)
- **Database:** PostgreSQL (Neon)
- **Storage:** Cloudinary
- **Hosting:** Render
- **Frontend:** Jinja2, TailwindCSS
- **Forms:** Flask-WTF with CSRF protection

## Live Demo

🔗 [https://nymora-anon.onrender.com](https://nymora-anon.onrender.com)

## Local Setup

\`\`\` bash
git clone https://github.com/Maheshranjanpatra/Nymora.git
cd Nymora
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your credentials
flask db upgrade
python run.py
\`\`\`

## Environment Variables

\`\`\`
SECRET_KEY=
DATABASE_URL=postgresql://...
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
ADMIN_USERNAME=
ADMIN_PASSWORD=
YOUTUBE_API_KEY=  # Optional
\`\`\`

## Founder

**Mahesh Ranjan Patra** — Mathematics student, Pondicherry University
[Portfolio](https://mahesh-portfolio-v1.netlify.app)


