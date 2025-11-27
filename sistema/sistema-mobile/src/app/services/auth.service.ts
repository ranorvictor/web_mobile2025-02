import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Storage } from '@ionic/storage-angular';
import { environment } from '../../environments/environment';

export interface LoginResponse {
  id: number;
  nome: string;
  email: string;
  token: string;
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private storageReady = this.storage.create();
  private TOKEN_KEY = 'auth_token';

  constructor(private http: HttpClient, private storage: Storage) {}

  async getToken(): Promise<string | null> {
    await this.storageReady;
    return await this.storage.get(this.TOKEN_KEY);
  }

  async setToken(token: string): Promise<void> {
    await this.storageReady;
    await this.storage.set(this.TOKEN_KEY, token);
  }

  async clearToken(): Promise<void> {
    await this.storageReady;
    await this.storage.remove(this.TOKEN_KEY);
  }

  login(usuario: string, senha: string) {
    const url = `${environment.apiUrl}/autenticacao-api/`;
    return this.http.post<LoginResponse>(url, { username: usuario, password: senha });
  }

  async logout(): Promise<void> {
    await this.clearToken();
  }
}
