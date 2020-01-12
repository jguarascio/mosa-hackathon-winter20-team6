# mosa-hackathon-team6

![GitHub Logo](/images/mosahack_team6_11jan2020_teambot.png)
Format: ![Preview our app!](https://github.com/jguarascio/mosa-hackathon-winter20-team6/tree/master/images/mosahack_team6_11jan2020_teambot.png)

## Inspiration
In an online program, it is often difficult to make real world connections with classmates. The goal of our Slack Bot is to facilitate introductions to fellow students and also make creation of teams more automatic.

## What it does
By sending a command to the slack bot within a channel, channel members will be teamed up in groups of 2 or 3 and conversation channel will be started.

## How we built it
The python code creates a listener using the slack RTM client inside the slackclient package. This code listens for the command and acts on it to create teams. Then channels for each "team" are created using the slack api.
To pair teammates together, we ran a random function to create pairs from a list.

## Challenges we ran into
Slack API was a bit difficult to learn at first and there isn't a whole lot of example code available. It is also important that the code be hosted on the cloud so that it can run remotely.
Also, the ability to automatically create a new private channel per pair was tougher to implement within the competition timeframe, as well as a more complex pairing algorithm.

## Accomplishments that we are proud of
Learning how to use the slack API.

## What we learned
How to create a pairing algorithm in python using `random` utility class   
How to communicate to a new API via python   
How to setup a bot   

## What's next for Slack Team Bot
Ideally we would like to host the team bot on a cloud server and integrate it with the MCIT channels so that staff can use it to automatically create teams for class projects and/or to create small networking groups.
We would also like to make our pairing algorithm more complex based on students' shared interests.

## Built By
Steve Brooks - [git](https://github.com/stevegbrooks) & [devpost](https://devpost.com/stevegbrooks)    
Eunice Hameyie - [git](https://github.com/ehameyie) & [devpost](https://devpost.com/ehameyie)    
Joe Guarascio - [git](https://github.com/jguarascio) & [devpost](https://devpost.com/jgua)

## Try it out!
Join our workspace at mcitteam6.slack.com and send the command getteams in a mention to @team6
