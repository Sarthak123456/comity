import { Component, OnInit } from '@angular/core';
import { LoginFormModel } from '../login-form-model';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginModel = new LoginFormModel("" , "")



  constructor() { }

  ngOnInit(): void {
  }

  onSubmit(){
    console.log(this.loginModel);
  }

}
