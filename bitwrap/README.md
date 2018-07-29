# Python API

This python API serves as an interface for the front end app.

As a design principle, all specifications needed to duplicate this functionality are pushed to the blockchain.

Event schemas are included to allows any other organization to replicate the features of the API.

If it were required to implement the application entirely as a distributed application on chain.
The event aggregation funcationality could be relocated from python to another smart contract language.

## see ./schemata folder for details

*schemata/specification.xml*  

Defines events that record updates for the application specification.


*schemata/event.xml*  

Defines events that are triggered by end-users interacting with the application.

*schemata/workflow.xml*  

Defines an example contract specification that demonstate an Authority executing a final sign-off.
