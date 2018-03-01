# cardschooli
![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![Build Status](https://travis-ci.org/m4k5/cardschooli.svg?branch=master)](https://travis-ci.org/m4k5/cardschooli)
[![Coverage Status](https://coveralls.io/repos/github/m4k5/cardschooli/badge.svg?branch=master)](https://coveralls.io/github/m4k5/cardschooli?branch=master)

Gamify education with cards!

### TODO:
- [x] dodawanie tekstu na awers
- [ ] zmienne przy generowaniu tesktu na awersy
- [ ] składanie PNG do duplexerowego PDF A4
> from fpdf import FPDF <br>
 pdf = FPDF() <br>
for image in imagelist:<br>
    pdf.add_page() <br>
    pdf.image(image,x,y,w,h) <br>
pdf.output("yourfile.pdf", "F") <br>
