# What I checked, and what the agent got wrong

Write this yourself, in your own words. It is the part of the repo that proves the work is yours.

## What the agent got wrong
I did not catch the agent making a wrong change in the fixes it applied. The real bug nobody had flagged was in fleet_utils.py: the km-to-miles constant was 1.609, which is km per mile, so the UK report showed 100 km as 160.9 miles instead of 62.1.

## What I checked before I accepted its work

I ran pytest, and all 4 tests pass, including the new test for a car with no last-service reading. I ran verify.py, and the 15000 km interval and the 80% threshold both pass as untouched. I confirmed with git diff that settings.cfg was not changed. The wear bug was a floor division (//) that turned 14,900 of 15,000 km into 0%. It now uses / and reads 99.3%, so the nearly-worn car is flagged.

## What the data actually said
Total mileage did not predict breakdowns. Cars that broke down averaged 53,448 km and cars that did not averaged 53,302 km. Age was the same too, about 5.9 years in both groups. The factors that did separate them were km since last service (correlation 0.40), average daily km (0.25) and load factor (0.22). I built the 0-100 risk score from those three. Cars that broke down average a score of 67.8 against 45.6 for the others. The score was checked on the same 120 cars it was built from, so its accuracy is probably a little optimistic.