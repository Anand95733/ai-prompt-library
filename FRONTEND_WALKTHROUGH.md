# Frontend Walkthrough - AI Prompt Library

## 🎯 Overview
Angular 19 standalone application with premium glass morphism design, featuring prompt browsing, creation, and live view counting.

## 📁 Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── components/
│   │   │   ├── prompt-list/          # Browse all prompts
│   │   │   ├── prompt-detail/        # View single prompt + views
│   │   │   └── add-prompt/           # Create new prompt
│   │   ├── services/
│   │   │   └── prompt.service.ts     # HTTP API calls
│   │   ├── app.component.ts          # Root component with nav
│   │   └── app.routes.ts             # Route definitions
│   ├── styles.css                    # Global styles
│   ├── main.ts                       # Bootstrap application
│   └── proxy.conf.json               # API proxy config
├── angular.json                      # Angular CLI config
├── package.json                      # Dependencies
└── tsconfig.json                     # TypeScript config
```

## 🚀 Step-by-Step Walkthrough

### Step 1: Application Bootstrap (main.ts)

**File**: `src/main.ts`

```typescript
import { bootstrapApplication } from '@angular/platform-browser';
import { provideRouter } from '@angular/router';
import { provideHttpClient } from '@angular/common/http';
import { AppComponent } from './app/app.component';
import { routes } from './app/app.routes';

bootstrapApplication(AppComponent, {
  providers: [
    provideRouter(routes),      // Enable routing
    provideHttpClient()         // Enable HTTP calls
  ]
}).catch(err => console.error(err));
```

**What happens here:**
1. Bootstraps the Angular app without NgModule (standalone)
2. Provides router for navigation
3. Provides HttpClient for API calls
4. Starts with AppComponent as root

---

### Step 2: Routes Configuration (app.routes.ts)

**File**: `src/app/app.routes.ts`

```typescript
import { Routes } from '@angular/router';
import { PromptListComponent } from './components/prompt-list/prompt-list.component';
import { PromptDetailComponent } from './components/prompt-detail/prompt-detail.component';
import { AddPromptComponent } from './components/add-prompt/add-prompt.component';

export const routes: Routes = [
  { path: '', redirectTo: '/prompts', pathMatch: 'full' },
  { path: 'prompts', component: PromptListComponent },
  { path: 'prompts/:id', component: PromptDetailComponent },
  { path: 'add-prompt', component: AddPromptComponent }
];
```

**Routes:**
- `/` → Redirects to `/prompts`
- `/prompts` → List all prompts
- `/prompts/:id` → View single prompt (e.g., `/prompts/1`)
- `/add-prompt` → Create new prompt

---

### Step 3: Root Component (app.component.ts)

**File**: `src/app/app.component.ts`

**Purpose**: Main layout with header navigation

**Key Features:**
- Header with logo and navigation
- RouterOutlet for child components
- Glass morphism header design
- Sticky positioning

**Template Structure:**
```html
<div class="app-container">
  <header class="header">
    <h1 class="logo">✨ AI Prompt Library</h1>
    <nav>
      <a routerLink="/prompts">Browse</a>
      <a routerLink="/add-prompt">+ Add Prompt</a>
    </nav>
  </header>
  <main>
    <router-outlet></router-outlet>  <!-- Child components render here -->
  </main>
</div>
```

---

### Step 4: Prompt Service (prompt.service.ts)

**File**: `src/app/services/prompt.service.ts`

**Purpose**: Centralized API communication

```typescript
@Injectable({ providedIn: 'root' })
export class PromptService {
  private apiUrl = '/prompts';  // Proxied to backend

  constructor(private http: HttpClient) {}

  // GET /prompts - List all prompts
  getPrompts(): Observable<Prompt[]> {
    return this.http.get<Prompt[]>(this.apiUrl);
  }

  // GET /prompts/:id - Get single prompt (increments views)
  getPrompt(id: number): Observable<Prompt> {
    return this.http.get<Prompt>(`${this.apiUrl}/${id}/`);
  }

  // POST /prompts - Create new prompt
  createPrompt(data: CreatePromptData): Observable<Prompt> {
    return this.http.post<Prompt>(this.apiUrl, data);
  }
}
```

**Interfaces:**
```typescript
export interface Prompt {
  id: number;
  title: string;
  content?: string;
  complexity: number;      // 1-10
  created_at: string;
  view_count?: number;     // Only in detail view
}

