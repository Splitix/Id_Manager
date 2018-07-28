import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { IdDetailsPage } from './id-details';

@NgModule({
  declarations: [
    IdDetailsPage,
  ],
  imports: [
    IonicPageModule.forChild(IdDetailsPage),
  ],
})
export class IdDetailsPageModule {}
