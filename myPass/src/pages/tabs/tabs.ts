import { Component } from '@angular/core';

import { ContactPage } from '../contact/contact';
import { HomePage } from '../home/home';
import { ResourcesPage } from '../resources/resources';


@Component({
  templateUrl: 'tabs.html'
})
export class TabsPage {

  tab1Root = HomePage;
  tab2Root = ResourcesPage;
  tab3Root = ContactPage;

  constructor() {

  }
}
