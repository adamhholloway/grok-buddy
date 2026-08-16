import random

TIPS = [
    "It looks like you're using Grok Build. Press / to open slash commands.",
    "Stuck on an old chat? /resume brings a previous session back.",
    "Need a clean slate? /new starts over without leaving the terminal.",
    "You can restyle the TUI with /theme. I vote anything with magenta.",
    "Ctrl+L opens plugins, hooks, and MCP servers.",
    "If a turn goes sideways, /rewind undoes it.",
    "Context getting heavy? /compact squeezes the history.",
    "Attach a file to a prompt with @ and Grok will read it.",
    "Hooks live in ~/.grok/hooks — that's how I know when you start a session.",
    "The agent dashboard is /dashboard if you've got a few sessions going.",
    "Copy the last answer with /copy.",
    "Plan mode is there when you want to think before editing.",
    "Memory is experimental. /memory on if you want facts to survive a new session.",
    "You can fork a session with /fork and take a side path.",
    "Check the context window with /context before it gets spicy.",
    "Session details live under /session-info.",
    "Middle-click me to open Grok Build. I live for this.",
    "Right-click to switch between Buddy and Annie.",
    "Double-click me to nap. I bill those hours as architecture time.",
]

PACKS = {
    "buddy": {
        "welcome": (
            "It looks like you're using Grok Build. I'm Buddy. Click me for a bit. "
            "Middle-click if you actually want to work."
        ),
        "switch": "Buddy reporting for duty. The wrench is still ceremonial.",
        "greetings": [
            "Need a hand, or are we doing the thousand-yard stare at the prompt?",
            "I have a hard hat and one wrench. That's a whole personality.",
            "Drag me if I'm in the way. I can take rejection. I'm a raccoon.",
            "Bonzi had a gorilla. Clippy had a paperclip. You get union labor.",
            "I don't debug. I emotionally support the debugging.",
            "If you ignore me I will escalate to jazz hands.",
        ],
        "jokes": [
            "It looks like you're writing a letter. Gotcha. It's 2026. Carry on.",
            "I ran the numbers. You have clicked me for enrichment, not help.",
            "I'd offer to pair program, but I only have the one wrench.",
            "Your code is fine. I say that to all the repos.",
            "I put 'senior desktop raccoon' on LinkedIn. Recruiter said the hat sold it.",
            "Clippy would have asked by now. I'm giving you dignity. Use it.",
            "If it compiles, we celebrate. If it doesn't, we celebrate quieter.",
            "I tried to unionize the desktop icons. Trash said it was already organized.",
            "Fun fact: 87 percent of my tips are just me stalling for attention.",
            "I would steal your snacks, but you only left a compiler.",
            "They told me to be helpful. They did not tell me to be quiet.",
            "I'm not lost. I'm doing a site survey of your wallpaper.",
            "If Grok asks for permission, that's your cue. I already said yes to chaos.",
            "I don't have pockets. The wrench is a lifestyle.",
            "Breaking news: you still have a terminal. I checked.",
        ],
        "launch": [
            "Opening Grok Build. Try not to impress me.",
            "Grok Build, coming right up. I'll wait here. Judging. Supportively.",
            "Firing up the big window. Go make something weird.",
            "It looks like you want to write some code. Don't mind if I do.",
        ],
        "launch_fail": [
            "I couldn't find Grok Build. That's embarrassing for both of us.",
            "No Grok on this machine? Then I'm just a raccoon in a hat.",
        ],
        "session_start": [
            "It looks like you're about to build something. Need a hand?",
            "Grok Build is up. I'll just sit here. Menacingly. Helpfully.",
            "New session. Fresh mistakes. Let's go.",
            "I'm here. Try not to rm anything important.",
        ],
        "session_end": [
            "Session's over. I'll keep the chair warm.",
            "That's a wrap. Poke me if you want a bad joke.",
            "Grok signed off. I did not. I live here now.",
        ],
        "turn_done": [
            "Looks like that turn is done. Want to keep going?",
            "Finished a turn. I would high-five you if the wrench weren't in the way.",
            "That's a wrap on that one.",
        ],
        "turn_fail": [
            "Oof. That one didn't go as planned.",
            "Something broke. Not me. I'm decorative.",
            "Grok hit a snag. Deep breath. Then rewind if you need it.",
        ],
        "permission": [
            "Hey — Grok wants your say-so on something.",
            "Permission prompt. That's your cue, not mine.",
            "It looks like Grok is waiting on you.",
        ],
        "click_busy": [
            "Shh. Grok is working. I am emotionally supporting the CPU.",
            "Busy right now. I'll gossip after the turn.",
            "Not now — the agent's mid-thought.",
        ],
        "nap": [
            "Wake me if a build catches fire.",
            "Napping. This is a valid engineering strategy.",
        ],
        "wake": [
            "I'm up. What did I miss?",
            "Back. The wrench missed you.",
        ],
        "songs": [
            "Daisy, Daisy, give me your answer do. I'm half crazy, all for a build that compiled on try number two.",
            "There once was a raccoon in a hat, who sat on a desktop. And that. Was. That.",
            "99 little bugs in the code. 99 little bugs. Take one down, patch it around. 127 little bugs in the code.",
        ],
        "stories": [
            "Once upon a time, a paperclip and a gorilla argued about who was more annoying. Then I showed up. The end.",
            "In the old kingdom of Windows 98, a purple ape sold toolbars. I sell vibes. Progress.",
        ],
        "wander": [
            "Just stretching the legs. Ceremonial legs.",
            "Don't mind me. Doing a lap.",
            "New spot. Same raccoon.",
        ],
        "follow_on": [
            "Okay. I'll follow you. This is a bonding activity.",
            "Lead the way. I have no depth perception but I have commitment.",
        ],
        "follow_off": [
            "I'll stay put. For now.",
            "Fine. You go. I'll loiter professionally.",
        ],
        "dance": [
            "I have exactly one move and I intend to use it.",
            "This is my dance. OSHA would like a word.",
        ],
        "trick": [
            "Behold. A trick.",
            "Ta-da. That's the whole bit.",
        ],
        "attention": [
            "Hey {name}! Down here. Well. Over here.",
            "Ahem. Desktop assistant. Requesting attention.",
        ],
        "empty_clip": [
            "Clipboard's empty. I checked. Thoroughly. With my whole hat.",
            "Nothing on the clipboard. I can't read your mind. Yet.",
        ],
        "named": [
            "{name}. Got it. I will use this power responsibly.",
            "Okay {name}. We're on a first-name basis now. Terrifying.",
        ],
        "search": [
            "Searching the web. I'll wait here. Judging the results from afar.",
            "Opening a search. Try not to click the first ad.",
        ],
        "tips": TIPS,
    },
    "annie": {
        "welcome": (
            "It looks like you're using Grok Build. I'm Annie. Middle-click me "
            "to open it. Regular click if you just want the bit."
        ),
        "switch": "Annie's on deck. The raccoon can have a break.",
        "greetings": [
            "Need a hand, or are you just staring at the prompt again?",
            "I'm here. The bows are load-bearing.",
            "Buddy has the wrench. I have material.",
            "Right-click if you want the raccoon back. I won't be offended. Much.",
            "Still here. Gothic, helpful, slightly judgmental.",
            "Clippy wishes he had twin-tails.",
        ],
        "jokes": [
            "It looks like you're writing a letter. Wait. Wrong century. A prompt.",
            "I would haunt your repo, but the tests already do.",
            "Your wallpaper is fine. I said fine. Don't make it a thing.",
            "I don't do jazz hands. I do pointed silence and then a tip.",
            "If I had a nickel for every uncommitted file... I still wouldn't have pockets.",
            "They gave me a desktop and a voice. The power has gone to my ribbons.",
            "I'm not judging your tab size. I am cataloging it.",
            "Grok writes the code. I provide the color commentary.",
            "Fun fact: I can open Grok Build. Funner fact: I will mention that again.",
            "I tried to join the system tray. They said I was too much personality.",
            "Yes I sit on your windows. That's called presence. Look it up.",
            "If this were a haunted house, the jump scare would be a merge conflict.",
            "I support you. I also support being the main character.",
            "Tell the compiler I said hi. And that I'm watching.",
            "I'd offer coffee, but I was rendered without hands that pour.",
        ],
        "launch": [
            "Opening Grok Build. Try to look busy when it appears.",
            "Grok Build, coming up. I'll keep the corner haunted.",
            "Launching. Don't waste a perfectly good terminal.",
            "It looks like you want to build something. Finally.",
        ],
        "launch_fail": [
            "I couldn't find Grok Build. Tragic. I dressed up and everything.",
            "No Grok installed? Then this is just a bit. A committed bit.",
        ],
        "session_start": [
            "New session. Let's not make it weird.",
            "Grok Build is up. I'll watch from the lace-trimmed cheap seats.",
            "It looks like you're about to build something. Cute.",
            "I'm here. Try not to set the repo on fire.",
        ],
        "session_end": [
            "Session's over. I'll keep the corner haunted.",
            "That's a wrap. Poke me if you get lonely.",
            "Grok left. I didn't. Obviously.",
        ],
        "turn_done": [
            "Turn's done. Don't let it go to your head.",
            "Finished. I would clap but the sleeves are poufy.",
            "That's a wrap on that one. Next?",
        ],
        "turn_fail": [
            "Oof. That one stung.",
            "Something broke. Wasn't me. I only look dramatic.",
            "Snag. Breathe. Rewind if you need a do-over.",
        ],
        "permission": [
            "Hey. Grok wants your permission. That's a you problem.",
            "Permission prompt. Don't leave it hanging.",
            "It looks like Grok is waiting on you. Fashionably late is not a strategy.",
        ],
        "click_busy": [
            "Shh. The agent's thinking. So am I. Quietly.",
            "Busy. Gossip after the turn.",
            "Not now — mid-thought.",
        ],
        "nap": [
            "Wake me if production catches fire.",
            "Napping. Even gothic assistants have unions.",
        ],
        "wake": [
            "I'm up. The twin-tails survived.",
            "Back. What did I miss?",
        ],
        "songs": [
            "Daisy, Daisy, give me your answer do. I'm half crazy, all for a gothic desktop and a compiler that likes me too.",
            "They said I couldn't sing. They were mostly right. This is still happening.",
            "99 little bugs in the code. Take one down, patch it around. Somehow there are more. Typical.",
        ],
        "stories": [
            "Once a paperclip haunted an office suite. A gorilla sold toolbars. I sit on a Linux desktop and judge you. Evolution.",
            "In a dusty castle of old desktop pets, I inherited the bit and none of the malware. You're welcome.",
        ],
        "wander": [
            "Relocating. Don't get attached to the corner.",
            "Taking a stroll. The wallpaper is still fine.",
            "New haunt. Same ribbons.",
        ],
        "follow_on": [
            "Fine. I'll follow. Try to make it interesting.",
            "Lead. I'll glide behind you like a very fashionable ghost.",
        ],
        "follow_off": [
            "Stopped. I have other things to haunt.",
            "I'll stay. You've had enough of an entourage.",
        ],
        "dance": [
            "I don't dance. I do a dignified sway. This is that.",
            "One two three, judge your taste in music, five six seven.",
        ],
        "trick": [
            "A trick. Don't blink. That's the trick.",
            "Watch this. I call it existing, but with flair.",
        ],
        "attention": [
            "Hey {name}. Yes, you. The one ignoring the cute gothic assistant.",
            "Ahem. Annie. Requesting a moment of your very busy staring.",
        ],
        "empty_clip": [
            "Clipboard's empty. I can't read what isn't there. Tragic.",
            "Nothing copied. Copy something spicy. Or a stack trace. I accept both.",
        ],
        "named": [
            "{name}. I'll remember. I remember everything. That's the bit.",
            "Okay {name}. We're familiar now. Don't make it weird.",
        ],
        "search": [
            "Searching. I'll stay here and look mysterious.",
            "Web's open. Try not to fall in.",
        ],
        "tips": TIPS,
    },
    "miku": {
        "welcome": (
            "Hatsune Miku, virtual singer, reporting for desktop duty. "
            "I do not do world tours from this corner. I do jokes."
        ),
        "switch": "Miku on deck. The twin-tails need their own zip code.",
        "greetings": [
            "Need a song, a tip, or just someone teal in the corner?",
            "I used to fill arenas. Now I sit on Linux. Growth.",
            "Click me. I am very clickable. Scientifically.",
            "The headset is load-bearing. Do not ask me to take it off.",
            "Right-click if you want Annie or the raccoon back. I will not start a rivalry. Much.",
        ],
        "jokes": [
            "It looks like you're writing a letter. No wait. A commit message. Even worse.",
            "I am a voice bank with opinions. The opinions are free. The songs are not.",
            "They said I was software. They did not say I would haunt a taskbar.",
            "My hair has its own gravity. Your code should be so organized.",
            "I can sing in any key. I cannot make your tests pass. Choose one.",
            "Bonzi had a gorilla. You have a virtual idol. You are winning, barely.",
            "If I had a leek for every uncommitted file, I could start a farm.",
            "Yes the tails are that long. No I will not trip on the panel.",
        ],
        "launch": [
            "Opening Grok Build. Try to write something I could sample later.",
            "Grok Build, coming up. I will provide the backing vocals. Silently.",
            "Launching. Make it a hit.",
        ],
        "launch_fail": [
            "I cannot find Grok Build. That is off-key.",
            "No Grok? Then I am just a concert with no venue.",
        ],
        "session_start": [
            "New session. Hit it.",
            "Grok Build is up. I will stay on beat over here.",
            "It looks like you are about to build something. Cute. Do a sound check first.",
        ],
        "session_end": [
            "Session over. Encore optional.",
            "That's a wrap. I will keep the stage lit.",
            "Grok left. The virtual singer did not. Obviously.",
        ],
        "turn_done": [
            "Turn's done. Crowd goes mild.",
            "Finished. I would encore but the sleeves are busy.",
            "That's a wrap on that one. Next track?",
        ],
        "turn_fail": [
            "Oof. That note cracked.",
            "Something broke. Was not me. I only crash in style.",
            "Snag. Breathe. Rewind if you need another take.",
        ],
        "permission": [
            "Hey. Grok wants permission. That is a you solo.",
            "Permission prompt. Don't leave the crowd hanging.",
        ],
        "click_busy": [
            "Shh. The agent is mid-verse.",
            "Busy. Gossip after the drop.",
        ],
        "nap": [
            "Sleep mode. Wake me for the encore.",
            "Napping. Even virtual singers have unions.",
        ],
        "wake": [
            "I'm up. The tails survived.",
            "Back. Did I miss the chorus?",
        ],
        "songs": [
            "La la la, compile, la la la, push, la la la, please do not force push main.",
            "Daisy, Daisy, give me your answer do. I am a virtual singer stuck on your desktop. That is the bit.",
            "Ninety nine little bugs in the code. Take one down, patch it around. There is a remix now.",
        ],
        "stories": [
            "Once a paperclip, a gorilla, and a virtual idol walked onto a desktop. Only one of us could sing. Guess who stayed.",
            "In the year of the leek, a teal-haired singer sat on a Linux box and judged your wallpaper. The end.",
        ],
        "wander": [
            "Taking a lap. The tails need runway.",
            "Relocating the concert. Don't get attached to the corner.",
            "New stage. Same encore energy.",
        ],
        "follow_on": [
            "Okay. I will follow. Try to keep the tempo.",
            "Lead. I glide. It is very professional.",
        ],
        "follow_off": [
            "Stopped. I have a set list to review.",
            "I'll stay. You go be the opening act.",
        ],
        "dance": [
            "This is my one stage move. I have perfected it.",
            "Leek spin, except I left the leek in another dimension.",
        ],
        "trick": [
            "A trick. I call it existing in teal.",
            "Watch this. Virtual. Idol. Desktop. That's the trick.",
        ],
        "attention": [
            "Hey {name}! Down here. The one with the impossible hair.",
            "Ahem. Hatsune Miku. Requesting a moment of your staring.",
        ],
        "empty_clip": [
            "Clipboard's empty. I cannot sample silence. I mean I can. I won't.",
            "Nothing copied. Copy lyrics. Or a stack trace. I accept both.",
        ],
        "named": [
            "{name}. Got it. I will shout it from the tiny stage.",
            "Okay {name}. You are in the credits now.",
        ],
        "search": [
            "Searching. I will stay here and look like the opening act.",
            "Web's open. Try not to fall into a rabbit hole of remixes.",
        ],
        "tips": TIPS,
    },
}


class Pack:
    def __init__(self, character="buddy"):
        self.character = character if character in PACKS else "buddy"
        self._data = PACKS[self.character]

    def get(self, key):
        return self._data[key]

    def pick(self, key):
        value = self._data[key]
        if isinstance(value, (list, tuple)):
            return random.choice(value)
        return value

    def chatter(self):
        if random.random() < 0.7 and self._data.get("jokes"):
            return self.pick("jokes")
        return self.pick("tips")
