# Python API

Forked from https://github.com/bitwrap/bitwrap-io

This API provides a translation layer, that Aggregates metadata from the Factom Blockchain
into a postgres database.

This allows the End user of the Id_Manager app to see progress working toward obtainaing a new 
ID or support package.

Additionally, it is planned to submit all relevant specifications for how the app functions
to the blockchain - with the idea that it could become fully decentralized at some point
or in the case the the organization hosting the API runs out of money or disappears,
it should be possible for another party to start the service back up again.

## Status
Currently Neither the Ionic Frontend app nor the Factom Code hare hooked into the API

TODO: actually finish stiching all these peices together

# Overview
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
