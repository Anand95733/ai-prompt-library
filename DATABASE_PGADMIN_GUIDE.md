# Database Access with pgAdmin 4

## 🎯 Overview
This guide shows you how to connect to your PostgreSQL database using pgAdmin 4 to view tables, data, and run queries.

---

## 📥 Step 1: Install pgAdmin 4

### Option A: Download Desktop Application
1. Visit: https://www.pgadmin.org/download/
2. Download for your OS (Windows/Mac/Linux)
3. Install and launch pgAdmin 4

### Option B: Use Docker (Recommended)
Add pgAdmin to your `docker-compose.yml`:

```yaml
services:
  # ... existing services ...

  pgadmin:
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    networks:
      - app-network
    depends_on:
      - db
```

Then run:
```bash
docker compose up -d pgadmin
```

Access pgAdmin at: **http://localhost:5050**

---

## 🔌 Step 2: Connect to Database

### Connection Details

| Field | Value |
|-------|-------|
| **Host** | `db` (if using Docker) or `localhost` (if pgAdmin is local) |
| **Port** | `5432` |
| **Database** | `promptdb` |
| **Username** | `promptuser` |
| **Password** | `promptpass` |

### Using pgAdmin Web (Docker)

1. **Open pgAdmin**: http://localhost:5050
2. **Login**:
   - Email: `admin@admin.com`
   - Password: `admin`

3. **Add New Server**:
   - Right-click "Servers" → "Register" → "Server"

4. **General Tab**:
   - Name: `AI Prompt Library`

5. **Connection Tab**:
   - Host name/address: `db`
   - Port: `5432`
   - Maintenance database: `promptdb`
   - Username: `promptuser`
   - Password: `promptpass`
   - Save password: ✓

6. **Click "Save"**

### Using pgAdmin Desktop (Local)

If pgAdmin is installed locally (not in Docker):

1. **Add New Server**
2. **Connection Tab**:
   - Host name/address: `localhost` (not `db`)
   - Port: `5432`
   - Maintenance database: `promptdb`
   - Username: `promptuser`
   - Password: `promptpass`

---

## 📊 Step 3: Explore the Database

### Navigate to Tables

```
Servers
└── AI Prompt Library
    └── Databases
        └── promptdb
            └── Schemas
                └── public
                    └── Tables
                        ├── auth_user
                        ├── django_migrations
                        ├── prompts_prompt  ← Our main table
                        └── ... (other Django tables)
```

### View Table Structure

1. **Right-click** `prompts_prompt`
2. **Select** "Properties"
3. **Click** "Columns" tab

**Columns**:
| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| id | integer | NO | nextval('prompts_prompt_id_seq') |
| title | character varying(255) | NO | |
| content | text | NO | |
| complexity | integer | NO | |
| created_at | timestamp with time zone | NO | now() |

---

## 🔍 Step 4: View Data

### Method 1: View/Edit Data

1. **Right-click** `prompts_prompt`
2. **Select** "View/Edit Data" → "All Rows"
3. **View** data in spreadsheet format

### Method 2: SQL Query

1. **Click** "Tools" → "Query Tool"
2. **Run queries**:

```sql
-- View all prompts
SELECT * FROM prompts_prompt ORDER BY created_at DESC;

-- Count total prompts
SELECT COUNT(*) FROM prompts_prompt;

-- View prompts by complexity
SELECT complexity, COUNT(*) as count 
FROM prompts_prompt 
GROUP BY complexity 
ORDER BY complexity;

-- Find prompts with specific complexity
SELECT id, title, complexity, created_at 
FROM prompts_prompt 
WHERE complexity >= 7;

-- Search prompts by title
SELECT * FROM prompts_prompt 
WHERE title ILIKE '%AI%';

-- Get recent prompts
SELECT id, title, created_at 
FROM prompts_prompt 
WHERE created_at > NOW() - INTERVAL '1 day';
```

---

## 📝 Step 5: Sample Queries

### Insert Test Data

