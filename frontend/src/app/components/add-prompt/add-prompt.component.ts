import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { PromptService } from '../../services/prompt.service';

@Component({
  selector: 'app-add-prompt',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, RouterLink],
  templateUrl: './add-prompt.component.html',
  styleUrls: ['./add-prompt.component.css']
})
export class AddPromptComponent {
  promptForm: FormGroup;
  submitting = false;
  serverErrors: any = {};

  constructor(
    private fb: FormBuilder,
    private promptService: PromptService,
    private router: Router
  ) {
    this.promptForm = this.fb.group({
      title: ['', [Validators.required, Validators.minLength(3)]],
      content: ['', [Validators.required, Validators.minLength(20)]],
      complexity: [5, [Validators.required, Validators.min(1), Validators.max(10)]]
    });

    this.promptForm.valueChanges.subscribe(() => {
      this.serverErrors = {};
    });
  }

  onSubmit() {
    if (this.promptForm.invalid) {
      this.promptForm.markAllAsTouched();
      return;
    }

    this.submitting = true;
    this.serverErrors = {};

    this.promptService.createPrompt(this.promptForm.value).subscribe({
      next: (prompt) => {
        this.router.navigate(['/prompts', prompt.id]);
      },
      error: (err) => {
        this.submitting = false;
        if (err.error?.errors) {
          this.serverErrors = err.error.errors;
        }
      }
    });
  }

  getFieldError(field: string): string | null {
    const control = this.promptForm.get(field);
    if (control?.invalid && (control.dirty || control.touched)) {
      if (control.errors?.['required']) return `${field} is required`;
      if (control.errors?.['minlength']) {
        const min = control.errors['minlength'].requiredLength;
        return `${field} must be at least ${min} characters`;
      }
      if (control.errors?.['min']) return `${field} must be at least 1`;
      if (control.errors?.['max']) return `${field} must be at most 10`;
    }
    return this.serverErrors[field] || null;
  }
}
