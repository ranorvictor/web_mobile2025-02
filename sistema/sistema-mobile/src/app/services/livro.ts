import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LivroService {

  private apiUrl = 'http://20.20.1.147:8000/livro/api/'; 

  constructor(private http: HttpClient) { }

  getLivros(): Observable<any> {
    return this.http.get(this.apiUrl);
  }
}