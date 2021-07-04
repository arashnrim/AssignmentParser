This file explains the context behind why and how Homework Parser works.

## Compiled list

(Almost) every day, the Exco members of my class compiles and sends the daily list of homework into the class chat (thank you!). An example of such a list looks like the image shown below.

<img height="350px" src="example.png">

## Manual edits

Before sending the contents of the message as an input, me, being the perfectionist I am, would take some time to edit the content — be it as minor as ensuring the standardisation of capitalisation or critical as ensuring the spelling of the subject, I try to take some time (though, not a lot) to at least make the content standardised.

## Parsing

On input, the program does the rest of the magic — identifying the due dates, associating the due dates with the tasks, and sending them over to Todoist via its API.