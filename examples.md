As for the upcoming workshop, I think that sticking with a pure Python example (i.e. standard library only, no extra packages) makes the most sense for a "Hello World" example. Here are my arguments for it:
- lower barrier of entry for participants, the example is less of a black box,
- it would make for a good opportunity to mention `pfaas` since it only supports standard Python library right now,
- less parts outside of the Golem domain which require explanation. 

As for `pfaas`: it would make for a great next step after the live demo, telling the participants how they can abstract away some of the complexity from the live coding example.
Given the above, here's my first pick for the "Hello World" example:

```
# Dictionary attack on some hash
    - input: dictionary slice, target hash, algorithm to use (optionally)
    - output: matching word from the dictionary or empty string
## Pros:
    - fits nicely into the existing tutorial, can be treated as an introduction to hashcat
    - practical problem
    - simple code
## Cons:
    - with both examples focused on cracking hashes this could somewhat suggest that we don't mind using Golem for bad stuff?
```

I'd like to know your thoughts on this, most importantly whether you share my only concern about that example.
One possible alternative:

```
# Sorting a large, random array of numbers
    - input: two options here
        - array slice
        - seed for random numbers generator, slice length
    - output: sorted slice
## Pros:
    - super simple, requires little explanation outside of Golem's domain

## Cons:
    - kind of boring
    - size of data to transfer grows proportionally to the input size
```

And here are some ideas I researched which require additional packages to run:

```
# Text-to-speech (simplified g-flite example)
    - input: slice of original text, includes full sentences only
    - output: audio file generated from input slice
## Pros:
    - practical problem
    - more interesting result compared to other examples
## Cons:
    - potentially large output data size (though these are .mp3 files, so not *that* bad)
    - more stuff to explain compared to previous examples

# Graphical plotting
## Example ideas
    - Perlin noise generation
    - Mandelbrot set visualisation
```

Possible examples:
- sorting a large, random array (only transfer the seed to providers)
    - if we push this far enough we could possibly even show performance gains?
    - lots of data to transfer if we simply send it over the wire
    - can we use random in vms?
- perlin noise generation
- dict attack on some hash
    - would play nicely with hashcat later on
    - no need to install external dependencies
    - limits the scope of the examples, suggests evil usage of golem? :(
- TTS using pyttsx3 and pydub
    - break text down into sentences
    - optionally try stiching the results together

