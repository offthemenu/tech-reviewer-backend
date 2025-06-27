# 🛠️ Tech Reviewer Backend

This is the FastAPI backend for the **wA Frontend Technical Reviewer** web app. It handles PDF upload, wireframe metadata, and user comments for technical UI reviews. The app is deployed using **Render** (backend + SQLite) and **Vercel** (frontend React app).

---

## 🌐 Tech Stack

- **Backend**: FastAPI  
- **Database**: SQLite3 (Render persistent disk)  
- **Deployment**: Render (with disk mount at `/data`)  
- **CSV Import**: `import_wireframes.py` to populate the wireframe table

---

## ⚙️ Features

- RESTful API for:
  - Wireframe dropdown metadata
  - Comment submission and retrieval
  - PDF upload and retrieval
- CORS support for Vercel frontend
- Auto-imports wireframe data if DB is empty (via lifespan hook)
- Markdown + PDF export support for comments

---

## 🗃️ Folder Structure

```
backend/
│
├── routers/                 # FastAPI route definitions
│   ├── wireframe.py
│   ├── comment.py
│   └── upload.py
│
├── data/                    # Contains wireframe_data.csv
│
├── models.py                # SQLAlchemy models
├── database.py              # Engine/session setup with Render-aware config
├── import_wireframes.py     # CSV import logic for wireframes
├── main.py                  # App entry point (uses lifespan for CSV import)
├── requirements.txt
└── .env                     # Optional local dev config
```

---

## 🚀 Render Deployment Steps

1. **Connect GitHub repo**
2. **Set Environment Variable**: `RENDER=true`
3. **Add disk**: mount at `/data` with `1GB`
4. **Pre-Deploy Command**:
   ```bash
   python -m import_wireframes
   ```
5. **Start Command**:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 10000
   ```

---

## 🧪 API Endpoints

### 📄 Wireframe Dropdowns  
`GET /v01/wireframe`  
Returns project → device → page metadata structure.

### 💬 Comments  
- `POST /v01/add_comment`  
- `GET /v01/comments?project=...&device=...`  
- `DELETE /v01/comment/:id`

### 🧾 Uploads  
- `POST /v01/upload_pdf`  
- `GET /uploads/<filename>`

---

## 🐛 Painpoints Solved

| Issue | Fix |
|------|-----|
| `axios` not resolving env vars | Ensure `.env` uses `VITE_API_BASE_URL` and Vercel has `VITE_` prefix |
| SQLite db not persisting | Created Render disk mounted at `/data` and updated DB URL dynamically |
| Wireframes not importing | Used absolute path in `import_wireframes.py` and verified during lifespan |
| GET `/wireframe` returned empty | Ensured the DB import runs at app startup, not just during pre-deploy |
| Git origin error | Resolved via `git remote remove origin` |
| Comments not persisting | Confirmed correct DB file was being written to: `/data/reviewer.db` |
| `on_event` deprecated | Migrated to `lifespan` with `@asynccontextmanager` |
| `html2pdf.js` missing types | Used a `declare module` workaround |
| Vercel still using localhost | Verified `.env` build settings with `VITE_API_BASE_URL` |

---

## 🔒 Optional: Password Protect Frontend

Use a wrapper component in the frontend to require password entry once per hour via `localStorage`.

---

## 📅 Last Updated

June 27, 2025