#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

STOP_WORDS = ["सेक्स", "Sex", "Chudai", "चुदाई", "चोदा", "कामुकता", "chodan", "सेक्स रस", "काम रस", "देसी सेक्स", "XXX story", "Sex story", "Chudai ki khanani", "हिन्दी सेक्स कहानियाँ", "इंडियन SEX कहानी", "चुदाई की कहानी", "सेक्स जोक्स", "सेक्स कहानियां", "सेक्स रस और काम रस", "Sucksex", "सेक्स ", "ತುಲ್ಲು ", "ರತಿ ಕಾವ್ಯ", "18+", "Adult", "Anti", "asleelam", "Aunti", "Aunty", "bengaliSex ", "Bhabhi", "bold", "choda", "chodai", "chodan", "chodo", "chodvu", "Chudai", "Desi", "garam", "Gilma", "hot", "HotSex ", "jokes", "kaamsutra", "kam", "kama ", "Kamakathaikal", "Kamasutra", "kambi ", "kamsutra", "kamukta", "kuth ", "maal ", "Maami", "mallu ", "Manmatha", "masala ", "Okkum", "porn", "pornography", "Pranay ", "Pundai", "raand", "rape", "secret ", "sexras", "sexy", "srungara ", "thund", "TullaMaja", "tullu", "vedi", "XXX", "अश्लील ", "इंडियन ", "काम", "कामरस ", "कामसूत्र", "कामुकता", "गरम", "चुदाई", "चोदले ", "चोदा", "देसी", "प्रणय", "बीपी ", "रस ", "सेक्स ", "हॉट", "অশ্লীলপ্রেম", "কামকবিতা", "কামসূত্র", "কামুক ", "গরম", "চোদা ", "চোদাচুদি", "দেশীসেক্স", "পর্ণ", "বাংলাসেক্স", "বৌদীরসাথে", "ব্লু", "সেক্স ", "ગરમ ", "ચોદવું", "પોર્ન", "પોર્નોગ્રાફી", "માલ", "રાંડ", "સેક્સ", "સેક્સી", "ஆணுறுப்பு", "ஓல்", "கள்ளத்தொடர்பு காம கதை", "காம", "காமக்", "கில்மா", "கூதி", "செக்ஸ்", "நைட்டி", "புண்டை", "பெண்ணுறுப்பு", "மன்மத", "மாமி", "కామం ", "రహస్య", "వేడి ", "శృంగార ", "సెక్స్", "ಕನ್ನಡ ಕಾಮ ", "ಕನ್ನಡ ಕುಟು೦ಬಕಾಮ ", "ಕನ್ನಡ ಸೆಕ್ಸ್ ಸ್ಟೋರಿ", "ಕಾಮಸೂತ್ರ ", "ಬಾಯ್‌ ಫ್ರೆಂಡ್‌ ", "ಮೊಲೆಗಳು ", "ರಹಸ್ಯ ಕಾಮ", "ಲೈಂಗಿಕ ", "ಲೈಂಗಿಕಾನುಭವ", "ಶೃಂಗಾರ ", "ಸೆಕ್ಸ್ ", "ಸ್ತನ ", "അശ്ലീല", "കംബി ", "കമ്പി ", "കമ്പി ജോക്ക്സ്", "കമ്പിക്കഥകള്‍", "കാമ", "കാമം", "കാമക്കഥകള്‍", "കുത്ത് ", "തുണ്ട്", "മലയാളം കാമ കഥകള്", "മല്ലു ", "വെടി", "যৌন", "চোদ্চদ", "যৌন", "কামের ", "fucking", "fuck", "মানবশরীর বিদ্যা", "പൂര്‍" ]
