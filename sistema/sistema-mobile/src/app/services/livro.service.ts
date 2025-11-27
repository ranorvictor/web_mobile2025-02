import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

export interface Livro {
  id: number;
  genero: number;
  titulo: string;
  sinopse?: string;
  ano: number;
  autor: number;
  editora: number;
  foto?: string;
}

@Injectable({ providedIn: 'root' })
export class LivroService {
  private baseUrl = `${environment.apiUrl}/livro/api/v1/livros`;

  constructor(private http: HttpClient) {}

  listar() {
    return this.http.get<Livro[]>(`${this.baseUrl}/`);
  }
}