```sql
-- Insert a single prompt
INSERT INTO prompts_prompt (title, content, complexity, created_at)
VALUES (
    'Write a marketing email',
    'Create a compelling marketing email for a new product launch',
    4,
    NOW()
);

-- Insert multiple prompts
INSERT INTO prompts_prompt (title, content, complexity, created_at)
VALUES 
    ('Generate SQL query', 'Convert natural language to SQL query', 7, NOW()),
    ('Write a poem', 'Create a haiku about technology', 2, NOW()),
    ('Debug Python code', 'Find and fix bugs in Python script', 8, NOW()),
    ('Summarize article', 'Summarize a long article in 3 sentences', 3, NOW());
```

### Update Data

```sql
-- Update a prompt's complexity
UPDATE prompts_prompt 
SET complexity = 5 
WHERE id = 1;

-- Update multiple prompts
UPDATE prompts_prompt 
SET complexity = complexity + 1 
WHERE complexity < 5;
```

### Delete Data

```sql
-- Delete a specific prompt
DELETE FROM prompts_prompt WHERE id = 1;

-- Delete old prompts
DELETE FROM prompts_prompt 
WHERE created_at < NOW() - INTERVAL '30 days';

-- Delete all prompts (careful!)
DELETE FROM prompts_prompt;
```

### Advanced Queries

```sql
-- Get prompts with statistics
SELECT 
    id,
    title,
    complexity,
    LENGTH(content) as content_length,
    created_at,
    AGE(NOW(), created_at) as age
FROM prompts_prompt
ORDER BY created_at DESC;

-- Find average complexity
SELECT AVG(complexity) as avg_complexity FROM prompts_prompt;

-- Get complexity distribution
SELECT 
    CASE 
        WHEN complexity BETWEEN 1 AND 3 THEN 'Easy'
        WHEN complexity BETWEEN 4 AND 6 THEN 'Medium'
        WHEN complexity BETWEEN 7 AND 10 THEN 'Hard'
    END as difficulty,
    COUNT(*) as count
FROM prompts_prompt
GROUP BY difficulty;

-- Full-text search
SELECT * FROM prompts_prompt 
WHERE 
    to_tsvector('english', title || ' ' || content) 
    @@ to_tsquery('english', 'AI & technology');
```

---

## 📈 Step 6: View Database Statistics

### Database Dashboard

1. **Click** on `promptdb` database
2. **Select** "Dashboard" tab
3. **View**:
   - Database size
   - Number of tables
   - Active connections
   - Transaction statistics

### Table Statistics

```sql
-- Table size
SELECT 
    pg_size_pretty(pg_total_relation_size('prompts_prompt')) as total_size,
    pg_size_pretty(pg_relation_size('prompts_prompt')) as table_size,
    pg_size_pretty(pg_indexes_size('prompts_prompt')) as indexes_size;

-- Row count
SELECT COUNT(*) FROM prompts_prompt;

-- Table info
SELECT 
    schemaname,
    tablename,
    tableowner,
    tablespace
FROM pg_tables 
WHERE tablename = 'prompts_prompt';
```

---

## 🔧 Step 7: Useful pgAdmin Features

### 1. Export Data

1. **Right-click** table → "Import/Export Data"
2. **Select** "Export"
3. **Choose** format (CSV, JSON, etc.)
4. **Click** "OK"

### 2. Backup Database

1. **Right-click** `promptdb`
2. **Select** "Backup..."
3. **Choose** filename and format
4. **Click** "Backup"

### 3. Restore Database

1. **Right-click** `promptdb`
2. **Select** "Restore..."
3. **Choose** backup file
4. **Click** "Restore"

### 4. View Query History

1. **Click** "Tools" → "Query History"
2. **View** all executed queries
3. **Re-run** previous queries

### 5. Explain Query Plan

```sql
EXPLAIN ANALYZE
SELECT * FROM prompts_prompt WHERE complexity > 5;
```

---

## 🐛 Troubleshooting

### Cannot Connect to Database

