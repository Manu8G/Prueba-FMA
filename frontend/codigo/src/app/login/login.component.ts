import { Component } from '@angular/core';
import { CreateSurveyServiceService } from '../services/create_survey/create-survey-service.service';
import { Router } from '@angular/router';
import { Usuario } from '../models/usuario/usuario.module';
import { AuthenticationService } from '../services/authentication/authentication.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrl: './login.component.css'
})
export class LoginComponent {
  title = 'AngularProject';
  
  loginData = {
    name: '',
    password: ''
  };

  data: any = {};
  modifiedData: any;

  constructor(private surveyService: CreateSurveyServiceService, private authenticationService: AuthenticationService, private router: Router) {} //, private cookieService: CookieService

  onSubmit(){
    const usuar: Partial<Usuario>  = {
      name: this.loginData.name,
      password: this.loginData.password
    };
    const usuarJSON = JSON.stringify(usuar);
    this.authenticationService.createToken(usuar);
  }
}
