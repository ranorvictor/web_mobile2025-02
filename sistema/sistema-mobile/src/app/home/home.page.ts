import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; 

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

import { LivroService } from '../services/livro.service';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
  standalone: true, 
  imports: [
    CommonModule, 
    IonContent, 
    IonHeader, 
    IonTitle, 
    IonToolbar, 
    IonList, 
    IonCard, 
    IonCardHeader, 
    IonCardSubtitle, 
    IonCardTitle, 
    IonCardContent,
    HttpClientModule
  ],
})
export class HomePage implements OnInit {

  listaLivros: any[] = [];

  constructor(private livroService: LivroService) {}

  ngOnInit() {
    this.carregarLivros();
  }

  carregarLivros() {
    this.livroService.listar().subscribe(
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