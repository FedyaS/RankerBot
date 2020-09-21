import os
import discord
import dotenv
import datetime
import calendar
import time
from discord.ext import tasks
import Events
import Methods
# discord is the main import to know, as well as discord.ext

# These 3 lines open the "secure" data file with the bot token and should not be shared, not really using this file for
# anything else
dotenv.load_dotenv('Data.env')
token = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# This opens a text file which I have been using to store the message id of the previous bot invitation (in case it
# crashes or needs to be restarted). Ultimately, this is a bad approach as txt sucks and we will probably need to use
# json to store all the events and reminders we will be working with.
DataFile = open("Data.txt", 'a+')
DataFile.seek(0)
perma_id = int(DataFile.read())  # This is the message id it gets from the data file
print(perma_id)

main_channel = 755138182701514903  # This is the id of the channel it sends announcements in

client = discord.Client(max_messages=1000)  # This is the discord client (bot itself) use client.something to do stuff
# It is also possible to use the discord class Bot (instead of Client), but I believe this has some limitations, while
# the only advantage would be that they provide a command interface (however I think it is not too powerful and
# switching to Bot will most likely break our code in multiple places).

now = datetime.datetime.now()  # Prints current date and time just as a test. Using these methods later as well.
current_time = now.time()
print(now, current_time)

# Two things to notice about the line after this comment:
# First, this represents the time at which the bot sends out the lunch reminder (7 am)
# Second, the datetime.time method converts h, m, s into a time format which can then be compared to the current time
# without any further conversions
expected_time = datetime.time(7, 00, 00)

# This logic basically checks if the expected time has already passed (whenever the bot is launched).
# If it has, the bot assumes today's announcement has already been sent and sets the day of the last ann to today
# Otherwise, the bot assumes the ann has not been sent. The point of this is so in case of a relaunch, the bot will not
# post an ann every time.
if expected_time < datetime.datetime.now().time():
    date_sent = datetime.datetime.now().date()
else:
    date_sent = 0

basic_message = "Reminder: There is a virtual lunch today from 11-12"  # The basis of the ann text

# Notice that the above lines of code are specific to that 1 lunch ann. Ultimately, these vars and methods will be made
# into a class called Event and each new ann will be an instantiation of that class.

# Universal yes / no replies to monitor attendance
no_emoji = "👎"
yes_emoji = "👍"

# I was thinking of making this the method to store all reminder and event objects. We would have a list for each and
# keep track of the free index. Once an object is no longer useful, it can be removed from the list and we mark that as
# a free index, available for use. This seems a bit shaky tho, so do you know any better methods?
reminders = []
next_reminder_indices = []
events = []
next_event_indices = []


# Prototype for shutting down
def shutdown():
    pass


# This is the core concept of the bot receiving messages. However, this way discord does it is actually outdated
# according to the asyncio docs (LMAO)

# The at basically means this method waits for that thing to happen and then goes through
# Notice each def has an async before it and needs to be named a specific name (according to discord API)

@client.event
async def on_ready():  # This is the case where the bot says it is "ready"
    lunch_server = client.get_guild(id=int(GUILD))
    print(lunch_server)
    print('Ranker is connected to:\n'
          f'{lunch_server.name}\n(id: {lunch_server.id})'
          )


