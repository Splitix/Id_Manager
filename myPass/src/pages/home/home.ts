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
	data: Observable<any>;

  constructor(public navCtrl: NavController, public httpClient: HttpClient) {
  	this.ids = this.httpClient.get('https://jsonplaceholder.typicode.com/posts/');
  }

  data = {
  	views: '9 Views',
  	title: 'Identification Card'
  };

  goToDetails(data):void {
    data = data || 'No Color Entered';

    console.log("here is the data: " + data);

    this.navCtrl.push(IdDetailsPage, {
      data: data
    });
  }


}


