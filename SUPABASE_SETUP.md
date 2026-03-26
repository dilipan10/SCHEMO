# Supabase Setup Guide for Schemo

## What You Need to Do in Supabase Dashboard

### Step 1: Create a Supabase Project
1. Go to https://supabase.com
2. Sign up or log in
3. Click "New Project"
4. Choose a project name (e.g., "schemo")
5. Set a strong database password
6. Select a region (choose closest to India for best performance)
7. Wait 2-3 minutes for project to be ready

### Step 2: Run the Schema SQL
1. In your Supabase dashboard, go to **SQL Editor** (left sidebar)
2. Click "New Query"
3. Copy the entire contents of `database/schema.sql`
4. Paste into the SQL editor
5. Click "Run" (or press Ctrl+Enter)
6. You should see: "Success. No rows returned"

This creates all 3 tables: `users`, `admins`, `schemes` with sample data.

### Step 3: Get Your Credentials
1. Go to **Project Settings** (gear icon in left sidebar)
2. Click **API** tab
3. You'll see two important values:

   - **Project URL**: looks like `https://xxxxx.supabase.co`
   - **Service Role Key**: long string starting with `eyJ...` (click "Reveal" to see it)

⚠️ **IMPORTANT**: Use the **service_role** key, NOT the anon key. The service role bypasses Row Level Security which is what the backend needs.

### Step 4: Update Your .env File
Open `.env` in your project root and replace:

```
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS...
```

Keep your existing `FLASK_SECRET_KEY` and `GEMINI_API_KEY` as is.

## What to Give Me

Once you've completed the steps above, provide me with:

1. **SUPABASE_URL** - Your project URL
2. **SUPABASE_KEY** - Your service role key (the long one)

I'll update your `.env` file and test the connection.

## Verify It Works

After I update your `.env`, I'll restart the Flask server and you should see:
- No more MySQL connection errors
- "Default admin created" message on first run
- App accessible at http://127.0.0.1:5000

## What Changed

- ✅ MySQL → PostgreSQL (Supabase)
- ✅ `mysql-connector-python` → `supabase-py`
- ✅ All SQL queries converted to Supabase client calls
- ✅ Schema converted to PostgreSQL syntax
- ✅ All function names kept identical (no changes to routes.py needed)
- ✅ Werkzeug password hashing unchanged
- ✅ Eligibility matching logic preserved
