# Event-Sim, Coming Soon!
A Python based event simulation engine. Heavily inspired by [Bransteele](https://brantsteele.net/hungergames/reaping.php).

---

## Table of Contents
- [Code Database](#code-database)
- [Districts and Tribute Organization](#districts-and-tribute-organization)
- [Bonds](#bonds)
- [Writing Events](#writing-events)
- [Fatal Events](#fatal-events)
- [Dead Tribute Flags](#dead-tribute-flags)
- [Best Practices](#best-practices)
- [Summary of Syntax](#summary-of-syntax)
- [Event Selection and Fallbacks](#event-selection-and-fallbacks)
- [Virginia's Userscript Compatibility](#virginias-userscript-compatibility)
- [Coming Soon](#coming-soon)
- [Contact](#contact)

---

## Code Database

Complete collection of community created Hunger Games event sets from the [Code Database](https://hgtools.neocities.org/static/codes), converted to standard format for use with this sim. 

### Download

**[Download All Codes (2.6 MB)](https://envs.sh/ROn.zip)**

**[Default Code](https://envs.sh/15A.zip )**

---

## Districts and Tribute Organization

### District Sizes

The simulator organizes tributes into districts (groups). You can choose from preset sizes or create custom districts:

**Preset sizes:**

* **2 tributes per district** (default)
* **3 tributes per district**  Larger districts
* **4 tributes per district**  Even larger groups
* **6 tributes per district**  Maximum preset size

**Custom mode:**

* Assign any tribute to any district number
* Create uneven district sizes (e.g., District 1 has 2 tributes, District 2 has 5)
* Maximum flexibility for non-standard simulations

### How to Set District Size

1. In the tribute input screen, locate the **"District Size"** dropdown menu
2. Select your preferred option:
   * `2`, `3`, `4`, or `6` for automatic equal distribution
   * `Custom` for manual district assignment

**Automatic mode:** Tributes are assigned to districts sequentially based on the size you choose. For example, with 12 tributes and district size 2:

* District 1: Tributes 1–2
* District 2: Tributes 3–4
* District 3: Tributes 5–6
* And so on...

**Custom mode:** Each tribute row will have an enabled district dropdown where you can manually select which district (1 through total number of tributes) that tribute belongs to.

### Custom District Names

You can customize district names under the **Customize** tab. Districts will display either:

* Your custom name (if specified)
* `District [number]` (default)

**Example:** Instead of "District 1", you could display "Faction X" or "The Gung Ho Guns" or any custom label.

To set custom names:

1. Click the **Customize** button in the sidebar
2. Navigate to the district naming section
3. Enter custom names for each district number

---

## Bonds

The simulator supports a simple bond system that increases the likelihood of specific tributes appearing in events together.

### How It Works

When creating tributes, you can specify a bond partner by entering their tribute number in the "Bond" field. Bonded tributes have a **50x higher chance** of being selected for the same event when both are:
- Alive
- Available (not already used in another event that turn)
- Compatible with the event requirements

### Setting Up Bonds

1. Enter the number of tributes and click "Confirm"
2. For each tribute, enter their bond partner's number in the "Bond" field
   - Example: For Tribute 1 to bond with Tribute 2, enter "2" in Tribute 1's bond field and "1" in Tribute 2's bond field
3. Bonds are manual - you must enter both sides of the partnership
4. Click "Confirm All Tributes" to finalize

### Important Notes

- Bonds increase pairing probability. Nothing is guaranteed.
- Bonds currently only work in two player pairings.
- If a bonded partner dies or gets different continuity flags, they may not pair.
- Bonds work independently of districts.
- Simple mode is designed for balanced gameplay without forced pairings.

### Advanced Mode (Coming Soon)

A future update will add dedicated bond events that **require** both partners to be alive and will guarantee they appear together for specific story moments.

---

# Writing Events

Please visit [Event-Writer](https://github.com/loveandpwns/Event-Writer) for a tool that helps you write events. 

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
5. `D` line - Number of "Ghosts" needed.

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

Standard format

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
# sets: knife_3
(Player1) sharpens (his/her1) knife on a strange-looking rock.
1
D

# requires: knife_3
# sets: 
A hand shoots out of the strange rock and forcefully takes the knife from (Player1).
1
D
```

The system tracks flags per tribute, allowing individual storylines to develop organically throughout the simulation.

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

* **Balance flagged and unflagged events** Too many flag requirements can starve the event pool
* **Strategic flag clearing** Empty `sets` fields reset tributes, allowing them to qualify for more events
* **Test continuity chains** Ensure flag progressions make logical sense
* **Vary participant counts** Mix solo events with group events for good gameplay
* **Consider flag persistence** Decide when flags should carry forward vs. clear after use

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
| `# sets:` | `flagname` | Give all participants this flag |
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

The event loader prioritizes events in this order:

1. Events where all flag requirements are met
2. Unflagged events (empty `requires` field)
3. Random selection from available pool

**Important:** Flagged tributes can participate in unflagged fatal events. This prevents "immortal flag chains" where a tribute gets stuck in a loop of flagged non-fatal events and can never be eliminated.

If a tribute has flags but no matching flagged events exist, they'll participate in unflagged events instead. To avoid repetitive fallback scenarios, maintain a diverse pool of both flagged and unflagged events.

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

**In the Simulator**: Click "Import Tributes" and the data loads automatically.

---

## Coming Soon

| Feature | Description |
|---------|-------------|
| **Better Customization** | More granular control over simulator visuals, behavior, and user settings. |
| **Advanced Bonds** | Advanced bond system. |
| **Complex District Events** | District or faction-specific events that evolve based on shared traits and history. |
| **Extra Events** | Support for Feast, Arena, and other special types of events. |

---

## Contact

**Author:** [loveandpwns](https://github.com/loveandpwns)  
**Email:** [loveandpwns@gmail.com](mailto:loveandpwns@gmail.com)  
**Discord:** `loveandpwns`

---

> *Event-Sim © 2025 - Created by loveandpwns
