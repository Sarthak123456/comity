import { Component, OnInit } from '@angular/core';
import {Title } from "@angular/platform-browser";
import { Router } from '@angular/router';
import { faPhoneAlt, faEnvelopeOpenText} from '@fortawesome/free-solid-svg-icons';
import { faYoutube, faInstagram, faFacebook } from '@fortawesome/free-brands-svg-icons';


@Component({
  selector: 'app-main-content',
  templateUrl: './main-content.component.html',
  styleUrls: ['./main-content.component.css']
})
export class MainContentComponent implements OnInit {
  faq:any;
  faPhoneAlt:any = faPhoneAlt;
  faFacebook:any = faFacebook;
  faInstagram:any = faInstagram;
  faYoutube:any = faYoutube;
  faEnvelopeOpenText:any = faEnvelopeOpenText;

  constructor(private titleService:Title, private router: Router) {
    // const title = this.getTitle(this.router.routerState, this.router.routerState.root).join(' | ');
    const title = ['Home'];
    // console.log(this.titleService.getTitle());
    this.titleService.setTitle(([this.titleService.getTitle() , title]).join(' | '));
    // this.titleService.setTitle("Home");
  }

  // getTitle(state:any, parent:any):any {
  //   const data = [];
  //   if (parent && parent.snapshot.data && parent.snapshot.data.title) {
  //     data.push(parent.snapshot.data.title);
  //   }

  //   if (state && parent) {
  //     data.push(... this.getTitle(state, state.firstChild(parent)));
  //   }
  //   return data;
  // }

  ngOnInit(): void {
    this.faq = [
      {
        "question" : 'What is ROSCA?',
        "answer" : '<strong>ROSCA is an online chit fund platform.</strong> It allows you to create your own group with your friends/family and selects a winner randomly. You can also bid for the money to receive the money that same month.'
      },
      {
        "question" : 'Why choose us?',
        "answer" : "<strong>ROSCA works on a unique 'no commission' model.</strong> It allows user to either use the app for free with randomly selected user or become a <strong>Superuser</strong> @ ₹99 flat without asking for commission from the total pooled amount."
      },
      {
        "question" : 'What commission I have to pay per month?',
        "answer" : "<strong>ROSCA works on a unique 'no commission' model.</strong> You don't need to pay any commission. You have to pay a flat subscription fees of ₹99 if you wish to bid that month otherwise you can also opt for our free model where, winner gets selected randomly and receives money if no bidding takes place."
      },
      {
        "question" :  'Why should I trust ROSCA?',
        "answer" : "<strong>ROSCA doesn't collect the money from the user.</strong> It lets you tranfer the money among yourselves using Gpay, Paytm, Phonepay upi id's and also via Bank account details and never collects the money therefore the money always remain between the group members."
      },
      {
        "question" : 'What if ROSCA turn out to be fraud?',
        "answer" : "<strong> God forbid, if we have to shut down one day then you won't be at loss since you are tranferring the money among yourselves.</strong> It doesn't collect money from the user and the money is always transferred peer-to-peer and is never handled by us."
      },
      {
        "question" : 'What if someone in the group runs away with the money?',
        "answer" : "<strong>ROSCA doesn't take any responsibility of the group members.</strong> Since it gives you the liberty to create your own group it can't take the responsibilty of the users and the user accept this term and condition among others while signing up for the app."
      },
      {
        "question" : 'What is the min and max amount of chit per month per user?',
        "answer" : "<strong>ROSCA allows a minimum of ₹100 and maximum of ₹1,00,000</strong> per user per month. You can opt for a higher chit value after contacting the customer care. The decision rests solely in the hands of Rosca to allow/deny the request."
      },
      {
        "question" : "What if I don't want to bid?",
        "answer" : "<strong>ROSCA works on a unique subscription model.</strong> You can opt to not bid that month and can tranfer the money to the randomly selected winner once the bidding window gets over."
      },
      {
        "question" : "What if I genuinely don't have money this month?",
        "answer" : "<strong>ROSCA doesn't have any say if the users defaults any month.</strong> The users can talk among themselves and come up with an optimal solution to the problem. if not, then any user can contact the customer service and the group will be marked as defaulted from the backend."
      },
      {
        "question" : 'Can I add myself more than once to the same group?',
        "answer" : "<strong>We don't allow any such arrangement as of now.</strong> But in future releases we will come up with it if we get enough queries regarding the same."
      },
      {
        "question" : 'Why choose ROSCA over bank loan/fds etc?',
        "answer" : "<strong>ROSCA works on peer-to-peer model.</strong> It lets you save/borrow money with almost no paper work and therefore you don't hav to pay any commission/interest on the monthly amount as opposed to the bank loan which charge huge interest every month. Moreover, you can even earn some profits if you wish to be a Superuser @₹99 and do competetive bidding."
      },
      {
        "question" : 'Why choose ROSCA when I can opt for loans?',
        "answer" : "<strong>ROSCA doesn't ask for any commission/interest on the monthly amount.</strong> Your group can start saving in just 10 minutes and the money is tranferred by each user directly to your account without any hidden charges."
      }
    ]

  }

}
