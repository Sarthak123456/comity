import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-about',
  templateUrl: './about.component.html',
  styleUrls: ['./about.component.css']
})
export class AboutComponent implements OnInit {

  allProducts = [
    {
    "name" : "Shoes",
    "price" : "20$"
  },
  {
    "name" : "T-Shirts",
    "price" : "30$"
  },
  {
    "name" : "Jackets",
    "price" : "100$"
  }
]

  constructor() { }

  ngOnInit(): void {

  }

  paymentSuccess(res): any {
    console.log("Payment successfull")
    // On a real app, we must first perform validation on the server by sending a request to rave to verify the transaction before anything else
    // this.serverService.verifyTransaction(res)
}

paymentFailure(): any{
    // Handle payment failure
}

}

