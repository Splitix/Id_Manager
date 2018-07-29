import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { AddServicesPage } from './add-services';

@NgModule({
  declarations: [
    AddServicesPage,
  ],
  imports: [
    IonicPageModule.forChild(AddServicesPage),
  ],
})
export class AddServicesPageModule {}
