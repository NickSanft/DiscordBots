all = {
    "join" : {
        "added" : ("Welcome, {0}! I've PMed you with information about the game and your character!"),
        "no_arg" : ("What courage; what ENTHUSIASM! You wish to join the game! ...And yet, you have not given me a name "
                      "by which to call you!\n\n`Usage: $join <name>`"),
        "exists" : ("You're already playing the game!")
    },
    "name" : {
        "no_arg" : ("If you'd like to change your name, you'll need to fill out everything correctly! :kissing_heart:\n\n"
                       "`Usage: $name <new_name>`"),
        "updated" : ("From this point forth, you shall be known as **{0}**! Go now, on to adventure! TO GLORY!"),
        "failed" : ("Oh god something went wrong")
    },
    "summary" : {
        "notfound" : ("You're not even playing the game! Are you too cowardly? Too *weak*? "
                       "Summarize yourself; there is no room for weaklings here!"),
        "stats" : ("**{1}** Level {2}\n\n:heart: Health: {5}/{4}\n:muscle: Fight: {6}"
                   "\n:fist: Body: {7}\n:raised_hands: Spirit: {8}"),
        "unspent" : ("\n\n*You still have* {3} *unspent ability points!*")
    },
    "whois" : {
        "no_arg" : ("Who is... who? Did you just suddenly stop speaking? I'll need a name to check my records!"
                    "\n\n`Usage: $whois <name>`"),
        "notfound" : ("There doesn't seem to be a player by the name **{0}**"),
        "found" : ("The player with the name **{0}** is, to no one's surprise, {1}.")
    },
    "players" : {
        "list" : ("Nosey, aren't we? Here's a list of every player in the game:\n"),
        "template" : ("\n**{0}** Level {1}")
    }
}
