markdown
# Event-Sim

A Python based event simulation engine. Heavily inspired by [Bransteele](https://brantsteele.net/hungergames/reaping.php).

**Please wait for v2. Download Removed.**

- [Contact](#contact)

---

## IN PROGRESS
**Simv2.0.0**

- Full system overhaul.
- Complete UI rewrite. Dark theme, modern layout, cleaner workflow.
- Complete engine rewrite. 
- EventWriter is now built into the main application.
- Flag system with multi-phase event chains. Events can require and set flags, creating narrative arcs that span multiple phases. A tribute can find a weapon in Day 1 and use it to kill someone in Night 2.
- AI commentator.
- Auto-host mode. Posts screenshots and AI commentary directly to 4chan threads using a Pass and API key. 
- Logs mode. Test auto host commentary without posting to a thread. Type "Logs" in the thread field.
- Image loading progress. See which images are loading and how many remain. Right click a tribute's portrait to reload their image.
- Visual bond system. Drag and drop tribute portraits to create bonds in the reaping preview.
- Bond protection mode. Bonded tributes can optionally never kill each other.
- Shared victory conditions. Victory by district, by bonds, or both.
- Faction mode with automatic bonding and faction flags.
- Season scraper. Import tributes and events from BrantSteele Classic and Experimental sims using a season code or URL.
- Full customization system. Fonts, colors, borders, backgrounds, text effects, shadows, outlines, and more.
- Death pacing system with budget and pressure controls. Seven difficulty modes from Low to Annihilation.
- Ghost events with configurable frequency. Seven ghost modes from None to High.
- No tribute name length limit.
- Every setting tested to ensure no tribute, bonded pair, or flag chain has an unfair advantage.

## Changelog

**Simv1.1.2**

- Fixed bug where multiple copies of the same tribute would populate fatal events when the bond mechanic was in use
- Bond selection during tribute input is now no longer deleted upon adding more tributes

**Simv1.1.1**

- Death rate system rebalanced
- Tribute portraits will now display based on the number of tributes specified in event metadata instead of event text
- Event file has been reuploaded without feast events
- Event fallback chain revamped

**Simv1.1.0**

- Added Fonts
- Better image handling for portraits and backgrounds

---

## Table of Contents
- [Code Database](#code-database)
- [Districts and Tribute Organization](#districts-and-tribute-organization)
- [Bonds](#bonds)
- [Bond Protection](#bond-protection)
- [Faction Mode](#faction-mode)
- [Multi Win](#multi-win)
- [Writing Events](#writing-events)
- [Fatal Events](#fatal-events)
- [Dead Tribute Flags](#dead-tribute-flags)
- [Best Practices](#best-practices)
- [Summary of Syntax](#summary-of-syntax)
- [Event Selection and Fallbacks](#event-selection-and-fallbacks)
- [Death Pacing](#death-pacing)
- [Ghost Events](#ghost-events)
- [AI Commentator and Auto-Host](#ai-commentator-and-auto-host)
- [Season Scraper](#season-scraper)
- [Virginia's Userscript Compatibility](#virginias-userscript-compatibility)
- [Screenshots](#screenshots)
- [FAQ](#faq)
- [Contact](#contact)

---

## Code Database

Complete collection of community created Hunger Games event sets from the [Code Database](https://hgtools.neocities.org/static/codes), converted to standard format for use with this sim.

### Download

**[Download All Codes (2.6 MB)](https://github.com/loveandpwns/Event-Sim/releases/download/Events/all_events.zip)**

**[Default Code](https://github.com/loveandpwns/Event-Sim/releases/download/Defaul_Events/Brant.Default.zip)**

**[Default Code With Flags](https://github.com/loveandpwns/Event-Sim/releases/download/Flags/Default.Events.With.Flags-AI.zip)**
- Default Code With Flags is made entirely with AI and is untested.

---

## Districts and Tribute Organization

### District Sizes

The simulator organizes tributes into districts (groups). You can choose from preset sizes or create custom districts:

**Preset sizes:**

* **1 tribute per district** Solo districts
* **2 tributes per district** (default)
* **3 tributes per district** Larger districts
* **4 tributes per district** Even larger groups
* **5 tributes per district** Large groups
* **6 tributes per district** Maximum preset size

**Custom mode:**

* Assign any tribute to any district number
* Create uneven district sizes (e.g., District 1 has 2 tributes, District 2 has 5)
* Maximum flexibility for non-standard simulations

### How to Set District Size

1. In the setup page, locate the **"District Size"** dropdown menu
2. Select your preferred option:
   * `1`, `2`, `3`, `4`, `5`, or `6` for automatic equal distribution
   * `Custom` for manual district assignment

**Automatic mode:** Tributes are assigned to districts sequentially based on the size you choose. For example, with 12 tributes and district size 2:

* District 1: Tributes 1-2
* District 2: Tributes 3-4
* District 3: Tributes 5-6
* And so on...

**Custom mode:** Each district has a spinbox where you can set how many tributes belong to it.

### Custom District Names

You can customize district names under the **Customize** menu. Districts will display either:

* Your custom name (if specified)
* `District [number]` (default)

**Example:** Instead of "District 1", you could display "Faction X" or "The Gung Ho Guns" or any custom label.

To set custom names:

1. Click the **Customize** button in the sidebar
2. Navigate to the district naming section
3. Enter custom names for each district number

---

## Bonds

The simulator supports a bond system that increases the likelihood of specific tributes appearing in non-fatal events together.

### How It Works

Bonded tributes have a **95% chance** of being selected together for non-fatal events when both are:
- Alive
- Available (not already used in another event that phase)
- Compatible with the event requirements

**Bonds only affect non-fatal event selection.** Fatal events treat all tributes equally regardless of bonds. This prevents bonded pairs from dying together at elevated rates.

### Setting Up Bonds

**Drag and drop:** In the reaping preview, drag one tribute's portrait onto another to create a bond between them. A colored border indicates bonded tributes.

**Right-click:** Right-click a bonded tribute's portrait to remove them from their bond group.

**Manual entry:** When editing the roster, enter a bond partner's number in the "Bond" field for each tribute.

### Important Notes

- Bonds increase the probability of tributes appearing in non-fatal events together. Nothing is guaranteed.
- Bonded tributes can still die. Bonds do not provide immunity.
- Fatal events ignore bonds entirely. Every tribute has an equal chance of being selected for fatal events.
- Bonds work independently of districts.
- If a bonded partner dies, the surviving tribute continues as normal.

---

## Bond Protection

Bond protection is an optional mode that prevents bonded tributes from killing each other.

### Modes

- **Normal:** Bonded tributes group together for non-fatal events but CAN kill each other in fatal events. This is the default.
- **Protected:** Bonded tributes group together for non-fatal events and can NEVER kill each other. If a fatal event would have a bonded tribute kill their partner, the event is rejected and a different one is selected.

### How to Enable

1. In the sidebar, set the **Bond Protection** dropdown to **Protected**
2. Set up bonds normally using drag-and-drop or manual entry

### Multi-Win Safety

When bond protection is set to Protected, the engine automatically enables bond-based victory detection. If all remaining tributes are mutually bonded and protected, the game ends in a shared victory instead of stalling forever.

---

## Faction Mode

### Simple Mode

Bonds all tributes in the same district. Bonded tributes are more likely to appear together in non-fatal events.

### Advanced Mode

Assigns faction flags based on district number. Tributes in district 1 get `faction1`, district 2 get `faction2`, etc.

**Faction events use variable substitution:**
- `faction1:1 faction2:2` means position 1 and position 2 must be from different factions
- The numbers are variables that map to whatever factions the selected tributes actually have
- One event works for any faction matchup

**Example events:**
```
# requires: faction1:1 faction2:2
# sets:
p1 ambushes p2 from an enemy faction.
```
```
# requires: faction1:1 faction1:2
# sets:
p1 betrays p2 despite being allies.
```

**Faction flags are filtered from normal event logic** so existing events continue working without modification.

**How to enable:** Select faction mode from the dropdown before starting simulation.

---

## Multi Win

The simulator supports shared victory conditions, allowing multiple tributes to win together based on districts or bonds.

### Shared Victory Modes

- **Victory by District**: If all remaining tributes are from the same district, they share the victory
- **Victory by Bonds**: If all remaining tributes are mutually bonded to each other, they share the victory
- **Combined Mode**: Enable both toggles to allow either condition to trigger a multi-win

### How to Use

1. In the sidebar, set the **"Multi-Win"** dropdown to **"Yes"**

2. When Multi-Win is enabled, two checkboxes appear:
   - **Victory by District**: Check this to allow district-based shared victories
   - **Victory by Bonds**: Check this to allow bond-based shared victories
   - You can enable one, both, or neither (if neither is checked, multi-win is effectively disabled)

3. Set up your tributes normally using districts and/or bonds

4. Run the simulation. The game will automatically end when all surviving tributes meet one of the enabled victory conditions

---

# Writing Events

## Basic Event Structure

Events are written in a text file that is based off of [Event Manager](https://hgtools.neocities.org/static/EventManagerHelp)

Every event follows a strict format that the event loader parses line by line:

```
# requires:
# sets:
(Player1) walks around a spooky cemetery.
1
D
```

**Line-by-line breakdown:**

1. `# requires:` - Flags that tributes must possess to qualify for this event
2. `# sets:` - Flags that will be applied to tributes after the event executes
3. Event text with player and pronoun placeholders
4. Number of living tributes required
5. `D` line - Number of ghosts needed

## Basic Events: No Flag Requirements

When both `requires` and `sets` fields are empty, any unflagged tribute can participate.

```
# requires:
# sets:
(Player1) finds a stick.
1
D
```

These "vanilla" events serve as the foundation of your event pool and ensure tributes always have available actions.

## The Requires Field: Filtering Participants

The `requires` field acts as a filter, restricting event participation to tributes who possess specific flags.

### All Participants Need the Same Flag

```
# requires: spooked
# sets:
(Player1) and (Player2) huddle together, still terrified.
2
D
```

Both Player1 and Player2 must have the `spooked` flag for this event to be eligible. If either tribute lacks the flag, the event cannot fire.

### Specific Participants Need Specific Flags

```
# requires: bloodlusted:1
# sets:
(Player1) attacks (Player2) without mercy.
2
D
```

The colon syntax (`:1`) specifies that only Player1 requires the `bloodlusted` flag. Player2 can be any available tribute.

### Multiple Players with Different Requirements

```
# requires: spooked:1 brave:2
# sets:
(Player1) screams while (Player2) tries to calm (him/her1) down.
2
D
```

Player1 must have `spooked`, Player2 must have `brave`. Each participant has distinct flag requirements.

## The Sets Field: Modifying Flags After Events

The `sets` field determines how tribute flags change after an event executes.

**Important:** The `sets` field REPLACES all flags on a tribute, it does not add to them. If a tribute has `armed` and the event sets `wounded`, the tribute now has `wounded` only. If you want the tribute to keep `armed`, the event must set `armed,wounded`. This is intentional. It gives the event writer full control over what flags a tribute has at any point.

### Clearing All Flags

```
# requires: spooked
# sets:
(Player1) finally calms down.
1
D
```

An empty `sets` field removes all flags from participating tributes, resetting them to a neutral state.

### Applying the Same Flag to All Participants

```
# requires:
# sets: injured
(Player1) trips and hurts (himself/herself1). (Player2) helps (him/her1) up but also gets hurt.
2
D
```

Both tributes receive the `injured` flag after this event completes.

### Applying Different Flags to Specific Participants

```
# requires:
# sets: killer:1
(Player1) murders (Player2) in cold blood.
2
1
2
```

Only Player1 receives the `killer` flag. Player2 dies in this event.

### Mixed Flag Assignment

```
# requires: paranoid:1
# sets: paranoid:1 scared:2
(Player1) attacks (Player2) thinking (he/she2) was a threat. (Player2) runs away terrified.
2
D
```

Player1 retains the `paranoid` flag, while Player2 receives the `scared` flag.

## Dead Players and Ghost Events

The `D` line specifies how many deceased tributes the event requires. This enables events where the dead interact with the living.

### No Dead Players Required

```
1
D
```

Standard format.

### Events Requiring Dead Players

```
1
D 1
```

This event needs one living tribute and one dead tribute.

**Example ghost event:**

```
# requires:
# sets: spooked
(Player1) sees the ghost of (Deadplayer1) and runs away in fear.
1
D 1
```

### Pure Ghost Events

```
# requires:
# sets:
(Deadplayer1) looms in the shadows.
0
D 1
```

Events with `0` living tributes and one or more dead tributes create atmospheric moments that don't directly involve living participants.

## Building Continuity Chains

Events can be linked together through flags to create narrative progressions:

```
# requires:
# sets: knife
(Player1) finds a rusty knife.
1
D

# requires: knife
# sets: knife_sharp
(Player1) sharpens (his/her1) knife on a strange-looking rock.
1
D

# requires: knife_sharp
# sets:
A hand shoots out of the strange rock and forcefully takes the knife from (Player1).
1
D
```

The system tracks flags per tribute, allowing individual storylines to develop organically throughout the simulation. A tribute who finds a knife in the Bloodbath can sharpen it on Day 1 and lose it on Night 1. Each step requires the previous flag and sets the next one.

## Advanced: OR Logic in Requirements

Use the pipe character (`|`) to create OR conditions:

```
# requires: injured|sick
# sets:
(Player1) rests to recover from (his/her1) condition.
1
D
```

The tribute needs either the `injured` OR `sick` flag to qualify.

## AND Logic

List multiple flags separated by spaces.

```
# requires: injured armed
# sets:
(Player1) brandishes (his/her1) weapon despite being hurt.
1
D
```

Player1 needs both `injured` AND `armed` flags.

### AND for Specific Players

```
# requires: paranoid:1 armed:1
# sets:
(Player1) attacks (Player2) with (his/her1) weapon, driven by fear.
2
D
```

Player1 needs both `paranoid` AND `armed`. Player2 can be anyone.

### Combining AND with OR

```
# requires: armed:1 injured|sick:2
# sets:
(Player1) defends (Player2), who is too weak to fight.
2
D
```

Player1 needs `armed` AND Player2 needs either `injured` OR `sick`.

---

## Fatal Events

Fatal events follow the same structure but include additional lines specifying killers and victims:

```
Fatal Day Events
# requires:
# sets:
(Player1) kills (Player2).
2
1
2
```

The last two lines indicate:

* Line 4: **Killer** (Player1 = position 1)
* Line 5: **Victim** (Player2 = position 2)

---

## Dead Tribute Flags

Flags work on dead tributes too. Dead tributes retain all their flags after death, allowing ghost events to reference their past.

**Requiring a dead tribute to have a flag:**

```
# requires: bloodlusted:d1
# sets:
(Player1) is haunted by the vengeful spirit of (Deadplayer1).
1
D 1
```

This event only fires if Deadplayer1 had the `bloodlusted` flag when alive or had it set after death.

**Setting a flag on a dead tribute:**

```
# requires:
# sets: cursed:d1
(Player1) desecrates (Deadplayer1)'s grave, cursing their spirit.
1
D 1
```

Deadplayer1 now has the `cursed` flag and can appear in future events that require it.

**Key point:** When a tribute dies, they keep all their flags. This allows you to create storylines that continue beyond death.

See the [Summary of Syntax](#summary-of-syntax) section for all dead tribute flag syntax options.

---

## Best Practices

* **Balance flagged and unflagged events.** Too many flag requirements can starve the event pool.
* **Strategic flag clearing.** Empty `sets` fields reset tributes, allowing them to qualify for more events.
* **Remember that sets replaces flags.** If a tribute should keep an existing flag through a new event, include it in the sets line.
* **Test continuity chains.** Ensure flag progressions make logical sense and that every stage of a chain has both non-fatal and fatal events available.
* **Vary participant counts.** Mix solo events with group events for variety.
* **Consider flag persistence.** Decide when flags should carry forward vs. clear after use.
* **Always provide unflagged events.** Flagged tributes can fall back to unflagged events if no matching flagged events exist. But if your unflagged pool is too small, gameplay gets repetitive.

---

## Summary of Syntax

### Living Tribute Requirements & Sets

| Field | Syntax | Meaning |
|-------|--------|---------|
| `# requires:` | *(empty)* | No requirements, any tribute qualifies |
| `# requires:` | `flagname` | All participants need this flag |
| `# requires:` | `flagname:1` | Only Player1 needs this flag |
| `# requires:` | `flag1:1 flag2:2` | Different flags for different players |
| `# requires:` | `flag1 flag2` | All participants need both flags (AND) |
| `# requires:` | `flag1\|flag2` | Participants need either flag (OR) |
| `# requires:` | `flag1:1 flag2:1` | Player1 needs both flags (AND) |
| `# requires:` | `flag1:1 flag2\|flag3:2` | Player1 needs flag1, Player2 needs flag2 OR flag3 |
| `# sets:` | *(empty)* | Clear all flags from participants |
| `# sets:` | `flagname` | Give all participants this flag (replaces existing flags) |
| `# sets:` | `flagname:1` | Only Player1 receives this flag |
| `# sets:` | `flag1:1,2` | Players 1 and 2 receive this flag |

### Dead Tribute Requirements & Sets

| Field | Syntax | Meaning |
|-------|--------|---------|
| `# requires:` | `flagname:d1` | Deadplayer1 must have this flag |
| `# requires:` | `flag1:d1 flag2:d2` | Different flags for different dead players |
| `# requires:` | `flag1 flag2:d1` | All living need flag1; Deadplayer1 needs flag2 |
| `# sets:` | `flagname:d1` | Give Deadplayer1 this flag (marks the corpse) |
| `# sets:` | `flag1:1 flag2:d1` | Player1 gets flag1; Deadplayer1 gets flag2 |
| `D` | `D` | No dead tributes needed |
| `D` | `D 1` | One dead tribute needed |
| `D` | `D 2` | Two dead tributes needed |

---

## Event Selection and Fallbacks

The engine prioritizes events in this order:

1. **Flagged events** that match the current tribute's flags
2. **Unflagged events** if no matching flagged events exist

**Important:** Flagged tributes can participate in unflagged fatal events. This prevents "immortal flag chains" where a tribute gets stuck in a loop of flagged non-fatal events and can never be eliminated.

If a tribute has flags but no matching flagged events exist, they fall back to unflagged events. To avoid repetitive fallback scenarios, maintain a diverse pool of both flagged and unflagged events.

---

## Death Pacing

The engine uses a budget and pressure system to control how many tributes die per phase. This prevents both massacres (everyone dying in the Bloodbath) and stalls (nobody dying for five phases in a row).

### Death Mode

Controls the overall lethality of the simulation. Set this in the sidebar before starting.

| Mode | Description |
|------|-------------|
| **Low** | Slow burn. Few deaths per phase. Games last longer. |
| **Medium** | Balanced. The default. |
| **High** | Aggressive. More deaths, shorter games. |
| **Very High** | Dangerous. Tributes drop fast. |
| **Extreme** | Brutal. Most tributes won't survive long. |
| **Nightmare** | Near-constant death. |
| **Annihilation** | Maximum lethality. Games end quickly. |

### How It Works

Each phase, the engine calculates a **death budget** based on how many tributes are alive and the current death mode. This is a hard cap on deaths for that phase.

Within that budget, a **pressure system** determines the probability of each individual event being fatal. Higher pressure means more fatal events are attempted.

The Bloodbath always has elevated lethality compared to normal Day/Night phases.

As the game approaches its end (final 5, final 3, final 2), the engine adjusts pacing to slow down and build tension rather than rushing to a conclusion.

Every phase is guaranteed at least one death to prevent stalling, unless a multi-win condition is already met.

---

## Ghost Events

Ghost events allow dead tributes to appear in events after they've been eliminated.

### Ghost Mode

Controls how frequently ghost events occur. Set this in the sidebar before starting.

| Mode | Frequency |
|------|-----------|
| **None** | Ghosts never appear |
| **Whisper** | Extremely rare |
| **Extremely Low** | Very rare |
| **Very Low** | Rare (default) |
| **Low** | Occasional |
| **Medium** | Moderate |
| **High** | Frequent |

Ghost probability scales with the number of dead tributes. More dead tributes means a slightly higher chance of ghost events firing.

Ghost events do not fire in the late game (3 or fewer tributes alive) to avoid cluttering the endgame.

### Writing Ghost Events

See the [Dead Players and Ghost Events](#dead-players-and-ghost-events) section under Writing Events for the syntax.

---

## AI Commentator and Auto-Host

The simulator can automatically post screenshots and AI-generated commentary to 4chan threads.

### Requirements

- A 4chan Pass (for posting)
- An API key from one of the supported providers

### Supported Providers

| Provider | Models |
|----------|--------|
| **Groq** | Llama 3.3 70B, Llama 3.1 70B, Llama 3.1 8B, Mixtral 8x7B, Gemma2 9B |
| **OpenAI** | GPT-4o, GPT-4o-mini, GPT-4 Turbo, GPT-3.5 Turbo |
| **Anthropic** | Claude Sonnet, Claude Haiku |

### How to Use

1. Set up your tributes and load events as normal
2. Go to **Tools > Auto Host**
3. Enter your 4chan Pass ID and PIN
4. Select a board and enter the thread number
5. Select an AI provider, enter your API key, and choose a model
6. Click **Start Auto Host**

The auto-host will simulate the game phase by phase, take a screenshot of each phase, generate commentary using the AI, and post the screenshot with commentary to the thread. There is a built-in delay between posts to avoid rate limiting.

### Logs Mode

If you want to test the AI commentary without posting to a thread, type **"Logs"** in the thread field instead of a thread number. The auto-host will run normally but skip all 4chan posting. Commentary is saved to a log file in the save folder.

### Commentary

The AI generates 2-3 sentences of commentary per phase based on the events that occurred. It uses the correct pronouns for each tribute based on their gender setting. The commentary is written in the style of a battle royale commentator.

---

## Season Scraper

Import tributes and events from existing BrantSteele seasons.

### How to Use

1. Go to the setup page and click **Load Season**
2. Enter either:
   - A season code (e.g., `XM8aErjk`)
   - A full BrantSteele URL
3. The scraper will detect whether it's an Original or Classic sim and download the season data
4. Events are saved locally and loaded into the simulator automatically

### Supported Sims

- **BrantSteele Original** (brantsteele.net)
- **BrantSteele Classic** (brantsteele.com/hungergames/classic)

---

## Virginia's Userscript Compatibility

This simulator is compatible with [Virginia's Hunger Games Script](https://github.com/zmnmxlntr/hg)

### Required Modification

The original Virginia's script needs two small changes to work with our simulator.

**Step 1: Add clipboard copying**

Find this exact line in the script:

```
GM_setValue("imgsStr", imgsStr.slice(0, -1));
```

**Add these lines immediately after it:**

```
GM_setClipboard(
    GM_getValue("nomsStr") + "\n" +
    GM_getValue("gensStr") + "\n" +
    GM_getValue("imgsStr")
);
alert("Tribute data copied to clipboard!");
```

**Step 2: Add the clipboard permission**

Find this exact line near the top of the script:

```
// @grant       GM_getValue
```

**Add this line immediately after it:**

```
// @grant       GM_setClipboard
```

Save the script.

### How to Use

**In the Simulator**: Click "Import Tributes" and the data loads automatically from your clipboard.

---

## Screenshots

*Screenshots will be updated for v2.0.0.*

---

## FAQ

### What is this?
A desktop Hunger Games-style event simulator. Inspired by BrantSteele but with more features and full offline support.

### Is there a rig button?
No, a rig button does not exist and will never exist. No one has directly asked for one either. You know better than to believe anon fanfiction.

### Can you prove it's not rigged?
I ran 40+ million simulations validating the bond system alone to ensure fairness. The methodology and results are documented in this README under the bond system section of the changelog.

### How do bonds work?
Bonded tributes are more likely to appear in non-fatal events together. Fatal events treat everyone equally regardless of bonds. Bonds do not protect tributes from dying. They do not guarantee anything. They increase the odds of interaction, not survival.

### What is bond protection?
An optional mode where bonded tributes cannot kill each other. This is separate from normal bonds. You have to enable it explicitly.

### What are flags?
Flags are tags that get attached to tributes during the simulation. Events can require specific flags and set new ones. This creates multi-phase storylines. For example, a tribute finds a weapon (sets `armed` flag), then a later event requires `armed` and has them use the weapon. See the [Writing Events](#writing-events) section.

### How does the AI commentator work?
It sends the events from each phase to an LLM (your choice of provider) and gets back 2-3 sentences of commentary. You need your own API key. Groq has a free tier.

### Someone is pretending to be you.
I post in the README. That's it.

---

## Contact

**Author:** [loveandpwns](https://github.com/loveandpwns)
**Email:** [loveandpwns@gmail.com](mailto:loveandpwns@gmail.com)
**Discord:** `loveandpwns`

---

> *Event-Sim © 2025 - Created by loveandpwns*
