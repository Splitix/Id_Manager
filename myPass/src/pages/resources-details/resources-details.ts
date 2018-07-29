import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { ContactDetailsPage } from '../contact-details/contact-details';

/**
 * Generated class for the ResourcesDetailsPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-resources-details',
  templateUrl: 'resources-details.html',
})
export class ResourcesDetailsPage {
	options:any = [
		{name:'Medicare Card', abv:'medicare', value:false},
		{name:'Check Stubs', abv:'paystub', value:false}
	]
	show:boolean = true;
	data:any;

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  	this.data = navParams.get('data');
  }

  checkbox(value, service):void {
  	console.log(service + ": " + value);
  	
  	if (this.options[0].value == true && this.options[1].value == true) {
  		this.show = false;
  		console.log("Show button");
  	} else {
  		this.show = true
  	}
  }

  goToContacts():void {
  	this.navCtrl.push(ContactDetailsPage, {
      data: {abv:'MAP', name:'Central Health', phone:'(512) 978-8130', address:'6633 E Hwy 290 #310, Austin, TX 78723', logo:'map_logo.png', map:'map_location.png'}
    });
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad ResourcesDetailsPage');
  }


}
