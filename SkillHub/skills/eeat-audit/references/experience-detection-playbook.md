# Experience Detection Playbook

Experience is whether the author has DONE the thing, not whether they have credentials. It's the dimension most pages fail on, the one AI-generated content can't fake, and the hardest to evaluate because the signals are stylistic, not structural. This playbook is how to read for it.

## The 30-second test

A careful reader can usually tell within 30 seconds of reading whether the author has done the thing. The reason isn't a single smoking-gun signal. It's an accumulation of small tells that are cheap to produce if you've done the work and expensive to fake if you haven't. Your job as an auditor is to notice the tells, count them, and trust the count.

The tells cluster around three behaviours:

1. **Moment-by-moment narration** of a specific thing that happened.
2. **Details only the doer would notice**, such as numbers, versions, timestamps, error messages.
3. **Unexpected observations** that contradict the obvious or the official line.

If you see all three in the first few paragraphs, the author has done it. If you see none, they haven't. The middle case, one or two signals, is where most content lives, and that's where the score sits at 4 to 6.

Google's Quality Rater Guidelines added the "Experience" E in December 2022 precisely because this kind of evaluation, intuitive though it is, is hard to automate. The algorithm looks for proxies (first-person pronouns, specific entities, original images), but a human reviewer can read the stylistic fingerprint faster and more accurately.

## Strong signals: what hands-on experience looks like in writing

### First-person moment-by-moment narration

"When I clicked X, the error message said Y, which I didn't expect because the docs say Z." This is the core. The author is reconstructing an actual sequence of events. The tense is past, the subject is "I," and the action is specific enough that another practitioner could recognise it.

### Specific numbers that would be invented if guessed

"The form accepted 47 characters in the username field before hitting the limit." Nobody guesses 47. A writer summarising other sources says "there's a character limit" or "around 50 characters." The specific number is evidence that somebody actually typed 48 and saw it fail.

Same principle applies to timestamps, durations, costs, and counts. "$2,438.17" beats "about $2,500." "Took us 19 days" beats "took about three weeks." Real practitioners know exact numbers because they were looking at them.

### Failure stories with mechanism

"It didn't work because the API was rate-limiting me at 15 requests per hour, which I only discovered after tracing the 429 responses." The story isn't just "it broke." It's "it broke for *this specific reason* and here's how I figured that out." The mechanism is the proof. A writer who hasn't hit the failure can't reconstruct the mechanism convincingly.

Corollary: the existence of any failure story at all is a strong signal. Writers who haven't done the work write as if everything went to plan, because they're narrating the plan, not the experience.

### Unexpected observations

"Nobody warned me that X causes Y because Z, so I had to figure it out from a 2019 GitHub issue." The unexpected observation is the thing the documentation doesn't mention, the edge case that's not in the tutorial, the fact that surprised the author. This is almost impossible to fake because the writer would need to know both what the conventional account says *and* what the exception is, and then have a reason to surface the exception.

### Original photos, screenshots, and diagrams tied to specific moments

Not stock imagery. Not generic illustrations. A photo of the actual thing the author worked with, in the actual setting, at the actual time. Screenshots are the strongest version of this: they're dated, timestamped, and context-specific. The signal is strongest when the screenshot matches a specific moment in the text ("here's the dashboard at day 7, before the fix").

### Explicit preferences with reasoning

"I always use X instead of Y, even though conventional wisdom says Y, because in my experience Z." The author has a view. They know the conventional wisdom exists and they disagree with it for a stated reason. Opinions without reasoning are weak; opinions with mechanism are Experience signals.

### References to specific product versions, software releases, or time periods

"This was on macOS 14.3 with Xcode 15.2 in February 2026." Versions and dates are cheap to include if you've actually done the thing. You know what you were running. They're expensive to include if you haven't, because you'd have to look them up and hope they're consistent with your other claims.

## Weak signals: research-desk writing dressed as experience

### Third-person narration of other people's examples

"Companies like Spotify have used this technique to..." This is summary. It's evidence the author read about Spotify, not that they did the thing. On its own it's fine (not every article is autobiographical), but if it's the *only* evidence offered as Experience, the score is 4 at best.

### Generic advice with no anchoring to a specific moment

"It's important to test your forms before launch." True, vacuous, unanchored. No moment, no numbers, no failure, nothing that ties the advice to the author's own work.

### "Best practices" without attribution

The phrase "best practices" is a warning sign. Best practices according to whom? Where are they written down? Who has tested them? If the answer is "everybody knows," the author is probably repeating common knowledge, not reporting experience.

### Stock photography that doesn't match the content

A blog post about configuring a Kubernetes cluster illustrated with a smiling woman at a laptop is an Experience anti-signal. The stock photo is saying "we didn't have a real image to use." Which usually means they didn't have a real workflow to screenshot.

### "According to studies" without identifying which

Same problem as stock photography but for research writing. Named studies with dates and authors are an Expertise signal. Unnamed studies are a Trust leak and a hint that the author didn't actually read the source.

### Credentials-dropping in place of concrete observations

"As a 20-year veteran of the industry, I can tell you that..." The author is claiming authority rather than demonstrating it. This is the "I'm an expert" trap: real experts show, they don't tell. A 20-year veteran has 20 years of specific stories to draw on. If they're not drawing on them, the 20 years are either exaggerated or weren't spent doing what they imply.

### Vague timeframes

"Recently," "nowadays," "in today's world," "lately" are all warning signs. Writers who have done the thing say "last March" or "in Q4 2025" or "as of the 14.3 release." Vague timeframes are what you write when you don't have a specific memory to anchor to.

## How to score Experience in 60 seconds

1. **Count first-person moment-narrations.** Each specific scene where the author describes what they did and what happened counts as one signal.
2. **Count specific numbers, versions, and dates** that would not be invented. Each counts as one signal.
3. **Count original visuals** clearly tied to the author's own work. Each counts as one signal.

Then score:

- **0 signals.** Score 1 to 3 (Absent). No evidence the author has done this.
- **1 to 3 signals.** Score 4 to 6 (Weak). Some evidence, probably one or two real data points diluted by research-desk prose.
- **4 or more signals.** Score 7 to 10 (Strong). Multiple independent tells, clustered. Score the top end if the page also has failure stories and unexpected observations.

Don't over-count. Three sentences from the same story are one signal, not three. The question is how many independent proofs of experience the page contains.

## Special cases

**Group authorship.** When a page is bylined to a team or has multiple authors, the Experience threshold is the same but the signals can come from any author. A "by the Engineering Team" page needs at least one author voice in the prose, or the Experience score is capped at 5 no matter how many names are on the byline.

**Ghost-written content.** Experience doesn't care who typed the words. If the named author has genuinely done the work and dictated the specifics to a writer, the signals will still appear in the prose. If the named author hasn't done the work and the ghost-writer is inventing plausible-sounding details, the signals will read as off: numbers too round, stories too smooth, failures suspiciously educational.

**Journalism and primary-source reporting.** A reporter interviewing sources isn't claiming Experience for themselves. They're surfacing the experience of others. Score Experience against the *subject's* experience as reported, not the writer's. The tells become "did the reporter get close enough to the subject to report specific details, or are they paraphrasing a press release?"

**Commissioned case studies.** An agency writing a case study about a client's project can legitimately claim Experience if the agency did the work. Score it like a first-person account but verify the specifics are the agency's own, not borrowed from the client's marketing copy.

## Cross-reference

`eeat-signal-embedding.md` covers the other side of this problem: how to CREATE experience signals when writing new content. This playbook is for detection. When the audit finds Experience gaps, point the user at the embedding reference for remediation techniques.
