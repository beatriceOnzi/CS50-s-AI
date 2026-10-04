# Analysis

## Layer TODO, Head TODO

The attention identified the objetc (in this case, the mask itself) of a phrasal verb.
In layer10 head10 i noticed a strong connection between the words "picked" , "up" and "a", representing the phrasal verb, and the mask, representing the object.

Similarly, in another observation, testing the prase "He bought a [MASK]", in layer0 head4, there was a relationship between "bought" and the mask.

Example Sentences:
- Then I picked up a [MASK] from the table.
- He bought a [MASK].

## Layer TODO, Head TODO

Testing the phrase "She went to the [MASK] with her friend", in layer4 head5, the attention indentified a relationship between "to" and "mask", as well as a relationship between "with" and "friend", demonstrating the connection among prepositions and its objetcs.

Likewise, in the layer1 head6 there is a strong conenction between the words "during" and "mask",
the preposition and its objetc.

Example Sentences:
- She went to the [MASK] with her friend
- I studied during the [MASK].

