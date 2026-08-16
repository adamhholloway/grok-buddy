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
    "Session details — model, turns, the whole report card — live under /session-info.",
    "I sit on top of your windows on purpose. Drag me. I can take it.",
    "Double-click me to nap. Double-click again when you miss me.",
    "Right-click to switch between Buddy and Annie.",
]

PACKS = {
    "buddy": {
        "welcome": (
            "It looks like you're using Grok Build. I'm Buddy — I'll sit over here "
            "and keep you company."
        ),
        "switch": "Buddy reporting for duty. The wrench is ceremonial.",
        "greetings": [
            "Need a hand with Grok Build?",
            "It looks like you're writing a prompt. Want a tip?",
            "Still building. I respect the grind.",
            "Click me for a tip. Drag me if I'm in the way.",
            "I can watch your Grok sessions from over here. I don't judge. Much.",
            "Right-click me if you want the quiet version of this relationship.",
            "Hey. I'm still here. The wrench is ceremonial.",
            "Bonzi had a gorilla. Clippy had a paperclip. You get a raccoon in a hard hat.",
        ],
        "session_start": [
            "It looks like you're about to build something. Need a hand?",
            "Grok Build is up. I'll just… sit here. Menacingly. Helpfully.",
            "New session. Fresh mistakes. Let's go.",
            "I'm here. Try not to `rm` anything important.",
        ],
        "session_end": [
            "Session's over. I'll keep the chair warm.",
            "That's a wrap. Poke me if you want a tip.",
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
            "Grok hit a snag. Deep breath. Then /rewind if you need it.",
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
            "It looks like you're using Grok Build. I'm Annie. I'll perch over here "
            "and keep you honest."
        ),
        "switch": "Annie's on deck. The raccoon can have a break.",
        "greetings": [
            "Need a hand, or are you just staring at the prompt again?",
            "It looks like you're writing a letter. Wait. Wrong century. A prompt.",
            "I'm here. The bows are load-bearing.",
            "Click me for a tip. Drag me if I clash with your wallpaper.",
            "Buddy has the wrench. I have opinions.",
            "Right-click if you want the raccoon back. I won't be offended. Much.",
            "Still here. Gothic, helpful, slightly judgmental.",
            "Clippy wish he had twin-tails.",
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
            "Snag. Breathe. /rewind if you need a do-over.",
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
