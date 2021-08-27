import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { HttpService } from '../http.service';


@Component({
  selector: 'app-view-payment-details',
  templateUrl: './view-payment-details.component.html',
  styleUrls: ['./view-payment-details.component.css']
})
export class ViewPaymentDetailsComponent implements OnInit {
  winner:any = '';
  data:any;

  constructor(private route: ActivatedRoute, private _httpService:HttpService) { }

  ngOnInit(): void {
    this.winner = this.route.snapshot.paramMap.get('winner') ? this.route.snapshot.paramMap.get('winner') : '';
    console.log("Winner in payment = " , this.winner);
    this.getPaymentDetailsByUsername();

  }


  getPaymentDetailsByUsername(){


    if(this.winner){
      this._httpService.getBankDetails(this.winner)
      .subscribe(
        data => {
          this.data = data;
          console.log("User bank details " , this.data);
          // this.openSnackBar("User bank details saved!", "close");
        },
        error => {
          console.log("error" , error)
          // this.openSnackBar("Error adding bank details", "close");

      }
        );
    }
  }

}
