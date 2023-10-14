"""
Created on Mon 11 Jul 21:17 2022
Finished on
@author: Cpt.Ender

https://www.codewars.com/kata/5571d9fc11526780a000011a
DESCRIPTION:
For this kata you will be using some meta-programming magic to create a new Thing object.
This object will allow you to define things in a descriptive sentence like format.

This challenge attempts to build on itself in an increasingly complex manner.

Examples of what can be done with "Thing":
jane = Thing('Jane')
jane.name # => 'Jane'

# can define boolean methods on an instance
jane.is_a.person
jane.is_a.woman
jane.is_not_a.man

jane.is_a_person # => True
jane.is_a_man # => False

# can define properties on a per instance level
jane.is_the.parent_of.joe
jane.parent_of # => 'joe'

# can define number of child things
# when more than 1, a tuple subclass is created
jane.has(2).legs
len(jane.legs) # => 2
isinstance(jane.legs[0], Thing) # => True

# can define single items
jane.has(1).head
isinstance(jane.head, Thing) # => True

# can define number of things in a chainable and natural format
>> Note: Python, unlike Ruby and Javascript, doesn't have a pretty syntax for
blocks of expressions and a forEach method for iterables. So you should implement this behaviour yourself.
jane.has(2).arms.each.having(1).hand.having(5).fingers
len(jane.arms[0].hand.fingers) # => 5

# can define properties on nested items
jane.has(1).head.having(2).eyes.each.being_the.color.blue.having(1).pupil.being_the.color.black

# can define methods: thing.can.verb(method, past='')
method = lambda phrase: "%s says: %s" % (name, phrase)
# or
def method(phrase):
  return "%s says: %s" % (name, phrase)
jane.can.speak(method, "spoke")

jane.speak("hello") # => "Jane says: hello"

# if past tense was provided then method calls are tracked
jane.spoke # => ["Jane says: hello"]
                                                                """


# class is_a:
#     def __init__(self):
#         self.personAttr = True
#
#     def
#
# class Thing(is_a):
#     def __init__(self, name):
#         self.name = name
#         self.is_a_man = False
#         self.is_a_woman = False
#         self.is_a = is_a()

class is_a:
    def __init__(self):
        self.is_a_person = False
        self.person = self.is_aF

    def is_aF(self):
        self.is_a_person = not self.is_a_person


class Thing(is_a):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.is_a = is_a()


jane = Thing('Jane')
print(jane.name)
jane.is_a.is_a_person

# jane.is_a.woman
# jane.is_not_a.man
# print(jane.is_a_person)
# jane.is_a.person
# print(jane.is_a_person)
