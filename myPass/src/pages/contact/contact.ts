import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';
import { ContactDetailsPage } from '../contact-details/contact-details';

@Component({
  selector: 'page-contact',
  templateUrl: 'contact.html'
})
export class ContactPage {
	medical:any = [
		{abv:'ARCH', name:'Austin Resource Center for the Homeless', phone:'(512) 305-4100', address:'500 E 7th St, Austin, TX 78701'},
		{abv:'MAP', name:'Central Health', phone:'(512) 978-8130', address:'6633 E Hwy 290 #310, Austin, TX 78723', logo:'map_logo.png', map:'map_location.png'},
		{abv:'SOAR', name:'SSI/SSDI Outreach, Access, and Recovery', phone:'518-439-7415', address:'345 Delaware Ave, Delmar, NY 12054'},
	];
	housing:any = [
		{abv:'ECHO', name:'Ending Community Homelessness Coalition', phone:'(512) 763-2917', address:' 300 E Highland Mall Blvd, Suite 200 Austin, Texas 78752'},,
	];
  constructor(public navCtrl: NavController) {
  	console.log(this.medical[0])
  }

  goToDetails(payload):void {
  	this.navCtrl.push(ContactDetailsPage, {
      data: payload
    });
  }

}