export interface CreatePromptData {
  title: string;
  content: string;
  complexity: number;
}
```

---

### Step 5: Prompt List Component

**File**: `src/app/components/prompt-list/prompt-list.component.ts`

**Purpose**: Display all prompts in a grid

**Lifecycle:**
1. `ngOnInit()` → Calls `loadPrompts()`
2. Service fetches data from API
3. Displays in card grid

**Key Features:**
- Card grid layout (responsive)
- Complexity badges with colors:
  - 1-3: Green (easy)
  - 4-6: Orange (medium)
  - 7-10: Red (hard)
- Click card → Navigate to detail
- Loading skeletons while fetching

**Template Structure:**
```html
<!-- Loading State -->
<div *ngIf="loading" class="grid">
  <div class="skeleton-card" *ngFor="let i of [1,2,3,4,5,6]"></div>
</div>

<!-- Empty State -->
<div *ngIf="!loading && prompts.length === 0" class="empty-state">
  <div class="empty-icon">📝</div>
  <h3>No prompts yet</h3>
  <a routerLink="/add-prompt">Create First Prompt</a>
</div>

<!-- Prompt Cards -->
<div *ngIf="!loading && prompts.length > 0" class="grid">
  <a *ngFor="let prompt of prompts" 
     [routerLink]="['/prompts', prompt.id]" 
     class="card">
    <h3>{{ prompt.title }}</h3>
    <span [class]="'complexity-badge ' + getComplexityClass(prompt.complexity)">
      {{ prompt.complexity }}
    </span>
    <span class="date">{{ prompt.created_at | date:'MMM d, y' }}</span>
  </a>
</div>
```

---

### Step 6: Prompt Detail Component

**File**: `src/app/components/prompt-detail/prompt-detail.component.ts`

**Purpose**: Display single prompt with full content and view count

**Lifecycle:**
1. Get `id` from route params
2. Call `getPrompt(id)` → Backend increments Redis counter
3. Display prompt with live view count

**Key Features:**
- Full prompt content
- Live view counter (👁 X views)
- Complexity badge
- Created date
- Back navigation

**Template Structure:**
```html
<div class="container">
  <a routerLink="/prompts">← Back to prompts</a>

  <!-- Loading Skeleton -->
  <div *ngIf="loading" class="detail-skeleton">...</div>

  <!-- Prompt Detail -->
  <div *ngIf="!loading && prompt" class="detail-card">
    <div class="detail-header">
      <h1>{{ prompt.title }}</h1>
      <span class="complexity-badge">Complexity: {{ prompt.complexity }}</span>
    </div>

    <div class="detail-meta">
      <span>📅 {{ prompt.created_at | date:'MMMM d, y' }}</span>
      <span>👁 {{ prompt.view_count }} views</span>  <!-- Live from Redis -->
    </div>

    <div class="detail-content">
      <h3>Prompt Content</h3>
      <p>{{ prompt.content }}</p>
    </div>
  </div>
</div>
```

**How View Counting Works:**
1. User visits `/prompts/1`
2. Frontend calls `GET /prompts/1/`
3. Backend increments Redis key `prompt:1:views`
4. Backend returns prompt + current view count
5. Frontend displays: "👁 5 views"

---

### Step 7: Add Prompt Component

**File**: `src/app/components/add-prompt/add-prompt.component.ts`

**Purpose**: Create new prompts with validation

**Form Setup:**
```typescript
this.promptForm = this.fb.group({
  title: ['', [Validators.required, Validators.minLength(3)]],
  content: ['', [Validators.required, Validators.minLength(20)]],
  complexity: [5, [Validators.required, Validators.min(1), Validators.max(10)]]
});
```

**Validation Rules:**
- **Title**: Required, minimum 3 characters
- **Content**: Required, minimum 20 characters
- **Complexity**: Required, 1-10 range

**Submission Flow:**
1. User fills form
2. Click "Create Prompt"
3. Frontend validates
4. POST to `/prompts`
5. Backend validates again
6. On success → Navigate to `/prompts/:id`
7. On error → Display inline errors

**Template Structure:**
```html
<form [formGroup]="promptForm" (ngSubmit)="onSubmit()">
  <!-- Title Input -->
  <div class="form-group">
    <label for="title">Title</label>
    <input id="title" formControlName="title" />
    <span *ngIf="getFieldError('title')" class="error-message">
      {{ getFieldError('title') }}
    </span>
  </div>

  <!-- Content Textarea -->
  <div class="form-group">
    <label for="content">Prompt Content</label>
    <textarea id="content" formControlName="content" rows="8"></textarea>
    <span *ngIf="getFieldError('content')" class="error-message">
      {{ getFieldError('content') }}
    </span>
  </div>

  <!-- Complexity Input -->
  <div class="form-group">
    <label for="complexity">Complexity (1-10)</label>
    <input id="complexity" type="number" formControlName="complexity" />
    <span class="help-text">Rate: 1 (simple) to 10 (advanced)</span>
    <span *ngIf="getFieldError('complexity')" class="error-message">
      {{ getFieldError('complexity') }}
    </span>
  </div>

  <button type="submit" [disabled]="submitting">
    {{ submitting ? 'Creating...' : 'Create Prompt' }}
  </button>
