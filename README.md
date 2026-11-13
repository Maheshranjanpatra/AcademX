<div align="center">
<img src="app/static/images/academx.svg" alt="AcademX logo" width="80" />

# AcademX

**Ask doubts anonymously. Learn effectively.**

A university-focused study platform combining anonymous Q&A, curated video playlists,
practice quizzes, past papers, and study materials in a calm, classic interface.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-4169E1?logo=postgresql&logoColor=white)](https://neon.tech/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-compiled-06B6D4?logo=tailwindcss&logoColor=white)](https://tailwindcss.com/)
[![PWA](https://img.shields.io/badge/PWA-installable-5A0FC8?logo=pwa&logoColor=white)](#-features)
[![Deployed on Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?logo=render&logoColor=white)](https://academx.onrender.com)

[Live Site](https://academx.onrender.com) ·
[Report a Bug](https://github.com/Maheshranjanpatra/AcademX/issues) ·
[Request a Feature](https://github.com/Maheshranjanpatra/AcademX/issues) ·
[Contact](mailto:myprojects.mahesh@gmail.com)

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Environment Variables](#-environment-variables)
- [Project Structure](#-project-structure)
- [Database & Migrations](#-database--migrations)
- [Key Workflows](#-key-workflows)
- [Performance](#-performance)
- [Deployment](#-deployment)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [Privacy](#-privacy)
- [License](#-license)
- [Author](#-author)

---

## 📖 Overview

**AcademX** is a lightweight, mobile-first study platform built for university students. It started from a familiar feeling, hesitating to ask a doubt out loud, and grew into an effort to make asking easier for everyone.

The core idea is simple: give students a **safe, anonymous space** to ask questions, paired with **real study tools** they actually use before exams.

The platform is live, actively maintained, and designed to scale from a single university to many.

---

## ✨ Features

### For Students

| Feature | Description |
|---|---|
| **Anonymous Q&A** | Ask without revealing your identity. Others see a random Nym ID (e.g. `@User_8472`), never your real name. |
| **Peer answers** | Answer questions and let authors mark the most helpful reply as the best answer. |
| **Practice quizzes** | Topic-wise and past-year-pattern MCQs with per-question explanations and a score breakdown. |
| **Video playlists** | YouTube playlists embedded ad-free, with per-video progress tracking. |
| **Past papers (PYQs)** | Admin-verified archive of previous exam papers. |
| **Study materials** | Notes, handouts, syllabus PDFs, and external links. |
| **Community uploads** | Contribute materials, playlists, and papers. Every submission is reviewed before going public. |
| **Learning streaks** | A small gamified egg that cracks and hatches as you finish videos. |
| **Math composer** | Type `$x^2$` and get a live LaTeX preview, plus a symbol palette for beginners. |
| **Guest sign-in** | Choose a department and avatar; receive a random pseudonymous ID without an account credential. |
| **PWA** | Installable to the home screen like a native app. |
| **Responsive UI** | Dedicated mobile bottom navigation and side drawer. |

### For Admins

- **Moderation dashboards** for papers, playlists, and materials, plus Q&A and user management
- **Batch actions** to approve or reject pending submissions
- **Guest management**: disable or delete pseudonymous guest profiles
- **Admin security**: environment-only credentials, CSRF-protected forms, short sessions, and a five-failure/15-minute sign-in limit
- **Review attribution**: paper and material approvals record the reviewing admin and timestamp

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.12 · Flask 3 · Flask-SQLAlchemy · Flask-Migrate |
| **Database** | PostgreSQL (Neon) · SQLAlchemy ORM |
| **Auth** | Anonymous guest sessions · environment-configured admin credentials · Flask-Login |
| **Frontend** | Jinja2 · Tailwind CSS (compiled) · Vanilla JS |
| **Typography** | Inter · Playfair Display |
| **Icons** | Material Symbols Rounded (subset) |
| **Math rendering** | MathJax 3 (lazy-loaded) |
| **File storage** | Backblaze B2 (S3-compatible) |
| **Forms & CSRF** | Flask-WTF · WTForms · CSRFProtect |
| **Hosting** | Render (web) · Neon (database) · Backblaze B2 (files) |
| **PWA** | Service Worker · Web App Manifest |

---

## 🚀 Getting Started

### Prerequisites

- Python **3.12+**
- Node.js **18+** (only for Tailwind compilation)
- A PostgreSQL database (the [Neon](https://neon.tech/) free tier works well)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/Maheshranjanpatra/Nymora.git
cd Nymora
```

**2. Create a virtual environment and install dependencies**

```bash
python3 -m venv venv
source venv/bin/activate        # Linux / macOS
# venv\Scripts\activate         # Windows

pip install --upgrade pip
pip install -r requirements.txt
```

**3. Install Node dependencies and build Tailwind**

```bash
npm install
npm run build:css
```

> The compiled file `app/static/css/tailwind.build.css` **is committed**, so Render can deploy without Node.

**4. Configure environment variables**

Create a `.env` file at the project root and set the variables below.

Fill in your own values. See [Environment Variables](#-environment-variables).

**5. Apply database migrations**

```bash
python -m flask db upgrade
```

**6. Run the app**

```bash
python run.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

---

## 🔐 Environment Variables

Create a `.env` file at the project root:

```dotenv
# Flask (at least 32 random characters)
SECRET_KEY=replace-with-at-least-32-random-characters

# Database (Neon / any Postgres)
DATABASE_URL="postgresql+psycopg://user:password@host/dbname?sslmode=require"

# Admin login (required; use a unique, strong password)
ADMIN_USERNAME=your-admin-username
ADMIN_PASSWORD=your-long-random-admin-password

# Set false only for local HTTP development; use true for HTTPS deployments
SESSION_COOKIE_SECURE=true

# Backblaze B2 (file uploads)
B2_KEY_ID=your-b2-key-id
B2_APPLICATION_KEY=your-b2-application-key
B2_BUCKET_NAME=nymora-uploads
B2_ENDPOINT=https://s3.us-west-004.backblazeb2.com
B2_REGION=us-west-004

# YouTube Data API (optional, for playlist imports)
YOUTUBE_API_KEY=your-youtube-api-key

# Telegram notifications (optional)
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_ADMIN_CHAT_ID=your-telegram-chat-id
```

| Variable | Required | Purpose |
|---|:---:|---|
| `SECRET_KEY` | ✅ | Session signing and CSRF protection |
| `DATABASE_URL` | ✅ | PostgreSQL connection string |
| `ADMIN_USERNAME` / `ADMIN_PASSWORD` | ✅ | Admin-only credentials; password must be at least 16 characters, with no insecure defaults |
| `SESSION_COOKIE_SECURE` | ✅ | Set `true` for HTTPS; use `false` only for local HTTP |
| `B2_*` | ✅ | Backblaze B2 bucket access for uploads |
| `YOUTUBE_API_KEY` | ❌ | Enables playlist imports |
| `TELEGRAM_BOT_TOKEN` / `TELEGRAM_ADMIN_CHAT_ID` | ❌ | Sends admin notifications for new questions and submissions |

> ⚠️ **Never commit `.env`.** It is already listed in `.gitignore`.

---

## 📁 Project Structure

```
Nymora/
├── app/
│   ├── __init__.py            # App factory, blueprint registration
│   ├── config.py              # Config class, DB URL normalization
│   ├── extensions.py          # db, migrate, login_manager, csrf
│   │
│   ├── forms/                 # WTForms (auth, qa, quiz, materials, ...)
│   ├── models/                # SQLAlchemy models
│   │   ├── user.py            # User, username property, anonymous_id
│   │   ├── question.py        # Question, Answer, Tag
│   │   ├── quiz.py            # Quiz, QuizQuestion, QuizAttempt
│   │   ├── video.py           # Playlist, Video, VideoProgress
│   │   ├── paper.py           # Paper (PYQs, admin-moderated)
│   │   ├── material.py        # Material (uploads + external links)
│   │   └── streak.py          # Streak (gamification)
│   │
│   ├── routes/                # Blueprints
│   │   ├── auth.py            # Guest profile creation, admin login, logout
│   │   ├── dashboard.py       # Home dashboard
│   │   ├── qa.py              # List, ask, view, answer, upvote
│   │   ├── quiz.py            # List, attempt, result
│   │   ├── video.py           # Playlists, watch, toggle-complete
│   │   ├── paper.py           # Papers list + upload
│   │   ├── materials.py       # Materials list, upload, my-uploads
│   │   ├── admin.py           # Moderation
│   │   └── pages.py           # Static pages, profile, error pages
│   │
│   ├── static/
│   │   ├── css/               # Compiled Tailwind + custom CSS
│   │   ├── js/                # mobile_nav, math_composer, spinner, ...
│   │   ├── images/            # SVG logo, WebP avatars, favicon
│   │   ├── manifest.json      # PWA manifest
│   │   └── sw.js              # Service Worker
│   │
│   ├── templates/
│   │   ├── base.html          # Root layout, lazy MathJax loader
│   │   ├── navbar.html        # Desktop nav, mobile bottom nav, drawer
│   │   ├── footer.html
│   │   ├── errors/            # 404, 413, 500, offline, slow, timeout
│   │   └── admin/             # Admin templates
│   │
│   └── utils/
│       ├── decorators.py      # admin_required, admin session timeout
│       ├── helpers.py         # B2 save_file, YouTube ID extractor
│       └── validators.py
│
├── migrations/                # Alembic migration history
├── src/input.css              # Tailwind source
├── tailwind.config.js
├── package.json
├── requirements.txt
└── run.py
```

---

## 🗄️ Database & Migrations

AcademX uses Flask-Migrate (Alembic) on top of SQLAlchemy. The anonymous-guest migration permanently removes stored Google subject, email, and registration-number columns after scrubbing historical account names. It retains existing posts and activity with pseudonymous IDs; take a database snapshot before applying it.

```bash
# After changing a model
python -m flask db migrate -m "Describe your change"
python -m flask db upgrade
```

<details>
<summary><b>Resetting a local, empty database</b></summary>

```bash
rm -rf migrations
python -m flask db init
python -m flask db migrate -m "Initial schema"
python -m flask db upgrade
```

</details>

> **Neon note:** `flask db upgrade` runs against the live database. Before applying the anonymization migration, take a secured snapshot for rollback and expire/remove it after validation because it contains the pre-migration identifiers.

---

## 🔄 Key Workflows

### Guest Sign-In

```mermaid
flowchart LR
    A[Choose department + avatar] --> B[Create guest profile]
    B --> C[Assign random User_XXXX ID]
    C --> D[Start guest session]
```

The four-digit ID is a pseudonym, not a credential. Clearing or allowing the browser session to expire loses access to that guest profile.

### Upload & Moderation

```mermaid
flowchart LR
    S[Student uploads] --> P[status = pending]
    P --> R{Admin review}
    R -- Approve --> A[status = approved<br/>visible publicly]
    R -- Reject --> X[status = rejected]
```

Only `status="approved"` items appear in public listings.

### Anonymity Model

- Every user receives a unique `anonymous_id` (e.g. `User_8472`) on signup.
- The application does not collect guest email, Google identity, or registration number.
- Contributions are linked to a pseudonymous profile so ownership and progress can be displayed.
- The `User_0000`–`User_9999` namespace supports at most 10,000 retained profiles.
- New questions and their answers are available immediately. Playlists, papers, and materials remain private until approved by an administrator.

### Math Composer

Any `<textarea class="mc-enabled">` is enhanced automatically with:

- A quick toolbar (x², a/b, √, ∫, ∑, π)
- A symbol palette (Greek letters, operations, arrows)
- A live preview that appears once `$…$` is typed
- `window.loadMathJax()`, a lazy MathJax loader shared with `base.html`

---

## ⚡ Performance

Nymora is deliberately lightweight.

| Optimization | Impact |
|---|---|
| Compiled Tailwind instead of CDN | ~400 KB → ~37 KB per page |
| Lazy MathJax (only when a page contains `$…$`) | ~350 KB saved on ~70% of pages |
| Two font families only (Inter + Playfair) | ~100 KB saved |
| Material Symbols subset to 49 icons | ~90 KB saved |
| SVG logo + WebP avatars | ~150 KB saved |

**Approximate first-load weight**

| Page type | Size |
|---|---|
| Light pages | ~250 KB |
| Math pages | ~600 KB |
| Repeat visits (service worker cache) | ~20 KB |

---

## ☁️ Deployment

### Render (web)

1. Push to `main` on GitHub. Render auto-deploys from `main`.
2. Add every variable from [Environment Variables](#-environment-variables) in the Render dashboard.

### Rebuilding Tailwind before deploy

`tailwind.build.css` is committed. After adding new utility classes to any template:

```bash
npm run build:css
git add app/static/css/tailwind.build.css
git commit -m "Rebuild Tailwind"
git push
```

During development you can run a watcher instead:

```bash
npm run watch:css
```

### Database (Neon)

- Region: `ap-southeast-1` (Singapore)
- Use the **pooled** connection string in `DATABASE_URL`
- Always include `?sslmode=require`

### File storage (Backblaze B2)

- Bucket: `nymora-uploads` (private)
- Files are served through presigned URLs via `get_file_url()` in `utils/helpers.py`
- Default presign expiry: 7 days

---

## 🗺️ Roadmap

**Shipped**

- [x] Guest sign-in with pseudonymous IDs
- [x] Q&A with best-answer marking
- [x] Quizzes with explanations
- [x] Video playlists with progress and streaks
- [x] Past papers with admin moderation
- [x] Study materials (uploads + external links)
- [x] Admin dashboards for all content types
- [x] PWA (installable, offline page)
- [x] Mobile bottom nav and side drawer
- [x] Math composer with live LaTeX preview
- [x] Performance overhaul (Tailwind build, lazy MathJax, WebP, SVG)

**Planned**

- [ ] Rich notification system (toast, in-app)
- [ ] Study groups and subject-wise rooms
- [ ] Offline-capable quiz attempts
- [ ] Email digests of unanswered questions
- [ ] Multi-university support (per-tenant branding)
- [ ] KaTeX migration (~2× faster math rendering)
- [ ] Full-text search across all content

Have an idea? [Open an issue](https://github.com/Maheshranjanpatra/Nymora/issues).

---

## 🤝 Contributing

Nymora is solo-maintained, but issues and pull requests are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push the branch: `git push origin feat/your-feature`
5. Open a Pull Request

If you touched any template, run `npm run build:css` before committing, otherwise stale styles may be deployed.

---

## 🛡️ Privacy

Full details are in the [Privacy Policy](https://nymora-anon.onrender.com/policy).

**In short:**

- Guest sign-in does not collect real names, email, Google identity, or registration numbers.
- Department, avatar, pseudonymous ID, and content/activity associated with that profile are stored.
- A guest ID is not a password; a cleared browser session cannot be recovered.
- Questions and answers are public immediately; papers, materials, and playlists become public only after admin approval.
- See the [Privacy Policy](https://nymora-anon.onrender.com/policy) for hosting and retention details.

---

## 📄 License

This project is provided for educational and academic use. See [`LICENSE`](./LICENSE) if present, or contact the maintainer for commercial or redistribution inquiries.

---

## 👤 Author

**Mahesh Ranjan Patra**
Mathematics, Pondicherry University

[Portfolio](https://mahesh-portfolio-v1.netlify.app) ·
[GitHub](https://github.com/Maheshranjanpatra) ·
[Email](mailto:myprojects.mahesh@gmail.com)

For bugs, open an [issue](https://github.com/Maheshranjanpatra/Nymora/issues). For everything else, email or use the in-app contact form.

---

<div align="center">

**Built with care, a quiet sanctuary for academic inquiry.**

⭐ If Nymora helped you, consider starring the repo.

</div>
