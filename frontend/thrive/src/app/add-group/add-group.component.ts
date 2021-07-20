import { Component, OnInit } from '@angular/core';
import {MatSnackBar} from '@angular/material/snack-bar';
import {TooltipPosition} from '@angular/material/tooltip';
import {FormControl} from '@angular/forms';


@Component({
  selector: 'app-add-group',
  templateUrl: './add-group.component.html',
  styleUrls: ['./add-group.component.css']
})
export class AddGroupComponent implements OnInit {

  positionOptions: TooltipPosition[] = ['below', 'above', 'left', 'right'];
  showBidAmountForm:Boolean = false;
  groupDetails = [
    {
      "groupName": "Sarthak's Group 1",
      "groupDuration" : "1 Month",
      "groupMembers" : ["Sarthak" , "Parvez" , "Rana" , "Tarun"],
      "groupStatus" : 0
    },
    {
      "groupName": "Sarthak's Group 4",
      "groupDuration" : "2 Weeks",
      "groupMembers" : ["Sarthak" , "Parvez" , "Rana" , "Tarun"],
      "groupStatus" : 0
    },
    {
      "groupName": "Sarthak's Group 2",
      "groupDuration" : "1 Week",
      "groupMembers" : ["Sarthak" , "Parvez" , "Rana" , "Tarun"],
      "groupStatus" : 1

    },
    {
      "groupName": "Sarthak's Group 3",
      "groupDuration" : "1 Day",
      "groupMembers" : ["Sarthak" , "Parvez" , "Rana" , "Tarun"],
      "groupStatus" : 2

    }
  ]



  constructor(private _snackBar: MatSnackBar) { }

  ngOnInit(): void {

  }

  showBidAmountForms(){

    console.log("Alert me !");
    this.openSnackBar("Highest Bid user is Sarthak with bid 100", "close");
    this.showBidAmountForm = true;


  }

  hideBidAmountForm(){
    this.showBidAmountForm = false;

  }

  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action);
  }

}
