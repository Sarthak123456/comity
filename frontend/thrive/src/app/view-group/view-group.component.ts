import { Component, Input, OnInit } from '@angular/core';
import { HttpService } from '../http.service';
import { ActivatedRoute } from '@angular/router';

export interface PeriodicElement {
  name: string;
  winner: number;
  start_comity: string;
  round:number
  bid_amount: number;
}

@Component({
  selector: 'app-view-group',
  templateUrl: './view-group.component.html',
  styleUrls: ['./view-group.component.css']
})
export class ViewGroupComponent implements OnInit {


  displayedColumns: string[] = ['name' , 'winner' , 'start_comity', 'bid_amount' , 'round'];

  ELEMENT_DATA: any = [];
  dataSource:any = [];

  groupId = ''

  users:any;
  constructor( private _httpService:HttpService , private route:ActivatedRoute) { }

  ngOnInit(): void {

    this.groupId = this.route.snapshot.params.groupId;
    this.viewGroup();
  }

  viewGroup(){

    this._httpService.viewGroup(this.groupId)
    .subscribe(
      data => {

      this.ELEMENT_DATA = data;
      // console.log(this.ELEMENT_DATA);
      // console.log(this.dataSource);
      // let jsonObj: any = JSON.parse(JSON.stringify(data));
      // console.log(JSON.parse(jsonObj.data));

      // this.users = JSON.parse(jsonObj.users.replaceAll("'" , '"'));

      // this.users = data;
      this.dataSource = this.ELEMENT_DATA;


  },
    error => {
      console.log("error" , error)
  })
  }



}
