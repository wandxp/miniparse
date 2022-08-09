import tinyparse as m
import sys

parser = m.ArgumentParser("Repeat a value.", "repeat", sys.argv)

includeCounter = parser.Flag('include-counter', 'Include a counter with each repetition.')
count = parser.Option('count', 'The number of times to repeat a value.', int )
phrase = parser.Argument('phrase', str, 'The value to repeat.')

if __name__ == '__main__':
    
    if count:
        repeatCounter = count
    else:
        repeatCounter = 5
    
    for i in range(0, repeatCounter): 
        if includeCounter:
            print(f"{i+1}: {phrase}")
        else:
            print(phrase)