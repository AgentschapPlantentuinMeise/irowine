# b-c-hackathon
Template for the B-Cubed hackathon taking place from 2 - 5 April 2024

## Introduction

The B-Cubed main goal is to standardise biodiversity data in order to enhance efficiency and accessibility.
This also implies that having a standardised biodiversity cube, it should be processable by different workflows
that take a cube (or several cubes) as an input. While you are hacking on your B-cubed hackathon project, try
to keep this in the back of your mind by coding a solution that runs everywhere (by means of having a well defined
`Dockerfile`), with any cube as as a starting point. If you want an extra challenge, have it run seemless with one
or more cubes.

## Instructions

1. After cloning and reading through this README feel free to erase this text and start out from scratch
2. Be sure to have a small cube for testing, under the `tests/data` directory. This cube should work well with your finished workflow
3. The `Dockerfile` should have an entrypoint that takes in 1 or more cube files from a local directory (e.g. `tests/data` after cloning)
4. Choose a more appropriate license, in case you find it more suitable than the MIT default license in this template

## Hackathon impact

Using this template will also allow us to track the impact of the hackathon and report on it.
In fact, we will try to run each hackathon project script with the cubes from all the other projects.
Thanks for thinking ahead by creating reusable code and helping out to make the hackathon a big success!
