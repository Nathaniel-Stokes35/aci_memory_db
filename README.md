# Overview

This program is mostly focused on the memory core of individual AI programs in my future structure. Using local repositories as holders for simple information the SQL is designed to be streamlined and easily accessible. This particular code is a barebones example of this system where a user can input MBTI values, Big Five Scores, and Event Perceptions to generate a tag for a Future Language model. These tags represent the "instinct" of the AI and are designed to provide nuanced context to dialog. You launch the program then set the values you desire to see the tag for, you select "search tags" and a SQL command will pull the relevant tag associated with those inputs. 

[Software Demo Video](https://youtu.be/-4RgNT22Rm4)

# Relational Database

The program focuses mainly on "Personality_tags" which is a Table that holds profile ID's comprised of MBTI personality Types, paired with an OCEAN big Five, then placed against an event's "Caution", "Curiosity", and "Empathy" Level to define a relevant tag for a future LLM.
{Describe the structure (tables) of the relational database that you created.}

# Development Environment

I used Android studio in the beginning but finished in VS Code.
I started in Kotlin, learning how to bridge the SQL scripts in an android environment but I eventually wrote the advanced queries in Python which was more familiar.
# Useful Websites

- [Kotlin](http://url.link.goes.here)
- [Kivy Tutorial](https://www.geeksforgeeks.org/python/kivy-tutorial/)

# Future Work

Filling out the other tables with real events will be a necessity.
Cleaning up the UI and having it play as the ACI generator will need so work.
Bringing the backend deeper into the SQL queries instead of simple user controlled slide bars are also a must.