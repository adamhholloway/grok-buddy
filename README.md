# Grok Buddy

A desktop pet for Grok Build on this computer. They sit on top of your windows, talk in a speech bubble (and out loud if you want), and react when a Grok session starts, needs permission, or finishes a turn.

Two characters: **Buddy** (raccoon in a hard hat) and **Annie** (gothic lolita, Annie voice). Right-click to switch.

## Use it

```bash
grok-buddy                 # start (or poke the one already running)
grok-buddy say "hey"       # make them talk
grok-buddy character annie # switch to Annie
grok-buddy character buddy # switch to Buddy
grok-buddy tip             # random Grok Build tip
grok-buddy hide            # vanish for 15 minutes
grok-buddy quit
```

- **Drag** to move
- **Click** for a tip
- **Double-click** to nap / wake
- **Right-click** for voice, idle chatter, hide, quit

He starts with the desktop and listens to Grok Build through hooks in `~/.grok/hooks/`.

## Install again

```bash
~/grok-buddy/install.sh
```
