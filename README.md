# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
FitFindr is an agent that allows a user to enter a description of what they are looking for as a query. The query is accepted and parsed and handed to the first tool search_listings, which searches a database of listings to look for any matches, and returns a list of listing dictionaries or an empty list. If empty, the agent stops. If matching listings are found, the closest match is selected and passed to suggest_outfit, which suggests 1-2 outfits based on the users wardrobe, or genral styling advice if the wardrobe is empty. Lastly the selected item and suggested outfit are passed to create_fit_card which generates a caption for the user, highlighting the thrifted item and the vibe of the suggested outfit.


---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->


### `search_listings`

- **What it does:** Searches the listing data for an item matching the description it receives as input, with size and price ceiling optionally included.
- **Inputs:** description (str), size (str) | None = None, max_price (float) | None = None
- **Returns:** A list of listing dictionaries, best keyword match first and at most 10 (`config.SEARCH_RESULT_LIMIT`), each with id, title, description, category, style_tags (list), size, condition, price (float), colors (list), brand (str or None), platform
- **When it has nothing:** Returns an empty list
- **What counts as a size match:** Whole tokens only, never a substring test. Both sizes are uppercased, anything in parentheses is dropped, and the listing size is split on `/`. The size matches if the requested size equals one of those tokens.
  - `M` matches `S/M` and `M/L`. `XL` matches `XL (oversized)`.
  - `L` does **not** match `XL`, and `S` does **not** match `US 7`. These are the two traps a substring test falls into.
  - Shoe sizes match exactly: `US 9` matches `US 9` but not `US 8.5`.
  - A waist request matches waist+inseam: `W30` matches `W30 L30`.
  - Any `One Size` listing matches every size request. It's meant to fit anyone, so filtering it out would hide items that would work.
  - With no size given, nothing is filtered by size.

### `suggest_outfit`

- **What it does:** Uses the gifted item and users wardrobe to suggest one or two maximum outfits.
- **Inputs:** new_item (listing dict), wardrobe (dict) 
- **Returns:** Non-empty string with 1-2 outfit suggestions from wardrobe
- **When it has nothing:** Non-empty string with general styling suggestions

### `create_fit_card`

- **What it does:** Generate a caption based off the new item and vibe of the outfit
- **Inputs:** outfit (str), new_item (listing dict)
- **Returns:** Non-empty string caption, 2-4 sentences in length
- **When it has nothing:** returns a descriptive string

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If search_listings returns an empty list, put a message in
        session["error"] naming what the user could change, and return the
        session without calling suggest_outfit. Otherwise take the first
        result, put it in session["selected_item"], and continue.

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** Regex, in `agent.py::parse_query`, with no model call. It pulls out three things in this order, cutting each one out of the text once it's found:
1.Price 2.Size 3.Description

**What moves through the session:** One dict, created by `new_session()`, holds everything. Each step writes its result into the session, and the next step reads it back from there. Nothing is passed straight from one call to the next.

| Order | Field | Written by | Read by |
|---|---|---|---|
| 1 | `query`, `wardrobe` | `new_session()` | `parse_query` / `suggest_outfit` |
| 2 | `parsed` (description, size, max_price) | `parse_query` | `search_listings` |
| 3 | `search_results` (list of listing dicts) | `search_listings` | the branch |
| 4 | `error` (only if the search came back empty; the run stops here) | the branch | `_show` / `app.py` |
| 5 | `selected_item` (`search_results[0]`) | the loop | `suggest_outfit`, `create_fit_card` |
| 6 | `outfit_suggestion` (str) | `suggest_outfit` | `create_fit_card` |
| 7 | `fit_card` (str) | `create_fit_card` | returned to the user |

If the run stops at step 4, `selected_item`, `outfit_suggestion` and `fit_card` stay `None`. If the model can't be reached, `error` is set instead and `search_results` is kept.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```
python app.py ask 'vintage graphic tee under $30'
[1] parse_query
      in:  vintage graphic tee under $30
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey, Y2K Baby Tee — Butterfly Print … +7 more
      →    10 match(es)
[3] select_item
      out: Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
[4] suggest_outfit
      in:  Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      out: **Outfit 1** - Graphic Tee — 2003 Tour Bootleg Style - Baggy straight-leg jeans, dark wash - Black combat boot…
      →    10 wardrobe item(s)
[5] create_fit_card
      in:  Graphic Tee — 2003 Tour Bootleg Style ($24.0, depop)
      out: I literally scored this 2003 tour bootleg graphic tee for only $24 on Depop and I'm obsessed with how heavy th…

  Found:    Graphic Tee — 2003 Tour Bootleg Style — $24.0 on depop

  Outfit:   **Outfit 1**
- Graphic Tee — 2003 Tour Bootleg Style
- Baggy straight-leg jeans, dark wash
- Black combat boots
- Vintage black denim jacket
- Black crossbody bag

*Why it works:* This creates an effortless, head-to-toe monochrome grunge aesthetic using classic streetwear layers and textures.

**Outfit 2**
- Graphic Tee — 2003 Tour Bootleg Style
- Wide-leg khaki trousers
- Brown leather belt
- Chunky white sneakers
- Black cropped zip hoodie

*Why it works:* Tucking the graphic tee into the trousers with a belt anchors the relaxed fit, while the hoodie and sneakers add a casual streetwear balance.

  Fit card: I literally scored this 2003 tour bootleg graphic tee for only $24 on Depop and I'm obsessed with how heavy the cotton is. I paired it with dark wash baggy jeans, a vintage denim jacket, and combat boots for the ultimate effortless monochrome grunge look. It also looks so sick tucked into khaki trousers with a belt and a cropped hoodie for a more casual streetwear vibe.

1 model calls this session, 1 served from cache, 358 prompt + 82 output tokens

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
[{'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}]
```


```
$ python -c "from tools import suggest_outfit; ..."

```
python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
**Outfit 1**
- Vintage Levi's 501 Jeans — Medium Wash
- White ribbed tank top
- Black combat boots
- Brown leather belt
- Vintage black denim jacket

*Why it works:* The medium-wash denim contrasts nicely with the black jacket, while the white tank and combat boots create a classic, edgy 90s aesthetic.

**Outfit 2**
- Vintage Levi's 501 Jeans — Medium Wash
- Oversized grey crewneck sweatshirt
- Chunky white sneakers
- Black crossbody bag

*Why it works:* The relaxed grey crewneck and white sneakers lean into effortless streetwear, perfectly complementing the straight-leg fit of the vintage Levi's.


```
$ python -c "from tools import create_fit_card; ..."

```
python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Scored these vintage Levi's 501 jeans for only $38 scrolling through Depop and I'm obsessed with the medium wash. I kept it super classic today by pairing them with fresh white sneakers for that ultimate effortless streetwear vibe. Honestly, nothing beats finding the perfect pair of broken-in denim that fits just right on the first try.
---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked for an evaluation of my 3 criterion to ensure they were testible.
- *What came back:* It gave me a two part rewritten criteria for getting inputting empty wardrobe in suggest_outfit for 5 different items.
- *What I changed:* i removed the first part of not returning empty which is handled by my code deterministicaly, and maintained just two specific garment criteria.

**Moment 2**

- *What I asked for:* I gave Claude my suggest_outfit spec.
- *What came back:* Returned a complete working function.
- *What I changed:* I added a role in the prompt, and modified the rules slightly.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
