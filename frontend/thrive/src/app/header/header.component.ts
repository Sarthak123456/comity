import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {

  loggedInUser:string|null = 'None';
  constructor() { }

  ngOnInit(): void {

    this.loggedInUser = localStorage.getItem("loggedInUser");

    // console.log("this.loggedInUser ngOnInit = " ,this.loggedInUser);

  }

  ngAfterContentInit(){


    //   this.loggedInUser = localStorage.getItem("loggedInUser");

    // console.log("this.loggedInUser ngAfterContentInit = " ,this.loggedInUser);



  }

  // ngAfterContentChecked(){
  //   if(this.loggedInUser != undefined || this.loggedInUser != 'None'){
  //     this.loggedInUser = localStorage.getItem("loggedInUser");
  //   }
  //   console.log("this.loggedInUser after checked = " ,this.loggedInUser);

  // }
}
