In order to run this app, open the "final-project/android" project
in Android Studio and choose to run the project on a phone. Connect your
phone to the computer and run the project on your phone. Search for how
to run an Android Studio app on a phone for specific instructions.

To run the server, open the "final-project/server" folder and follow the
instructions in the "final-project/server/README.md" file. The
instructions explain how to create the Node and MongoDB containers and
then how to link the two containers.

The server implements a RESTful API with Node.js and MongoDB. The two main actions are
GET and POST on "/messages". The GET action requires two parameters:
"latitude" and "longitude". It returns a JSON object with the 50 closest messages from the database sorted by distance from the given latitude and longitude. The POST action requires four parameters: "id", "message", "latitude", and "longitude". It adds the object with the given fields to the MongoDB database.

When the app is first opened it does a GET action on "/messages" and
displays a list of the returned messages. The user is able to refresh
the message list by swiping down on the message list. The user is able to add a
message by pressing the add button in the ActionBar. This does a POST action on "/messages" with the user-supplied
message and the user's latitude and longitude which is found from the
device sensors (GPS, Wi-Fi, etc.). The user is also able to
see the given messages on a Google Map by pressing the map button in the
ActionBar. This Map View displays all of the messages on the map as well
as the user's current location.
