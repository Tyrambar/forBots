from datetime import datetime

e = [
'Fundraising on preseed stages',
'AI & Microbiome', 'Mixpanel - New vs. old best practices',  
]

e_adress = [
            "Ahad Ha'Am St 54", 'Ha-Umanim St 12 · Tel Aviv-Yafo',
            'Ben Yehuda 32 (Beit ELAL). Level 2 Tel Aviv',]
			
e_dates = {
    e[0]: datetime(2020, 1, 7, 18),
    e[1]: datetime(2020, 1, 12, 18), 
    e[2]: datetime(2020, 1, 15, 18),
}

events_d = {
e[0]: 
"""How can you convince your investors that your venture has a future? What you should do to bring them to "Yes"? How you demonstrate you are the expert on your market and technology? To raise investment for a product, the entrepreneurs have to present a plan, according to which, investors can assess the economic feasibility and the prospects of the product to produce a fast ROI.""",
e[1]: """We are excited to host our 7th meetup of AI in Genomics! 

Note that this event will be hosted at Google Campus for Startups (Tel Aviv). 
In this event, Prof. Elhanan Borenstein (TAU) and Dr. Yael Silberberg (BiomX) will demonstrate how AI is used to better understand human microbiome and its relation to health and disease. 

Schedule: 
17:45 - Gathering + Pizzas 😊 
18:15 - Prof. Elhanan Borenstein (TAU) 
"Studying the Human Microbiome: From Big Data to Models" 
19:00 - Dr. Yael Silberberg (Head of data science at BiomX Ltd) 
"Microbiome Based Biomarker Discovery for Disease State""",
e[2] : """This meetup is for those who realize that Analytics is no longer just a shortcut for Google Analytics. 
Along with their bitter rival Amplitude, Mixpanel is currently, without a doubt, the leading behavioral Analytics platform. Built specifically for Product Managers, it is a tool so powerful that it is often used only to a fraction of its capabilities. 
But for those attending that is about to change! 

If you understand the importance of strong Analytics skills to a PM's tool box, this meetup is a must. If you don't, this meetup should convince you of that 😊 
*Most of the features we'll discuss are included in Mixpanel's free version. 

Previously published articles on the subject by Yoav on Mind the Product: 
- Why do you Need to Rethink Your Analytics Strategy? 
- Life Beyond Google Analytics: Pick the Best Tools for the Job 

Agenda: 
18:30 - Meet and Mingle 
18:40 - A word from our hosts at Le Wagon 
18:45 - Main event - Mixpanel Analytics lecture "New features vs. good old best practices (practical tips & tricks)” - Yoav Yechiam, Y-Perspective (now part of the Product-Alliance) 
20:15 - QA (Analytics questions from any type or form are welcomed)"""
}