# YETI Chat Bot

Most of these bots require cookies from a logged in account.

For firefox:
use the cookies.txt extension
open the page you need cookies from and save the cookies for that site
update the pickler.py to convert the cookies for that txt file to .pkl
update the call from the chatbotscraper to use the .pkl file

also, you'll need to update the geckodriver location on your machine.

# CSV Information

## YETI bot

The yeti_responses.csv contains all questions from both yeti_questions and yeti_extra_questions. It was run in 4 test batches, as the chatbot became too unstable for futher testing each round. After many queries, either the time between replies becomes excessive, or the bot stops interpreting altogether. Use the time estimates with this compounding delay effect in mind.

test 1: extra_qs "What are the dimensions of the YETI Tundra 65?" -> "If my YETI zipper breaks is it covered under warranty?"

test 2: extra_qs "What proof do I need to submit a YETI warranty claim?" -> "You mentioned custom engraving—how long does it take to ship?"

test 3: extra_qs "You said the YETI Rambler is durable—how does it compare to competitors?" -> "My YETI order was lost in transit—can you resend it?"

test 4: extra_qs last 5 questions AND all yeti_qs

FYI:
The message when something is broken for YETI chat is "I am here to assist with any questions or concerns you might have about ...(some variable issue)... feel free to ask!"

The start and end might be useful for noting failures if any occured that I didn't catch. Those would indicate an issue with answering the question at baseline, not just because of deterioration (since I already accounted for that with batch testing).


## Rufus Bot

This bot's script is not perfect, so responses sometimes only caught the tail end of a much longer paragraph. Number of words may be skewed significantly for this reason, and time to completion is a better estimate for the length of each reply. Overall, the bot struggled to answer many questions, especially complex questions, accurately but was alway incredibly fast to begin replying, even when experiencing repeated query fatigue.

Time_only_responses
test 1: extra_qs "" -> ""
test 2: extra_qs "Is the Kindle Oasis currently in stock?" -> "Do all Fire TV devices support Alexa voice control?"
test 3: extra_qs "What Amazon smart home devices come in black? Do they have a matte finish?" -> "Can I track my Amazon order in real-time?"
test 4: extra_qs "Does Amazon allow order cancellations before shipping?" -> ""

responses (better data)
test 1: "What are the dimensions of the Fire Max 11 tablet?" -> "Is the Kindle Oasis currently in stock?"
test 2: "How much does the Ring Video Doorbell Pro 2 cost?" -> "Does Amazon allow order cancellations before shipping?"

test 3: "The engraving on my Kindle Paperwhite is incorrect—how can I fix it?" -> end

## Fi Bot

Mixed bag, but most important takeaway is that all questions ran in only 2 tests. This indicates the strong resistance to repeated query fatigue, unlike other bots here.

test 1: gps_qs start -> ""
test 2: gps_qs "You said the Fi Collar can be tracked in real-time—how often does it update?" -> end


# Uncertainty Transformer Model

The transformer model used in this code is **facebook/bart-large-mnli**, which is a pre-trained model based on the BART architecture designed for natural language understanding tasks. It uses a sequence-to-sequence approach to predict the most likely labels for a given input, leveraging large-scale pretraining on text data. In this case, the model classifies responses as "certain," "uncertain," or "evasive" by evaluating the relationship between the response and the candidate labels. It then calculates a score for each label, selecting the one with the highest confidence. The model is effective at detecting uncertainty or evasiveness due to its ability to understand context and nuances in language.

# Yes-or-no Data

The yes_no code analyzes chatbot responses to determine how many questions and answers are "yes/no" type. It checks if a question begins with a modal verb (like "can," "is," or "should") to classify it as a yes/no question. Then, it evaluates the response to see if it starts with "yes" or "no." The results are counted and written to an output CSV file, showing the total number of yes/no questions and responses. The file also includes the chatbot's name for tracking.