**Error**: `could not connect to server: Connection refused`

**Solutions**:
1. Check Docker containers are running:
   ```bash
   docker compose ps
   ```

2. Check database logs:
   ```bash
   docker compose logs db
   ```

3. Verify connection details match `.env` file

4. If using local pgAdmin, use `localhost` not `db`

### Permission Denied

**Error**: `permission denied for table prompts_prompt`

**Solution**: Ensure you're using the correct username (`promptuser`)

### Database Does Not Exist

**Error**: `database "promptdb" does not exist`

**Solution**: Run migrations:
```bash
docker compose exec backend python manage.py migrate
```

---

## 📊 Monitoring View Counts (Redis)

While pgAdmin shows PostgreSQL data, view counts are stored in Redis. To view them:

### Connect to Redis CLI

```bash
docker compose exec redis redis-cli
```

### View All View Counts

```redis
# List all prompt view keys
KEYS prompt:*:views

# Output:
# 1) "prompt:1:views"
# 2) "prompt:2:views"
# 3) "prompt:3:views"

# Get specific view count
GET prompt:1:views
# Output: "5"

# Get all view counts
MGET prompt:1:views prompt:2:views prompt:3:views
# Output:
# 1) "5"
# 2) "12"
# 3) "3"
```

### Set View Count Manually

```redis
# Set view count
SET prompt:1:views 100

# Increment view count
INCR prompt:1:views

# Decrement view count
DECR prompt:1:views
```

---

## 🎯 Common Tasks

### 1. View All Prompts with Details

```sql
SELECT 
    id,
    title,
    LEFT(content, 50) || '...' as content_preview,
    complexity,
    TO_CHAR(created_at, 'YYYY-MM-DD HH24:MI:SS') as created
FROM prompts_prompt
ORDER BY created_at DESC;
```

### 2. Find Most Complex Prompts

```sql
SELECT * FROM prompts_prompt 
WHERE complexity = (SELECT MAX(complexity) FROM prompts_prompt);
```

### 3. Get Prompts Created Today

```sql
SELECT * FROM prompts_prompt 
WHERE DATE(created_at) = CURRENT_DATE;
```

### 4. Count Prompts by Complexity

```sql
SELECT 
    complexity,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) as percentage
FROM prompts_prompt
GROUP BY complexity
ORDER BY complexity;
```

### 5. Search Prompts

```sql
-- Case-insensitive search
SELECT * FROM prompts_prompt 
WHERE 
    LOWER(title) LIKE '%python%' 
    OR LOWER(content) LIKE '%python%';
```

---

## 📚 Additional Resources

- [pgAdmin Documentation](https://www.pgadmin.org/docs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [Redis CLI Commands](https://redis.io/commands)

---

## 🎓 Practice Exercises

### Exercise 1: Data Analysis
```sql
-- Find the average complexity by month
SELECT 
    DATE_TRUNC('month', created_at) as month,
    AVG(complexity) as avg_complexity,
    COUNT(*) as prompt_count
FROM prompts_prompt
GROUP BY month
ORDER BY month DESC;
```

### Exercise 2: Data Cleanup
```sql
-- Find duplicate titles
SELECT title, COUNT(*) 
FROM prompts_prompt 
GROUP BY title 
HAVING COUNT(*) > 1;
```

### Exercise 3: Performance
```sql
-- Create index for faster searches
CREATE INDEX idx_prompts_complexity ON prompts_prompt(complexity);
CREATE INDEX idx_prompts_created_at ON prompts_prompt(created_at DESC);
```

---

## ✅ Quick Reference

### Connection String
```
postgresql://promptuser:promptpass@localhost:5432/promptdb
```

### Common SQL Commands
```sql
\dt                    -- List tables
\d prompts_prompt      -- Describe table
\l                     -- List databases
\du                    -- List users
\q                     -- Quit
```

### pgAdmin Shortcuts
- `F5` - Execute query
- `F7` - Explain query
- `F8` - Explain analyze
- `Ctrl+Space` - Auto-complete
