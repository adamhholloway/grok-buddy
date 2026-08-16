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
