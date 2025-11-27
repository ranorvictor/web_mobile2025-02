import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; // Importante para *ngFor e *ngIf

// Importe TODOS os componentes visuais que vai usar
import { 
  IonContent, 
  IonHeader, 
  IonTitle, 
  IonToolbar, 
  IonList, 
  IonCard, 
  IonCardHeader, 
  IonCardSubtitle, 
  IonCardTitle, 
  IonCardContent 
} from '@ionic/angular/standalone';

import { LivroService } from '../services/livro';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: true, // Garanta que isso está true
  imports: [
    CommonModule, // Necessário para lógica (if/for)
    IonContent, 
    IonHeader, 
    IonTitle, 
    IonToolbar, 
    IonList, 
    IonCard, 
    IonCardHeader, 
    IonCardSubtitle, 
    IonCardTitle, 
    IonCardContent
  ],
})
export class HomePage implements OnInit {

  listaLivros: any[] = [];

  constructor(private livroService: LivroService) {}

  ngOnInit() {
    this.carregarLivros();
  }

  carregarLivros() {
    this.livroService.getLivros().subscribe(
      (data) => {
        console.log('Livros:', data);
        this.listaLivros = data;
      },
      (error) => {
        console.error('Erro:', error);
      }
    );
  }
}