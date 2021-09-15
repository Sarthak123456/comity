import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';


@Injectable({
  providedIn: 'root'
})
export class HttpService {

  base_url = 'https://thrivefund.herokuapp.com/';
  constructor(private _http:HttpClient) { }


  login(loginForm:any){
    const formData = new FormData();
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    formData.set('email' , loginForm.email)
    formData.set('password' , loginForm.password)

    return this._http.post(this.base_url+'/login' , formData);

  }

  getGroups(token:any){
    const formData = new FormData();
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    if (token !== null && token){

      formData.set('token' , token)

    }

    return this._http.post(this.base_url+'get/groups', formData)
  }

  addGroup(groupData:any, token:any){
    const formData = new FormData();
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    if (groupData !== null &&  token !== null){

      formData.set('name' , groupData.name)
      formData.set('duration' , groupData.duration)
      formData.set('amount' , groupData.amount)
      formData.set('token' , token)

    }

    return this._http.post(this.base_url+"/addGroup" , formData);
  }

  deleteAllGroups(){

    return this._http.delete(this.base_url+"/delete/groups")

  }


  deleteGroup(id:string){

    return this._http.delete(this.base_url+"delete/group/"+id)

  }

  getUsername(userName:any){

    const formData = new FormData();
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    formData.set('user' , userName.user);

    return this._http.post(this.base_url+"get/user/" , formData)
  }

  addUserToGroup(userName:any, groupId:string){

    const formData = new FormData();
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    formData.set('username' , userName);
    formData.set('g_id' , groupId);

    return this._http.post(this.base_url+"/add/user/" , formData)
  }

  viewGroup(groupId:string){

    const formData = new FormData();
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    formData.set('g_id' , groupId);

    return this._http.post(this.base_url+"/get/group/users/" , formData)

  }

  startGroup(token:any , groupId:string){

    const formData = new FormData();
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    if (token!== null && token) {

      formData.set('g_id' , groupId);
      formData.set('token' , token);

    }


    return this._http.post(this.base_url+"/group/start/" , formData)

  }

  submitBidForm(userName:string|null, amount:any, groupId:string){

    const formData = new FormData();
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    if(userName!== null && userName){

      formData.set('g_id' , groupId);
      formData.set('username' , userName);
      formData.set('bid_amount' , amount);
    }


    return this._http.post(this.base_url+"/submit/bid" , formData)

  }


  signUpUser(signUp:any){

    const formData = new FormData();
    console.log("signUp in service = "  , signUp.firstName)
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    formData.set('first_name' , signUp.firstName);
    formData.set('last_name' , signUp.lastName);
    formData.set('password' , signUp.confirmPassword);
    formData.set('username' , signUp.userName);
    formData.set('email' , signUp.email);
    formData.set('mobile' , signUp.mobile);
    formData.set('address_line_1' , signUp.addressLine1);
    formData.set('address_line_2' , signUp.addressLine2);
    // console.log(formData.get('first_name'));


    return this._http.post(this.base_url+"/signup" , formData)

  }

  saveBankDetails(bankDetails:any, loggedInUser:any, gpayQr:File, phonepeQr:File, paytmQr:File){

    const formData = new FormData();
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    formData.append('name' ,  loggedInUser);
    formData.append('account_number' , bankDetails.accountNumber);
    formData.append('ifsc' , bankDetails.ifsc);
    formData.append('branch_address' , bankDetails.branchAddress);
    formData.append('gpay_qr' , gpayQr ? gpayQr : '');
    formData.append('paytm_qr' , paytmQr ? paytmQr : '');
    formData.append('phonepe_qr' , phonepeQr ? phonepeQr : '');
    // console.log(formData.get('first_name'));


    return this._http.post(this.base_url+"/bank_details" , formData)

  }

  getBankDetails(winner:string){

    const formData = new FormData();
    console.log("winner in service = "  , winner)
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    formData.append('name' ,  winner);


    return this._http.post(this.base_url+"/get/bank_details" , formData)

  }

  getRazorPayOrderId(group_id:string, order_amount:any, token:any){

    const formData = new FormData();
    console.log("group_id = "  , group_id)
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    formData.append('group_id' ,  group_id);
    formData.append('order_amount' ,  order_amount);
    formData.append('token' ,  token);




    return this._http.post(this.base_url+"/get/razorpay/order_id/" , formData)

  }

  saveRazorPayPaymentDetails(razorpay_payment_id:string, razorpay_order_id:any, razorpay_signature:string, token:any){

    const formData = new FormData();
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    formData.append('razorpay_payment_id' ,  razorpay_payment_id);
    formData.append('razorpay_order_id' ,  razorpay_order_id);
    formData.append('razorpay_signature' ,  razorpay_signature);

    formData.append('token' ,  token);




    return this._http.post(this.base_url+"/get/razorpay/save/" , formData)

  }

  deleteUser(userName:any, groupId:any){
    const formData = new FormData();

    formData.append('username' ,  userName);
    formData.append('g_id' ,  groupId);
    console.log(userName , groupId);

    return this._http.post(this.base_url+"/delete/group/user/" , formData)


  }
}
