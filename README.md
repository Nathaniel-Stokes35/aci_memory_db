# Overview

This project is a prototype of a structured data classification system designed to map psychological and contextual inputs into deterministic “personality-event tags” using a relational database. The system explores how structured inputs (MBTI, Big Five personality traits, and event-based perception scores) can be stored, queried, and transformed into classification outputs that could later be used as conditioning signals for a downstream language model. This repository represents the backend data modeling and tagging layer of a larger multi-component system architecture. A separate frontend prototype (Kotlin-based UI) explores the user interaction layer of this system.

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
