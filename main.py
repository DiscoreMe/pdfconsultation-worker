import pdfrw
from pdfrw import PdfDict

template = pdfrw.PdfReader('test_form.pdf')

ans = template.Root.Pages.Kids[0].Annots[0].update(PdfDict(V='(test)'))


pdfrw.PdfWriter().write('output.pdf', template)

fs = template.Root.AcroForm.Fields

for f in fs:
    print(f.Kids)
    print(f.T.decode())
    
