import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { ResourcesDetailsPage } from '../resources-details/resources-details';
import { AddServicesPage } from '../add-services/add-services';

/**
 * Generated class for the ResourcesPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-resources',
  templateUrl: 'resources.html',
})
export class ResourcesPage {
	data: Observable<any>;
	payload: any = [
	  	{abv: 'MAP', name:'Medical Access Program', status:'green', status_comp:'100% - Ready'},
	  	{abv: 'ECHO', name:'Ending Community Homelessness Coalition', status:'green', status_comp:'100% - Ready'},
	  	{abv: 'SOAR', name:'SSI/SSDI Outreach, Access, and Recovery', status:'red', status_comp:'50% - Incomplete'},
	  ];

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  	this.data = navParams.get('data');

  	if (this.data != null) {
  		for(let item of this.data) {
			  console.log(item)
			  this.payload.push(item)
			}
  	}
  	
	  console.log(this.payload);
  	this.printLog(this.payload);
  }

  // data = {
  // 	id: {
  // 		name: 'Card'
  // 	}
  // }

  

  printLog(data):void {
  	console.log(data);
  }


  ionViewDidLoad() {
    console.log('ionViewDidLoad ResourcesPage');
  }

  goToAddService(payload):void {
  	this.navCtrl.push(AddServicesPage, {
      data: payload
    });
  }

  goToDetails(payload):void {
    this.navCtrl.push(ResourcesDetailsPage, {
      data: payload
    });
  }

}
