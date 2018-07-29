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
	  	{abv: 'ABC', name:'Any Baby Can', status:'green', status_comp:'100% - Ready', icon:'medical_icon.png'},
	  	{abv: 'LIFE', name:'Lifeworks', status:'red', status_comp:'90% - Incomplete', icon:'hand_icon.png'},
	  	{abv: 'SOCIAL WORK', name:'Travis County HHS Social Work Services', status:'red', status_comp:'50% - Incomplete', icon:'hand_icon.png'},
      {abv: 'HELPING HANDS', name:'The Helping Hands Center', status:'red', status_comp:'50% - Incomplete', icon:'clothes_icon.png'},
      {abv: 'FRONT', name:'Front Steps', status:'red', status_comp:'50% - Incomplete', icon:'clothes_icon.png'},
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
