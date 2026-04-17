import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { PromptService, Prompt } from '../../services/prompt.service';

@Component({
  selector: 'app-prompt-detail',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './prompt-detail.component.html',
  styleUrls: ['./prompt-detail.component.css']
})
export class PromptDetailComponent implements OnInit {
  prompt: Prompt | null = null;
  loading = true;

  constructor(
    private route: ActivatedRoute,
    private promptService: PromptService
  ) {}

  ngOnInit() {
    this.route.paramMap.subscribe(params => {
      const id = Number(params.get('id'));
      if (id) {
        this.loadPrompt(id);
      }
    });
  }

  loadPrompt(id: number) {
    this.loading = true;
    this.promptService.getPrompt(id).subscribe({
      next: (data) => {
        this.prompt = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading prompt:', err);
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