</form>
```

---

### Step 8: Proxy Configuration

**File**: `src/proxy.conf.json`

**Purpose**: Proxy API calls to backend during development

```json
{
  "/prompts": {
    "target": "http://backend:8000",
    "secure": false,
    "changeOrigin": true
  }
}
```

**How it works:**
- Frontend runs on `http://localhost:4200`
- API calls to `/prompts` → Proxied to `http://backend:8000/prompts`
- Avoids CORS issues in development
- In production, use environment-specific URLs

---

## 🎨 Design System

### Colors
```css
--bg-primary: #0f172a      /* Dark blue background */
--bg-card: #1e293b         /* Card background */
--accent: #6366f1          /* Indigo accent */
--text: #f8fafc            /* Light text */
--text-muted: #94a3b8      /* Muted text */
```

### Complexity Badge Colors
```css
/* 1-3: Green */
.complexity-low {
  background: rgba(34, 197, 94, 0.2);
  color: #4ade80;
  box-shadow: 0 0 20px rgba(34, 197, 94, 0.3);
}

/* 4-6: Orange */
.complexity-medium {
  background: rgba(251, 146, 60, 0.2);
  color: #fb923c;
  box-shadow: 0 0 20px rgba(251, 146, 60, 0.3);
}

/* 7-10: Red */
.complexity-high {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
  box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
}
```

### Glass Morphism Effect
```css
.card {
  background: rgba(30, 41, 59, 0.6);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 1rem;
  transition: all 200ms ease;
}

.card:hover {
  transform: translateY(-4px);
  border-color: rgba(99, 102, 241, 0.5);
  box-shadow: 0 20px 40px rgba(99, 102, 241, 0.2);
}
```

---

## 🧪 Testing the Frontend

### 1. View All Prompts
```
Navigate to: http://localhost:4200/prompts
Expected: Grid of prompt cards
```

### 2. View Prompt Detail
```
Click any prompt card
Expected: Full prompt content + view count
Each visit increments the counter
```

### 3. Create New Prompt
```
Navigate to: http://localhost:4200/add-prompt
Fill form:
  - Title: "Test Prompt" (min 3 chars)
  - Content: "This is a test prompt content" (min 20 chars)
  - Complexity: 5 (1-10)
Click "Create Prompt"
Expected: Redirect to new prompt detail page
```

### 4. Validation Testing
```
Try submitting with:
  - Title: "ab" → Error: "Title must be at least 3 characters"
  - Content: "short" → Error: "Content must be at least 20 characters"
  - Complexity: 11 → Error: "Complexity must be between 1 and 10"
```

---

## 🔧 Development Commands

```bash
# Install dependencies
cd frontend
npm install

# Run dev server (standalone)
npm start
# Access: http://localhost:4200

# Build for production
npm run build
# Output: dist/ai-prompt-library/

# Run with Docker
docker compose up frontend
```

---

## 📦 Key Dependencies

```json
{
  "@angular/core": "^19.0.0",           // Core framework
  "@angular/router": "^19.0.0",         // Routing
  "@angular/forms": "^19.0.0",          // Reactive forms
  "@angular/common": "^19.0.0",         // Common utilities
  "rxjs": "~7.8.0",                     // Reactive programming
  "zone.js": "~0.15.0"                  // Change detection
}
```

---

## 🎯 Key Concepts

### 1. Standalone Components
- No NgModule required
- Import dependencies directly in component
- Cleaner, more modular code

### 2. Reactive Forms
- Form state managed by FormGroup
- Built-in validators
- Real-time validation feedback

### 3. Observables (RxJS)
- Async data streams
- Subscribe to get data
- Automatic cleanup

### 4. Route Parameters
```typescript
// Get ID from URL
const id = Number(this.route.snapshot.paramMap.get('id'));
```

### 5. Angular Pipes
```html
<!-- Format date -->
{{ prompt.created_at | date:'MMM d, y' }}
```

---

## 🚀 Next Steps

1. Open browser: http://localhost:4200
2. Browse existing prompts
3. Click a prompt to see details (watch view count increment!)
4. Create a new prompt
5. Inspect Network tab to see API calls
6. Check Redux DevTools for state (if added)

---

## 💡 Tips

- Use Chrome DevTools → Network tab to see API calls
- Use Angular DevTools extension for debugging
- Check console for errors
- Hot reload works automatically (HMR enabled)
