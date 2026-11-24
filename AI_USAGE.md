# AI usage

Keep all three headings exactly as they are. If this file is missing or any heading is
missing, the grader stops and gives 0 ("AI_USAGE.md missing or incomplete"). The content
is not scored, but your Track Mentor reads it and the W8 defence can ask about it.

## Tools

<!-- Which tools you used (ChatGPT, Copilot, Claude, Cursor, none...) and for which parts. -->
chatGPT, Copilot

## What AI got wrong

<!-- At least one thing an assistant got wrong that you changed, and how you noticed
(a test failed, the docs said otherwise, you ran it). -->
when creating the test test_requested_at_includes_timezone_z_or_offset it checks only the
z and did not check the offset so I added it. 

## In my own words

<!-- Answer without AI, one or two sentences each. -->

1. Pick one mutant your first draft of tests did not kill. Why not, and what did you add?

A mutant that returned inbox transfers in request order could pass a test with only (one transfer). I added a test that creates a (high-priority transfer) before an (urgent one) and checks that urgent appears first; it also checks request order for transfers with equal priority.

2. Why is a test that only asserts `status_code == 409` weaker than one that asserts the problem `type`?

A 409 only tells me that some conflict occurred; it could be the wrong conflict. Checking the ((problem type)) confirms the API returned the ((specific error the test intended to trigger)).