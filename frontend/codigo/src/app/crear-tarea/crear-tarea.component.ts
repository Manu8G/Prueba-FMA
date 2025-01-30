import { Component } from '@angular/core';
import { UsuarioService } from '../services/usuario/usuario.service';
import { Usuario } from '../models/usuario/usuario.module';
import { Paciente } from '../models/paciente/paciente.module';
import { FormControl } from '@angular/forms';
import { ToastrService } from 'ngx-toastr';
import { Router } from '@angular/router';

@Component({
  selector: 'app-crear-tarea',
  templateUrl: './crear-tarea.component.html',
  styleUrl: './crear-tarea.component.css'
})
export class CrearTareaComponent {
  data: any = {};
  modifiedData: any;
  showPacienteFields = false;
  myControl = new FormControl('');
  tipos: string[] = ['admin','profesional','paciente'];

  constructor(private usuarioService: UsuarioService, private router: Router, private toastr: ToastrService) {}

  onTipoUsuarioChange(): void {
    this.showPacienteFields = String(this.myControl.value) == 'paciente';
  }

  onSubmit(): void {
    if(String(this.myControl.value) == 'paciente'){
      
      const usuario: Paciente  = {
        nombre_y_apellidos: this.data.name,
        password: this.data.password,
        role: String(this.myControl.value),
        dni: this.data.dni,
        estado: this.data.estado,
        nacionalidad: this.data.nacionalidad,
        fecha_nacimiento: String(this.data.nacimiento),
        email: this.data.email
      };
      this.usuarioService.createPatientUser(usuario).subscribe({
        next: (response) => {
          this.modifiedData = response;
          let mensaje = this.data.name + ' se creo con exito'
          this.toastr.success(mensaje,'Usuario creado');
          this.router.navigate(['/modify_user'])
        },
        error: (err) => {
          this.toastr.error('No se pudo crear el usuario', 'Error');
          console.error('Error:', err);
        }
      });

    }else{
      const usuario: Usuario  = {
        name: this.data.name,
        password: this.data.password,
        role: String(this.myControl.value),
        accessToken: ''
      };
      
      this.usuarioService.createUser(usuario).subscribe({
        next: (response) => {
          this.modifiedData = response;
          let mensaje = this.data.name + ' se creo con exito'
          this.toastr.success(mensaje,'Usuario creado');
          this.router.navigate(['/modify_user'])
        },
        error: (err) => {
          this.toastr.error('No se pudo crear el usuario', 'Error');
          console.error('Error:', err);
        }
      });
    }
    
  }  
}
