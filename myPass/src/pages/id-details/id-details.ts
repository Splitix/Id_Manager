import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';

/**
 * Generated class for the IdDetailsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-id-details',
  templateUrl: 'id-details.html',
})
export class IdDetailsPage {

	color: string;
	id: any;

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  	this.id = navParams.get('data');
  	console.log(this.id);
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad IdDetailsPage');
  }

}
