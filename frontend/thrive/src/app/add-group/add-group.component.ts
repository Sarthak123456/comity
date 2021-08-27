import { Component, OnInit, ElementRef, ViewChild} from '@angular/core';
import {MatSnackBar} from '@angular/material/snack-bar';
import { HttpService } from '../http.service';
import { AddGroup } from '../add-group';
import { Username } from '../username';
import { BankDetails } from '../bank-details';
import { Bidform } from '../bid-form';


@Component({
  selector: 'app-add-group',
  templateUrl: './add-group.component.html',
  styleUrls: ['./add-group.component.css']
})
export class AddGroupComponent implements OnInit {
  // @ViewChild('staticBackdrop') staticBackdrop:ElementRef;

  groupDetails: any = [];
  newGroup = new AddGroup('Test Group' , '1m' , 1000);
  groupId:string ='';
  groupIds:any = [];
  activeGroupCount:number = 0;
  inactiveGroupCount:number = 0;
  completedGroupCount:number = 0;
  userName = new Username("");
  bidForm = new Bidform(0);
  userDetails:any = '';
  showBankDetailsModal:boolean = true;
  loggedInUser:any = '';
  data:any;
  gpayQR!: File;
  paytmQR!: File;
  phonepeQR!: File;
  bankDetails = new BankDetails('' , '' , '');
  formatter = new Intl.NumberFormat(undefined, {
    style: 'currency',
    currency: 'INR',

    // These options are needed to round to whole numbers if that's what you want.
    //minimumFractionDigits: 0, // (this suffices for whole numbers, but will print 2500.10 as $2,500.1)
    //maximumFractionDigits: 0, // (causes 2500.99 to be printed as $2,501)
  });


  constructor(private _snackBar: MatSnackBar, private _httpService:HttpService) { }

  ngOnInit(): void {
    this.getGroups();
  }

  ngAfterContentChecked():void {

    this.groupDetails.forEach((element: any, i:number) => {
      var y = document.getElementById('bidButton' + i );
      if(y && y.style.display !== "none"){
        if(element.minBidAmountUser ===  localStorage.getItem("loggedInUser")){
          if(y){
            y.style.display = "none";
          }
        }

      }
    });


  }

  ngAfterViewInit(){

    // this.staticBackdrop.nativeElement.click();


  }

  setgroupId(id:string){
    this.groupId = id;

  }

  getGroups(){
    this._httpService.getGroups()
    .subscribe(
      data => {
        console.log(data)
        this.groupDetails = [];
        this.groupIds = [];
        this.data = data;
        console.log("getGroups = " ,data);

        this.loggedInUser = localStorage.getItem("loggedInUser");

        console.log("loggedInUser in add group " , this.loggedInUser);

        // let jsonObj: any = JSON.parse(JSON.stringify(data));
      // console.log(jsonObj.groups);
      // let groupDetail = data;
      // this.groupDetails = data;


      // console.log(this.groupDetails);

      // this.groupId = data.g_id\

      this.data.forEach((element: any, i:number) => {
        element.usersInGroup.forEach((user: string|any) => {
          if(user.name === this.loggedInUser){
            // console.log("Users in group " , element.g_id , user.name);

            // console.log("get group element = " , element, this.loggedInUser)
            this.groupIds.push(element.g_id);
            this.groupDetails.push(element);
            if (element.status === 'active'){
              this.activeGroupCount ++;

             } else if(element.status === 'inactive'){
              this.inactiveGroupCount ++;

             } else{
              this.completedGroupCount ++;
             }
            // console.log("groupDetails = " , this.groupDetails);
            return

          }


        });

        // if(element.minBidAmountUser === 'testUserForRestApi'){
          //   var y = document.getElementById('bidButton' + i );
          //   console.log(element.minBidAmountUser);
          //   console.log("index = " , i);
        //   console.log('bidButton' + i );

        //   console.log("y = " , y);
        //   if(y){
        //     y.style.display = "none";
        //   }
        // }

        if(this.groupDetails.length > 0 && this.groupDetails[0].account_number !== undefined && this.groupDetails[0].account_number !== null && this.groupDetails[0].account_number && this.groupDetails[0].ifsc){
          this.showBankDetailsModal = false;
        }
      });
      // this.activeGroupCount= this.groupDetails.length;

  },
    error => {
      console.log("error" , error)
      this.openSnackBar("Email or password wrong " + error.message, "close");

  })

  }