@client.event
async def on_message(message):  # This is the case the bot receives a message

    if message.content[0] == '!':  # Pretty much our command prefix.

        if message.content == '!!':  # The !! command
            response = 'Hello'
            await message.channel.send(response)  # Notice that you have to use await before function calls for stuff
            # like retrieving messages an info from discord

        elif message.content == "!Who is coming today?" or message.content == "!who":  # The !who command
            # The result of !who will be to see who reacted with thumbs up to a certain event and send that out
            # Currently, this is specific to the lunch event, but later it should be implemented to work for any event

            all_names = []  # Names of all attendees
            temp_channel = client.get_channel(id=main_channel)  # The channel where the bot sends ann
            # BTW, notice that to get a message from a given id, I have to first retrieve the channel which contains
            # that message. Why? Because Discord devs are furries.

            # Once again, main_channel var shouldn't be constant
            # It will need to be changed so it works for different reminders, not just the specific one

            reaction_message = await temp_channel.fetch_message(id=perma_id)  # Fetching the message containing the
            # original invite the bot had sent. perma_id will need to be changed to be specific for whichever event we
            # are working with

            reactions = reaction_message.reactions  # Getting reactions from the message we fetched

            # This for loop counts all people who reacted yes and adds those to our names list
            for reaction in reactions:  # Going through each reaction to our message
                if reaction.emoji == yes_emoji:  # Finding the yes reaction
                    attendees = await reaction.users().flatten()  # This method looks weird, but is the one recommended
                    # by the Discord api. It basically gets a list of all the users who reacted with said reaction

                    for attendee in attendees:  # Adding each reacted user
                        all_names.append(attendee.display_name)

            # Formatting the reply for who will attend. This should be fixed up so the grammar is correct in case 0 or 1
            # people are attending. Maybe also make it look better somehow?
            reply = "```"
            for name in all_names:
                reply = reply + name + "\n"
            reply = reply + "are all attending!```"

            await message.channel.send(reply)  # Once again, use await to send a reply

        elif message.content[0:6] == '!remind':  # The remind command
            # This command would be a way for users to set a simple reminder for themselves / others (vs an Event which
            # would also have attendance)

            # The format of the command would be:
            # AT or IN keywords preceding the time of day or duration respectively
            # TO keyword preceding the text of the reminder (aka the name of the reminder)
            # People who are pinged will be pinged again once the reminder is sent by the bot, though the reminder does
            # not have to have someone signified to be pinged.
            # Note we could have a keyword for this, but not sure if we should. A keyword would make the command
            # longer, but also make it easier to separate the text of the command from the people pinged.

            # Example reminders:
            # !remind AT 7:30 TO Eat some food @Fedya @Dennis
            # !remind AT 7 TO Brush your teeth
            # !remind IN 5 minutes TO Take a break @Fedya @Dennis
            # !remind IN 1 hour TO Finish your homework

            # For the following part we could use regex since you have some knowledge with that xD
            ms = message.content  # String of the whole command message
            args = ms.split()  # The message split by white space
            success = False
            reply = ""
            arg_error_reply = "Your !remind command did not provide enough arguments or the right arguments"

            if len(args) < 5:  # 5 is pretty much the min amount of words in the command
                reply = arg_error_reply  # All we do is set the reply and the bot will send it at the end
            elif 'TO' not in args:  # No TO keyword
                reply = arg_error_reply
            elif 'AT' not in args or 'IN' not in args:
                reply = arg_error_reply
            elif args[1] != 'AT' and args[1] != 'IN':
                reply = arg_error_reply
            elif 'TO' not in args:
                reply = arg_error_reply

            else:
                clock = -1
                timer = -1
                if 'AT' == args[1]:  # Case where AT is the second word (!remind AT)
                    clock = Methods.string_to_time(args[2], args[3])

                elif 'IN' == args[1]:  # Case where IN is the second word (!remind IN)
                    timer = Methods.string_to_duration(args[2])


@client.event
async def on_reaction_add(reaction, user):  # On reaction being added, not really using this currently
    # the main reason being that it is easier and safer to count reactions later, using the message id instead of live
    # counting reactions.

    pass
    # await reaction.message.channel.send("Hi")


@tasks.loop(seconds=30)  # This method, well hidden by the Discord API so no one can find it, represents the zenith of
# civilization. It allows a background task to run, every given amount of time. This will be used to monitor reminders
# and events and check if the time has come.
async def time_monitor():
    global date_sent, no_emoji, yes_emoji, basic_message, perma_id
    current_time = datetime.datetime.now().time()  # Gets the current time
    if current_time >= expected_time:  # Checks if expected time is surpassed
        # Once more, this will need reformatting so that it can be done with all reminders and events at the same time

        if date_sent != datetime.datetime.now().date():  # If the last day sent is NOT today
            # Three different methods which basically all get the date, but in slightly different formats.
            # Could fix this, but it is risky.
            date_sent = datetime.datetime.now().date()
            my_date = datetime.date.today()
            month_day = my_date.day

            suffix = Methods.select_suffix(month_day)
            if my_date.isoweekday() >= 6:  # Case where it is the weekend
                pass
            else:
                # Send the reminder
                week_day = calendar.day_name[my_date.weekday()]
                channel = client.get_channel(id=main_channel)
                common_message = f"```Reminder: \nThere is a virtual lunch today ({week_day} the {month_day}{suffix}) from 11am-12pm. Who is going? React Below!```"
                message = await channel.send(common_message)

                perma_id = message.id  # Remember the message id so we can count reactions later

                # Bot adds the initial reactions to encourage reactions by users
                await message.add_reaction(yes_emoji)
                await message.add_reaction(no_emoji)

                # Writing the message id to the data file.
                # This needs reworking as we want to store many objects and their info, rather than a single id.
                DataFile.truncate(0)
                DataFile.write(str(perma_id))

                # Save the file immediately so in case of crashes we don't loose stuff
                DataFile.flush()
                os.fsync(DataFile.fileno())

time_monitor.start()  # Starts the background time_monitor function
client.run(token)  # Starts the client. Nothing below this will run.
