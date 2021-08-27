import { Component, OnInit } from '@angular/core';
import { Signup } from '../signup';
import { HttpService } from '../http.service';
import {MatSnackBar} from '@angular/material/snack-bar';


@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {
  signUp = new Signup("" , '' , '' , '' , '' , '' , '', '' , '');
  constructor(private _snackBar: MatSnackBar, private _httpService:HttpService) { }

  ngOnInit(): void {

  }


  onSignUp(){
    console.log(this.signUp);

    this._httpService.signUpUser(this.signUp)
      .subscribe(
        data => {
          console.log("User signed up" , data);
          this.openSnackBar("Added new user!", "close");
        },
        error => {
          console.log("error" , error)
          this.openSnackBar("Error adding user", "close");

      }
        );


  }

  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action);
  }

}
