import { Component, OnInit,OnChanges, SimpleChanges, DoCheck, AfterContentInit, AfterContentChecked, AfterViewInit, AfterViewChecked, OnDestroy} from '@angular/core';
import {MatSnackBar} from '@angular/material/snack-bar';
import { HttpService } from '../http.service';
import { AddGroup } from '../add-group';
import { Username } from '../username';
import { BankDetails } from '../bank-details';
import { Bidform } from '../bid-form';
import { WindowRefService } from '../window-ref.service';


@Component({
  selector: 'app-add-group',
  templateUrl: './add-group.component.html',
  styleUrls: ['./add-group.component.css']
})
export class AddGroupComponent implements OnInit, OnChanges, DoCheck, AfterContentInit, AfterContentChecked, AfterViewInit, AfterViewChecked, OnDestroy {
  // @ViewChild('staticBackdrop') staticBackdrop:ElementRef;

  // groupDetails: any = [];
  // groupIds:any = [];
  groupId:any = '';


  newGroup = new AddGroup('Test Group' , '1m' , 1000);
  // activeGroupId:string ='';
  // inactiveGroupId:string ='';
  // completedGroupId:string ='';
  activeGroupDetails:any = [];
  inactiveGroupDetails:any =[];
  completedGroupDetails:any =[];
  // activeGroupIds:any = [];
  // inactiveGroupIds:any =[];
  // completedGroupIds:any =[];
  activeGroupCount:number = 0;
  inactiveGroupCount:number = 0;
  completedGroupCount:number = 0;
  userName = new Username("");
  bidForm = new Bidform(0);
  userDetails:any = '';
  showBankDetailsModal:boolean = true;
  showBidForm = false;
  loggedInUser:any = '';
  token:any = '';
  data:any;
  invite:any;
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


  constructor(private _snackBar: MatSnackBar, private _httpService:HttpService, private winRef: WindowRefService) {
  }

  ngOnChanges(changes: SimpleChanges){
    console.log("Called ngOnChanges" , changes);

  }

  ngOnInit(): void {
    this.getGroups();
  }

  ngDoCheck(){
    // console.log("Called ngDoCheck");

  }

  ngAfterContentInit(){
    // console.log("Called ngAfterContentInit");


  }

