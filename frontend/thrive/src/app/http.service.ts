import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';


@Injectable({
  providedIn: 'root'
})
export class HttpService {

  url = 'http://127.0.0.1:8000/login';
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

    return this._http.post(this.url , formData);

  }

  getGroups(){
    return this._http.get("http://127.0.0.1:8000/get/groups")
  }

  addGroup(groupData:any, username:string|null){
    const formData = new FormData();
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    if (groupData !== null &&  username !== null){

      formData.set('name' , groupData.name)
      formData.set('duration' , groupData.duration)
      formData.set('amount' , groupData.amount)
      formData.set('user' , username)

    }

    return this._http.post("http://127.0.0.1:8000/addGroup" , formData);
  }

  deleteAllGroups(){

    return this._http.delete("http://127.0.0.1:8000/delete/groups")

  }


  deleteGroup(id:string){

    return this._http.delete("http://127.0.0.1:8000/delete/group/"+id)

  }

  getUsername(userName:any){

    const formData = new FormData();
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    formData.set('user' , userName.user);

    return this._http.post("http://127.0.0.1:8000/get/user/" , formData)
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

    return this._http.post("http://127.0.0.1:8000/add/user/" , formData)
  }

  viewGroup(groupId:string){

    const formData = new FormData();
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    formData.set('g_id' , groupId);

    return this._http.post("http://127.0.0.1:8000/get/group/users/" , formData)

  }

  startGroup(userName:string |null , groupId:string){

    const formData = new FormData();
    let httpOptions = {
        headers: new HttpHeaders({
            'Content-Type': 'multipart/form-data; charset=UTF-8'
        })
    };

    if (userName!== null && userName) {

      formData.set('g_id' , groupId);
      formData.set('username' , userName);

    }


    return this._http.post("http://127.0.0.1:8000/group/start/" , formData)

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


    return this._http.post("http://127.0.0.1:8000/submit/bid" , formData)

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


    return this._http.post("http://127.0.0.1:8000/signup" , formData)

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


    return this._http.post("http://127.0.0.1:8000/bank_details" , formData)

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


    return this._http.post("http://127.0.0.1:8000/get/bank_details" , formData)

  }
}
