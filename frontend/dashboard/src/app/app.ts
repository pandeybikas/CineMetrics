import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],
  templateUrl: './app.html',
<<<<<<< HEAD
  styleUrl: './app.css'
=======
  styleUrl: './app.scss'
>>>>>>> aec07ea73961790d85e1fa777ecae8e988c86af8
})
export class App {
  protected readonly title = signal('dashboard');
}
