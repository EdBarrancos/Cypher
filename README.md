# Cypher

A chat program design to play ttrpgs games that supports characters who speak different languages

## Setup

- Get the server up and running `python3 src/server.py`
- Check the servver IP's address by running the command `ip address show`
- Set the Server's IP and PORT in the client and director's script
- Make sure all computers are in the same network
- Run the clients
    - Set name and languages spoken by your character
- Run the director

## Messaging

### Client

Write language:message

For example: `common:Hello Sire. We need your help`

If the others players speak the selected language they will visualise the message you sent. If they did not, they will only see your character's name, the spoken language and a bunch of `?`
The director always sees the name, language and message

### Director

Write character_name:language:message

For example: `King:common:Why should I help you?`

The same logic as for the clients will apply when distributing the message.