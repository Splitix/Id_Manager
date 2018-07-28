import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';

@Component({
  selector: 'page-contact',
  templateUrl: 'contact.html'
})
export class ContactPage {

	contacts = [
		"Austin Resource Center for the Homeless",
		"Central Health",
		"Austin Community Court",
	]

	contact_data = {
		"Austin Resource Center for the Homeless": {
			Phone: "(512) 305-4100",
			Address: "500 E 7th St, Austin, TX 78701"
		},
		"Central Health": {
			Phone: "(512) 978-8130",
			Address: "6633 E Hwy 290 #310, Austin, TX 78723"
		},
		"Austin Community Court": {
			Phone: "(512) 974-4879",
			Address: "719 E 6th St, Austin, TX 78701"
		}
	}

  constructor(public navCtrl: NavController) {

  }

}
