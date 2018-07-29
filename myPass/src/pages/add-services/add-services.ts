import { Component } from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { ResourcesPage } from '../resources/resources';

/**
 * Generated class for the AddServicesPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-add-services',
  templateUrl: 'add-services.html',
})
export class AddServicesPage {
	payload: any = [
	  	{abv: 'JOSH', name:'Joshua Good Deed Service', status:'green', status_comp:'100% - Ready'},
	  	{abv: 'ECHO', name:'Ending Community Homelessness Coalition', status:'green', status_comp:'100% - Ready'},
	  	{abv: 'SOAR', name:'SSI/SSDI Outreach, Access, and Recovery', status:'red', status_comp:'50% - Incomplete'},
	  ];
	service:any = [];

  constructor(public navCtrl: NavController, public navParams: NavParams) {
  }

  ionViewDidLoad() {
    console.log('ionViewDidLoad AddServicesPage');
  }

  addService(data):void {

  	this.service.push(data);
  }

  goToDetails(payload):void {
  	this.navCtrl.push(ResourcesPage, {
      data: this.service
    });
  }

}
