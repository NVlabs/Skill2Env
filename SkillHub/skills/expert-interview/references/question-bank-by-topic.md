# Question Bank by Topic

The SKILL.md has four core questions. This file expands the bank so the agent has real options to pick from. You're still only asking 2-4 questions per interview. The point is that the quality of the picks matters more than the quantity asked, and a bigger bank means better picks.

## Core questions (the universal four)

These stay as-is from SKILL.md. Every interview should draw at least one of these, usually two.

1. "What do most people get wrong about [topic]?"
2. "Can you give me a specific example — a client, a project, a number?"
3. "What surprised you when you actually did this?"
4. "Who should NOT follow this advice, and why?"

Everything below is topic-specific. Pick questions that fit what the user is actually writing about. Don't ask them in order; pick the 2-3 that are most likely to surface something an AI couldn't fabricate.

## Technical / how-to content

For tutorials, step-by-step guides, setup walkthroughs, debugging posts, configuration docs.

1. "What error does almost everyone hit first?"
2. "What step do beginners always skip?"
3. "What did you waste the most time on when you first did this?"
4. "What's the edge case that breaks most tutorials?"
5. "Which assumption in the official docs is wrong or outdated?"
6. "What's the fastest way to know if you're doing it wrong?"
7. "Which tool from the tutorial is actually optional?"
8. "What's the thing you wish someone had told you before starting?"
9. "How do you know you're done — not just done with the first pass, but actually done?"
10. "What breaks at scale that doesn't break in a toy example?"
11. "Which step in the standard tutorial is a waste of time?"
12. "What's the debug command you reach for when nothing works?"

The goldmine questions here are #3 and #10. Time-wasters and scale failures are very hard for an AI to hallucinate convincingly because they depend on the user's actual stack and traffic profile. That specificity is what the downstream writing skill needs.

## Comparison / review content

For "X vs Y" posts, product roundups, tool reviews, stack recommendations.

1. "Which one would you actually recommend to a friend, and why?" (the real answer, not the official one)
2. "Where do reviewers always get X vs Y wrong?"
3. "What's the thing about X that the marketing hides?"
4. "Which is worse than it looks? Which is better than it looks?"
5. "When would you recommend neither of these?"
6. "Who is the wrong person to ask about this comparison?"
7. "What breaks your opinion — what would have to be true for you to switch?"
8. "Which feature sounds important but doesn't matter in practice?"
9. "What's the gotcha in the pricing?"
10. "What's a better comparison nobody is making?"
11. "Which one did you quietly migrate away from, and why?"

The best question in this set is usually #10. If the user names a comparison that nobody else is writing about, you've found the article angle before you've even finished the interview.

## Thought leadership / opinion content

For contrarian takes, industry commentary, predictions, strategy posts.

1. "What's the contrarian take you've been holding back?"
2. "What's the conventional wisdom you used to believe that you no longer do?"
3. "What's everyone in your field wrong about right now?"
4. "Where do you think this is heading in 2 years?"
5. "What would have to happen for your opinion to change?"
6. "What's the unpopular prediction you're willing to put a number on?"
7. "Which authority in your field do you respect least, and why?"
8. "What's the taboo question nobody will answer directly?"
9. "What are you actively wrong about right now, and how do you know?"
10. "What would you do differently if you were starting today?"
11. "What's the thing you say to clients that you'd never say on LinkedIn?"

Question #9 is the most powerful and the hardest to get a good answer to. If you get one, the article writes itself. "What I'm wrong about" is the rarest genre in SEO content because most thought leadership is defensive.

## Case study / results content

For client stories, before/after posts, "we tried X for 90 days" content, growth reports.

1. "Start with the result number — what did it actually change?"
2. "What did you try first that didn't work?"
3. "At what point did you think it wouldn't work?"
4. "What was the unexpected thing you learned?"
5. "Who was the one person whose input mattered most?"
6. "What did you spend the most money on? The most time on?"
7. "What would you do differently next time?"
8. "Can you put a cost on the mistake?"
9. "What's the thing you can't publish publicly but it matters?"
10. "What was the moment you knew it was working?"
11. "What did the client actually say when you showed them the result?"

Question #9 is a signal question. Even if the user can't use the answer, it tells you where the real story is. Once you know the part that's unpublishable, you can ask "what's the most you can share about that?" and usually get 60% of the value.

## How to pick 2-4 questions from this bank

The bank has ~45 questions across four content types. You'll ask maybe three. How to pick:

1. **One contrarian-seeking question.** Always. This is what gives the final article an angle. The core question #1 ("what do most people get wrong about X?") is the safe default. If the user is opinionated, the thought-leadership bank has sharper versions.
2. **One specificity-forcing question.** Always. The core question #2 ("specific example, client, number") is the safe default. For case study topics, start with "what did it actually change?". For how-to topics, "what did you waste the most time on?" gets a specific story faster.
3. **One failure or scope question.** Always. Either "who should NOT follow this advice" (good for opinion and comparison content) or "what breaks at scale" (good for technical content) or "at what point did you think it wouldn't work" (good for case studies).
4. **Optional fourth question.** Only if the first three answers were short. A fourth question is a cost, not a benefit, if answers have been flowing. Stop when you have enough.

If you're not sure which category the topic falls into, default to the four core questions and skip the topic-specific ones. The core four work on almost any topic.

## When an answer is weak

Sometimes a user gives a vague answer. Don't move on. Vague answers can almost always be rescued by one well-placed follow-up. Patterns that work:

- User says "it depends on the situation": ask "what's the most recent situation where it applied?"
- User says "a few years ago": ask "can you remember which year?"
- User says "a client of ours": ask "what industry were they in? how big?"
- User says "most people": ask "who specifically? can you name one?"
- User says "a lot": ask "roughly how many? order of magnitude?"
- User says "it worked well": ask "what changed numerically?"

The goal is not to interrogate. The goal is to give the user a specific hook to remember a specific moment. Once they're in a specific memory, the details come out naturally.

## A note on follow-ups

Ask one question at a time. Wait for the answer. Follow up before asking the next question on the list. Quality of follow-ups matters more than quantity of initial questions.

The funnel method from qualitative research is the pattern to copy: broad question, then narrower probes that drill into whatever the user said, then move on. A typical good interview looks like:

- Q1 (broad): "What do most people get wrong about running a small SaaS support team?"
- Follow-up: "You said two people is a bad number — why specifically two?"
- Follow-up: "What happens at the handoff?"
- Follow-up: "Can you give me a number — how often did that happen?"
- Q2 (specific): "Walk me through the one time it broke worst."

That's five exchanges off one initial question. By the end you have a named failure mode with a number attached to it. That's more valuable than asking five different initial questions and getting five surface answers.

Standard follow-up probes that work on almost any answer:

- "Can you put a number on that?"
- "When was the last time that happened?"
- "What did you try before that worked?"
- "How did that compare to what you expected?"
- "Who else was involved?"
- "What would you do differently?"

If an answer is vague, keep probing. If an answer is specific, write it down verbatim and move on.

## Cross-reference

See `information-gain-writing.md` in this references folder for the theory behind why specificity in answers is what makes content unrankable by an AI. The short version: Google's Information Gain scoring compares your content against what the user has already seen on the topic. A named client or a real failure mode can't be in the other results, because nobody else has them. Generic opinions can. Your job in this interview is to extract the stuff that can't be anywhere else.
