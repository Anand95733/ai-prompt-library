import { Component } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, RouterLink],
  template: `
    <div class="app-container">
      <header class="header">
        <div class="header-content">
          <h1 class="logo">✨ AI Prompt Library</h1>
          <nav class="nav">
            <a routerLink="/prompts" class="nav-link">Browse</a>
            <a routerLink="/add-prompt" class="nav-link nav-link-primary">+ Add Prompt</a>
          </nav>
        </div>
      </header>
      <main class="main-content">
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
  styles: [`
    .app-container {
      min-height: 100vh;
    }

    .header {
      background: rgba(30, 41, 59, 0.8);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      position: sticky;
      top: 0;
      z-index: 100;
    }

    .header-content {
      max-width: 1200px;
      margin: 0 auto;
      padding: 1.5rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .logo {
      font-size: 1.5rem;
      font-weight: 700;
      background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }

    .nav {
      display: flex;
      gap: 1rem;
    }

    .nav-link {
      padding: 0.5rem 1rem;
      border-radius: 0.5rem;
      transition: all 200ms ease;
      font-weight: 500;
    }

    .nav-link:hover {
      background: rgba(99, 102, 241, 0.1);
    }

    .nav-link-primary {
      background: #6366f1;
      color: white;
      box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
    }

    .nav-link-primary:hover {
      background: #818cf8;
      box-shadow: 0 0 30px rgba(99, 102, 241, 0.5);
    }

    .main-content {
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem;
    }
  `]
})
export class AppComponent {}