  showBidAmountForms(i:any, g_id:string){
    this.setgroupId(g_id);
    var x = document.getElementById('showBidAmountForm' + i);
    var y = document.getElementById('subscribe' + i );

    if(this.groupDetails[0].superuser == true){


    // var x = document.getElementById("myDIV");
      if (x && x.style.display === "none") {
        x.style.display = "block";
      } else if(x) {
        x.style.display = "none";
      }
  } else{
    if (y && y.style.display === "none") {
      y.style.display = "block";
    } else if(y) {
      y.style.display = "none";
    }


  }
    // this.openSnackBar("Highest Bid user is Sarthak with bid 100", "close");

  }


  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action);
  }

  addGroup(){
    this._httpService.addGroup(this.newGroup, this.loggedInUser)
    .subscribe(
      data => {
        console.log("Added Group" , data)
        this.data = data;

        if(this.data.admin == this.loggedInUser){
          this.groupIds.push(this.data.g_id);
          this.groupDetails.push(data);
        }
        // let jsonObj: any = JSON.parse(JSON.stringify(data));
        // let groupDetail = JSON.parse(jsonObj.groups);

        // this.data.forEach((element: any, i:number) => {
        //   element.usersInGroup.forEach((user: string|any) => {
        //     if(user.name == this.loggedInUser){
        //       console.log("Users in group " , element.g_id , user.name);

        //         // console.log("add group element = " , element, this.loggedInUser)
        //         this.groupIds.push(element.g_id);
        //         this.groupDetails.push(element);
        //         console.log("groupDetails = " , this.groupDetails);
        //         // let groupDetail = jsonObj
        //         // this.groupDetails.push(groupDetail);
        //         // this.groupIds.push(groupDetail.g_id);
        //         return

        //       }
        //     }


        //     );

        //   });
        this.activeGroupCount = this.groupDetails.length;
        this.openSnackBar("Added new group!", "close");
      },
      error => {
        console.log("error" , error)
        this.openSnackBar("Error adding group", "close");

    }
      );
  }

  deleteAllGroups(){
    this._httpService.deleteAllGroups()
    .subscribe(
      data => {
        console.log("Success" , data)
        this.openSnackBar("Deleted all group!", "close");

    },
      error => {
        console.log("error" , error)
        this.openSnackBar("Error deleting group", "close");

    }
      );
    console.log("Deleted all groups");
  }

  deleteGroup(index:number){
    console.log("index =" , index);
    console.log("id =" , this.groupIds[index]);
    let id = this.groupIds[index];
    this._httpService.deleteGroup(id)
    .subscribe(
      data => {
        this.openSnackBar("Deleted group " + id, "close");
        this.groupDetails.splice(index,1);
        this.groupIds.splice(index,1);
        this.activeGroupCount= this.groupDetails.length;
        // this.getGroups();


    },
      error => {
        console.log("error" , error)
        this.openSnackBar("Error deleting group " + id, "close");

    }
      );
    console.log("Deleted group " + id );

  }

  searchUser(){
    this.userDetails="";
    this._httpService.getUsername(this.userName)
    .subscribe(
      data => {
        this.userDetails = data;

    },
      error => {
        console.log("error" , error);
        this.openSnackBar(`User with username {this.userName.user} not found` , "close");

    }
      );

  }

  addUserToGroup(userDetails:any){
    this._httpService.addUserToGroup(userDetails.userName , this.groupId)
    .subscribe(
      data => {
        console.log("Added to group" ,  this.groupId);
        // this.userDetails = data;

    },
      error => {
        console.log("error" , error);
        this.openSnackBar("Error adding group", "close");

    }
      );


  }

  startGroup(index:number){
    let g_id = this.groupIds[index];
    let pendingUsers:string[] = [];
    if(this.showBankDetailsModal){
      this.openSnackBar("Please fill Bank Details", "close");
    } else{

    this._httpService.startGroup(this.loggedInUser , g_id)
    .subscribe(
      data => {
        this.userDetails = data;
        console.log("userDetails = " , data)

        if(this.userDetails.winner == true){
          this.openSnackBar(this.userDetails.name +" winner for round " + this.userDetails.round , "close");

        } else{
          Object.values(data).forEach(user => {pendingUsers.push(user.name)})
          this.openSnackBar(pendingUsers.join(', ') +" pending", "close");

        }

        // this.userDetails = data;
    },
      error => {
        console.log("error" , error);
        this.openSnackBar("Error starting group " + error.message, "close");

    }
      );

  }
}

  bidAmount(){
    console.log(this.bidForm.amount);
    console.log(this.groupId);
    console.log(this.groupDetails)

    var minBidAmount = this.groupDetails.find((item: any) => item.g_id === this.groupId);
    console.log(minBidAmount.bid_amount);

    if(this.bidForm.amount <= minBidAmount.bid_amount){
      this.openSnackBar("Bid amount should be more than "+ "\u20B9"+ minBidAmount.bid_amount , "close");

    } else if(this.bidForm.amount <= minBidAmount.minBidAmount){
      this.openSnackBar("Minimum Bid amount should be "+ minBidAmount.minBidAmount , "close");

    } else if(this.bidForm.amount > minBidAmount.totalAmount){
      this.openSnackBar("Bid can't be more than total amount "+ minBidAmount.totalAmount , "close");

    } else{
      this._httpService.submitBidForm(this.loggedInUser , this.bidForm.amount, this.groupId)
      .subscribe(
        data => {
          // let groupDetail = JSON.parse(JSON.stringify(data));

          this.openSnackBar("Bid submitted successfully", "close");
          // this.userDetails = data;
      },
        error => {
          console.log("error" , error);
          this.openSnackBar("Error submitting bid "+ error.message, "close");

      }
    );

    }

  }


  onGpayImageChanged(event:any){
    this.gpayQR = event.target.files[0];
    console.log(this.gpayQR);
  }
  onPaytmImageChanged(event:any){
    this.paytmQR = event.target.files[0];
    console.log(this.paytmQR);
  }
  onPhonepeImageChanged(event:any){
    this.phonepeQR = event.target.files[0];
    console.log(this.phonepeQR);
  }


  onBankDetails(){
    console.log(this.bankDetails);

    this._httpService.saveBankDetails(this.bankDetails, this.loggedInUser, this.gpayQR, this.phonepeQR, this.paytmQR)
    .subscribe(
      data => {
        console.log("User bank details saved" , data);
        this.openSnackBar("User bank details saved!", "close");
      },
      error => {
        console.log("error" , error)
        this.openSnackBar("Error adding bank details", "close");

    }
      );


  }


}
