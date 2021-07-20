import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AddGroupComponent } from './add-group/add-group.component';
import { LoginComponent } from './login/login.component';
import { MainContentComponent } from './main-content/main-content.component';
import { SignUpComponent } from './sign-up/sign-up.component';
import { ViewGroupComponent } from './view-group/view-group.component';
import { ViewPaymentDetailsComponent } from './view-payment-details/view-payment-details.component';

const routes: Routes = [
  { path: '', component: MainContentComponent },
  { path: 'login', component: LoginComponent },
  { path: 'addGroup', component: AddGroupComponent },
  { path: 'viewGroup', component: ViewGroupComponent },
  { path: 'viewPaymentDetails', component: ViewPaymentDetailsComponent },
  { path: 'signup', component: SignUpComponent }


];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
