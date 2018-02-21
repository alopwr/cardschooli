# cardschooli
![forthebadge](http://forthebadge.com/images/badges/built-with-love.svg)
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)


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
