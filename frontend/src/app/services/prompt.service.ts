import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Prompt {
  id: number;
  title: string;
  content?: string;
  complexity: number;
  created_at: string;
  view_count?: number;
}

export interface CreatePromptData {
  title: string;
  content: string;
  complexity: number;
}

@Injectable({
  providedIn: 'root'
})
export class PromptService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) {}

  getPrompts(): Observable<Prompt[]> {
    return this.http.get<Prompt[]>(`${this.apiUrl}/`);
  }

  getPrompt(id: number): Observable<Prompt> {
    return this.http.get<Prompt>(`${this.apiUrl}/${id}/`);
  }

  createPrompt(data: CreatePromptData): Observable<Prompt> {
    return this.http.post<Prompt>(`${this.apiUrl}/`, data);
  }
}
