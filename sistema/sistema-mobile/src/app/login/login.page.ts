import { FormsModule } from '@angular/forms';
import { Storage } from '@ionic/storage-angular';
import { HttpClient, HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { TokenInterceptor } from '../services/token.interceptor';
import { Component, OnInit } from '@angular/core';
import { CapacitorHttp, HttpOptions, HttpResponse } from '@capacitor/core';
import { IonContent, LoadingController, NavController, AlertController, ToastController, IonList, IonItem, IonInput, IonButton } from '@ionic/angular/standalone';
import { Usuario } from './usuario.model';

@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
  standalone: true,
  imports: [IonList, IonItem, IonInput, IonButton, IonContent, FormsModule, HttpClientModule],
  providers: [Storage, { provide: HTTP_INTERCEPTORS, useClass: TokenInterceptor, multi: true }]
})
export class LoginPage implements OnInit {

  constructor(
    public controle_carregamento: LoadingController,
    public controle_navegacao: NavController,
    public controle_alerta: AlertController,
    public controle_toast: ToastController,
    public storage: Storage
  , private http: HttpClient) { }

  async ngOnInit() {
    await this.storage.create();
  }

  public instancia: { username: string, password: string } = {
    username: '',
    password: ''
  };

  async autenticarUsuario() {

    // Inicializa interface com efeito de carregamento
    const loading = await this.controle_carregamento.create({message: 'Autenticando...', duration: 15000});
    await loading.present();

    // Define informações do cabeçalho da requisição
    this.http.post('http://127.0.0.1:8000/autenticacao-api/', this.instancia)
      .subscribe({
        next: async (data: any) => {
          let usuario: Usuario = Object.assign(new Usuario(), data);
          await this.storage.set('usuario', usuario);
          await this.storage.set('auth_token', data?.token);
          loading.dismiss();
          this.controle_navegacao.navigateRoot('/home');
        },
        error: async (erro) => {
          console.error(erro);
          loading.dismiss();
          this.apresenta_mensagem(erro?.status || 400);
        }
      });
  }

  async apresenta_mensagem(codigo: number) {
    const mensagem = await this.controle_toast.create({
      message: `Falha ao autenticar usuário: código ${codigo}`,
      cssClass: 'ion-text-center',
      duration: 2000
    });
    mensagem.present();
  }
}