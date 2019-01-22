# intellify

## Reports
1. Create a folder named 'data'
2. Run analyse.py 
3. For every school participating, a separate folder with the name as the school ID is created inside the 'data' folder. This folder contains a HTML file corresponding to the report and a few JPGs showing marks distribution.
4. Install 'xhtml2pdf'
5. Run script.py
6. The above creates a pdf from the html file, stored in the same location as the html.

## Recommendation System
1. The system currently works for the 45 questions that were provided to me.
2. Open recommend.py
3. Go to line 103, enter indices of the 10 questions that will be considered 'already asked'.
4. Go to line 104, enter the response of the student to these questions. '0' means wrong and '1' means correct.
5. Some default question indices and their response array is already defined in line 103 and line 104.
6. Run recommend.py
7. The output will show the next 10 questions that should be asked to this student.
8. The output also shows the skill level and difficulty of every question to help appreciate the next 10 question recommendation