import { Component, OnInit } from '@angular/core';
import { Signup } from '../signup';
import { HttpService } from '../http.service';
import {MatSnackBar} from '@angular/material/snack-bar';
import { Title } from '@angular/platform-browser';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent implements OnInit {
  signUp = new Signup("" , '' , '' , '' , '' , '' , parseInt(''), '' , '', false);
  data:any;
  constructor(private _snackBar: MatSnackBar, private _httpService:HttpService, private titleService:Title) {
    const title = ['Sign Up'];
    // console.log(this.titleService.getTitle());
    this.titleService.setTitle(([this.titleService.getTitle() , title]).join(' | '));

   }

  ngOnInit(): void {

  }


  onSignUp(){
    console.log(this.signUp);

    if(!this.signUp.userName){
      this.openSnackBar("Please fill user name!", "close");
    } else if( !this.signUp.lastName ){
      this.openSnackBar("Please fill last name!", "close");
    } else if(this.signUp.mobile == null || this.signUp.mobile  == undefined){
      this.openSnackBar("Please fill mobile number!", "close");
    } else if(this.signUp.mobile.toString(10).split('').length < 10 || typeof(this.signUp.mobile) !== "number"){
      this.openSnackBar("Please enter valid mobile number, don't include country code(+91)", "close");
    } else if( !this.signUp.firstName ){
      this.openSnackBar("Please fill first name !", "close");
    } else if( !this.signUp.email ){
      this.openSnackBar("Please fill email!", "close");
    } else if(this.signUp.email.indexOf('@') === -1 ){
      this.openSnackBar("Please fill valid email!", "close");
    } else if( !this.signUp.addressLine1 ){
      this.openSnackBar("Please fill address line 1!", "close");
    } else if( !this.signUp.addressLine2 ){
      this.openSnackBar("Please fill address line 2!", "close");
    } else if( !this.signUp.password ){
      this.openSnackBar("Please fill password!", "close");
    } else if( !this.signUp.confirmPassword ){
      this.openSnackBar("Please fill confirm password!", "close");
    } else if(this.signUp.confirmPassword !== this.signUp.password){
      this.openSnackBar("Password and Confirm password don't match!", "close");
    } else if(!this.signUp.agreetnc){
      this.openSnackBar("Please agree to out Terms & Conditions", "close");
    }
    // mobile password userName email confirmPassword addressLine1 addressLine2


    else{
      this._httpService.signUpUser(this.signUp)
        .subscribe(
          data => {
            this.data = data;
            if(this.data.message !== 'success'){
              this.openSnackBar(this.data.message, "close");

            }else{
              console.log("User signed up" , this.data);
              this.openSnackBar("Added new user!", "close");
              this.signUp = new Signup("" , '' , '' , '' , '' , '' , parseInt(''), '' , '', false);
              // this.router.navigate(['/login']);
            }
          },
          error => {
            console.log("error" , error)
            this.openSnackBar("Error adding user", "close");

        }
          );

    }



  }

  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action, {"duration": 3000});
  }

}
