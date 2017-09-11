#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

STOP_WORDS = [" ತುಲ್ಲು ಕಥೆಗಳು ", " ರತಿ ಕಾವ್ಯ", "#kaamsutra katha ", "#సెక్స్", "Adult stories", "Amma nanna", "AntiDiary", "Aunty tullu kathegalu", "Boothu kathalu", "Chudai ki khananiDESIBEES ", "Desi sex stories", "Double meaning stories", "Gilma", "Gujarati sex story", "Indian Secret Sex Stories", "Indian kannada erotic sex stories", "Indian sex stories", "Kamakathaikal", "Kamasutra stories in Kannada", "Kamasutra", "Kannada +18 Night stories", "Kannada 18+ Stories ", "Kannada Adult Stories", "Kannada Hot Love Stories", "Kannada Hot Sex Stories", "Kannada XXX Story", "Kannada mood  Stories", "Kannada rape story", "Manmatha Kathaigal", "Pranay katha", "Sex kathai", "Sex stories", "Sucksex", "Tamil Aunty Sex Stories", "Tamil Bhabhi", "Tamil Gilma Stories", "Tamil Pundai Okkum Kathaigal", "Tamil Sex Stories", "Tamil rape story 18+", "Tulla Maja - Sex Story", "Tulla Maja", "XXX  कथा ", "XXX garam wartao", "XXX kannada story", "XXX story", "XXX story,", "XXX સ્ટોરી", "adult stories", "aunty sex stories ", "bengali Sex stories", "bhabhi ", "choda", "chodai", "chodan", "chodan", "chodo", "chodvu", "desi sex", "desi stories ", "erotic sex", "erotic", "garam katha ", "hindi sex kahaniya", "hot sex", "hot stories ", "indian sex kahani ", "indian sex stories ", "kaamsutra", "kama kathakal", "kama kathalu", "kama", "kamasutra stories ", "kambi jokes", "kambi kadha", "kambi katha", "kambi kathakal", "kambi story", "kampi", "kampikkathakaḷ", "kamukta ", "kamukta ", "kamukta", "kuth kathakal", "kuth story", "maal ", "malayalam aunty story", "mallu aunty", "mallu sex stories", "mallu stories ", "marathi hot stories", "masala story ", "masala story", "porn ", "porn ", "porn jokes", "porn jokes", "porn stories", "porn stories", "porn", "porn", "pornography ", "pornography", "pornography", "raand", "rape", "secret sex", "sex jokes", "sex jokes", "sex kahaniya", "sex kathalu", "sex kathe", "sex ras aur kam ", "sex stories", "sex stories", "sex story ", "sex", "sex", "sexy", "srungara kathalu", "srungara", "srungaram ", "suck", "tamil kamakathaikal", "xxx telugu kathalu", "xxx", "xxx", "xxx", "xxx", "xxx", "अनैतिक कथा ", "अश्लील कथा ", "इंडियन SEX कहानी", "काम रस ", "कामसूत्रमुकता ", "कामुकता", "गरम कथा ", "चुदाई की कहानी", "चोदले ", "चोदा", "डबलमिनिंग कथा ", "देसी सेक्स कथा ", "देसी सेक्स,", "प्रणय कथा ", "मराठी सेक्स कथा ", "सेक्स ", "सेक्स कथा ", "सेक्स कह जोक्स", "सेक्स रस और काम रस", "सेक्स विनोद ", "हिन्दी सेक्स कहानियाँ", "हॉट कथा ", "অশ্লীল প্রেমের কবিতা", "কাম কবিতা", "কামসূত্র বই", "কামুক গল্প", "চোদা চুদি", "চোদাচুদির গল্প", "দেশবাংলা সেক্স গল্প", "বাজে গল্প", "বেশ্যার প্রেম", "বৌদীর সাথে", "মশলা গল্প", "রসের গল্প", "সেক্স স্টোরি", "সেক্স", "ગરમ વાતો ", "ગુજરાતી સેક્સ સ્ટોરી", "ચોદવું", "પોર્ન", "પોર્નોગ્રાફી",  "સેક્સ", "સેક્સી", "அத்தை காமக்கதைகள்", "ஆணுறுப்பு", "ஓல்", "கள்ள தொடர்பு காம கதை", "ாம கதைகள்", "காமக் கதைகள்", "கில்மா கதைகள்", "கில்மா", "கூதி", "செக்ஸ் கதைகள்", "டீச்சர் காம கதைகள்", "கள்", "தமிழ் குடும்ப செக்ஸ் கதைகள்", "நைட்டி", "புண்டை", "பெண்ணுறுப்பு", "மன்மத கதைகள்", "மாமி காமக் கதை", "மாமி", "తెలుగు కామం ", "శృంగార కథలు ", "ಆಂಟಿ ಕಾಮ ಕಥೆ ", "ಕನ್ನಡ +೧೮ ಕಥೆಗಳು", "ಕನ್ಗಳು", "ಕನ್ನಡ ಸೆಕ್ಸ್ ಸ್ಟೋರಿ", "ಕಾಮಸೂತ್ರ ", "ಬಾಯ್<200c> ಫ್ರೆಂಡ್<200c> ಸೆಕ್ಸ್<200c>", "ಮೊಲೆಗಳು ", "ರಹಸ್ಯ ಕಾಮ ಕಥೆಗಳು", "ಲೈಂಗಿಕ ಕಥೆಗಳು ", "ಲೈಂಗಿಕಾನುಭವ", "ಶೃಂಗಾರ ಕಥೆಗಳು ", "ಸರ್ವೋಚ್ಚ ಕನ್ನಡ ಕಾಮ ಕಥೆಗಳ ನ ಕಥೆಗಳು ", "അശ്ലീല കഥകൾ", "കംബി കഥകള്<200d>", "കംബി", "കമ്പി ജോക്ക്സ്", "കമ്പി നോവൽ", "കമ്പി മലയാളം കഥകള്<200d>", "കമ്പി", "കമ്പിക്കഥകള്<200d>", "കാമ കഥകള്<200d>", "കാമം", "കാമക്കഥകള്200d>", "കുത്ത്", "തുണ്ട് കഥകള്<200d>", "തുണ്ട്", "മലയാളം കാമ കഥകള്", "വെടി",
"सेक्स", "Sex", "Chudai", "चुदाई", "चोदा", "कामुकता", "chodan", "सेक्स रस", "काम रस", "देसी सेक्स", "XXX story", "Sex story", "Chudai ki khanani", "हिन्दी सेक्स कहानियाँ", "इंडियन SEX कहानी", "चुदाई की कहानी", "सेक्स जोक्स", "सेक्स कहानियां", "सेक्स रस और काम रस", ]
