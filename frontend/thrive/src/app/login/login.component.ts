import { Component, OnInit } from '@angular/core';
import { HttpService } from '../http.service';
import { LoginFormModel } from '../login-form-model';
import {Router} from "@angular/router"
import {MatSnackBar} from '@angular/material/snack-bar';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  loginModel = new LoginFormModel("testUserForRestApi" , "Sarthak123")



  constructor(private _httpService:HttpService, private router: Router, private _snackBar: MatSnackBar) { }

  ngOnInit(): void {
  }

  onSubmit(){
    this._httpService.login(this.loginModel)
    .subscribe(
      data => {
        let jsonObj: any = JSON.parse(JSON.stringify(data));
        let user = jsonObj.user
        this.openSnackBar("Welcome " +  user +'!', "close")
        localStorage.setItem("loggedInUser", user);
        this.router.navigate(['/addGroup'])

    },
      error => {
        console.log("error" , error)
        this.openSnackBar("Email or password wrong", "close");

    }
      );
  }

  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action);
  }

}
