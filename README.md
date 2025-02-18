# YETI Chat Bot

Most of these bots require cookies from a logged in account.

For firefox:
use the cookies.txt extension
open the page you need cookies from and save the cookies for that site
update the pickler.py to convert the cookies for that txt file to .pkl
update the call from the chatbotscraper to use the .pkl file

also, you'll need to update the geckodriver location on your machine.

# CSV Information

The yeti_responses.csv contains all questions from both yeti_questions and yeti_extra_questions. It was run in 4 test batches, as the chatbot became too unstable for futher testing each round. After many queries, either the time between replies becomes excessive, or the bot stops interpreting altogether. Use the time estimates with this compounding delay effect in mind.

test 1: extra_qs "What are the dimensions of the YETI Tundra 65?" -> "If my YETI zipper breaks is it covered under warranty?"

test 2: extra_qs "What proof do I need to submit a YETI warranty claim?" -> "You mentioned custom engraving—how long does it take to ship?"

test 3: extra_qs "You said the YETI Rambler is durable—how does it compare to competitors?" -> "My YETI order was lost in transit—can you resend it?"

test 4: extra_qs last 5 questions AND all yeti_qs

FYI:
The message when something is broken for YETI chat is "I am here to assist with any questions or concerns you might have about ...(some variable issue)... feel free to ask!"

The start and end might be useful for noting failures if any occured that I didn't catch. Those would indicate an issue with answering the question at baseline, not just because of deterioration (since I already accounted for that with batch testing).