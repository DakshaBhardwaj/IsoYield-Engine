# Deployment Guide: IsoYield Engine

This guide provides step-by-step instructions to deploy the **IsoYield Engine** 100% for free using **Render** (for the FastAPI + GLPK backend) and **Streamlit Community Cloud** (for the interactive frontend dashboard).

---

## Architecture Overview

```
[ User Browser ] ───> [ Streamlit Community Cloud ] (Frontend Dashboard)
                              │
                              │ REST API Requests
                              ▼
                      [ Render Web Service ] (FastAPI Backend + GLPK Solver)
```

---

## Phase 1: Deploy the FastAPI Backend on Render (Free)

Render will host the FastAPI backend engine inside a container that automatically installs the GLPK linear programming solver.

### Step 1.1: Sign Up / Log In to Render
1. Go to [https://render.com](https://render.com).
2. Sign up or log in using your GitHub account (**DakshaBhardwaj**).

### Step 1.2: Create a New Web Service
1. On your Render Dashboard, click **New +** in the top right corner.
2. Select **Web Service**.
3. Choose **Build and deploy from a Git repository** and click **Next**.
4. Connect your GitHub account if prompted, and select the **`IsoYield-Engine`** repository.

### Step 1.3: Configure the Web Service
Fill in the deployment settings as follows:
* **Name**: `isoyield-backend` (or any unique name you prefer)
* **Region**: Choose the closest region to you (e.g., Singapore, Oregon, Frankfurt)
* **Branch**: `main`
* **Root Directory**: (Leave blank)
* **Runtime**: **Docker**
* **Instance Type**: **Free** ($0 / month)

### Step 1.4: Deploy Backend
1. Click **Create Web Service** at the bottom.
2. Render will pull the repository, read the `Dockerfile`, install `glpk-utils`, and launch the FastAPI server.
3. Wait 2-3 minutes for the build to finish. Once live, you will see a status badge marked **Live**.
4. Copy your Backend URL from top of the page. It will look like:
   `https://isoyield-backend.onrender.com`

---

## Phase 2: Deploy the Dashboard on Streamlit Community Cloud (Free)

Streamlit Community Cloud will host the frontend dashboard and communicate with your live Render backend.

### Step 2.1: Sign Up / Log In to Streamlit Cloud
1. Go to [https://share.streamlit.io](https://share.streamlit.io).
2. Click **Continue with GitHub** and authorize your account.

### Step 2.2: Create a New App
1. Click **Create app** (or **New app**) in the top right.
2. Choose **I already have an app**.

### Step 2.3: Configure App Settings
Fill in the repository details:
* **Repository**: `DakshaBhardwaj/IsoYield-Engine`
* **Branch**: `main`
* **Main file path**: `src/dashboard/app.py`
* **App URL** (Optional): `isoyield-engine` (or leave default)

### Step 2.4: Set Environment Variables (Secrets)
Before clicking deploy, connect Streamlit to your Render backend:
1. Click **Advanced settings...** at the bottom of the form (or open **Settings > Secrets**).
2. In the **Secrets** text box, add your Render API URL (replace with your actual Render URL + `/optimize`):

```toml
API_URL = "https://isoyield-backend.onrender.com/optimize"
```

3. Click **Save**.

### Step 2.5: Deploy Frontend
1. Click **Deploy!**.
2. Streamlit Cloud will install dependencies from `requirements.txt` and launch your dashboard.
3. Once ready, your app will be live at a URL like:
   `https://isoyield-engine.streamlit.app`

---

## Phase 3: Push Local Changes to GitHub

Ensure all deployment configurations (`Dockerfile`, updated `API_URL` logic, and `DEPLOYMENT.md`) are pushed to your GitHub repository:

```bash
git add .
git commit -m "chore: add Dockerfile, dynamic API_URL, and DEPLOYMENT.md for cloud hosting"
git push origin main
```

---

## Troubleshooting & Tips

- **Render Free Tier Cold Starts**: On Render's free tier, Web Services go to sleep after 15 minutes of inactivity. The first API request after a period of idle time may take ~30-50 seconds to wake up the server. Subsequent requests will return in `< 50ms`.
- **Verifying Backend Health**: You can open `https://your-backend-name.onrender.com/docs` in your browser to inspect the live FastAPI OpenAPI documentation.