  ngAfterContentChecked():void {
    this.activeGroupDetails.forEach((element: any, i:number) => {
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
  // this.groupDetails = [];
  // this.groupIds = [];
  // this.activeGroupDetails = [];
  // this.inactiveGroupDetails =[];
  // this.completedGroupDetails =[];
  // this.activeGroupIds = [];
  // this.inactiveGroupIds =[];
  // this.completedGroupIds =[];
  // this.getGroups();
  //   console.log("Called ngAfterViewInit");
  }
  ngAfterViewChecked(){
    // console.log("Called ngAfterViewChecked");
  }

  ngOnDestroy(){
    // console.log("Called ngOnDestroy");

  }


  setgroupId(id:string){
    this.groupId = id;

  }

  getGroups(){
    this._httpService.getGroups(localStorage.getItem("token"))
    .subscribe(
      data => {
        console.log(data)
        // this.groupDetails = [];
        // this.groupIds = [];
        this.data = data;
        this.token = localStorage.getItem("token");
        this.loggedInUser = localStorage.getItem("loggedInUser");
        console.log("loggedInUser in add group " , this.loggedInUser);

      this.data.forEach((element: any, i:number) => {
        element.usersInGroup.forEach((user: string|any) => {
          if(user.username === this.loggedInUser){

            if(user.superuser === true ){
            this.showBidForm = true;
            }
            // console.log("Users in group " , element.g_id , user.name);

            // console.log("get group element = " , element, this.loggedInUser)
            if (element.status === 'active'){
              // this.activeGroupIds.push(element.g_id);
              this.activeGroupDetails.push(element);
              this.activeGroupCount ++;


             } else if(element.status === 'inactive'){
              // this.inactiveGroupIds.push(element.g_id);
              this.inactiveGroupDetails.push(element);
              this.inactiveGroupCount ++;

             } else{
              // this.completedGroupIds.push(element.g_id);
              this.completedGroupDetails.push(element);
              this.completedGroupCount ++;
             }
             if(user.account_number !== undefined && user.account_number !== null && user.account_number && user.ifsc){
              this.showBankDetailsModal = false;
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

      });

      // console.log("getGroups = " ,this.groupDetails[0]);
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
    console.log("activeGroupDetails = " , this.activeGroupDetails)

    // this.getGroups();

    if(this.showBidForm){


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
    this._httpService.addGroup(this.newGroup, localStorage.getItem("token"))
    .subscribe(
      data => {
        console.log("Added Group" , data)
        this.data = data;

        if(this.data.admin === this.loggedInUser){
          console.log("this.data.admin == loggedInUser = " , this.data.admin === this.loggedInUser);
          // this.inactiveGroupIds.push(this.data.g_id);
          this.inactiveGroupDetails.push(data);
          this.inactiveGroupCount ++;


          // this.groupIds.push(this.data.g_id);
          // this.groupDetails.push(data);
        }

        this.inactiveGroupCount = this.inactiveGroupDetails.length;
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

  deleteGroup(index:number, id:any, status:string){
    // console.log("index =" , index);

    // let id = this.inactiveGroupDetails.find((item: any) => item.index === index);
    console.log("id =" , id);

    this._httpService.deleteGroup(id)
    .subscribe(
      data => {
        console.log('delete = ' , data);
        if(status == 'inactive'){
          this.inactiveGroupDetails.splice(index,1);
          // this.inactiveGroupIds.splice(index,1);
          this.inactiveGroupCount= this.inactiveGroupDetails.length;
          this.openSnackBar("Deleted group " + id, "close");

        } else if(status == 'completed'){
          this.completedGroupDetails.splice(index,1);
          // this.completedGroupIds.splice(index,1);
          this.completedGroupCount= this.completedGroupDetails.length;
          this.openSnackBar("Deleted group " + id, "close");

        }

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
        // console.log("Added to group" ,  this.groupId);
        let idx = -1;

        let newItem= this.inactiveGroupDetails.find((item:any, i:any) => {
          // console.log("inactiveGroupDetails = " , item)
          // console.log("inactiveGroupDetails = " , item.g_id )
          // console.log("groupId = " , this.groupId);
          if(item.g_id == this.groupId){
            idx = i;
            return item;
          }
        });

        let index = idx;

        // console.log("newItem.g_id = " , newItem.g_id);
        // console.log("index = " , index);
        // console.log("inactiveGroupDetails = " , this.inactiveGroupDetails);


        // Add to the array
        if(userDetails.userName  !== this.loggedInUser){
          newItem.usersInGroup.push(userDetails);
        }
        // this.inactiveGroupIds.push(newItem.g_id);

        // Remove from the array
        // this.inactiveGroupDetails.splice(index,1);
        // this.inactiveGroupIds.splice(index,1);


        // this.inactiveGroupCount= this.inactiveGroupDetails.length;
        // // this.openSnackBar("Deleted group " + this.groupId, "close");
        // // this.userDetails = data;

    },
      error => {
        console.log("error" , error);
        this.openSnackBar("Error adding group", "close");

    }
      );


  }

  startGroup(index:number, groupId:any){
    let g_id = groupId
    // console.log("groupId = " , groupId);
    console.log("g_id = " , g_id);
    let pendingUsers:string[] = [];
    if(this.showBankDetailsModal){
      this.openSnackBar("Please fill Bank Details", "close");
    } else{

    this._httpService.startGroup(this.token , g_id)
    .subscribe(
      data => {
        this.userDetails = data;
        console.log("userDetails = " , data);

        let idx = -1;

        let newItem = this.inactiveGroupDetails.find((item:any, i:any) => {
          // console.log("inactiveGroupDetails = " , item)
          // console.log("inactiveGroupDetails = " , item.g_id )
          // console.log("inactiveGroupDetails = " , this.groupId);
          if(item.g_id == groupId){
            idx = i;
            return item;
          }
        });

        // let index = idx;

        console.log("newItem.g_id = " , newItem);
        console.log("index = " , idx);
        // console.log("inactiveGroupDetails = " , this.inactiveGroupDetails)


        if(this.userDetails.winner == true){
          if(newItem !== undefined){
            newItem.status = 'active';


            // Add to the array
            this.activeGroupDetails.splice(index,0,newItem);
            // this.activeGroupIds.splice(index,0,newItem.g_id);

            // Remove from the array
            this.inactiveGroupDetails.splice(index,1);
            // this.inactiveGroupIds.splice(index,1);

            this.inactiveGroupCount= this.inactiveGroupDetails.length;
            this.activeGroupCount= this.activeGroupDetails.length;

          }
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
    // console.log(this.bidForm.amount);
    // console.log(this.groupId);
    // console.log(this.groupDetails)

    var minBidAmount = this.activeGroupDetails.find((item: any) => item.g_id === this.groupId);
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

    if(this.gpayQR === undefined && this.paytmQR == undefined && this.phonepeQR == undefined || (this.bankDetails.accountNumber === '' && this.bankDetails.ifsc == '')){
      this.openSnackBar("Please enter atleast 2 payment detail", "close");
    } else{
    this._httpService.saveBankDetails(this.bankDetails, this.loggedInUser, this.gpayQR, this.phonepeQR, this.paytmQR)
    .subscribe(
      data => {
        console.log("User bank details saved" , data);
        console.log("User bank details saved" , this.bankDetails);
        this.openSnackBar("User bank details saved!", "close");
      },
      error => {
        console.log("error" , error)
        this.openSnackBar("Error adding bank details", "close");

    }
      );
  }


  }

  createRzpayOrder(group_id:any) {
    const order_amount = 105 * 100;
    let order_id = ''
    let order_response:any;
    const token = localStorage.getItem("token")
    // calling api to create order_id

    this._httpService.getRazorPayOrderId(group_id , order_amount, token)
    .subscribe(
      data => {

        console.log("got Razor Pay Order Id" , data);
        order_response = data
        if(order_response.createRazorPayOrderId === "True"){
          order_id = order_response.order_id.id;
          console.log("order_id = " , order_id)
        }
        if(order_id !== undefined && order_id !== '' ){
          this.payWithRazor(order_id, order_amount)

        }
      },
      error => {
        console.log("error" , error)
        this.openSnackBar("Error getting Razorpay order id", "close");

    }
      );


  }

  payWithRazor(order_id:any, order_amount:number) {
    // const order_id = '';

    // const order_id = this.createRzpayOrder(group_id)
    console.log("order_id = " , order_id)
    if(order_id !== undefined){
      const options: any = {
        key: 'rzp_test_nu9LsvfHJHqHQx',
        amount: order_amount, // amount should be in paise format to display Rs 1255 without decimal point
        currency: 'INR',
        name: 'Thrive', // company name or product name
        description: 'Monthly subscription',  // product description
        image: 'http://127.0.0.1:8000/static/assets/logo.png', // company logo or product image
        order_id: order_id, // order_id created by you in backend
        modal: {
          // We should prevent closing of the form when esc key is pressed.
          escape: false,
        },
        notes: {
          // include notes if any
        },
        theme: {
          color: '#0c238a'
        }
      };
      options.handler = ((response:any, error:any) => {
        options.response = response;
        // console.log(response);
        const token = localStorage.getItem("token")
        // alert(response.razorpay_payment_id);
        // alert(response.razorpay_order_id);
        // alert(response.razorpay_signature)
        // console.log(options);
        // call your backend api to verify payment signature & capture transaction
        if(response.razorpay_payment_id  && response.razorpay_order_id && response.razorpay_signature && token ){
          this._httpService.saveRazorPayPaymentDetails(response.razorpay_payment_id , response.razorpay_order_id, response.razorpay_signature, token)
          .subscribe(
            data => {
              let paymentResponse:any;

              console.log("saveRazorPayPaymentDetails" , data);
              paymentResponse = data;

              if(paymentResponse.Razorpay_payment == "success"){
                window.location.reload();
                this.openSnackBar("Payment successful", "close");

              } else{
                this.openSnackBar("Payment failed", "close");

              }
              // order_response = data
              // if(order_response.createRazorPayOrderId === "True"){
              //   order_id = order_response.order_id.id;
              //   console.log("order_id = " , order_id)
              // }
              // if(order_id !== undefined && order_id !== '' ){
              //   this.payWithRazor(order_id, order_amount)

              // }
            },
            error => {
              console.log("error" , error)
              this.openSnackBar("Error saving Razorpay payment details ", "close");

          }
            );

        }

      });
      options.modal.ondismiss = (() => {
        // handle the case when user closes the form while transaction is in progress
        console.log('Transaction cancelled.');
      });
      const rzp = new this.winRef.nativeWindow.Razorpay(options);
      rzp.open();

    }
  }

  inviteUserToGroup(){
    const groupId = this.groupId;
    console.log(groupId);

    const details = this.inactiveGroupDetails.find((item:any) => {
      return item.g_id == groupId;

    });
    console.log(details);
    // const url = `https://wa.me/91${number}?text=Hi%20There!`
    // formatter.format(group.totalAmount).split('.')[0]
    // const text = encodeURIComponent(`${details.admin} Invited you to join group with monthly cost of ${details.amount} \n Join: http://localhost:4200/login`);
    const text = encodeURIComponent(`${details.admin} Invited you to join group with monthly cost of ${this.formatter.format(details.amount).split('.')[0]} \n Join: http://localhost:4200/login`);
    const url = `https://wa.me/?text=${text}&lang=en`
    window.open(url, "_blank");
  }


}
