# TakeMeter

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, the
> notebook, the baseline, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> head -5 data/practice_labels.csv     # the shape your labels.csv needs
> ```
>
> Then open `takemeter.ipynb` **in this folder** — in VS Code, or with
> `jupyter notebook` if you prefer. Pick the kernel: the `.venv` inside this
> project. Run section 1, which reports the hardware you'll be training on.
> Everything else waits until you have data.
>
> Nothing to upload, nothing to connect, no accounts and no keys. The notebook
> runs on your machine and writes next to your code.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     Unit 5 asks for the first five sections. Unit 6 adds the five below them.

     Everything is pasted as TEXT. No screenshots, no images.

     ⚠️ The confusion matrix especially. The notebook prints one as a markdown
     table, ready to copy. A screenshot of a matrix earns nothing. Paste the
     table.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 5 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Your community, and what your classifier sorts posts into. Three or four
     sentences. -->

TakeMeter reads posts from r/sitcoms, a subreddit where fans talk about TV
comedies, and sorts each one by what the post is doing. It labels a post as an
`opinion`, a `discussion_prompt` , or `news_tribute`. The point
is to tell apart posts that offer a take from posts that ask for one, which is
a line that question-style titles blur. It is trained and run entirely on my
own machine, using a small model fine-tuned on about 180 labelled posts.

---

## Label Taxonomy

<!-- Each label: a one-sentence definition and two real examples from your
     reading. Then your decision rule for the hardest boundary.

     The decision rule is worth a point on its own and it's the thing most
     people leave out. Every taxonomy has a hardest boundary. Name yours. -->

### `opinion`

**Definition:** The poster states their own view about a show, character, actor or episode, positive or negative.

**Example 1:**

> Married With Children was on another level 🤣

**Example 2:**

> The Office is insufferable, I'm sorry :( I just don't get it, I mean I had to suffer through 4 seasons to try and find the funny

### `discussion_prompt`

**Definition:** The poster's main purpose is to ask the community for opinions, recommendations or memories, without stating their own position.

**Example 1:**

> What character starts amazing and ends insufferable to you

**Example 2:**

> 14 years ago today “Don’t Trust The B—— in Apt 23” premiered. Did you like the show?

### `news_tribute`

**Definition:** The post shares news, an anniversary, a tribute, a photo or clip, or a promotion, with no view of its own about the show.

**Example 1:**

> Happy 80th Birthday to The Fonz Henry Winkler 10/30/1945

**Example 2:**

> First look at the ‘Big Bang Theory’ spin-off series ‘STUART FAILS TO SAVE THE UNIVERSE’.

### The hardest boundary

**Which two labels:** `discussion_prompt` vs. `opinion`

**The decision rule I used every time:**

If the post states its own position about a specific show or character, label it `opinion`, even if it ends with a question. If it only asks and states no position, it's `discussion_prompt`. Test: "Could I say what the poster thinks?" If yes, it's `opinion`.

Other rules: a mixed opinion (some praise, some criticism) is still `opinion`. A post that shares news or a tribute and adds its own view ("RIP James, everyone should watch Apt 23!") is `opinion`. Sarcasm is labelled by the stance the poster means. Memes with no readable text, off-topic posts and recurring mod threads are dropped.

---

## The Dataset

<!-- Where you collected from, how you labelled, your counts, and three hard
     cases. -->

**Where the posts came from:** Sitcoms subreddit r/sitcoms

**How I labelled them:** <!-- Cold first? Pre-labelled with AI and corrected?
Labelled about 20-30 cold, and then pre-labelled the rest with AI and reviewed.

**Counts per label:**

| Label             | Count | Share |
| ----------------- | ----- | ----- |
| discussion_prompt | 85    | 46%   |
| opinion           | 65    | 35%   |
| news_tribute      | 34    | 18%   |
| **Total**         | 184   | 100%  |

**Three hard cases**

<!-- Any post that made you pause: what it was, which two labels it could have
     been, and what you chose. These are worth more than the easy 190. -->

**1.**

> _The post:_ "Friends - favorite to least favorite character? What does your list look like? My favorite to least favorite - Rachel, Joey, Ross, Monica, Chandler, Phoebe."
>
> _Could have been:_ `discussion_prompt` or `opinion`
>
> _I chose `opinion`, because:_ It is phrased as a question and invites replies, but the poster gives their own full ranking, so I can say what they think. That passes my decision rule ("could I say what the poster thinks?"), which makes a stated position win over question form. I first labelled it `discussion_prompt` and changed it after applying the rule. Two similar ranking posts got the same label.

**2.**

> _The post:_ "14 years ago today “Veep” premiered. Did you like the show ?"
>
> _Could have been:_ `discussion_prompt` or `news_tribute`
>
> _I chose `discussion_prompt`, because:_ The anniversary is only the hook. The post's purpose is to ask the community for opinions, and it states no view of its own. About 18 posts followed this template, so I kept two and removed the rest, so near-identical posts could not land on both sides of the train/test split.

**3.**

> _The post:_ "Fay Ripley: The pilot of Cold Feet bombed"
>
> _Could have been:_ `news_tribute` or `opinion`
>
> _I chose `opinion`, because:_ The headline carries a verdict on the show (it "bombed"), not just an event. The catch is that the view belongs to the actress, not the poster, so this is the weakest of my `opinion` labels. A reasonable reader could call it `news_tribute`.

---

## The Training Run

<!-- Your starting model, your settings, and anything you changed and why. -->

**Base model:**

device: cpu (CPU)
torch: 2.2.2

**Settings:** <!-- epochs, learning rate, batch size, seed -->

EPOCHS = 10
LEARNING_RATE = 2e-5
BATCH_SIZE = 16

seed = 42

**Anything I changed from the defaults, and why:**

Changed epoch size to 10 because the model was returning 0.00 f-scores for two labels, likely defaulting to one label.

**Split sizes:** <!-- train / val / test, and per-label counts in the test
split. If a label had fewer than about 8 in test, say so — it explains a lot
of next unit's variance. -->

train 139 · val 31 · test 30

                   train  val  test

label  
discussion_prompt 58 13 13
opinion 47 11 10
news_tribute 34 7 7

[note] 'news_tribute' has only 7 examples in the test split.

---

## How I Used AI

<!-- Two specific moments — what you asked, what came back, what you changed.

     ⚠️ Plus disclosure of any pre-labelling. If you had a model pre-label a
     batch and then read and corrected every one, say that. It's an allowed
     workflow and disclosing it costs you nothing. Not disclosing it is the
     problem. -->

**Moment 1: choosing the labels**

- _What I asked for:_ I asked which labels would suit the data. I started from hot_take / analysis / reaction, and AI read the first 110 posts I'd collected.
- _What came back:_ AI said those labels fit r/sitcoms poorly: analysis was under 3% of posts and reaction was rare. About 45% of posts were questions asking for opinions. It proposed praise / criticism / discussion_prompt, with a decision rule for questions that also state a view. After labelling, criticism was only 11 of 154 rows (7%), so I asked about balance and it offered options, with counts for each.
- _What I changed:_ I chose to merge praise and criticism into one `opinion` label and add `news_tribute` for posts with no view of their own, which gave a 52 / 31 / 17% split. I kept the decision rule ("could I say what the poster thinks?") and applied it myself, which is why I moved the Friends ranking post from discussion_prompt to opinion.

**Moment 2: avoiding leakage**

- _What I asked for:_ I said I wanted to absolutely avoid leakage between train and test, after AI flagged posts that looked alike.
- _What came back:_ AI read how the notebook splits (a random 70/15/15 split, with a duplicate check that only catches exact copies) and found 18 near-identical posts of the form "N years ago today 'Show' premiered. Did you like the show?". It explained that they would land on both sides of the split and inflate my scores, and recommended keeping two.
- _What I changed:_ I agreed, and chose to keep two of the 18 and remove the other 16, taking the dataset from 200 to 184 posts. I also relabelled the one inconsistent sibling ("Rules Of Engagement") to discussion_prompt before it was removed.

**Pre-labelling disclosure:**
I used AI to pre-label my dataset, and I reviewed it. I labelled about 20-30 posts cold first. AI then pre-labelled the rest, under the definitions I wrote, and I read every row and agreed with the labels except four I changed myself (the Friends and Boy Meets World ranking posts and the "best outfits" post from discussion_prompt to opinion, and the Cold Feet headline from news_tribute to opinion). AI also wrote the script that collected the posts from r/sitcoms and the first drafts of my label definitions and hard cases, which I edited. The final labels, the decision rule and the choice to merge and cut posts are mine.

<!-- ═══════════════════════ UNIT 6 — THE TEST ═══════════════════════

     Don't fill these in during unit 5.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Baseline vs. Trained

<!-- Both models on the same posts. `python baseline.py --trained results.json`
     prints this table for you. -->

| Measure                  | Baseline | Trained | Difference |
| ------------------------ | -------- | ------- | ---------- |
| Overall accuracy         | 0.600    | 0.700   | +0.100     |
| Macro F1                 | 0.457    | 0.659   | +0.202     |
| F1 — `discussion_prompt` | 0.727    | 0.800   | +0.073     |
| F1 — `news_tribute`      | 0.000    | 0.545   | +0.545     |
| F1 — `opinion`           | 0.645    | 0.632   | -0.014     |

**What I predicted before I looked:**

My trained model will have better F1 scores for the smaller datasets with labels news_tribute and opinion.

**What the gap actually means:**

<!-- If the baseline matched your trained model, your fine-tuning added
     nothing — and that is a real finding, not a failure. Say it plainly. -->

---

## Run Log — Before

<!-- Five criteria across three seeds. The notebook's section 6 prints the
     spread table; the Target and Verdict columns are yours. -->

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
| --------- | ------ | ------- | ------ | --------- | ------- |
| 1.        |        |         |        |           |         |
| 2.        |        |         |        |           |         |
| 3.        |        |         |        |           |         |
| 4.        |        |         |        |           |         |
| 5.        |        |         |        |           |         |

### Confusion matrix

<!-- ⚠️ TYPED AS A MARKDOWN TABLE. The notebook prints one ready to paste.
     An image of a matrix earns nothing. -->

| true \ predicted |     |     |     |
| ---------------- | --- | --- | --- |
| \*\*\*\*         |     |     |     |
| \*\*\*\*         |     |     |     |
| \*\*\*\*         |     |     |     |

**My biggest off-diagonal number, and what it means:**

<!-- Not "the model made mistakes" — WHICH boundary it didn't learn, and which
     direction. "7 real analysis posts were called hot_take and only 3 went the
     other way" is a direction, not just an error rate. -->

---

## Verdicts and Diagnoses

<!-- MET or MISSED against LAST UNIT's target. The target has to hold across
     all three seeds, not turn up sometimes. -->

| #   | Criterion | Target | Verdict | How I decided |
| --- | --------- | ------ | ------- | ------------- |
| 1   |           |        |         |               |
| 2   |           |        |         |               |
| 3   |           |        |         |               |
| 4   |           |        |         |               |
| 5   |           |        |         |               |

**Diagnoses**

<!-- For each miss: the cause, and how you know. The four common causes are:
     too few examples for a label, a boundary you applied inconsistently, a
     genuinely hard label pair, and a task the model can't reach from this
     much data.

     ⚠️ Use your agreement report as evidence. It is the only instrument you
     have that can tell a LABELLING problem from a MODEL problem, and this
     section is graded on whether you used it that way. -->

---

## Agreement Report

<!-- Your rate against the staff set, and every disagreement adjudicated.

     Remember you labelled these 30 under the STAFF taxonomy in
     data/staff_taxonomy.md, not your own — so every argument below is made
     from those definitions and those decision rules. -->

**Agreement rate:** **_ / 30 = _**%

<!-- Nobody grades this number. A 60% who argues every disagreement from the
     stated rules beats a 95% who wrote "staff was right" nine times. Several
     of the 30 were chosen because they're genuinely ambiguous — you should be
     winning some of these. -->

**Disagreements**

<!-- Three lines each: the post, both labels, and who you think is right and
     why — grounded in the staff definitions you were both applying.

     Then sort each into one of three piles:
       (a) the rule covered it and I applied it loosely → a consistency problem
       (b) the rule genuinely doesn't say               → a gap in the definitions
       (c) the rule is ambiguous here and my reading is defensible → argue it.
           This is a legitimate win.

     Pile (a) is the one that matters most for your diagnosis: if you applied a
     written rule two different ways on 30 posts, that is direct evidence about
     what you did across your own 200. -->

**1.**

> _The post:_
>
> _Staff said / I said:_
>
> _My call, and why:_
>
> _Which pile:_

**2.**

> _The post:_
>
> _Staff said / I said:_
>
> _My call, and why:_
>
> _Which pile:_

**What the pattern in my disagreements tells me:**

---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
| --------- | ------ | ------- | ------ | --------- | ------- |
| 1.        |        |         |        |           |         |
| 2.        |        |         |        |           |         |
| 3.        |        |         |        |           |         |
| 4.        |        |         |        |           |         |
| 5.        |        |         |        |           |         |

**Did it help, and how do I know:**

<!-- If it didn't, say so. Relabelling that didn't help is a genuinely
     interesting result and earns full credit. -->

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped. -->

**The gap between what I meant my labels to capture and what the model
learned:**

<!-- Two sentences. Your confusion matrix is the evidence. -->

<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 5

       [ ] criteria.md has five numbered criteria, each naming a NUMBER
       [ ] Each has a reason underneath tied to your data or taxonomy
       [ ] labels.csv: at least 150 rows, text/label/note, ONE file not split
       [ ] No label above 70%
       [ ] All five unit 5 sections have real content
       [ ] Label Taxonomy includes the decision rule for your hardest boundary
       [ ] The Dataset includes three hard cases
       [ ] results.json and test_split.csv committed (the notebook does this)
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 6

       [ ] Baseline vs. Trained table, with your prediction written beforehand
       [ ] Run Log — Before, five criteria across three seeds
       [ ] Confusion matrix TYPED AS A MARKDOWN TABLE
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, using the agreement report as evidence
       [ ] Agreement Report with every disagreement adjudicated
       [ ] One improvement, with Run Log — After
       [ ] What's Still Broken
       [ ] results_three_seeds_before.json, results_three_seeds_after.json,
           baseline_results.json and
           agreement_results.json committed
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
