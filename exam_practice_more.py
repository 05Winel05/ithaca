"""40 original advanced multiple-choice items for local short-form practice.
These are NOT official SAT/ACT/TOEFL/IELTS/DET questions or score predictions.
"""
# tuple(topic, prompt, options, correct-option index, explanation)
MORE = {
'SAT': [
('Algebra','For f(x)=2x²−8x+1, what is the minimum value of f(x)?',['−7','−3','1','9'],0,'Complete the square: f(x)=2(x−2)²−7.'),
('Algebra','If 3^(x+1)=81, what is x?',['2','3','4','5'],1,'81=3^4, so x+1=4 and x=3.'),
('Algebra','If x²−5x+6=0, what is the sum of its distinct roots?',['2','3','5','6'],2,'The roots are 2 and 3; their sum is 5.'),
('Data analysis','The average of five numbers is 18. Four are 11, 17, 20, and 24. Find the fifth.',['16','18','19','22'],1,'The total is 90; the known four total 72, leaving 18.'),
('Data analysis','A price increases 20% then decreases 25%. What is the net percentage change?',['5% decrease','10% decrease','5% increase','No change'],1,'1.20 × 0.75=0.90, a 10% decrease.'),
('Data analysis','In a sample, 54 of 120 prefer buses. Estimate the proportion as a percentage.',['35%','40%','45%','54%'],2,'54 divided by 120 is 0.45.'),
('Reading & Writing','Which punctuation correctly joins two independent clauses?',['The study ended, the data was analyzed.','The study ended; the data was analyzed.','The study ended the data was analyzed.','The study ended: and the data was analyzed.'],1,'A semicolon can join two closely related independent clauses.'),
('Reading & Writing','A study sampled only people who volunteered online. Which limitation is most relevant?',['Volunteer bias','Mathematical rounding','A controlled variable','Accurate random sampling'],0,'People who choose to volunteer may differ from the broader population.')
],
'ACT': [
('English','Choose the most concise revision: “In spite of the fact that it was late, we continued.”',['Despite that it was late, we continued.','Although it was late, we continued.','Due to it was late, we continued.','Since of lateness, we continued.'],1,'Although replaces the wordy introductory phrase.'),
('English','Which sentence correctly sets off a nonessential clause?',['My uncle who lives in Dallas, runs.','My uncle, who lives in Dallas, runs.','My uncle who, lives in Dallas runs.','My uncle, who lives in Dallas runs.'],1,'Nonessential relative clauses take commas on both sides.'),
('Math','A circle has radius 5. What is its area?',['10π','20π','25π','50π'],2,'Area=πr²=25π.'),
('Math','Solve |2x−1|=7. What is the product of the two solutions?',['−12','−8','8','12'],0,'Solutions are x=4 and x=−3; product is −12.'),
('Reading','A researcher reports that both groups improved, but the control group improved slightly more. What is supported?',['The treatment was definitely effective.','Only the treatment group improved.','The control group improved more in this study.','Neither group changed.'],2,'The text explicitly says the control group improved slightly more.'),
('Reading','An essay begins with a question and ends by returning to it. This structure most likely serves to:',['Frame the discussion around a central issue','Eliminate the need for evidence','Conceal the main argument','Describe events randomly'],0,'Returning to the original question helps unify the argument.'),
('Science reasoning','A graph rises from 5 units at minute 2 to 17 units at minute 6. Average rate of change?',['2 units/min','3 units/min','4 units/min','6 units/min'],1,'(17−5)/(6−2)=12/4=3 units per minute.'),
('Science reasoning','Two experiments use different temperatures and different materials. Why is a causal conclusion difficult?',['There are no measurements','More than one variable changed','The variables are numerical','The samples are labeled'],1,'Changing two factors prevents isolating one variable’s effect.')
],
'TOEFL': [
('Academic reading','A passage states: “The new hypothesis challenged the prevailing model.” “Prevailing” most nearly means:',['Widely accepted','Recently rejected','Rarely tested','Secret'],0,'Prevailing means common or dominant in the field.'),
('Academic reading','The author provides a counterexample after stating a rule. The purpose is most likely to:',['Illustrate a limitation','Change the subject','Define a synonym','Describe a procedure'],0,'A counterexample shows where a generalization may fail.'),
('Academic reading','If an article says a migration began before a drought, what can be inferred?',['The drought certainly caused it.','Migration started earlier than the drought.','The drought never happened.','The two events were simultaneous.'],1,'The passage establishes the order, not causation.'),
('Language use','Choose the correct completion: “Had the team collected more data, they ___ a stronger conclusion.”',['will reach','would have reached','reached','would reach'],1,'A past unreal conditional uses would have + past participle.'),
('Language use','Choose the best sentence.',['The results suggests changes.','The result suggest changes.','The results suggest changes.','The results suggesting changes.'],2,'Plural results takes plural verb suggest.'),
('Vocabulary','“The findings are tentative.” Tentative means:',['Final and certain','Provisional and uncertain','Unrelated','Expensive'],1,'Tentative findings may change with more evidence.'),
('Vocabulary','“The researchers sought to replicate the trial.” Replicate means:',['Repeat','Conceal','Fund','End'],0,'To replicate a study is to repeat it to test results.'),
('Vocabulary','Which is closest to “mitigate” in “mitigate the effects of flooding”?',['Worsen','Measure','Reduce','Predict'],2,'Mitigate means make less severe.')
],
'IELTS': [
('Academic reading','A passage says solar output fluctuates seasonally. Fluctuates means:',['Remains fixed','Varies','Stops permanently','Doubles each year'],1,'Fluctuate means vary over time.'),
('Academic reading','Which statement is supported by “The study suggests a link but does not establish a cause”?',['Causation is proven.','There is no relationship.','An association was observed.','All variables were controlled.'],2,'A link can be observed without proving a cause.'),
('Academic reading','An author contrasts rural and urban transport before proposing a shared solution. The main organization is:',['Chronology','Comparison followed by proposal','Definition only','Random examples'],1,'The writer compares settings, then proposes a common solution.'),
('Grammar','Choose the correct sentence.',['Neither solution are suitable.','Neither solutions is suitable.','Neither solution is suitable.','Neither solution were suitable.'],2,'Neither takes singular agreement in this construction.'),
('Grammar','Choose the best sentence.',['By 2030, the bridge will have been completed.','By 2030, the bridge has complete.','By 2030, the bridge will completed.','By 2030, the bridge were completed.'],0,'The future perfect passive is will have been completed.'),
('Vocabulary','In academic writing, “substantial increase” means:',['A small reduction','A significant rise','An unknown amount','No change'],1,'Substantial indicates considerable magnitude.'),
('Vocabulary','“The proposal is feasible.” Feasible means:',['Practical to carry out','Already rejected','Not permitted','Theoretical only'],0,'Feasible means possible or practical.'),
('Vocabulary','“The figures were revised.” Revised most nearly means:',['Ignored','Updated','Copied unchanged','Estimated blindly'],1,'Revised figures have been updated or corrected.')
],
'DET': [
('Fill in the blank','Complete: “If she had studied earlier, she ___ more confident.”',['would feel','would have felt','will have felt','feels'],1,'Third conditional: would have + past participle.'),
('Fill in the blank','Complete: “The report was ___ detailed that we could repeat the experiment.”',['such','too','so','much'],2,'The pattern is so + adjective + that.'),
('Fill in the blank','Complete: “Despite ___ tired, he finished his assignment.”',['be','being','was','been'],1,'Despite is followed by a noun or -ing phrase.'),
('Read and select','Which is a correctly spelled English word?',['accomodate','accommodate','acommodate','accommadate'],1,'Accommodate has double c and double m.'),
('Read and select','Which is a correctly spelled English word?',['definately','definitly','definitely','definetely'],2,'Definitely is the correct spelling.'),
('Read and select','Which is a correctly spelled English word?',['occurrence','occurence','ocurrance','occurance'],0,'Occurrence contains double c and double r.'),
('Reading','Text: “Mira postponed the event because the venue was unavailable.” Why was it postponed?',['Low attendance','Unavailability of the venue','Bad weather','A change in speaker'],1,'The reason is explicitly given: the venue was unavailable.'),
('Reading','Text: “While the prototype was inexpensive, its maintenance costs were high.” Which contrast is described?',['Low purchase cost versus high upkeep','High initial cost versus low upkeep','Fast performance versus slow setup','Low demand versus high supply'],0,'The sentence contrasts initial affordability with high maintenance costs.')
]
}
def expanded_questions():
    result={}
    for exam,items in MORE.items():
        result[exam]=[]
        for i,(topic,text,options,correct,explanation) in enumerate(items,1):
            assert len(options)==4 and 0<=correct<4 and explanation
            result[exam].append({'id':f'{exam.lower()}final{i:02d}','topic':topic,'difficulty':'advanced','text':text,'options':options,'correct':correct,'explanation':explanation})
    return result
