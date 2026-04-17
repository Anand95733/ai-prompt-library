import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { PromptService, Prompt } from '../../services/prompt.service';

@Component({
  selector: 'app-prompt-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './prompt-list.component.html',
  styleUrls: ['./prompt-list.component.css']
})
export class PromptListComponent implements OnInit {
  prompts: Prompt[] = [];
  loading = true;

  constructor(private promptService: PromptService) {}

  ngOnInit() {
    this.loadPrompts();
  }

  loadPrompts() {
    this.loading = true;
    this.promptService.getPrompts().subscribe({
      next: (data) => {
        this.prompts = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading prompts:', err);
        this.loading = false;
      }
    });
  }

  getComplexityClass(complexity: number): string {
    if (complexity <= 3) return 'complexity-low';
    if (complexity <= 6) return 'complexity-medium';
    return 'complexity-high';
  }
}
