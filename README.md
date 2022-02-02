# chromonica-sheet-transposer
This script could transpose chromonica sheet by semi-tones 

## Background

A popular way in China to record chromonica sheet is called 数字谱:

> Twinkle-Twinkle Lil' Star
> 
> 1 1 5 5 6 6 5 4 4 3 3 2 2 1

* `[]` for an octave above
* `()` for an octave below
* `#` for a semi-tone up
* `b` for a semi-tone down
* nested brackets are allowed to represent more octaves

For example, if 1 = C, then #1 = C#, #3 = b4 = F

## Usage

`python chromonica-sheet-converter -o OFFSET input.txt`

Try `python chromonica-sheet-converter -h` for more detail.

## Note

Currently doesn't support `b` symbol as usual chromonica sheet only use `#`.
