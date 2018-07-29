import { NgModule } from '@angular/core';
import { IonicPageModule } from 'ionic-angular';
import { ResourcesDetailsPage } from './resources-details';

@NgModule({
  declarations: [
    ResourcesDetailsPage,
  ],
  imports: [
    IonicPageModule.forChild(ResourcesDetailsPage),
  ],
})
export class ResourcesDetailsPageModule {}
