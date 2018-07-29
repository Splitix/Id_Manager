import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';
import { IdDetailsPage } from '../id-details/id-details';

import { Observable } from 'rxjs/Observable';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})

export class HomePage {
	ids: Observable<any>;
	name: string;
	// data: Observable<any>;

  constructor(public navCtrl: NavController, public httpClient: HttpClient) {
  	// this.ids = this.httpClient.get('https://jsonplaceholder.typicode.com/posts/');
  }

  data = [
    {views: '9 Views',title: 'Identification Card', front:'idCard.jpg', back:'idCard_back.png', expires:'01-01-2020', verified:'Sean Thornton', color:'color1.png', exp_status:'exp_bar_good.png'},
    {views: '2 Views',title: 'Birth Certificate', front:'idCard.jpg', back:'idCard_back.png', expires:'00-00-0000', verified:'Joe Smith', color:'color2.png', exp_status:'exp_bar_good.png'},
    {views: '2 Views',title: 'Passport', front:'idCard.jpg', back:'idCard_back.png', expires:'01-01-2018', verified:'Joe Smith', color:'color3.png', exp_status:'exp_bar_bad.png'},
    {views: '7 Views',title: 'MAP Card', front:'map_card.jpg', back:'idCard_back.png', expires:'09-01-2020', verified:'John Doe', color:'color4.png', exp_status:'exp_bar_good.png'},
    {views: '1 Views',title: 'Disability Id', front:'idCard.jpg', back:'idCard_back.png', expires:'09-01-2018', verified:'Chuck Norris', color:'color1.png', exp_status:'exp_bar_soon.png'},
  ];

  goToDetails(data):void {
    data = data || 'No Color Entered';

    console.log("here is the data: " + data);

    this.navCtrl.push(IdDetailsPage, {
      data: data
    });
  }


}


